# SQL Solutions – Assignment 2

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

# Question 3: CourseInfo & StudentInfo

## 1. Create Tables & Sequences

```sql
CREATE TABLE CourseInfo (
	CourseName VARCHAR2(10) PRIMARY KEY,
	Fees       NUMBER(10,2) NOT NULL,
	HOD        VARCHAR2(50) NOT NULL,
	CampusID   VARCHAR2(10) NOT NULL,
	CONSTRAINT chk_course_name
		CHECK (CourseName IN ('BCA','BBA','MCA','MBA','BTech')),
	CONSTRAINT chk_campus_id
		CHECK (CampusID LIKE 'C%')
);
```

```sql
CREATE TABLE StudentInfo (
	StudentID   NUMBER PRIMARY KEY,
	StudentName VARCHAR2(50) NOT NULL,
	CourseName  VARCHAR2(10) NOT NULL,
	Semester    NUMBER(2) NOT NULL,
	Marks       NUMBER(5,2) NOT NULL,
	CONSTRAINT fk_student_course
		FOREIGN KEY (CourseName) REFERENCES CourseInfo(CourseName),
	CONSTRAINT chk_semester
		CHECK (Semester >= 1),
	CONSTRAINT chk_marks
		CHECK (Marks BETWEEN 0 AND 100)
);
```

```sql
CREATE SEQUENCE StudentInfo_Seq
	START WITH 101
	INCREMENT BY 1;
```

```sql
CREATE OR REPLACE TRIGGER StudentInfo_BI
BEFORE INSERT ON StudentInfo
FOR EACH ROW
WHEN (NEW.StudentID IS NULL)
BEGIN
	SELECT StudentInfo_Seq.NEXTVAL
	INTO :NEW.StudentID
	FROM dual;
END;
/
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO CourseInfo (CourseName, Fees, HOD, CampusID) VALUES ('BCA',   42000, 'Dr. Sen',    'C1')
	INTO CourseInfo (CourseName, Fees, HOD, CampusID) VALUES ('BBA',   38000, 'Dr. Kapoor', 'C1')
	INTO CourseInfo (CourseName, Fees, HOD, CampusID) VALUES ('MCA',   50000, 'Dr. Dutta',  'C2')
	INTO CourseInfo (CourseName, Fees, HOD, CampusID) VALUES ('MBA',   55000, 'Dr. Roy',    'C1')
	INTO CourseInfo (CourseName, Fees, HOD, CampusID) VALUES ('BTech', 60000, 'Dr. Bose',   'C2')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Debasis', 'BCA',   2, 78)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Neha',   'BCA',   6, 84)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Arjun',  'BBA',   2, 76)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Ananya', 'BBA',   6, 82)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Amit',   'MBA',   2, 85)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Meera',  'MBA',   4, 89)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Rajesh', 'MCA',   3, 88)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Sneha',  'MCA',   4, 91)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Karan',  'BTech', 7, 79)
	INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Priya',  'BTech', 8, 93)
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### (i) List the names of the undergraduate courses only.

```sql
SELECT CourseName
FROM CourseInfo
WHERE CourseName IN ('BCA','BBA','BTech');
```

### (ii) List the number of those courses that are taught in Campus C1.

```sql
SELECT COUNT(*) AS course_count
FROM CourseInfo
WHERE CampusID = 'C1';
```

### (iii) List the names of those courses that are taught in Campus C1 and Fees ranges between 36000 and 46000.

```sql
SELECT CourseName
FROM CourseInfo
WHERE CampusID = 'C1'
  AND Fees BETWEEN 36000 AND 46000;
