# SQL Solutions – Assignment 3

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

# Question 5: EMP & DEPT

## 1. Create Tables

```sql
CREATE TABLE DEPT (
	DEPT#    NUMBER PRIMARY KEY,
	DNAME    VARCHAR2(20) NOT NULL,
	LOCATION VARCHAR2(20) NOT NULL
);
```

```sql
CREATE TABLE EMP (
	EMP#     NUMBER PRIMARY KEY,
	ENAME    VARCHAR2(20) NOT NULL,
	JOB      VARCHAR2(20),
	HIREDATE DATE,
	MANAGER# NUMBER,
	SALARY   NUMBER(10,2),
	COMM     NUMBER(10,2),
	DEPT#    NUMBER,
	CONSTRAINT fk_emp_dept
		FOREIGN KEY (DEPT#) REFERENCES DEPT (DEPT#)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO DEPT (DEPT#, DNAME, LOCATION) VALUES (10, 'ACCOUNTING', 'NEW YORK')
	INTO DEPT (DEPT#, DNAME, LOCATION) VALUES (20, 'RESEARCH',   'DALLAS')
	INTO DEPT (DEPT#, DNAME, LOCATION) VALUES (30, 'SALES',      'CHICAGO')
	INTO DEPT (DEPT#, DNAME, LOCATION) VALUES (40, 'OPERATIONS', 'BOSTON')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7839,'KING',   'PRESIDENT', TO_DATE('1990-06-09','YYYY-MM-DD'), NULL, 5000, NULL, 10)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7566,'JONES',  'MANAGER',   TO_DATE('1995-10-31','YYYY-MM-DD'), 7839, 2975, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7698,'BLAKE',  'MANAGER',   TO_DATE('1992-06-11','YYYY-MM-DD'), 7839, 2850, NULL, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7782,'CLARK',  'MANAGER',   TO_DATE('1993-05-14','YYYY-MM-DD'), 7839, 2450, NULL, 10)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7902,'FORD',   'ANALYST',   TO_DATE('1997-12-05','YYYY-MM-DD'), 7566, 3000, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7788,'SCOTT',  'ANALYST',   TO_DATE('1996-03-05','YYYY-MM-DD'), 7566, 3000, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7369,'SMITH',  'CLERK',     TO_DATE('1993-06-13','YYYY-MM-DD'), 7902,  800, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7876,'ADAMS',  'CLERK',     TO_DATE('1999-06-04','YYYY-MM-DD'), 7788, 1100, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7900,'JAMES',  'CLERK',     TO_DATE('2000-06-23','YYYY-MM-DD'), 7698,  950, NULL, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7934,'MILLER', 'CLERK',     TO_DATE('2000-01-21','YYYY-MM-DD'), 7782, 1300, NULL, 10)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7499,'ALLEN',  'SALESMAN',  TO_DATE('1998-08-15','YYYY-MM-DD'), 7698, 1600,  300, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7521,'WARD',   'SALESMAN',  TO_DATE('1996-03-26','YYYY-MM-DD'), 7698, 1250,  500, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7654,'MARTIN', 'SALESMAN',  TO_DATE('1998-12-05','YYYY-MM-DD'), 7698, 1250, 1400, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7844,'TURNER', 'SALESMAN',  TO_DATE('1995-06-04','YYYY-MM-DD'), 7698, 1500, NULL, 30)
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### (i) List the name, salary and PF amounts of all employees (PF is calculated as 10% of the basic)

```sql
SELECT
	ENAME,
	SALARY,
	(SALARY * 0.10) AS PF
FROM EMP
ORDER BY ENAME;
```

### (ii) List the number of employees and average salary in DEPT# 20.

```sql
SELECT
	COUNT(*)    AS employee_count,
	AVG(SALARY) AS avg_salary
FROM EMP
WHERE DEPT# = 20;
```

### (iii) List the department number and total salary payable in each department.

```sql
SELECT
	DEPT#,
	SUM(SALARY) AS total_salary
FROM EMP
GROUP BY DEPT#
ORDER BY DEPT#;
```

### (iv) List the names of the employees who are more than 20 years old in the company.

```sql
SELECT ENAME
FROM EMP
WHERE MONTHS_BETWEEN(SYSDATE, HIREDATE) / 12 > 20
ORDER BY ENAME;
```

### (v) List the names of the employees whose name either starts or ends with 'S'.

```sql
SELECT ENAME
FROM EMP
WHERE ENAME LIKE 'S%'
	OR ENAME LIKE '%S'
