<h1 align="center">DBMS-LAB</h1>

<p align="center">
	<a href="https://github.com/DebaA17/DBMS-LAB/actions/workflows/oracle-ci.yml">
		<img alt="Oracle SQL CI" src="https://img.shields.io/github/actions/workflow/status/DebaA17/DBMS-LAB/oracle-ci.yml?label=Oracle%20SQL%20CI" />
	</a>
</p>

DBMS lab work and SQL solutions aligned with the academic syllabus (BPPIMT, 4th semester). The SQL in this repository is written for **Oracle Database Express Edition (Oracle XE)** and uses Oracle-specific syntax such as `INSERT ALL` and `TO_DATE(...)`.

## What’s Inside

- SQL scripts/solutions for lab assignments
- Table creation + sample data inserts
- Query solutions (aggregation, filtering, subqueries, etc.)
- Solutions for the 5 PCA2 Exam Lab Copy assignments (located in `PCA2-labcopy/`)

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

3. **Resetting / Cleaning the Database**:
	If you need to delete all existing tables and start with a clean environment, execute this PL/SQL block:

	```sql
	BEGIN
	  FOR r IN (SELECT table_name FROM user_tables) LOOP
	    EXECUTE IMMEDIATE 'DROP TABLE "' || r.table_name || '" CASCADE CONSTRAINTS PURGE';
	  END LOOP;
	END;
	/
	```

## CI (GitHub Actions)

This repository uses GitHub Actions to automatically run SQL scripts from each assignment Solution.md against an Oracle Database Free Docker container (compatible with most Oracle XE syntax).

- Workflow: [.github/workflows/oracle-ci.yml](.github/workflows/oracle-ci.yml)

How to view results

- Go to the Actions tab on GitHub
- Select a workflow run
- Click a job to see step-by-step logs in the web UI
- Download the oracle-sql-logs artifact to view full per-assignment log files
    

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
