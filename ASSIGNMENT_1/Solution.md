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


