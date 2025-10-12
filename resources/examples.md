# spellscript examples
a collection of scripts i made during development that you may find useful<br>
and again, these examples show proper indentation and formatting, but if you're a menace, spellscript was designed to be written like an essay, so you can put it all in one line (no indents needed either)

## table of contents

1. [basics](#basics)
2. [arithmetic & variables](#arithmetic--variables)
3. [conditionals](#conditionals)
4. [loops](#loops)
5. [arrays](#arrays)
6. [functions](#functions)
7. [strings](#strings)
8. [user input](#user-input)
9. [complete programs](#complete-programs)

---

## basics

### hello world

```spellscript
begin the grimoire.
inscribe whispers of "hello, world!".
close the grimoire.
```

**output:** `hello, world!`

---

## arithmetic & variables

### calculator

```spellscript
begin the grimoire.
summon the x with essence of 25.
summon the y with essence of 5.

inscribe whispers of "sum: " bound with x greater by y.
inscribe whispers of "difference: " bound with x lesser by y.
inscribe whispers of "product: " bound with x multiplied by y.
inscribe whispers of "quotient: " bound with x divided by y.
close the grimoire.
```

**output:**
```
sum: 30
difference: 20
product: 125
quotient: 5
```

### floating point

```spellscript
begin the grimoire.
summon the pi with essence of 3point14.
summon the radius with essence of 5.
summon the circumference with essence of 2 multiplied by pi multiplied by radius.

inscribe whispers of "circumference: " bound with circumference.
close the grimoire.
```

### negative numbers

```spellscript
begin the grimoire.
summon the debt with essence of 0 lesser by 100.
summon the payment with essence of 25.
enchant debt with debt greater by payment.

inscribe whispers of "remaining debt: " bound with debt.
close the grimoire.
```

**output:** `remaining debt: -75`

---

## conditionals

### simple if-else

```spellscript
begin the grimoire.
summon the score with essence of 75.

if the signs show score greater than 60 then inscribe whispers of "pass" otherwise inscribe whispers of "fail".
close the grimoire.
```

### nested conditionals

```spellscript
begin the grimoire.
summon the grade with essence of 85.

if the signs show grade greater than 90 then inscribe whispers of "a" otherwise if the signs show grade greater than 80 then inscribe whispers of "b" otherwise if the signs show grade greater than 70 then inscribe whispers of "c" otherwise inscribe whispers of "f".
close the grimoire.
```

**output:** `b`

### complex conditions

```spellscript
begin the grimoire.
summon the age with essence of 25.
summon the hasticket with essence of truth.
summon the isblocked with essence of falsehood.

if the signs show age greater than 18 and hasticket and not isblocked then inscribe whispers of "access granted" otherwise inscribe whispers of "access denied".
close the grimoire.
```

---

## loops

### counting

```spellscript
begin the grimoire.
summon the i with essence of 1.
repeat the incantation 5 times to begin:
    inscribe i.
    enchant i with i greater by 1.
end loop.
close the grimoire.
```

**output:** `1 2 3 4 5`

### traverse array

```spellscript
begin the grimoire.
summon the fruits with essence of collection holding whispers of "apple" and whispers of "banana" and whispers of "cherry".

traverse fruits with each fruit to begin:
    inscribe fruit.
end traverse.
close the grimoire.
```

### traverse with index

```spellscript
begin the grimoire.
summon the colors with essence of collection holding whispers of "red" and whispers of "blue".

traverse colors with each color at idx to begin:
    inscribe idx bound with whispers of ": " bound with color.
end traverse.
close the grimoire.
```

**output:**
```
0: red
1: blue
```

### multiplication table

```spellscript
begin the grimoire.
summon the row with essence of 1.
repeat the incantation 3 times to begin:
    summon the col with essence of 1.
    repeat the incantation 3 times to begin:
        summon the product with essence of row multiplied by col.
        inscribe row bound with whispers of " x " bound with col bound with whispers of " = " bound with product.
        enchant col with col greater by 1.
    end loop.
    enchant row with row greater by 1.
end loop.
close the grimoire.
```

---

## arrays

### basic operations

```spellscript
begin the grimoire.
summon the numbers with essence of collection holding 10 and 20 and 30.

inscribe whispers of "array: ".
inscribe numbers.

inscribe whispers of "first: " bound with numbers at position 0.
inscribe whispers of "length: " bound with length of numbers.

enchant numbers at position 1 with 99.
append 40 to numbers.

inscribe whispers of "modified: ".
inscribe numbers.
close the grimoire.
```

**output:**
```
array: 
[10, 20, 30]
first: 10
length: 3
modified: 
[10, 99, 30, 40]
```

### building array in loop

```spellscript
begin the grimoire.
summon the squares with essence of collection holding 0.
summon the i with essence of 1.

repeat the incantation 5 times to begin:
    append i multiplied by i to squares.
    enchant i with i greater by 1.
end loop.

inscribe squares.
close the grimoire.
```

**output:** `[0, 1, 4, 9, 16, 25]`

### modifying during traverse

```spellscript
begin the grimoire.
summon the numbers with essence of collection holding 1 and 2 and 3 and 4 and 5.

traverse numbers with each num at i to begin:
    enchant numbers at position i with num multiplied by 2.
end traverse.

inscribe numbers.
close the grimoire.
```

**output:** `[2, 4, 6, 8, 10]`

---

## functions

### simple function

```spellscript
begin the grimoire.
conjure ritual named square with x to return x multiplied by x.

inscribe whispers of "7 squared = " bound with through ritual square with 7.
close the grimoire.
```

**output:** `7 squared = 49`

### multiple parameters

```spellscript
begin the grimoire.
conjure ritual named add with a and b to return a greater by b.

inscribe whispers of "15 + 25 = " bound with through ritual add with 15 and 25.
close the grimoire.
```

### multi-line function

```spellscript
begin the grimoire.
conjure ritual named calculatearea with width and height to begin:
    inscribe whispers of "calculating...".
    summon the area with essence of width multiplied by height.
    return area.
end ritual.

inscribe whispers of "area: " bound with through ritual calculatearea with 5 and 10.
close the grimoire.
```

**output:**
```
calculating...
area: 50
```

### function with conditionals

```spellscript
begin the grimoire.
conjure ritual named getgrade with score to begin:
    if the signs show score greater than 90 then return whispers of "a".
    if the signs show score greater than 80 then return whispers of "b".
    if the signs show score greater than 70 then return whispers of "c".
    return whispers of "f".
end ritual.

inscribe whispers of "95 = " bound with through ritual getgrade with 95.
inscribe whispers of "75 = " bound with through ritual getgrade with 75.
close the grimoire.
```

**output:**
```
95 = a
75 = c
```

### nested function calls

```spellscript
begin the grimoire.
conjure ritual named double with x to return x multiplied by 2.
conjure ritual named addten with x to return x greater by 10.

conjure ritual named process with x to begin:
    summon the step1 with essence of through ritual double with x.
    return through ritual addten with step1.
end ritual.

inscribe whispers of "(5 * 2) + 10 = " bound with through ritual process with 5.
close the grimoire.
```

**output:** `(5 * 2) + 10 = 20`

### function with array

```spellscript
begin the grimoire.
conjure ritual named sumarray with arr to begin:
    summon the total with essence of 0.
    traverse arr with each element to begin:
        enchant total with total greater by element.
    end traverse.
    return total.
end ritual.

summon the numbers with essence of collection holding 10 and 20 and 30 and 40.
inscribe whispers of "sum: " bound with through ritual sumarray with numbers.
close the grimoire.
```

**output:** `sum: 100`

---

## strings

### concatenation

```spellscript
begin the grimoire.
summon the first with essence of whispers of "hello".
summon the second with essence of whispers of "world".
summon the combined with essence of first bound with whispers of " " bound with second.

inscribe combined.
close the grimoire.
```

**output:** `hello world`

### strings with numbers

```spellscript
begin the grimoire.
summon the name with essence of whispers of "alice".
summon the age with essence of 25.
summon the message with essence of name bound with whispers of " is " bound with age bound with whispers of " years old".

inscribe message.
close the grimoire.
```

**output:** `alice is 25 years old`

---

## user input

### basic input

```spellscript
begin the grimoire.
inquire whispers of "what is your name?" into name.
inscribe whispers of "hello, " bound with name bound with whispers of "!".
close the grimoire.
```

**sample interaction:**
```
what is your name? alice
hello, alice!
```

### input with type conversion

```spellscript
begin the grimoire.
inquire whispers of "enter a number:" into input.
transmute input into number.

inscribe whispers of "doubled: " bound with input multiplied by 2.
close the grimoire.
```

**sample interaction:**
```
enter a number: 7
doubled: 14
```

---

## complete programs

### factorial

```spellscript
begin the grimoire.
conjure ritual named factorial with n to begin:
    if the signs show n less than 2 then return 1.
    summon the result with essence of 1.
    summon the i with essence of 2.
    repeat the incantation 20 times to begin:
        if the signs show i greater than n then return result.
        enchant result with result multiplied by i.
        enchant i with i greater by 1.
    end loop.
    return result.
end ritual.

inscribe whispers of "5! = " bound with through ritual factorial with 5.
inscribe whispers of "7! = " bound with through ritual factorial with 7.
close the grimoire.
```

**output:**
```
5! = 120
7! = 5040
```

### fibonacci

```spellscript
begin the grimoire.
conjure ritual named fibonacci with n to begin:
    if the signs show n less than 2 then return n.
    summon the a with essence of 0.
    summon the b with essence of 1.
    summon the i with essence of 2.
    repeat the incantation 50 times to begin:
        if the signs show i greater than n then return b.
        summon the next with essence of a greater by b.
        enchant a with b.
        enchant b with next.
        enchant i with i greater by 1.
    end loop.
    return b.
end ritual.

inscribe whispers of "fibonacci(10) = " bound with through ritual fibonacci with 10.
close the grimoire.
```

**output:** `fibonacci(10) = 55`

### find maximum in array

```spellscript
begin the grimoire.
conjure ritual named findmax with arr to begin:
    summon the max with essence of arr at position 0.
    traverse arr with each element to begin:
        if the signs show element greater than max then enchant max with element.
    end traverse.
    return max.
end ritual.

summon the numbers with essence of collection holding 15 and 42 and 8 and 99 and 23.
inscribe whispers of "maximum: " bound with through ritual findmax with numbers.
close the grimoire.
```

**output:** `maximum: 99`

### bubble sort

```spellscript
begin the grimoire.
summon the arr with essence of collection holding 64 and 34 and 25 and 12 and 22.

inscribe whispers of "before: ".
inscribe arr.

summon the i with essence of 0.
repeat the incantation 5 times to begin:
    summon the j with essence of 0.
    repeat the incantation 4 times to begin:
        summon the current with essence of arr at position j.
        summon the nextidx with essence of j greater by 1.
        summon the next with essence of arr at position nextidx.
        
        if the signs show current greater than next then enchant arr at position j with next.
        if the signs show current greater than next then enchant arr at position nextidx with current.
        
        enchant j with j greater by 1.
    end loop.
    enchant i with i greater by 1.
end loop.

inscribe whispers of "after: ".
inscribe arr.
close the grimoire.
```

**output:**
```
before: 
[64, 34, 25, 12, 22]
after: 
[12, 22, 25, 34, 64]
```

### temperature converter

```spellscript
begin the grimoire.
conjure ritual named celsiustofahrenheit with c to begin:
    summon the temp1 with essence of c multiplied by 9.
    summon the temp2 with essence of temp1 divided by 5.
    return temp2 greater by 32.
end ritual.

inquire whispers of "enter celsius:" into input.
transmute input into number.

inscribe whispers of "fahrenheit: " bound with through ritual celsiustofahrenheit with input.
close the grimoire.
```

**sample interaction:**
```
enter celsius: 5
fahrenheit: 41
```

### array statistics

```spellscript
begin the grimoire.
conjure ritual named getmin with arr to begin:
    summon the min with essence of arr at position 0.
    traverse arr with each element to begin:
        if the signs show element less than min then enchant min with element.
    end traverse.
    return min.
end ritual.

conjure ritual named getmax with arr to begin:
    summon the max with essence of arr at position 0.
    traverse arr with each element to begin:
        if the signs show element greater than max then enchant max with element.
    end traverse.
    return max.
end ritual.

conjure ritual named getaverage with arr to begin:
    summon the total with essence of 0.
    traverse arr with each element to begin:
        enchant total with total greater by element.
    end traverse.
    return total divided by length of arr.
end ritual.

summon the data with essence of collection holding 15 and 23 and 8 and 42 and 16.

inscribe whispers of "data: ".
inscribe data.
inscribe whispers of "min: " bound with through ritual getmin with data.
inscribe whispers of "max: " bound with through ritual getmax with data.
inscribe whispers of "avg: " bound with through ritual getaverage with data.
close the grimoire.
```

**output:**
```
data: 
[15, 23, 8, 42, 16]
min: 8
max: 42
avg: 20.8
```

### grade calculator

```spellscript
begin the grimoire.
conjure ritual named getgrade with score to begin:
    if the signs show score greater than 90 then return whispers of "a".
    if the signs show score greater than 80 then return whispers of "b".
    if the signs show score greater than 70 then return whispers of "c".
    if the signs show score greater than 60 then return whispers of "d".
    return whispers of "f".
end ritual.

summon the scores with essence of collection holding 95 and 87 and 73 and 55.

inscribe whispers of "grades:".
traverse scores with each score to begin:
    inscribe through ritual getgrade with score.
end traverse.
close the grimoire.
```

**output:**
```
grades:
a
b
c
f
```

---