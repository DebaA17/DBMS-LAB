# SQL Solutions – Assignment 4

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

# Question 1: Customer, Truck, City & Shipment

## 1. Create Tables & Trigger

```sql
CREATE TABLE Customer (
	cust_id        NUMBER PRIMARY KEY,
	cust_name      VARCHAR2(50) NOT NULL,
	annual_revenue NUMBER(12,2) NOT NULL,
	cust_type      VARCHAR2(20) NOT NULL,
	CONSTRAINT chk_cust_type
		CHECK (cust_type IN ('manufacturer', 'wholesaler', 'retailer', 'distributor'))
);
```

```sql
CREATE TABLE Truck (
	truck_no    VARCHAR2(20) PRIMARY KEY,
	driver_name VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE City (
	city_name  VARCHAR2(50) PRIMARY KEY,
	population NUMBER NOT NULL
);
```

```sql
CREATE TABLE Shipment (
	shipment_no      NUMBER PRIMARY KEY,
	cust_id          NUMBER NOT NULL,
	weight           NUMBER(10,2) NOT NULL,
	truck_no         VARCHAR2(20) NOT NULL,
	start_city       VARCHAR2(50) NOT NULL,
	destination_city VARCHAR2(50) NOT NULL,
	CONSTRAINT fk_shipment_cust FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
	CONSTRAINT fk_shipment_truck FOREIGN KEY (truck_no) REFERENCES Truck(truck_no),
	CONSTRAINT fk_shipment_start FOREIGN KEY (start_city) REFERENCES City(city_name),
	CONSTRAINT fk_shipment_dest FOREIGN KEY (destination_city) REFERENCES City(city_name)
);
```

```sql
CREATE SEQUENCE cust_id_seq
	START WITH 100
	INCREMENT BY 1;
```

```sql
CREATE OR REPLACE TRIGGER trg_cust_id
BEFORE INSERT ON Customer
FOR EACH ROW
WHEN (NEW.cust_id IS NULL)
BEGIN
	SELECT cust_id_seq.NEXTVAL
	INTO :NEW.cust_id
	FROM dual;
END;
/
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('ABC Corp', 15000000, 'manufacturer')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Global Traders', 5000000, 'wholesaler')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Mega Retail', 2000000, 'retailer')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Express Distrib', 8000000, 'distributor')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Truck (truck_no, driver_name) VALUES ('TRK001', 'Amit Sen')
	INTO Truck (truck_no, driver_name) VALUES ('TRK002', 'Suresh Kumar')
	INTO Truck (truck_no, driver_name) VALUES ('TRK003', 'Rajesh Sharma')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO City (city_name, population) VALUES ('Kolkata', 15000000)
	INTO City (city_name, population) VALUES ('Delhi',   20000000)
	INTO City (city_name, population) VALUES ('Mumbai',  22000000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES (5001, 100, 2500.50, 'TRK001', 'Kolkata', 'Delhi')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES (5002, 101, 1200.00, 'TRK002', 'Kolkata', 'Kolkata')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES (5003, 102, 3100.00, 'TRK001', 'Delhi', 'Mumbai')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES (5004, 100, 1500.75, 'TRK003', 'Mumbai', 'Kolkata')
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### i) Give the details for those shipments where the start-city and destination-city are same

```sql
SELECT * FROM Shipment
WHERE start_city = destination_city;
```

### ii) Give the driver names who participated in maximum numbers of shipments?

```sql
SELECT t.driver_name
FROM Truck t
JOIN Shipment s ON t.truck_no = s.truck_no
GROUP BY t.truck_no, t.driver_name
HAVING COUNT(s.shipment_no) = (
	SELECT MAX(COUNT(shipment_no))
	FROM Shipment
	GROUP BY truck_no
);
```

### iii) Give the name of the city never appears in destination-city.

```sql
SELECT city_name FROM City
MINUS
SELECT DISTINCT destination_city FROM Shipment;
```

### iv) Give the name of the cities whose population is more than the average of all the cities.

```sql
SELECT city_name FROM City
WHERE population > (SELECT AVG(population) FROM City);
```

### v) Give the shipment details where the starting character of customer name and the last character of driver name is ‘A’.

```sql
SELECT s.*
FROM Shipment s
JOIN Customer c ON s.cust_id = c.cust_id
JOIN Truck t ON s.truck_no = t.truck_no
WHERE c.cust_name LIKE 'A%'
  AND UPPER(t.driver_name) LIKE '%A';
