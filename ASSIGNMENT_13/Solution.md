# PL/SQL Solutions – Assignment 13

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Greatest of Four Numbers

Write a PL/SQL block to find the greatest among four entered integers using substitution/bind variables.

```sql
DECLARE
	var1 NUMBER;
	var2 NUMBER;
	var3 NUMBER;
	var4 NUMBER;
BEGIN
	var1 := :var1;
	var2 := :var2;
	var3 := :var3;
	var4 := :var4;

	IF (var1 > var2 AND var1 > var3 AND var1 > var4) THEN
		DBMS_OUTPUT.PUT_LINE(var1 || ' is greatest');
	ELSIF (var2 > var1 AND var2 > var3 AND var2 > var4) THEN
		DBMS_OUTPUT.PUT_LINE(var2 || ' is greatest');
	ELSIF (var3 > var1 AND var3 > var2 AND var3 > var4) THEN
		DBMS_OUTPUT.PUT_LINE(var3 || ' is greatest');
	ELSIF (var4 > var1 AND var4 > var2 AND var4 > var3) THEN
		DBMS_OUTPUT.PUT_LINE(var4 || ' is greatest');
	ELSE
		DBMS_OUTPUT.PUT_LINE('Numbers are equal or no single greatest number exists.');
	END IF;
END;
/
```

---

## 2. Addition Program

Write a PL/SQL block to perform the addition of two numbers.

```sql
DECLARE
	var1 NUMBER := 10;
	var2 NUMBER := 20;
	var3 NUMBER;
BEGIN
	var3 := var1 + var2;
	DBMS_OUTPUT.PUT_LINE('Result is: ' || var3);
END;
/
```

---

## 3. Alphabet Case Checker

Write a PL/SQL block to check whether an entered alphabet is in uppercase or lowercase.

```sql
DECLARE
	accpt_char CHAR(1);
BEGIN
	accpt_char := :accpt_char;

	IF (ASCII(accpt_char) BETWEEN 65 AND 90) THEN
		DBMS_OUTPUT.PUT_LINE('The character is in UPPER Case');
	ELSIF (ASCII(accpt_char) BETWEEN 97 AND 122) THEN
		DBMS_OUTPUT.PUT_LINE('The character is in LOWER Case');
	ELSE
		DBMS_OUTPUT.PUT_LINE('The input is not an alphabet');
	END IF;
END;
/
```
