# SQL Solutions – Employee Table Queries

## 1. Create User Space

```sql
CREATE USER firstname IDENTIFIED BY lastname;
GRANT CONNECT, RESOURCE TO firstname;
```

> **Note:** If you are unable to do it, just simply head over to the home page and go to Administration and Database Users, then create a new DB user with username [your actual name] and password as your title (last name) and grant DBA permission or select all permissions. That's all.

---

## 2. Create Employee Table

```sql
CREATE TABLE Employee (
    empno NUMBER PRIMARY KEY,
    ename VARCHAR2(20),
    job VARCHAR2(20),
    mgrno NUMBER,
    hiredate DATE,
    salary NUMBER(10,2),
    commission NUMBER(10,2),
    deptno NUMBER(10)
);
```

---

## 3. Insert Data

```sql
INSERT ALL
    INTO Employee VALUES (7369,'SMITH','CLERK',7902,TO_DATE('1993-06-13','YYYY-MM-DD'),800,NULL,20)
    INTO Employee VALUES (7499,'ALLEN','SALESMAN',7698,TO_DATE('1998-08-15','YYYY-MM-DD'),1600,300,30)
    INTO Employee VALUES (7521,'WARD','SALESMAN',7698,TO_DATE('1996-03-26','YYYY-MM-DD'),1250,500,30)
    INTO Employee VALUES (7566,'JONES','MANAGER',7839,TO_DATE('1995-10-31','YYYY-MM-DD'),2975,NULL,20)
    INTO Employee VALUES (7698,'BLAKE','MANAGER',7839,TO_DATE('1992-06-11','YYYY-MM-DD'),2850,NULL,30)
    INTO Employee VALUES (7782,'CLARK','MANAGER',7839,TO_DATE('1993-05-14','YYYY-MM-DD'),2450,NULL,10)
    INTO Employee VALUES (7788,'SCOTT','ANALYST',7566,TO_DATE('1996-03-05','YYYY-MM-DD'),3000,NULL,20)
    INTO Employee VALUES (7839,'KING','PRESIDENT',NULL,TO_DATE('1990-06-09','YYYY-MM-DD'),5000,NULL,10)
    INTO Employee VALUES (7844,'TURNER','SALESMAN',7698,TO_DATE('1995-06-04','YYYY-MM-DD'),1500,NULL,30)
    INTO Employee VALUES (7876,'ADAMS','CLERK',7788,TO_DATE('1999-06-04','YYYY-MM-DD'),1100,NULL,20)
    INTO Employee VALUES (7900,'JAMES','CLERK',7698,TO_DATE('2000-06-23','YYYY-MM-DD'),950,NULL,30)
    INTO Employee VALUES (7934,'MILLER','CLERK',7782,TO_DATE('2000-01-21','YYYY-MM-DD'),1300,NULL,10)
    INTO Employee VALUES (7902,'FORD','ANALYST',7566,TO_DATE('1997-12-05','YYYY-MM-DD'),3000,NULL,20)
    INTO Employee VALUES (7654,'MARTIN','SALESMAN',7698,TO_DATE('1998-12-05','YYYY-MM-DD'),1250,1400,30)
SELECT * FROM dual;
```

---

# Queries and Answers

---

### (i) Display the ename of those employees whose job is 'CLERK'.

```sql
SELECT ename 
FROM Employee 
WHERE job = 'CLERK';
```

---

### (ii) Display the empno, ename and salary of those employees working in deptno = 30.

```sql
SELECT empno, ename, salary
FROM Employee
WHERE deptno = 30;
```

---

### (iii) Display the total salary paid to employees.

```sql
SELECT SUM(salary) AS total_salary
FROM Employee;
```

---

### (iv) Display the maximum, minimum and average salaries paid to employee.

```sql
SELECT 
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary,
    AVG(salary) AS avg_salary
FROM Employee;
```

---

### (v) Display the ename and salary of the employee getting maximum salary.

```sql
SELECT ename, salary
FROM Employee
WHERE salary = (SELECT MAX(salary) FROM Employee);
```

---

### (vi) Display the total salary given to each department.

```sql
SELECT deptno, SUM(salary) AS total_salary
FROM Employee
GROUP BY deptno;
```

---

### (vii) Display the total salary given to 'SALESMAN'.

```sql
SELECT SUM(salary) AS total_salesman_salary
FROM Employee
WHERE job = 'SALESMAN';
```

---

### (viii) Display the name of the employee getting second maximum salary.

```sql
SELECT ename
FROM Employee
WHERE salary = (
    SELECT MAX(salary)
    FROM Employee
    WHERE salary < (SELECT MAX(salary) FROM Employee)
);
```

---

### (ix) Display the name and salary of those employees who are working in the same department as Ford.

```sql
SELECT ename, salary
FROM Employee
WHERE deptno = (
    SELECT deptno 
    FROM Employee 
    WHERE ename = 'FORD'
);
```

---

### (x) Display the name and designation of those employees who are getting a commission.

```sql
SELECT ename, job
FROM Employee
WHERE commission IS NOT NULL;
```

---

### (xi) Display the description of the table structure Employee.

```sql
DESC Employee;
```