```

---
---

# Question 2: Employee, Department & Manager

## 1. Create Tables

```sql
CREATE TABLE Department (
	deptno NUMBER PRIMARY KEY,
	dname  VARCHAR2(50) NOT NULL,
	city   VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Employee (
	empno    VARCHAR2(10) PRIMARY KEY,
	emp_name VARCHAR2(50) NOT NULL,
	salary   NUMBER(10,2) NOT NULL,
	hiredate DATE NOT NULL,
	city     VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_empno_e CHECK (empno LIKE 'E%')
);
```

```sql
CREATE TABLE Manager (
	mgrno       VARCHAR2(10) PRIMARY KEY,
	deptno      NUMBER NOT NULL,
	manger_name VARCHAR2(50) NOT NULL,
	salary      NUMBER(10,2) NOT NULL,
	hiredate    DATE NOT NULL,
	city        VARCHAR2(50) NOT NULL,
	CONSTRAINT fk_manager_dept FOREIGN KEY (deptno) REFERENCES Department(deptno),
	CONSTRAINT chk_mgrno_m CHECK (mgrno LIKE 'M%')
);
```

```sql
CREATE TABLE Empmgr (
	empno VARCHAR2(10) NOT NULL,
	mgrno VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_empmgr PRIMARY KEY (empno, mgrno),
	CONSTRAINT fk_empmgr_emp FOREIGN KEY (empno) REFERENCES Employee(empno),
	CONSTRAINT fk_empmgr_mgr FOREIGN KEY (mgrno) REFERENCES Manager(mgrno)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Department (deptno, dname, city) VALUES (10, 'DEVELOPMENT', 'Kolkata')
	INTO Department (deptno, dname, city) VALUES (20, 'SUPPORT',     'Delhi')
	INTO Department (deptno, dname, city) VALUES (30, 'SALES',       'Mumbai')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E101', 'Debasis Biswas', 35000, TO_DATE('2005-06-15','YYYY-MM-DD'), 'Kolkata')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E102', 'Priya Sharma', 42000, TO_DATE('2006-03-10','YYYY-MM-DD'), 'Delhi')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E103', 'Suresh Kumar', 28000, TO_DATE('2006-11-20','YYYY-MM-DD'), 'Kolkata')
	INTO Employee (empno, emp_name, salary, hiredate, city) VALUES ('E104', 'Amit Sen',     50000, TO_DATE('2004-01-05','YYYY-MM-DD'), 'Mumbai')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M201', 10, 'Vikram Roy',   48000, TO_DATE('2003-05-12','YYYY-MM-DD'), 'Kolkata')
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M202', 20, 'Neha Gupta',   40000, TO_DATE('2005-09-01','YYYY-MM-DD'), 'Delhi')
	INTO Manager (mgrno, deptno, manger_name, salary, hiredate, city) VALUES ('M203', 30, 'Rajesh Gupta', 55000, TO_DATE('2002-12-15','YYYY-MM-DD'), 'Mumbai')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Empmgr (empno, mgrno) VALUES ('E101', 'M201')
	INTO Empmgr (empno, mgrno) VALUES ('E102', 'M202')
	INTO Empmgr (empno, mgrno) VALUES ('E103', 'M201')
	INTO Empmgr (empno, mgrno) VALUES ('E104', 'M203')
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### i) Give the employee names who earn more than their manager.

```sql
SELECT e.emp_name
FROM Employee e
JOIN Empmgr em ON e.empno = em.empno
JOIN Manager m ON em.mgrno = m.mgrno
WHERE e.salary > m.salary;
```

### ii) Give the name of the managers who have no employee under his supervision from the same city as of him.

```sql
SELECT m.manger_name
FROM Manager m
WHERE NOT EXISTS (
	SELECT 1
	FROM Empmgr em
	JOIN Employee e ON em.empno = e.empno
	WHERE em.mgrno = m.mgrno
	  AND e.city = m.city
);
```

### iii) Give the name of the manager who has maximum number of employees under his supervision.

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

### iv) Give the name of the employees who have been hired in the year 2006.

```sql
SELECT emp_name
FROM Employee
WHERE TO_CHAR(hiredate, 'YYYY') = '2006';
```

### v) Give the name of the city where no manager is located.

```sql
SELECT city FROM Department
MINUS
SELECT DISTINCT city FROM Manager;
```

---
---

# Question 3: Employee, Project & Parts

## 1. Create Tables

```sql
CREATE TABLE Employee_Q3 (
	empno   NUMBER PRIMARY KEY,
	empname VARCHAR2(50) NOT NULL,
	city    VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Project (
	pno   VARCHAR2(10) PRIMARY KEY,
	pname VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Part (
	partno   VARCHAR2(10) PRIMARY KEY,
	partname VARCHAR2(50) NOT NULL,
	color    VARCHAR2(20) NOT NULL
);
```

```sql
CREATE TABLE Use (
	pno    VARCHAR2(10) NOT NULL,
	partno VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_use PRIMARY KEY (pno, partno),
	CONSTRAINT fk_use_project FOREIGN KEY (pno) REFERENCES Project(pno),
	CONSTRAINT fk_use_part FOREIGN KEY (partno) REFERENCES Part(partno)
);
```

```sql
CREATE TABLE Works (
	empno NUMBER NOT NULL,
	pno   VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_works PRIMARY KEY (empno, pno),
	CONSTRAINT fk_works_emp FOREIGN KEY (empno) REFERENCES Employee_Q3(empno),
	CONSTRAINT fk_works_proj FOREIGN KEY (pno) REFERENCES Project(pno)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Employee_Q3 (empno, empname, city) VALUES (1, 'Debasis Biswas', 'Kolkata')
	INTO Employee_Q3 (empno, empname, city) VALUES (2, 'Amit Sharma',   'Delhi')
	INTO Employee_Q3 (empno, empname, city) VALUES (3, 'Sonia Sen',     'Kolkata')
	INTO Employee_Q3 (empno, empname, city) VALUES (4, 'Rajesh Gupta',  'Mumbai')
	INTO Employee_Q3 (empno, empname, city) VALUES (5, 'Swati Roy',     'Kolkata')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Project (pno, pname) VALUES ('Proj1', 'Website Redesign')
	INTO Project (pno, pname) VALUES ('Proj2', 'Mobile App')
	INTO Project (pno, pname) VALUES ('Proj3', 'Data Analytics')
	INTO Project (pno, pname) VALUES ('Proj4', 'Cloud Migration')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Part (partno, partname, color) VALUES ('Part1', 'Processor',    'Red')
	INTO Part (partno, partname, color) VALUES ('Part2', 'Memory Board',  'Blue')
	INTO Part (partno, partname, color) VALUES ('Part3', 'Cabling',       'Red')
	INTO Part (partno, partname, color) VALUES ('Part4', 'Chassis',       'Black')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Use (pno, partno) VALUES ('Proj1', 'Part1')
	INTO Use (pno, partno) VALUES ('Proj1', 'Part2')
	INTO Use (pno, partno) VALUES ('Proj1', 'Part3')
	INTO Use (pno, partno) VALUES ('Proj2', 'Part1')
	INTO Use (pno, partno) VALUES ('Proj2', 'Part2')
	INTO Use (pno, partno) VALUES ('Proj3', 'Part1')
	INTO Use (pno, partno) VALUES ('Proj3', 'Part3')
	INTO Use (pno, partno) VALUES ('Proj4', 'Part1')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Works (empno, pno) VALUES (1, 'Proj1')
	INTO Works (empno, pno) VALUES (1, 'Proj2')
	INTO Works (empno, pno) VALUES (2, 'Proj1')
	INTO Works (empno, pno) VALUES (3, 'Proj2')
	INTO Works (empno, pno) VALUES (3, 'Proj3')
	INTO Works (empno, pno) VALUES (4, 'Proj4')
	INTO Works (empno, pno) VALUES (5, 'Proj1')
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### a) Give the name of the employees who are working on more than 1 project.

```sql
SELECT e.empname
FROM Employee_Q3 e
JOIN Works w ON e.empno = w.empno
GROUP BY e.empno, e.empname
HAVING COUNT(w.pno) > 1;
```

### b) Give the name of the city where the maximum employees are located.

```sql
SELECT city
FROM Employee_Q3
GROUP BY city
HAVING COUNT(empno) = (
	SELECT MAX(COUNT(empno))
	FROM Employee_Q3
	GROUP BY city
);
```

### c) Give the part names, which are used in all the projects.

```sql
SELECT p.partname
FROM Part p
JOIN Use u ON p.partno = u.partno
GROUP BY p.partno, p.partname
HAVING COUNT(DISTINCT u.pno) = (SELECT COUNT(*) FROM Project);
```

### d) Give the name of the projects in which employees are working whose name start with 'S'.

```sql
SELECT DISTINCT pr.pname
FROM Project pr
JOIN Works w ON pr.pno = w.pno
JOIN Employee_Q3 e ON w.empno = e.empno
WHERE e.empname LIKE 'S%';
```

### e) Give the name of the project which use maximum red part.

```sql
SELECT pr.pname
FROM Project pr
JOIN Use u ON pr.pno = u.pno
JOIN Part p ON u.partno = p.partno
WHERE p.color = 'Red'
GROUP BY pr.pno, pr.pname
HAVING COUNT(u.partno) = (
	SELECT MAX(COUNT(u2.partno))
	FROM Use u2
	JOIN Part p2 ON u2.partno = p2.partno
	WHERE p2.color = 'Red'
	GROUP BY u2.pno
);
```

### f) Give the name of the projects, which has used exactly 3 parts.

```sql
SELECT pr.pname
FROM Project pr
JOIN Use u ON pr.pno = u.pno
GROUP BY pr.pno, pr.pname
HAVING COUNT(u.partno) = 3;
```

---
---

# Question 4: Banking Schema III

## 1. Create Tables

```sql
CREATE TABLE Branch_Q4 (
	branch_name VARCHAR2(50) PRIMARY KEY,
	branch_city VARCHAR2(50) NOT NULL,
	assets      NUMBER(12,2) NOT NULL
);
```

```sql
CREATE TABLE Customer_Q4 (
	customer_name VARCHAR2(50) PRIMARY KEY,
	street        VARCHAR2(50) NOT NULL,
	city          VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Loan_Q4 (
	branch_name VARCHAR2(50) NOT NULL,
	loan_no     VARCHAR2(10) PRIMARY KEY,
	amount      NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_loan_branch_q4 FOREIGN KEY (branch_name) REFERENCES Branch_Q4(branch_name)
);
```

```sql
CREATE TABLE Borrower_Q4 (
	customer_name VARCHAR2(50) NOT NULL,
	loan_no       VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_borrower_q4 PRIMARY KEY (customer_name, loan_no),
	CONSTRAINT fk_borrower_cust_q4 FOREIGN KEY (customer_name) REFERENCES Customer_Q4(customer_name),
	CONSTRAINT fk_borrower_loan_q4 FOREIGN KEY (loan_no) REFERENCES Loan_Q4(loan_no)
);
```

```sql
CREATE TABLE Account_Q4 (
	branch_name VARCHAR2(50) NOT NULL,
	account_no  VARCHAR2(10) PRIMARY KEY,
	balance     NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_account_branch_q4 FOREIGN KEY (branch_name) REFERENCES Branch_Q4(branch_name)
);
```

```sql
CREATE TABLE Depositor_Q4 (
	customer_name VARCHAR2(50) NOT NULL,
	account_no    VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_depositor_q4 PRIMARY KEY (customer_name, account_no),
	CONSTRAINT fk_depositor_cust_q4 FOREIGN KEY (customer_name) REFERENCES Customer_Q4(customer_name),
	CONSTRAINT fk_depositor_acc_q4  FOREIGN KEY (account_no) REFERENCES Account_Q4(account_no)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Branch_Q4 (branch_name, branch_city, assets) VALUES ('Salt Lake',     'Kolkata',  30000)
	INTO Branch_Q4 (branch_name, branch_city, assets) VALUES ('New Market',    'Kolkata',  15000)
	INTO Branch_Q4 (branch_name, branch_city, assets) VALUES ('Connaught Place','Delhi',   50000)
	INTO Branch_Q4 (branch_name, branch_city, assets) VALUES ('Colaba',        'Mumbai',   45000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Customer_Q4 (customer_name, street, city) VALUES ('Debasis Biswas',   'Salt Lake Sec 1', 'Kolkata')
	INTO Customer_Q4 (customer_name, street, city) VALUES ('Rahul Roy',       'Lake Road',       'Kolkata')
	INTO Customer_Q4 (customer_name, street, city) VALUES ('Priya Sharma',    'Noida Sec 62',    'Delhi')
	INTO Customer_Q4 (customer_name, street, city) VALUES ('Neha Gupta',      'Karol Bagh',      'Delhi')
	INTO Customer_Q4 (customer_name, street, city) VALUES ('Vikram Malhotra', 'Bandra West',     'Mumbai')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Account_Q4 (branch_name, account_no, balance) VALUES ('Salt Lake',      'A101', 15000)
	INTO Account_Q4 (branch_name, account_no, balance) VALUES ('New Market',      'A102', 8000)
	INTO Account_Q4 (branch_name, account_no, balance) VALUES ('Connaught Place', 'A103', 35000)
	INTO Account_Q4 (branch_name, account_no, balance) VALUES ('Colaba',          'A104', 25000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Depositor_Q4 (customer_name, account_no) VALUES ('Debasis Biswas',   'A101')
	INTO Depositor_Q4 (customer_name, account_no) VALUES ('Rahul Roy',       'A102')
	INTO Depositor_Q4 (customer_name, account_no) VALUES ('Priya Sharma',    'A103')
	INTO Depositor_Q4 (customer_name, account_no) VALUES ('Vikram Malhotra', 'A104')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Loan_Q4 (branch_name, loan_no, amount) VALUES ('Salt Lake',      'L101', 20000)
	INTO Loan_Q4 (branch_name, loan_no, amount) VALUES ('New Market',     'L102', 10000)
	INTO Loan_Q4 (branch_name, loan_no, amount) VALUES ('Connaught Place','L103', 40000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Borrower_Q4 (customer_name, loan_no) VALUES ('Debasis Biswas',   'L101')
	INTO Borrower_Q4 (customer_name, loan_no) VALUES ('Rahul Roy',       'L102')
	INTO Borrower_Q4 (customer_name, loan_no) VALUES ('Priya Sharma',    'L103')
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### a) Give the customer name who has account but not any loan.

```sql
SELECT customer_name FROM Depositor_Q4
MINUS
SELECT customer_name FROM Borrower_Q4;
```

### b) Give the name of the customer who has either (10000-20000) or (30000-40000) in their account.

```sql
SELECT DISTINCT d.customer_name
FROM Depositor_Q4 d
JOIN Account_Q4 a ON d.account_no = a.account_no
WHERE a.balance BETWEEN 10000 AND 20000
   OR a.balance BETWEEN 30000 AND 40000;
```

### c) Which branch has issued maximum amount of loan?

```sql
SELECT branch_name
FROM Loan_Q4
WHERE amount = (SELECT MAX(amount) FROM Loan_Q4);
```

### d) Give the name of the customer who has maximum balance in their account.

```sql
SELECT d.customer_name
FROM Depositor_Q4 d
JOIN Account_Q4 a ON d.account_no = a.account_no
WHERE a.balance = (SELECT MAX(balance) FROM Account_Q4);
```

### e) Give the name of the customer who has opened an account in a city in which he is not located.

```sql
SELECT DISTINCT d.customer_name
FROM Depositor_Q4 d
JOIN Account_Q4 a ON d.account_no = a.account_no
JOIN Branch_Q4 b ON a.branch_name = b.branch_name
JOIN Customer_Q4 c ON d.customer_name = c.customer_name
WHERE b.branch_city <> c.city;
```

---
---

# Question 5: Flights & Aircraft

## 1. Create Tables

```sql
CREATE TABLE Aircraft (
	aid  NUMBER PRIMARY KEY,
	type VARCHAR2(30) NOT NULL
);
```

```sql
CREATE TABLE Flights (
	flno    VARCHAR2(10) PRIMARY KEY,
	aid     NUMBER NOT NULL,
	company VARCHAR2(50) NOT NULL,
	CONSTRAINT fk_flights_aircraft FOREIGN KEY (aid) REFERENCES Aircraft(aid)
);
```

```sql
CREATE TABLE Employees (
	eid    NUMBER PRIMARY KEY,
	ename  VARCHAR2(50) NOT NULL,
	salary NUMBER(10,2) NOT NULL
);
```

```sql
CREATE TABLE Certified (
	eid NUMBER NOT NULL,
	aid NUMBER NOT NULL,
	CONSTRAINT pk_certified PRIMARY KEY (eid, aid),
	CONSTRAINT fk_certified_emp FOREIGN KEY (eid) REFERENCES Employees(eid),
	CONSTRAINT fk_certified_air FOREIGN KEY (aid) REFERENCES Aircraft(aid)
);
```

```sql
CREATE TABLE Schedule (
	eid              NUMBER NOT NULL,
	flno             VARCHAR2(10) NOT NULL,
	source_city      VARCHAR2(50) NOT NULL,
	destination_city VARCHAR2(50) NOT NULL,
	s_date           DATE NOT NULL,
	CONSTRAINT pk_schedule PRIMARY KEY (eid, flno, s_date),
	CONSTRAINT fk_schedule_emp FOREIGN KEY (eid) REFERENCES Employees(eid),
	CONSTRAINT fk_schedule_flight FOREIGN KEY (flno) REFERENCES Flights(flno)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Aircraft (aid, type) VALUES (1, 'Boeing 747')
	INTO Aircraft (aid, type) VALUES (2, 'Airbus A320')
	INTO Aircraft (aid, type) VALUES (3, 'Boeing 737')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Flights (flno, aid, company) VALUES ('AI101', 1, 'Air India')
	INTO Flights (flno, aid, company) VALUES ('6E202', 2, 'IndiGo')
	INTO Flights (flno, aid, company) VALUES ('SG303', 3, 'SpiceJet')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Employees (eid, ename, salary) VALUES (501, 'Debasis Biswas', 80000)
	INTO Employees (eid, ename, salary) VALUES (502, 'Pooja Bose',   95000)
	INTO Employees (eid, ename, salary) VALUES (503, 'Rohan Sen',    45000)
	INTO Employees (eid, ename, salary) VALUES (504, 'Sunita Das',   75000)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Certified (eid, aid) VALUES (501, 1)
	INTO Certified (eid, aid) VALUES (501, 2)
	INTO Certified (eid, aid) VALUES (502, 2)
	INTO Certified (eid, aid) VALUES (504, 3)
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Schedule (eid, flno, source_city, destination_city, s_date) VALUES (501, 'AI101', 'Kolkata', 'Delhi',  TO_DATE('2024-07-10','YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, s_date) VALUES (502, '6E202', 'Delhi',   'Mumbai', TO_DATE('2024-07-11','YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, s_date) VALUES (504, 'SG303', 'Mumbai',  'Kolkata', TO_DATE('2024-07-12','YYYY-MM-DD'))
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### a) Give the name of the employee who has certification on more than 1 type of aircrafts.

```sql
SELECT e.ename
FROM Employees e
JOIN Certified c ON e.eid = c.eid
GROUP BY e.eid, e.ename
HAVING COUNT(c.aid) > 1;
```

### b) Give the name of the employee who has no certification.

```sql
SELECT ename FROM Employees
MINUS
SELECT DISTINCT e.ename
FROM Employees e
JOIN Certified c ON e.eid = c.eid;
```

### c) Give the name of the city where from maximum flight takes off (source_city)?

```sql
SELECT source_city
FROM Schedule
GROUP BY source_city
HAVING COUNT(flno) = (
	SELECT MAX(COUNT(flno))
	FROM Schedule
	GROUP BY source_city
);
```

### d) Give the name of the company, which spend maximum salary for their employees.

```sql
SELECT f.company
FROM Flights f
JOIN Schedule s ON f.flno = s.flno
JOIN Employees e ON s.eid = e.eid
GROUP BY f.company
HAVING SUM(e.salary) = (
	SELECT MAX(SUM(e2.salary))
	FROM Flights f2
	JOIN Schedule s2 ON f2.flno = s2.flno
	JOIN Employees e2 ON s2.eid = e2.eid
	GROUP BY f2.company
);
```

### e) Give the name of the company which has maximum type of flight.

```sql
SELECT company
FROM Flights
GROUP BY company
HAVING COUNT(DISTINCT flno) = (
	SELECT MAX(COUNT(DISTINCT flno))
	FROM Flights
	GROUP BY company
);
```

---
---

# Question 6: Parts & Suppliers

## 1. Create Tables

```sql
CREATE TABLE Parts_Q6 (
	p_id   VARCHAR2(10) PRIMARY KEY,
	p_name VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE Supplier_Q6 (
	s_id   VARCHAR2(10) PRIMARY KEY,
	s_name VARCHAR2(50) NOT NULL
);
```

```sql
CREATE TABLE SPJ (
	s_id VARCHAR2(10) NOT NULL,
	p_id VARCHAR2(10) NOT NULL,
	cost NUMBER(10,2) NOT NULL,
	CONSTRAINT pk_spj PRIMARY KEY (s_id, p_id),
	CONSTRAINT fk_spj_supplier FOREIGN KEY (s_id) REFERENCES Supplier_Q6(s_id),
	CONSTRAINT fk_spj_parts FOREIGN KEY (p_id) REFERENCES Parts_Q6(p_id)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Parts_Q6 (p_id, p_name) VALUES ('P1', 'Pen')
	INTO Parts_Q6 (p_id, p_name) VALUES ('P2', 'Paper')
	INTO Parts_Q6 (p_id, p_name) VALUES ('P3', 'Pencil')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Supplier_Q6 (s_id, s_name) VALUES ('S1', 'SOne')
	INTO Supplier_Q6 (s_id, s_name) VALUES ('S2', 'STwo')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO SPJ (s_id, p_id, cost) VALUES ('S1', 'P1', 10.00)
	INTO SPJ (s_id, p_id, cost) VALUES ('S1', 'P2', 15.00)
	INTO SPJ (s_id, p_id, cost) VALUES ('S2', 'P2', 12.00)
	INTO SPJ (s_id, p_id, cost) VALUES ('S2', 'P3', 8.00)
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### a) Give the parts name supplied by S1.

```sql
SELECT DISTINCT p.p_name
FROM Parts_Q6 p
JOIN SPJ s ON p.p_id = s.p_id
WHERE s.s_id = 'S1'
ORDER BY p.p_name;
```

### b) Select the number of parts supplied by each supplier.

```sql
SELECT s_id, COUNT(DISTINCT p_id) AS parts_count
FROM SPJ
GROUP BY s_id
ORDER BY s_id;
```

### c) What parts are supplied only by S1?

```sql
SELECT p.p_name
FROM Parts_Q6 p
JOIN SPJ s ON p.p_id = s.p_id
WHERE s.s_id = 'S1'
  AND NOT EXISTS (
		SELECT 1
		FROM SPJ s2
		WHERE s2.p_id = s.p_id
		  AND s2.s_id <> 'S1'
  )
ORDER BY p.p_name;
```

### d) Give name of the parts which one is supplied by all the supplier.

```sql
SELECT p.p_name
FROM Parts_Q6 p
JOIN SPJ s ON p.p_id = s.p_id
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT s.s_id) = (SELECT COUNT(*) FROM Supplier_Q6)
ORDER BY p.p_name;
```

### e) What parts are supplied by both S1 & S2?

```sql
SELECT p.p_name
FROM Parts_Q6 p
JOIN SPJ s ON p.p_id = s.p_id
WHERE s.s_id IN ('S1', 'S2')
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT s.s_id) = 2
ORDER BY p.p_name;
```

### f) Give the supplier name who supplied parts of maximum cost.

```sql
SELECT DISTINCT s.s_name
FROM Supplier_Q6 s
JOIN SPJ sp ON s.s_id = sp.s_id
WHERE sp.cost = (SELECT MAX(cost) FROM SPJ);
```
