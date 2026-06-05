# SQL Solutions – Assignment 9 (Employee & Manager Schema)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Tables

**(A) Department**

```sql
CREATE TABLE Department (
	deptno NUMBER PRIMARY KEY,
	dname  VARCHAR2(50) NOT NULL,
	city   VARCHAR2(50) NOT NULL
);
```

**(B) Employee**

```sql
CREATE TABLE Employee (
	empno    VARCHAR2(10) PRIMARY KEY,
	emp_name VARCHAR2(50) NOT NULL,
	salary   NUMBER(10,2) NOT NULL,
	hiredate DATE NOT NULL,
	city     VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_empno_prefix
		CHECK (empno LIKE 'E%')
);
```

**(C) Manager**

```sql
CREATE TABLE Manager (
	mgrno       VARCHAR2(10) PRIMARY KEY,
	deptno      NUMBER NOT NULL,
	manger_name VARCHAR2(50) NOT NULL,
	salary      NUMBER(10,2) NOT NULL,
	hiredate    DATE NOT NULL,
	city        VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_mgrno_prefix
		CHECK (mgrno LIKE 'M%'),
	CONSTRAINT fk_manager_dept
		FOREIGN KEY (deptno) REFERENCES Department(deptno)
);
```

**(D) Empmgr**

```sql
CREATE TABLE Empmgr (
	empno VARCHAR2(10),
	mgrno VARCHAR2(10),
	CONSTRAINT pk_empmgr
		PRIMARY KEY (empno, mgrno),
	CONSTRAINT fk_empmgr_employee
		FOREIGN KEY (empno) REFERENCES Employee(empno),
	CONSTRAINT fk_empmgr_manager
		FOREIGN KEY (mgrno) REFERENCES Manager(mgrno)
);
```

---

## 2. Insert Data

**(A) Insert into Department**

```sql
INSERT ALL
	INTO Department (deptno, dname, city) VALUES (10, 'HR',      'Kolkata')
	INTO Department (deptno, dname, city) VALUES (20, 'IT',      'Delhi')
	INTO Department (deptno, dname, city) VALUES (30, 'Sales',   'Mumbai')
	INTO Department (deptno, dname, city) VALUES (40, 'Support', 'Chennai')
SELECT * FROM dual;
```

**(B) Insert into Employee**

```sql
INSERT ALL
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E201', 'Alice Cooper',    85000,  TO_DATE('2006-03-10', 'YYYY-MM-DD'), 'Delhi')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E202', 'Charlie Brown',   75000,  TO_DATE('2007-06-15', 'YYYY-MM-DD'), 'Kolkata')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E203', 'Diana Prince',    60000,  TO_DATE('2006-11-20', 'YYYY-MM-DD'), 'Mumbai')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E204', 'Evan Wright',     110000, TO_DATE('2008-01-10', 'YYYY-MM-DD'), 'Delhi')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E205', 'Fiona Gallagher', 90000,  TO_DATE('2005-12-05', 'YYYY-MM-DD'), 'Kolkata')
SELECT * FROM dual;
```

**(C) Insert into Manager**

```sql
INSERT ALL
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M101', 10, 'John Doe',    80000,  TO_DATE('2005-04-12', 'YYYY-MM-DD'), 'Kolkata')
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M102', 20, 'Jane Smith',  120000, TO_DATE('2004-09-01', 'YYYY-MM-DD'), 'Delhi')
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M103', 30, 'Bob Johnson', 95000,  TO_DATE('2006-05-15', 'YYYY-MM-DD'), 'Mumbai')
SELECT * FROM dual;
```

**(D) Insert into Empmgr**

```sql
INSERT ALL
	INTO Empmgr (empno, mgrno) VALUES ('E201', 'M101')
	INTO Empmgr (empno, mgrno) VALUES ('E202', 'M101')
	INTO Empmgr (empno, mgrno) VALUES ('E203', 'M102')
	INTO Empmgr (empno, mgrno) VALUES ('E204', 'M102')
	INTO Empmgr (empno, mgrno) VALUES ('E205', 'M103')
SELECT * FROM dual;
```

---

## 3. User-Friendly Form Design (Employee Table)

The following is a clean form layout designed to safely capture input for inserting records into the **Employee** table.

### Form Controls & Validations

| Field Label | Input Control Type | Validation Rules / HTML Attributes |
| :--- | :--- | :--- |
| **Employee ID** | Text Input | `required`, `pattern="^E.+"` (Must start with 'E'), `maxlength="10"` |
| **Employee Name** | Text Input | `required`, `maxlength="50"` |
| **Salary** | Number Input | `required`, `min="0"`, `step="0.01"` |
| **Hire Date** | Date Picker | `required` (Restricted to format `YYYY-MM-DD`) |
| **City** | Text Input | `required`, `maxlength="50"` |

---

# Queries and Answers

---

### (i) Give the employee names who earn more than their manager.

```sql
SELECT DISTINCT e.emp_name
FROM Employee e
JOIN Empmgr em ON e.empno = em.empno
JOIN Manager m ON em.mgrno = m.mgrno
WHERE e.salary > m.salary
ORDER BY e.emp_name;
```

---

### (ii) Give the name of the managers who have no employee under his supervision from the same city as of him.

```sql
SELECT m.manger_name
FROM Manager m
WHERE NOT EXISTS (
	SELECT 1
	FROM Empmgr em
	JOIN Employee e ON em.empno = e.empno
	WHERE em.mgrno = m.mgrno
	  AND e.city = m.city
)
ORDER BY m.manger_name;
```

---

### (iii) Give the name of the manager who has maximum number of employees under his supervision.

```sql
SELECT m.manger_name
FROM Manager m
JOIN Empmgr em ON m.mgrno = em.mgrno
GROUP BY m.mgrno, m.manger_name
HAVING COUNT(em.empno) = (
	SELECT MAX(COUNT(empno))
	FROM Empmgr
	GROUP BY mgrno
);
```

---

### (iv) Give the name of the employees who have been hired in the year 2006.

```sql
SELECT emp_name
FROM Employee
WHERE EXTRACT(YEAR FROM hiredate) = 2006
ORDER BY emp_name;
```

---

### (v) Give the name of the city where no manager is located.

```sql
SELECT DISTINCT city
FROM Department
WHERE city NOT IN (
	SELECT city
	FROM Manager
	WHERE city IS NOT NULL
)
UNION
SELECT DISTINCT city
FROM Employee
WHERE city NOT IN (
	SELECT city
	FROM Manager
	WHERE city IS NOT NULL
);
```
