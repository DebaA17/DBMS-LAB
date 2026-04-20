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
    

## Notes (Compatibility)

- These scripts target **Oracle SQL** (Oracle XE). If you try to run them on MySQL/PostgreSQL/SQLite, you will likely need small syntax changes.
- For Oracle, `NULL` commissions/salaries behave as expected in aggregate queries (e.g., `SUM`).

---

## Git LFS (Linux-DBMS.zip)

`Linux-DBMS.zip` contains my **Oracle XE (10g) Debian-based installation bundle** (the `.deb` files + related setup/notes).

After extracting the zip, check inside:

- `Linux-DEB`

You can delete the zip after extraction if you want to keep the directory clean:

```bash
rm Linux-DBMS.zip
```

The zip is stored using **Git LFS**. If you clone/download the repo without LFS, you may get a small *pointer file* and `unzip` will fail.

### Debian/Ubuntu (Debian-based distros)

```bash
sudo apt update
sudo apt install -y git-lfs
git lfs install
git lfs pull
```

## License

See [LICENSE](LICENSE).