```

### (iv) List the student names and course names of those students studying in postgraduate courses.

```sql
SELECT StudentName, CourseName
FROM StudentInfo
WHERE CourseName IN ('MCA','MBA');
```

### (v) List the names of students studying in 2nd Semester.

```sql
SELECT StudentName
FROM StudentInfo
WHERE Semester = 2;
```

### (vi) List the names of students studying in Final Semester.

```sql
SELECT StudentName
FROM StudentInfo
WHERE Semester = (SELECT MAX(Semester) FROM StudentInfo);
```

### (vii) List the names and marks of students arranged as per descending marks.

```sql
SELECT StudentName, Marks
FROM StudentInfo
ORDER BY Marks DESC;
```

### (viii) List the names of student and course for the top three students along with their marks.

```sql
SELECT StudentName, CourseName, Marks
FROM (
	SELECT StudentName, CourseName, Marks
	FROM StudentInfo
	ORDER BY Marks DESC
)
WHERE ROWNUM <= 3;
```

### (ix) List the StudentID, StudentName and Fees of the student named 'Rahul'.

```sql
SELECT s.StudentID, s.StudentName, c.Fees
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE s.StudentName = 'Rahul';
```

### (x) List the name, semester and HOD of those students studying in MCA or MBA.

```sql
SELECT s.StudentName, s.Semester, c.HOD
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE s.CourseName IN ('MCA','MBA');
```

### (xi) List the names, course and semester of those students for the course that 'Rajesh' is studying.

```sql
SELECT s.StudentName, s.CourseName, s.Semester
FROM StudentInfo s
WHERE s.CourseName = (
	SELECT CourseName
	FROM StudentInfo
	WHERE StudentName = 'Rajesh'
);
```

### (xii) List the number of students studying in BCA Course.

```sql
SELECT COUNT(*) AS student_count
FROM StudentInfo
WHERE CourseName = 'BCA';
```

### (xiii) List the names of all students who attend classes in Campus C2.

```sql
SELECT s.StudentName
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE c.CampusID = 'C2';
```

### (xiv) List the names and fees of all students who pays Rs. 46000 or more Semester Fees.

```sql
SELECT s.StudentName, c.Fees
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE c.Fees >= 46000;
```

---
---

# Question 4: Parts, Supplier & Cost

## 1. Create Tables

```sql
CREATE TABLE Parts (
	p_id   VARCHAR2(10) PRIMARY KEY,
	p_name VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_parts_name
		CHECK (p_name LIKE 'P%')
);
```

```sql
CREATE TABLE Supplier (
	s_id   VARCHAR2(10) PRIMARY KEY,
	s_name VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_supplier_name
		CHECK (s_name LIKE 'S%')
);
```

```sql
CREATE TABLE Cost (
	s_id VARCHAR2(10) NOT NULL,
	p_id VARCHAR2(10) NOT NULL,
	cost NUMBER(10,2) NOT NULL,
	CONSTRAINT pk_cost PRIMARY KEY (s_id, p_id),
	CONSTRAINT fk_cost_supplier FOREIGN KEY (s_id) REFERENCES Supplier (s_id),
	CONSTRAINT fk_cost_parts    FOREIGN KEY (p_id) REFERENCES Parts (p_id),
	CONSTRAINT chk_cost_positive CHECK (cost > 0)
);
```

---

## 2. Insert Data

```sql
INSERT ALL
	INTO Parts (p_id, p_name) VALUES ('P1', 'PEN')
	INTO Parts (p_id, p_name) VALUES ('P2', 'PAPER')
	INTO Parts (p_id, p_name) VALUES ('P3', 'PENCIL')
	INTO Parts (p_id, p_name) VALUES ('P4', 'PCLIP')
	INTO Parts (p_id, p_name) VALUES ('P5', 'PAD')
	INTO Parts (p_id, p_name) VALUES ('P6', 'PLATE')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Supplier (s_id, s_name) VALUES ('S1', 'SOne')
	INTO Supplier (s_id, s_name) VALUES ('S2', 'STwo')
	INTO Supplier (s_id, s_name) VALUES ('S3', 'SThree')
SELECT * FROM dual;
```

```sql
INSERT ALL
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P1',  5)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P2', 12)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P3',  8)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P4', 20)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P5',  7)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P2', 11)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P3',  9)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P4', 18)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P6',  6)
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P2', 10)
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P4', 25)
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P6',  7)
SELECT * FROM dual;
```

---

## 3. Queries and Answers

### (i) Display the parts’ name supplied by supplier S1.

```sql
SELECT DISTINCT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id = 'S1'
ORDER BY p.p_name;
```

### (ii) Display the number of parts supplied by each supplier.

```sql
SELECT c.s_id, COUNT(DISTINCT c.p_id) AS parts_count
FROM Cost c
GROUP BY c.s_id
ORDER BY c.s_id;
```

### (iii) Display the names of the parts supplied by supplier S1 only.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id = 'S1'
  AND NOT EXISTS (
		SELECT 1
		FROM Cost c2
		WHERE c2.p_id = c.p_id
		  AND c2.s_id <> 'S1'
  )
ORDER BY p.p_name;
```

### (iv) Display the name of the parts supplied by all the suppliers.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT c.s_id) = (SELECT COUNT(*) FROM Supplier)
ORDER BY p.p_name;
```

### (v) Display the name of the parts supplied by both S1 and S2.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id IN ('S1', 'S2')
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT c.s_id) = 2
ORDER BY p.p_name;
```

### (vi) Display the supplier name who supplies parts of maximum cost.

```sql
SELECT DISTINCT s.s_name
FROM Supplier s
JOIN Cost c ON c.s_id = s.s_id
WHERE c.cost = (SELECT MAX(cost) FROM Cost);
```

### (vii) Display the part and supplier id’s for the three lowest cost parts.

```sql
SELECT s_id, p_id, cost
FROM (
	SELECT s_id, p_id, cost
	FROM Cost
	ORDER BY cost ASC, s_id, p_id
)
WHERE ROWNUM <= 3;
```

### (viii) Display the part name with minimum cost.

```sql
SELECT DISTINCT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.cost = (SELECT MIN(cost) FROM Cost)
ORDER BY p.p_name;
```

### (ix) Find the total number of parts supplied by supplier S1.

```sql
SELECT COUNT(DISTINCT p_id) AS total_parts_by_s1
FROM Cost
WHERE s_id = 'S1';
```

### (x) Find the total number of parts supplied by supplier S2 with cost greater than Rs. 10.

```sql
SELECT COUNT(DISTINCT p_id) AS total_parts_by_s2_cost_gt_10
FROM Cost
WHERE s_id = 'S2'
  AND cost > 10;
```
