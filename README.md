<h1 align="center">DBMS Lab Solutions</h1>

<p align="center">
  <a href="https://github.com/DebaA17/DBMS-LAB/actions/workflows/oracle-ci.yml">
    <img alt="Oracle SQL CI" src="https://img.shields.io/github/actions/workflow/status/DebaA17/DBMS-LAB/oracle-ci.yml?label=Oracle%20SQL%20CI&logo=github&style=flat-square" />
  </a>
</p>

Academic DBMS lab solutions aligned with the 4th-semester syllabus (BPPIMT), written specifically for **Oracle Database Express Edition (Oracle XE)**.

---

## 📂 Navigation

### 🎓 Lab Notebook Preparation
* **[BCA 4th Sem Lab Notebook Solutions (1-5)](./notebook-copy/)** - *(Notebook work only, NOT actual exam questions)*

### 📝 Semester Assignments
* [Assignment 1-2: Employee Queries](./ASSIGNMENT_1-2)
* [Assignment 3: EMP & DEPT](./ASSIGNMENT_3)
* [Assignment 4: Joins & Subqueries](./ASSIGNMENT_4)
* [Assignment 5: SQL Functions](./ASSIGNMENT_5)
* [Assignment 6: Exception Handling](./ASSIGNMENT_6)
* [Assignment 7: Cursors](./ASSIGNMENT_7)
* [Assignment 8: Procedures & Functions](./ASSIGNMENT_8)
* [Assignment 9: Database Triggers](./ASSIGNMENT_9)
* [Assignment 10: PL/SQL Packages](./ASSIGNMENT_10)
* [Assignment 11: Package Overloading](./ASSIGNMENT_11)
* [Assignment 12: Advanced Triggers](./ASSIGNMENT_12)
* [Assignment 13: Interactive PL/SQL](./ASSIGNMENT_13)

---

## ⚡ Quick Start

### Database Reset
To drop all existing tables and start with a clean environment in your Oracle APEX or SQL workspace, run this block:

```sql
BEGIN
  FOR r IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE "' || r.table_name || '" CASCADE CONSTRAINTS PURGE';
  END LOOP;
END;
/
```

---

## 📦 Installer Bundle

The Debian-compatible installation bundle `Linux-DBMS.zip` (Oracle XE 10g) is hosted on [GitHub Releases](https://github.com/DebaA17/DBMS-LAB/releases/tag/linux-dbms-zip-v1).
