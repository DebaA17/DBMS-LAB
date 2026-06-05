# PL/SQL Solutions – Assignment 8

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Greatest and Smallest of Four Integers

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
	-- Initialize greatest and smallest with the first number
	greatest := a;
	smallest := a;

	-- Compare and find the greatest number
	IF b > greatest THEN greatest := b; END IF;
	IF c > greatest THEN greatest := c; END IF;
	IF d > greatest THEN greatest := d; END IF;

	-- Compare and find the smallest number
	IF b < smallest THEN smallest := b; END IF;
	IF c < smallest THEN smallest := c; END IF;
	IF d < smallest THEN smallest := d; END IF;

	-- Display results
	DBMS_OUTPUT.PUT_LINE('Input numbers: ' || a || ', ' || b || ', ' || c || ', ' || d);
	DBMS_OUTPUT.PUT_LINE('Greatest number: ' || greatest);
	DBMS_OUTPUT.PUT_LINE('Smallest number: ' || smallest);
END;
/
```

---

## 2. Leap Year Checker

Write a PL/SQL block to check whether an entered year is a leap year or not.

```sql
DECLARE
	y NUMBER := 2024;
BEGIN
	IF (MOD(y,4)=0 AND MOD(y,100)<>0) OR MOD(y,400)=0 THEN
		DBMS_OUTPUT.PUT_LINE(y || ' is a Leap Year.');
	ELSE
		DBMS_OUTPUT.PUT_LINE(y || ' is NOT a Leap Year.');
	END IF;
END;
/
```

---

## 3. Fixed Deposit Maturity Calculator

Given the amount deposited and the number of years, calculate the amount on maturity based on the bank's interest policy:
* (i) Deposit `< 2000` and years `>= 2` $\rightarrow$ `5%`
* (ii) Deposit `[2000, 6000)` and years `>= 2` $\rightarrow$ `7%`
* (iii) Deposit `>= 6000` and years `>= 1` $\rightarrow$ `8%`
* (iv) All deposits for `>= 5` years $\rightarrow$ `10%`
* (v) All other deposits $\rightarrow$ `3%`

```sql
DECLARE
	P NUMBER := 5000;  -- Principal amount deposited
	N NUMBER := 3;     -- Number of years
	R NUMBER;          -- Interest rate
	A NUMBER;          -- Maturity amount
BEGIN
	-- Determine interest rate based on rules (evaluating highest rate rule first)
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

	-- Calculate maturity amount compounded annually: A = P * (1 + R/100)^N
	A := P * POWER((1 + R/100), N);

	-- Display results
	DBMS_OUTPUT.PUT_LINE('Principal Deposited: Rs. ' || P);
	DBMS_OUTPUT.PUT_LINE('Number of Years:     ' || N);
	DBMS_OUTPUT.PUT_LINE('Interest Rate:       ' || R || '%');
	DBMS_OUTPUT.PUT_LINE('Amount on Maturity:  Rs. ' || ROUND(A, 2));
END;
/
```
