# SQL Solutions – Assignment 11 (Flights & Aircraft Schema)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

*Note: In Oracle SQL, `DATE` is a reserved keyword. The date column in the `Schedule` table has been named `flight_date` to prevent compilation and execution errors.*

---

## 1. Create Tables

**(A) Aircraft**

```sql
CREATE TABLE Aircraft (
	aid  VARCHAR2(10) PRIMARY KEY,
	type VARCHAR2(50) NOT NULL
);
```

**(B) Flights**

```sql
CREATE TABLE Flights (
	flno    VARCHAR2(10) PRIMARY KEY,
	aid     VARCHAR2(10) NOT NULL,
	company VARCHAR2(50) NOT NULL,
	CONSTRAINT fk_flights_aircraft
		FOREIGN KEY (aid) REFERENCES Aircraft(aid)
);
```

**(C) Employees**

```sql
CREATE TABLE Employees (
	eid    VARCHAR2(10) PRIMARY KEY,
	ename  VARCHAR2(50) NOT NULL,
	salary NUMBER(10,2) NOT NULL
);
```

**(D) Certified**

```sql
CREATE TABLE Certified (
	eid VARCHAR2(10) NOT NULL,
	aid VARCHAR2(10) NOT NULL,
	CONSTRAINT pk_certified
		PRIMARY KEY (eid, aid),
	CONSTRAINT fk_certified_employee
		FOREIGN KEY (eid) REFERENCES Employees(eid),
	CONSTRAINT fk_certified_aircraft
		FOREIGN KEY (aid) REFERENCES Aircraft(aid)
);
```

**(E) Schedule**

```sql
CREATE TABLE Schedule (
	eid              VARCHAR2(10) NOT NULL,
	flno             VARCHAR2(10) NOT NULL,
	source_city      VARCHAR2(50) NOT NULL,
	destination_city VARCHAR2(50) NOT NULL,
	flight_date      DATE NOT NULL,
	CONSTRAINT pk_schedule
		PRIMARY KEY (eid, flno, flight_date),
	CONSTRAINT fk_schedule_employee
		FOREIGN KEY (eid) REFERENCES Employees(eid),
	CONSTRAINT fk_schedule_flight
		FOREIGN KEY (flno) REFERENCES Flights(flno)
);
```

---

## 2. Insert Data

**(A) Insert into Aircraft**

```sql
INSERT ALL
	INTO Aircraft (aid, type) VALUES ('A01', 'Boeing 737')
	INTO Aircraft (aid, type) VALUES ('A02', 'Boeing 777')
	INTO Aircraft (aid, type) VALUES ('A03', 'Airbus A320')
	INTO Aircraft (aid, type) VALUES ('A04', 'Airbus A350')
SELECT * FROM dual;
```

**(B) Insert into Flights**

```sql
INSERT ALL
	INTO Flights (flno, aid, company) VALUES ('F101', 'A01', 'Air India')
	INTO Flights (flno, aid, company) VALUES ('F102', 'A02', 'Air India')
	INTO Flights (flno, aid, company) VALUES ('F103', 'A03', 'Indigo')
	INTO Flights (flno, aid, company) VALUES ('F104', 'A04', 'SpiceJet')
SELECT * FROM dual;
```

**(C) Insert into Employees**

```sql
INSERT ALL
	INTO Employees (eid, ename, salary) VALUES ('E01', 'Rahul Sharma', 90000)
	INTO Employees (eid, ename, salary) VALUES ('E02', 'Priya Patel',   120000)
	INTO Employees (eid, ename, salary) VALUES ('E03', 'Amit Verma',    85000)
	INTO Employees (eid, ename, salary) VALUES ('E04', 'Vikram Singh',  95000)
	INTO Employees (eid, ename, salary) VALUES ('E05', 'Neha Gupta',    60000)
SELECT * FROM dual;
```

**(D) Insert into Certified**

```sql
INSERT ALL
	INTO Certified (eid, aid) VALUES ('E01', 'A01')
	INTO Certified (eid, aid) VALUES ('E01', 'A02')
	INTO Certified (eid, aid) VALUES ('E02', 'A03')
	INTO Certified (eid, aid) VALUES ('E03', 'A01')
	INTO Certified (eid, aid) VALUES ('E04', 'A04')
SELECT * FROM dual;
```

**(E) Insert into Schedule**

```sql
INSERT ALL
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E01', 'F101', 'Delhi',   'Mumbai',    TO_DATE('2026-06-01', 'YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E01', 'F102', 'Delhi',   'Kolkata',   TO_DATE('2026-06-02', 'YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E02', 'F103', 'Mumbai',  'Delhi',     TO_DATE('2026-06-01', 'YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E03', 'F101', 'Kolkata', 'Delhi',     TO_DATE('2026-06-01', 'YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E04', 'F104', 'Chennai', 'Delhi',     TO_DATE('2026-06-01', 'YYYY-MM-DD'))
	INTO Schedule (eid, flno, source_city, destination_city, flight_date) VALUES ('E05', 'F103', 'Delhi',   'Chennai',   TO_DATE('2026-06-03', 'YYYY-MM-DD'))
SELECT * FROM dual;
```

---

# Queries and Answers

---

### a) Give the name of the employee who has certification on more than 1 type of aircrafts.

```sql
SELECT e.ename
FROM Employees e
JOIN Certified c ON e.eid = c.eid
JOIN Aircraft a ON c.aid = a.aid
GROUP BY e.eid, e.ename
HAVING COUNT(DISTINCT a.type) > 1;
```

---

### b) Give the name of the employee who has no certification.

```sql
SELECT ename
FROM Employees
WHERE eid NOT IN (
	SELECT DISTINCT eid
	FROM Certified
);
```

---

### c) Give the name of the city where from maximum flight takes off (source_city)?

```sql
SELECT source_city
FROM Schedule
GROUP BY source_city
HAVING COUNT(*) = (
	SELECT MAX(COUNT(*))
	FROM Schedule
	GROUP BY source_city
);
```

---

### d) Give the name of the company, which spend maximum salary for their employees.

```sql
SELECT company
FROM (
	SELECT DISTINCT f.company, e.eid, e.salary
	FROM Flights f
	JOIN Schedule s ON f.flno = s.flno
	JOIN Employees e ON s.eid = e.eid
)
GROUP BY company
HAVING SUM(salary) = (
	SELECT MAX(SUM(salary))
	FROM (
		SELECT DISTINCT f2.company, e2.eid, e2.salary
		FROM Flights f2
		JOIN Schedule s2 ON f2.flno = s2.flno
		JOIN Employees e2 ON s2.eid = e2.eid
	)
	GROUP BY company
);
```

---

### e) Give the name of the company which has maximum type of flight.

```sql
SELECT f.company
FROM Flights f
JOIN Aircraft a ON f.aid = a.aid
GROUP BY f.company
HAVING COUNT(DISTINCT a.type) = (
	SELECT MAX(COUNT(DISTINCT a2.type))
	FROM Flights f2
	JOIN Aircraft a2 ON f2.aid = a2.aid
	GROUP BY f2.company
);
```
