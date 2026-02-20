# SQL Solutions – Assignment 2 (CourseInfo & StudentInfo)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Tables

```sql
CREATE TABLE CourseInfo (
	CourseName VARCHAR2(10) PRIMARY KEY,
	Fees NUMBER(10,2) NOT NULL,
	HOD VARCHAR2(50) NOT NULL,
	CampusID VARCHAR2(10) NOT NULL,
	CONSTRAINT chk_course_name
		CHECK (CourseName IN ('BCA','BBA','MCA','MBA','BTech')),
	CONSTRAINT chk_campus_id
		CHECK (CampusID LIKE 'C%')
);

CREATE TABLE StudentInfo (
	StudentID NUMBER PRIMARY KEY,
	StudentName VARCHAR2(50) NOT NULL,
	CourseName VARCHAR2(10) NOT NULL,
	Semester NUMBER(2) NOT NULL,
	Marks NUMBER(5,2) NOT NULL,
	CONSTRAINT fk_student_course
		FOREIGN KEY (CourseName) REFERENCES CourseInfo(CourseName),
	CONSTRAINT chk_semester
		CHECK (Semester >= 1),
	CONSTRAINT chk_marks
		CHECK (Marks BETWEEN 0 AND 100)
);

-- Auto-increment StudentID from 101
CREATE SEQUENCE StudentInfo_Seq
	START WITH 101
	INCREMENT BY 1;

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

INSERT ALL
  INTO StudentInfo (StudentName, CourseName, Semester, Marks) VALUES ('Rahul',  'BCA',   2, 78)
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

# Queries and Answers

---

### (i) List the names of the undergraduate courses only.

```sql
SELECT CourseName
FROM CourseInfo
WHERE CourseName IN ('BCA','BBA','BTech');
```

---

### (ii) List the number of those courses that are taught in Campus C1.

```sql
SELECT COUNT(*) AS course_count
FROM CourseInfo
WHERE CampusID = 'C1';
```

---

### (iii) List the names of those courses that are taught in Campus C1 and Fees ranges between 36000 and 46000.

```sql
SELECT CourseName
FROM CourseInfo
WHERE CampusID = 'C1'
  AND Fees BETWEEN 36000 AND 46000;
```

---

### (iv) List the student names and course names of those students studying in postgraduate courses.

```sql
SELECT StudentName, CourseName
FROM StudentInfo
WHERE CourseName IN ('MCA','MBA');
```

---

### (v) List the names of students studying in 2nd Semester.

```sql
SELECT StudentName
FROM StudentInfo
WHERE Semester = 2;
```

---

### (vi) List the names of students studying in Final Semester.

```sql
SELECT StudentName
FROM StudentInfo
WHERE Semester = (SELECT MAX(Semester) FROM StudentInfo);
```

---

### (vii) List the names and marks of students arranged as per descending marks.

```sql
SELECT StudentName, Marks
FROM StudentInfo
ORDER BY Marks DESC;
```

---

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

---

### (ix) List the StudentID, StudentName and Fees of the student named 'Rahul'.

```sql
SELECT s.StudentID, s.StudentName, c.Fees
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE s.StudentName = 'Rahul';
```

---

### (x) List the name, semester and HOD of those students studying in MCA or MBA.

```sql
SELECT s.StudentName, s.Semester, c.HOD
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE s.CourseName IN ('MCA','MBA');
```

---

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

---

### (xii) List the number of students studying in BCA Course.

```sql
SELECT COUNT(*) AS student_count
FROM StudentInfo
WHERE CourseName = 'BCA';
```

---

### (xiii) List the names of all students who attend classes in Campus C2.

```sql
SELECT s.StudentName
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE c.CampusID = 'C2';
```

---

### (xiv) List the names and fees of all students who pays Rs. 46000 or more Semester Fees.

```sql
SELECT s.StudentName, c.Fees
FROM StudentInfo s
JOIN CourseInfo c ON c.CourseName = s.CourseName
WHERE c.Fees >= 46000;
```

