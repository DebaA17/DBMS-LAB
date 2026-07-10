# PL/SQL Solutions – Assignment 5

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## Prerequisites (Setup EMP & DEPT tables)

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
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7499,'ALLEN',  'SALESMAN',  TO_DATE('1998-08-15','YYYY-MM-DD'), 7698, 1600, 300, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7521,'WARD',   'SALESMAN',  TO_DATE('1996-03-26','YYYY-MM-DD'), 7698, 1250, 500, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7844,'TURNER', 'SALESMAN',  TO_DATE('1995-06-04','YYYY-MM-DD'), 7698, 1500, NULL, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7900,'JAMES',  'CLERK',     TO_DATE('2000-06-23','YYYY-MM-DD'), 7698, 950, NULL, 30)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7934,'MILLER', 'CLERK',     TO_DATE('2000-01-21','YYYY-MM-DD'), 7782, 1300, NULL, 10)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7369,'SMITH',  'CLERK',     TO_DATE('1993-06-13','YYYY-MM-DD'), 7902, 800, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7876,'ADAMS',  'CLERK',     TO_DATE('1999-06-04','YYYY-MM-DD'), 7788, 1100, NULL, 20)
	INTO EMP (EMP#, ENAME, JOB, HIREDATE, MANAGER#, SALARY, COMM, DEPT#) VALUES (7654,'MARTIN', 'SALESMAN',  TO_DATE('1998-12-05','YYYY-MM-DD'), 7698, 1250, 1400, 30)
SELECT * FROM dual;
```

---

### 1. Find Greatest and Smallest of Four Integers

Write a PL/SQL block to find the greatest and smallest among four entered integers.

```sql
DECLARE
	a NUMBER := 15;
	b NUMBER := 42;
	c NUMBER := 8;
	d NUMBER := 23;
	greatest NUMBER;
	smallest NUMBER;
BEGIN
	greatest := a;
	smallest := a;

	IF b > greatest THEN greatest := b; END IF;
	IF c > greatest THEN greatest := c; END IF;
	IF d > greatest THEN greatest := d; END IF;

	IF b < smallest THEN smallest := b; END IF;
	IF c < smallest THEN smallest := c; END IF;
	IF d < smallest THEN smallest := d; END IF;

	DBMS_OUTPUT.PUT_LINE('Numbers: ' || a || ', ' || b || ', ' || c || ', ' || d);
	DBMS_OUTPUT.PUT_LINE('Greatest: ' || greatest);
	DBMS_OUTPUT.PUT_LINE('Smallest: ' || smallest);
END;
/
```

---

### 2. Leap Year Checker

Write a PL/SQL block to check whether an entered year is a leap year or not.

```sql
DECLARE
	y NUMBER := 2024;
BEGIN
	IF (MOD(y, 4) = 0 AND MOD(y, 100) <> 0) OR MOD(y, 400) = 0 THEN
		DBMS_OUTPUT.PUT_LINE(y || ' is a Leap Year.');
	ELSE
		DBMS_OUTPUT.PUT_LINE(y || ' is NOT a Leap Year.');
	END IF;
END;
/
```

---

### 3. Fixed Deposit Maturity Calculator

Given the amount deposited and the number of years, calculate the amount on maturity based on the interest rules.

```sql
DECLARE
	P NUMBER := 5000;  -- Principal amount deposited
	N NUMBER := 3;     -- Number of years
	R NUMBER;          -- Interest rate
	A NUMBER;          -- Maturity amount
BEGIN
	IF N >= 5 THEN
		R := 10;
	ELSIF P < 2000 AND N >= 2 THEN
		R := 5;
	ELSIF P >= 2000 AND P < 6000 AND N >= 2 THEN
		R := 7;
	ELSIF P >= 6000 AND N >= 1 THEN
		R := 8;
	ELSE
		R := 3;
	END IF;

	A := P * POWER((1 + R/100), N);

	DBMS_OUTPUT.PUT_LINE('Principal: Rs. ' || P);
	DBMS_OUTPUT.PUT_LINE('Years:     ' || N);
	DBMS_OUTPUT.PUT_LINE('Rate:      ' || R || '%');
	DBMS_OUTPUT.PUT_LINE('Maturity:  Rs. ' || ROUND(A, 2));
END;
/
```

---

### 4. Conditional Salary Update

Write a PL/SQL block to update the salary of employee number 7788 to 4000, only if his salary is less than 4000.

```sql
DECLARE
	emp_id      NUMBER := 7788;
	current_sal NUMBER;
BEGIN
	SELECT SALARY INTO current_sal FROM EMP WHERE EMP# = emp_id;
	
	IF current_sal < 4000 THEN
		UPDATE EMP SET SALARY = 4000 WHERE EMP# = emp_id;
		DBMS_OUTPUT.PUT_LINE('Salary updated to 4000.');
	ELSE
		DBMS_OUTPUT.PUT_LINE('Salary is already 4000 or more.');
	END IF;
END;
/
```

---

### 5. Conditional Commission Update

Write a PL/SQL block to update the commission of employee number 7369 by 10% if commission is not null and if null then update it by 25%.

```sql
DECLARE
	emp_id       NUMBER := 7369;
	current_comm NUMBER;
	current_sal  NUMBER;
BEGIN
	SELECT COMM, SALARY INTO current_comm, current_sal FROM EMP WHERE EMP# = emp_id;
	
	IF current_comm IS NOT NULL THEN
		UPDATE EMP SET COMM = COMM * 1.10 WHERE EMP# = emp_id;
		DBMS_OUTPUT.PUT_LINE('Commission increased by 10%.');
	ELSE
		UPDATE EMP SET COMM = current_sal * 0.25 WHERE EMP# = emp_id;
		DBMS_OUTPUT.PUT_LINE('Commission set to 25% of salary.');
	END IF;
END;
/
```

---

### 6. Loop Circle Area Calculation

Write a PL/SQL code to calculate the area of a circle for a radius varying from 3 to 7. Store the radius and the corresponding values of the calculated area in the table called calculate.

```sql
CREATE TABLE calculate (
	radius NUMBER,
	area   NUMBER(10,2)
);
```

```sql
DECLARE
	pi CONSTANT NUMBER := 3.14159265;
	v_area      NUMBER;
BEGIN
	FOR r IN 3..7 LOOP
		v_area := pi * r * r;
		INSERT INTO calculate VALUES (r, v_area);
	END LOOP;
	COMMIT;
	DBMS_OUTPUT.PUT_LINE('Circle areas inserted into table.');
END;
/
```

---

### 7. Reverse Even Numbers Printer

Write a PL/SQL block to print even numbers in reverse order in the range accepted by the user.

```sql
DECLARE
	start_val NUMBER := 2;
	end_val   NUMBER := 20;
BEGIN

	FOR i IN REVERSE start_val..end_val LOOP
		IF MOD(i, 2) = 0 THEN
			DBMS_OUTPUT.PUT_LINE(i);
		END IF;
	END LOOP;
END;
/
```

---

### 8. Whole Numbers in Temp Table

Write a PL/SQL block to print first 50 whole numbers. Insert the list in the Temp table.

```sql
CREATE TABLE Temp (
	num NUMBER
);
```

```sql
DECLARE
BEGIN
	FOR i IN 0..49 LOOP
		INSERT INTO Temp VALUES (i);
	END LOOP;
	COMMIT;
	DBMS_OUTPUT.PUT_LINE('First 50 whole numbers inserted into Temp.');
END;
/
```

---

### 9. Year Leap Check Range

Write a PL/SQL block to insert the list of years from 2000 to 2100 and show whether each year is leap year or not in another attribute.

```sql
CREATE TABLE YearCheck (
	year    NUMBER,
	is_leap VARCHAR2(10)
);
```

```sql
DECLARE
BEGIN
	FOR y IN 2000..2100 LOOP
		IF (MOD(y, 4) = 0 AND MOD(y, 100) <> 0) OR MOD(y, 400) = 0 THEN
			INSERT INTO YearCheck VALUES (y, 'LEAP');
		ELSE
			INSERT INTO YearCheck VALUES (y, 'NOT LEAP');
		END IF;
	END LOOP;
	COMMIT;
	DBMS_OUTPUT.PUT_LINE('Years from 2000 to 2100 checks saved.');
END;
/
```

---

### 10. Fibonacci Generator

Write A Program To Generate First 25 Terms Of The Fibonacci Series.

```sql
DECLARE
	n1   NUMBER := 0;
	n2   NUMBER := 1;
	temp NUMBER;
BEGIN
	DBMS_OUTPUT.PUT_LINE('Fibonacci Series (25 terms):');
	DBMS_OUTPUT.PUT_LINE(n1);
	DBMS_OUTPUT.PUT_LINE(n2);
	FOR i IN 3..25 LOOP
		temp := n1 + n2;
		DBMS_OUTPUT.PUT_LINE(temp);
		n1 := n2;
		n2 := temp;
	END LOOP;
END;
/
```

---

### 11. Design Printer

Write A Program To Print The Following Design:
```
    1
   121
  12321
 1234321
123454321
```

```sql
DECLARE
	max_lines CONSTANT NUMBER := 5;
	space_str          VARCHAR2(100);
	num_str            VARCHAR2(100);
BEGIN
	FOR i IN 1..max_lines LOOP
		space_str := RPAD(' ', max_lines - i, ' ');
		num_str := '';
		
		FOR j IN 1..i LOOP
			num_str := num_str || j;
		END LOOP;
		
		FOR j IN REVERSE 1..(i-1) LOOP
			num_str := num_str || j;
		END LOOP;
		
		DBMS_OUTPUT.PUT_LINE(space_str || num_str);
	END LOOP;
END;
/
```

---

### 12. Case Check & Print 2nd Character

Write a PL/SQL block to accept a character from the user and check whether it is in upper or lower case and print 2nd char?

```sql
DECLARE
	accpt_char CHAR(1) := 'g';
	next_char  CHAR(1);
BEGIN

	IF (ASCII(accpt_char) BETWEEN 65 AND 90) THEN
		DBMS_OUTPUT.PUT_LINE('The character is in UPPER Case');
	ELSIF (ASCII(accpt_char) BETWEEN 97 AND 122) THEN
		DBMS_OUTPUT.PUT_LINE('The character is in LOWER Case');
	ELSE
		DBMS_OUTPUT.PUT_LINE('The input is not an alphabet');
	END IF;
	
	next_char := CHR(ASCII(accpt_char) + 1);
	DBMS_OUTPUT.PUT_LINE('The 2nd character is: ' || next_char);
END;
/
```

---

### 13. Reverse and Palindrome Checker

Write a PL/SQL block to accept a text and reverse the given text, also check the text is palindrome or not.

```sql
DECLARE
	orig_text VARCHAR2(100) := 'madam';
	rev_text  VARCHAR2(100) := '';
BEGIN

	FOR i IN REVERSE 1..LENGTH(orig_text) LOOP
		rev_text := rev_text || SUBSTR(orig_text, i, 1);
	END LOOP;

	DBMS_OUTPUT.PUT_LINE('Original Text: ' || orig_text);
	DBMS_OUTPUT.PUT_LINE('Reversed Text: ' || rev_text);

	IF UPPER(orig_text) = UPPER(rev_text) THEN
		DBMS_OUTPUT.PUT_LINE('The text is a palindrome.');
	ELSE
		DBMS_OUTPUT.PUT_LINE('The text is NOT a palindrome.');
	END IF;
END;
/
```

---

### 14. Copy Employee Row to New Table

Write a PL/SQL block to insert all the details of the employee No 7698 to a new table MyEmp, which has the same structure as EMPLOYEE table.

```sql
CREATE TABLE MyEmp AS SELECT * FROM EMP WHERE 1 = 0;
```

```sql
DECLARE
BEGIN
	INSERT INTO MyEmp
	SELECT * FROM EMP WHERE EMP# = 7698;
	COMMIT;
	DBMS_OUTPUT.PUT_LINE('Employee 7698 copied to MyEmp successfully.');
END;
/
```

---

### 15. Simple Interest Function

Write a function that will calculate the simple interest after passing the appropriate parameter.

```sql
CREATE OR REPLACE FUNCTION calc_simple_interest(
	p_principal IN NUMBER,
	p_rate      IN NUMBER,
	p_time      IN NUMBER
) RETURN NUMBER IS
BEGIN
	RETURN (p_principal * p_rate * p_time) / 100;
END;
/
```

---

### 16. Factorial Function

Write a function to calculate the factorial of a number passed as parameter.

```sql
CREATE OR REPLACE FUNCTION calc_factorial(
	p_num IN NUMBER
) RETURN NUMBER IS
	v_fact NUMBER := 1;
BEGIN
	IF p_num < 0 THEN
		RETURN NULL;
	END IF;
	FOR i IN 1..p_num LOOP
		v_fact := v_fact * i;
	END LOOP;
	RETURN v_fact;
END;
/
```

---

### 17. Commission Check & Increment Function

Write a function that checks whether an employee is availing any commission or not. If availing, then returns his salary with 10% increment. The employee number has to be passed as parameter to the function and the returned salary is updated in the table.

```sql
CREATE OR REPLACE FUNCTION check_comm_and_increment(
	p_empno IN NUMBER
) RETURN NUMBER IS
	v_sal  NUMBER;
	v_comm NUMBER;
BEGIN
	SELECT SALARY, COMM INTO v_sal, v_comm
	FROM EMP
	WHERE EMP# = p_empno;
	
	IF v_comm IS NOT NULL AND v_comm > 0 THEN
		v_sal := v_sal * 1.10;
		UPDATE EMP SET SALARY = v_sal WHERE EMP# = p_empno;
		COMMIT;
	END IF;
	
	RETURN v_sal;
END;
/
```

---

### 18. Salary Increment Procedure

Write a procedure that increases the salary of an employee. Employee number and the amount to be incremented should be passed as parameters to the procedure.

```sql
CREATE OR REPLACE PROCEDURE increment_salary(
	p_empno  IN NUMBER,
	p_amount IN NUMBER
) IS
BEGIN
	UPDATE EMP
	SET SALARY = SALARY + p_amount
	WHERE EMP# = p_empno;
	COMMIT;
	DBMS_OUTPUT.PUT_LINE('Salary incremented successfully.');
END;
/
```