ORDER BY ENAME;
```

---
---

# Question 6: Banking Schema II

## 1. Create Tables

```sql
CREATE TABLE Branch (
	BName  VARCHAR2(50) PRIMARY KEY,
	BCity  VARCHAR2(50) NOT NULL,
	Assets NUMBER(12,2) NOT NULL
);
```

```sql
CREATE TABLE Customer (
	CName VARCHAR2(50) PRIMARY KEY,
	CCity VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Loan (
	LoanNo VARCHAR2(10) PRIMARY KEY,
	BName  VARCHAR2(50) NOT NULL,
	Amount NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_loan_branch FOREIGN KEY (BName) REFERENCES Branch (BName)
);
```

```sql
CREATE TABLE Borrower (
	CName  VARCHAR2(50) NOT NULL,
	LoanNo VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_borrower PRIMARY KEY (CName, LoanNo),
	CONSTRAINT fk_borrower_cust FOREIGN KEY (CName) REFERENCES Customer (CName),
	CONSTRAINT fk_borrower_loan FOREIGN KEY (LoanNo) REFERENCES Loan (LoanNo)
);
```

```sql
CREATE TABLE Account (
	AccNo   VARCHAR2(10) PRIMARY KEY,
	BName   VARCHAR2(50) NOT NULL,
	Balance NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_account_branch FOREIGN KEY (BName) REFERENCES Branch (BName)
);
```

```sql
CREATE TABLE Depositor (
	CName VARCHAR2(50) NOT NULL,
	AccNo VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_depositor PRIMARY KEY (CName, AccNo),
	CONSTRAINT fk_depositor_cust FOREIGN KEY (CName) REFERENCES Customer (CName),
	CONSTRAINT fk_depositor_acc  FOREIGN KEY (AccNo) REFERENCES Account (AccNo)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Branch (BName, BCity, Assets) VALUES ('Salt Lake',     'Kolkata',  30000)
	INTO Branch (BName, BCity, Assets) VALUES ('New Market',    'Kolkata',  15000)
	INTO Branch (BName, BCity, Assets) VALUES ('Connaught Place','Delhi',   50000)
	INTO Branch (BName, BCity, Assets) VALUES ('Chandni Chowk', 'Delhi',    12000)
	INTO Branch (BName, BCity, Assets) VALUES ('Colaba',        'Mumbai',   45000)
	INTO Branch (BName, BCity, Assets) VALUES ('Andheri',       'Mumbai',   25000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Customer (CName, CCity) VALUES ('Debasis Biswas',   'Kolkata')
	INTO Customer (CName, CCity) VALUES ('Rahul Roy',       'Kolkata')
	INTO Customer (CName, CCity) VALUES ('Priya Sharma',    'Delhi')
	INTO Customer (CName, CCity) VALUES ('Neha Gupta',      'Delhi')
	INTO Customer (CName, CCity) VALUES ('Vikram Malhotra', 'Mumbai')
	INTO Customer (CName, CCity) VALUES ('Rohan Joshi',     'Mumbai')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Account (AccNo, BName, Balance) VALUES ('A101', 'Salt Lake',      15000)
	INTO Account (AccNo, BName, Balance) VALUES ('A102', 'New Market',      8000)
	INTO Account (AccNo, BName, Balance) VALUES ('A103', 'Connaught Place',35000)
	INTO Account (AccNo, BName, Balance) VALUES ('A104', 'Chandni Chowk',   5000)
	INTO Account (AccNo, BName, Balance) VALUES ('A105', 'Colaba',         25000)
	INTO Account (AccNo, BName, Balance) VALUES ('A106', 'Andheri',        12000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Depositor (CName, AccNo) VALUES ('Debasis Biswas',   'A101')
	INTO Depositor (CName, AccNo) VALUES ('Rahul Roy',       'A102')
	INTO Depositor (CName, AccNo) VALUES ('Priya Sharma',    'A103')
	INTO Depositor (CName, AccNo) VALUES ('Neha Gupta',      'A104')
	INTO Depositor (CName, AccNo) VALUES ('Vikram Malhotra', 'A105')
	INTO Depositor (CName, AccNo) VALUES ('Rohan Joshi',     'A106')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Loan (LoanNo, BName, Amount) VALUES ('L101', 'Salt Lake',      20000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L102', 'New Market',     10000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L103', 'Connaught Place',40000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L104', 'Colaba',         30000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L105', 'Andheri',        15000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Borrower (CName, LoanNo) VALUES ('Debasis Biswas',   'L101')
	INTO Borrower (CName, LoanNo) VALUES ('Rahul Roy',       'L102')
	INTO Borrower (CName, LoanNo) VALUES ('Priya Sharma',    'L103')
	INTO Borrower (CName, LoanNo) VALUES ('Vikram Malhotra', 'L104')
	INTO Borrower (CName, LoanNo) VALUES ('Rohan Joshi',     'L105')
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### i) List the names of those branches that have assets in between 20000 and 40000.

```sql
SELECT BName FROM Branch
WHERE Assets BETWEEN 20000 AND 40000
ORDER BY BName;
```

### ii) List the names of those customers along with the branch names who have an account in the same city as they live in.

```sql
SELECT DISTINCT d.CName, a.BName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE b.BCity = c.CCity
ORDER BY d.CName;
```

### iii) Write the names of those customers who have an account, a loan or both.

```sql
SELECT CName FROM Depositor
UNION
SELECT CName FROM Borrower
ORDER BY CName;
```

### iv) Write the names of those customers who have both an account and a loan.

```sql
SELECT CName FROM Depositor
INTERSECT
SELECT CName FROM Borrower
ORDER BY CName;
```

### v) Write the names of those customers who have either an account or a loan.

```sql
SELECT CName FROM (
	SELECT CName FROM Depositor
	MINUS
	SELECT CName FROM Borrower
)
UNION
SELECT CName FROM (
	SELECT CName FROM Borrower
	MINUS
	SELECT CName FROM Depositor
)
ORDER BY CName;
```

### vi) Write the names of all customers having account balance more than 10000.

```sql
SELECT DISTINCT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
WHERE a.Balance > 10000
ORDER BY d.CName;
```

### vii) Write the names of all customers along with branch name and branch city having account balance less than 10000.

```sql
SELECT d.CName, a.BName, b.BCity
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
WHERE a.Balance < 10000
ORDER BY d.CName;
```

### viii) Write the names of all customers along with branch name, branch city and customer city having account balance between 10000 and 20000.

```sql
SELECT d.CName, a.BName, b.BCity, c.CCity
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE a.Balance BETWEEN 10000 AND 20000
ORDER BY d.CName;
```

### ix) List the names of those customers along with branch name for those customers who have a loan amount more than account balance.

```sql
SELECT b.CName, l.BName
FROM Borrower b
JOIN Loan l ON b.LoanNo = l.LoanNo
JOIN Depositor d ON b.CName = d.CName
JOIN Account a ON d.AccNo = a.AccNo
WHERE l.Amount > a.Balance
ORDER BY b.CName;
```

### x) List the names of those customers who have an account but no loan.

```sql
SELECT CName FROM Depositor
MINUS
SELECT CName FROM Borrower
ORDER BY CName;
```

### xi) List the branch name along with branch city that issued highest loan amount.

```sql
SELECT BName, BCity
FROM Branch
WHERE BName IN (
	SELECT BName
	FROM Loan
	WHERE Amount = (SELECT MAX(Amount) FROM Loan)
);
```

### xii) List the names of those customers who has opened an account in a city in which he is not located.

```sql
SELECT DISTINCT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE b.BCity <> c.CCity
ORDER BY d.CName;
```

### xiii) List the branch city along with total amount of loan issued by the banks.

```sql
SELECT b.BCity, SUM(l.Amount) AS total_loan_amount
FROM Loan l
JOIN Branch b ON l.BName = b.BName
GROUP BY b.BCity
ORDER BY b.BCity;
```

### xiv) List the names of those customers who have an account in a branch in Kolkata but have a loan at a bank in Mumbai.

```sql
SELECT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b1 ON a.BName = b1.BName
WHERE b1.BCity = 'Kolkata'
  AND d.CName IN (
	SELECT b.CName
	FROM Borrower b
	JOIN Loan l ON b.LoanNo = l.LoanNo
	JOIN Branch b2 ON l.BName = b2.BName
	WHERE b2.BCity = 'Mumbai'
  )
ORDER BY d.CName;
```
