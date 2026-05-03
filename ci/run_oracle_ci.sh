#!/usr/bin/env bash
set -euo pipefail

# Runs Oracle-backed SQL checks in CI.
# - Starts an Oracle DB Free container (if not already running)
# - Creates an app user
# - Extracts SQL from ASSIGNMENT_*/Solution.md into .sql scripts
# - Runs each generated script with SQL*Plus
# - Writes logs into .ci-out/logs and exits non-zero on any SQL error

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/.ci-out"
SQL_DIR="${OUT_DIR}/sql"
LOG_DIR="${OUT_DIR}/logs"

ORACLE_IMAGE="${ORACLE_IMAGE:-docker.io/gvenzl/oracle-free:23}"
ORACLE_CONTAINER="${ORACLE_CONTAINER:-oracledb}"
ORACLE_PASSWORD="${ORACLE_PASSWORD:-oracle}"
ORACLE_PDB="${ORACLE_PDB:-FREEPDB1}"

APP_USER="${APP_USER:-lab_ci}"
APP_PASSWORD="${APP_PASSWORD:-lab_ci}"

mkdir -p "${SQL_DIR}" "${LOG_DIR}"

start_oracle_if_needed() {
  if docker ps --format '{{.Names}}' | grep -qx "${ORACLE_CONTAINER}"; then
    echo "Oracle container '${ORACLE_CONTAINER}' already running"
    return
  fi

  if docker ps -a --format '{{.Names}}' | grep -qx "${ORACLE_CONTAINER}"; then
    echo "Removing existing container '${ORACLE_CONTAINER}'"
    docker rm -f "${ORACLE_CONTAINER}" >/dev/null
  fi

  echo "Starting Oracle container '${ORACLE_CONTAINER}' from '${ORACLE_IMAGE}'"
  docker run -d \
    --name "${ORACLE_CONTAINER}" \
    -p 1521:1521 \
    -e ORACLE_PASSWORD="${ORACLE_PASSWORD}" \
    "${ORACLE_IMAGE}" >/dev/null
}

wait_for_oracle() {
  echo "Waiting for Oracle to become ready..."

  local deadline=$((SECONDS + 600))
  while (( SECONDS < deadline )); do
    # Healthcheck (preferred) if present
    local health
    health="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "${ORACLE_CONTAINER}" 2>/dev/null || true)"
    if [[ "${health}" == "healthy" ]]; then
      echo "Oracle container is healthy"
      return
    fi

    # Fallback: try a quick SQL*Plus connection inside the container
    if docker exec "${ORACLE_CONTAINER}" bash -lc "echo 'select 1 from dual;' | sqlplus -s system/${ORACLE_PASSWORD}@localhost/${ORACLE_PDB} >/dev/null" 2>/dev/null; then
      echo "Oracle SQL*Plus connection OK"
      return
    fi

    sleep 5
  done

  echo "Timed out waiting for Oracle startup"
  docker logs "${ORACLE_CONTAINER}" | tail -200
  return 1
}

create_app_user() {
  echo "Creating app user '${APP_USER}'"

  local setup_sql
  setup_sql="${OUT_DIR}/setup_user.sql"

  cat >"${setup_sql}" <<SQL
whenever sqlerror exit sql.sqlcode rollback
set echo on

BEGIN
  EXECUTE IMMEDIATE 'CREATE USER ${APP_USER} IDENTIFIED BY ${APP_PASSWORD}';
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE = -1920 THEN NULL; ELSE RAISE; END IF;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'ALTER USER ${APP_USER} QUOTA UNLIMITED ON USERS';
EXCEPTION
  WHEN OTHERS THEN
    -- If USERS tablespace differs, ignore (fresh DB usually has USERS).
    NULL;
END;
/

GRANT CONNECT, RESOURCE TO ${APP_USER};
exit
SQL

  local log_file="${LOG_DIR}/00_setup_user.log"
  local exit_code

  set +e
  docker exec -i "${ORACLE_CONTAINER}" bash -lc "set -o pipefail; sqlplus -s -L system/${ORACLE_PASSWORD}@localhost/${ORACLE_PDB}" <"${setup_sql}" 2>&1 | tee "${log_file}"
  exit_code=${PIPESTATUS[0]}
  set -e

  if grep -Eq "ORA-[0-9]{5}|SP2-[0-9]{4}|PLS-[0-9]{5}|LRM-[0-9]{5}|compilation errors" "${log_file}"; then
    echo "FAILED: setup user (detected Oracle/SQL*Plus error text in log)"
    return 1
  fi
  if [[ ${exit_code} -ne 0 ]]; then
    echo "FAILED: setup user (exit ${exit_code})"
    return "${exit_code}"
  fi
}

