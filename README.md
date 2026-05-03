# DBMS-LAB

DBMS lab work and SQL solutions aligned with the academic syllabus (BPPIMT, 4th semester). The SQL in this repository is written for **Oracle Database Express Edition (Oracle XE)** and uses Oracle-specific syntax such as `INSERT ALL` and `TO_DATE(...)`.

## What’s Inside

- SQL scripts/solutions for lab assignments
- Table creation + sample data inserts
- Query solutions (aggregation, filtering, subqueries, etc.)

## Prerequisites

- **Oracle Database Express Edition (XE)** installed and running
- One of the following clients/tools:
  - SQL*Plus (command-line)
  - Oracle SQL Developer
  - Oracle APEX SQL Workshop (if available in your XE setup)

## Quick Start (Oracle XE)

1. Create a database user (example):

	```sql
	CREATE USER firstname IDENTIFIED BY lastname;
	GRANT CONNECT, RESOURCE TO firstname;
	```

2. Connect using your preferred client and run the assignment SQL in order:
	- Create table(s)
	- Insert sample data
	- Run the queries

## CI (GitHub Actions)

This repo includes a GitHub Actions workflow that runs the SQL blocks from each assignment `Solution.md` against an **Oracle Database Free** Docker container (close enough for most Oracle-XE-compatible lab SQL).

- Workflow: [.github/workflows/oracle-ci.yml](.github/workflows/oracle-ci.yml)
- Logs: if any script fails, the job fails and uploads an `oracle-sql-logs` artifact.
    

## Notes (Compatibility)

- These scripts target **Oracle SQL** (Oracle XE). If you try to run them on MySQL/PostgreSQL/SQLite, you will likely need small syntax changes.
- For Oracle, `NULL` commissions/salaries behave as expected in aggregate queries (e.g., `SUM`).

---

## Oracle XE Installer Bundle (Release)

`Linux-DBMS.zip` (Oracle XE 10g Debian-based installer bundle) is hosted as a **GitHub Release asset**:

- https://github.com/DebaA17/DBMS-LAB/releases/tag/linux-dbms-zip-v1

After downloading and extracting, check inside:

- `Linux-DEB`

## License

See [LICENSE](LICENSE).