recreate_schema_user() {
  local schema_user="$1"
  local schema_password="$2"
  local log_file="$3"

  local setup_sql
  setup_sql="${OUT_DIR}/setup_${schema_user}.sql"

  cat >"${setup_sql}" <<SQL
whenever oserror exit 9
whenever sqlerror exit sql.sqlcode rollback
set echo on

BEGIN
  EXECUTE IMMEDIATE 'DROP USER ${schema_user} CASCADE';
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE = -1918 THEN NULL; ELSE RAISE; END IF;
END;
/

CREATE USER ${schema_user} IDENTIFIED BY ${schema_password};

BEGIN
  EXECUTE IMMEDIATE 'ALTER USER ${schema_user} QUOTA UNLIMITED ON USERS';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

GRANT CONNECT, RESOURCE TO ${schema_user};
exit
SQL

  set +e
  docker exec -i "${ORACLE_CONTAINER}" bash -lc "set -o pipefail; sqlplus -s -L system/${ORACLE_PASSWORD}@localhost/${ORACLE_PDB}" <"${setup_sql}" 2>&1 | tee "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e

  if grep -Eq "ORA-[0-9]{5}|SP2-[0-9]{4}|PLS-[0-9]{5}|LRM-[0-9]{5}|compilation errors" "${log_file}"; then
    echo "FAILED: schema setup for ${schema_user} (detected error text in log)"
    return 1
  fi
  if [[ ${exit_code} -ne 0 ]]; then
    echo "FAILED: schema setup for ${schema_user} (exit ${exit_code})"
    return "${exit_code}"
  fi
}

extract_sql() {
  echo "Extracting SQL blocks from markdown into ${SQL_DIR}"
  python3 "${ROOT_DIR}/ci/extract_sql_from_md.py" --out-dir "${SQL_DIR}"
}

run_sql_scripts() {
  echo "Running generated SQL scripts via SQL*Plus"

  local failed=0
  for sql_file in "${SQL_DIR}"/*.sql; do
    local base
    base="$(basename "${sql_file}")"
    local log_file="${LOG_DIR}/${base%.sql}.log"
    local exit_code

    # Run each assignment in its own schema so tables/triggers/etc don't collide.
    local schema_user
    schema_user="CI_${base%.sql}"
    schema_user="$(echo "${schema_user}" | tr '[:lower:]-' '[:upper:]_')"
    # Oracle username limit is 30 chars.
    schema_user="${schema_user:0:30}"
    local schema_password="${schema_user}"
    local schema_log_file="${LOG_DIR}/${base%.sql}.schema.log"

    recreate_schema_user "${schema_user}" "${schema_password}" "${schema_log_file}"

    echo "--- Running ${base} ---"

    # Run inside the container so we always have SQL*Plus available.
    # Use pipefail so ORA- errors propagate as a failing exit status.
    set +e
    docker exec -i "${ORACLE_CONTAINER}" bash -lc "set -o pipefail; sqlplus -s -L ${schema_user}/${schema_password}@localhost/${ORACLE_PDB}" <"${sql_file}" 2>&1 | tee "${log_file}"
    exit_code=${PIPESTATUS[0]}
    set -e

    # sqlplus can still exit 0 while printing errors (e.g., compilation errors).
    if grep -Eq "ORA-[0-9]{5}|SP2-[0-9]{4}|PLS-[0-9]{5}|LRM-[0-9]{5}|compilation errors" "${log_file}"; then
      echo "FAILED: ${base} (detected Oracle/SQL*Plus error text in log)"
      failed=1
      break
    fi

    if [[ ${exit_code} -ne 0 ]]; then
      echo "FAILED: ${base} (exit ${exit_code})"
      failed=1
      break
    fi
  done

  return "${failed}"
}

main() {
  command -v docker >/dev/null || { echo "docker is required"; return 2; }
  command -v python3 >/dev/null || { echo "python3 is required"; return 2; }

  start_oracle_if_needed
  wait_for_oracle
  extract_sql
  run_sql_scripts
}

main "$@"
