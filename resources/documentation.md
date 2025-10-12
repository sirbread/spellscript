# spellscript documentation

**version:** 1.0  
**author:** sirbread  
**last updated:** 2025-10-11

---

## table of contents

1. [table of contents](#table-of-contents)
2. [getting started](#getting-started)
3. [program structure](#program-structure)
4. [syntax rules](#syntax-rules)
5. [variables](#variables)
6. [data types](#data-types)
7. [operators](#operators)
8. [conditionals](#conditionals)
9. [loops](#loops)
10. [arrays](#arrays-1)
11. [functions](#functions)
12. [string operations](#string-operations)
13. [type conversion](#type-conversion)
14. [input/output](#inputoutput)
15. [utility commands](#utility-commands)
16. [language behavior](#language-behavior)
17. [limitations](#limitations)
18. [syntax quick reference](#syntax-quick-reference)

---

## getting started

### installation

save the interpreter as `spellscript.py` and ensure python 3.6+ is installed.

### running a spell

```bash
python spellscript.py filename.spell
```

### hello world

```spellscript
begin the grimoire.
inscribe whispers of "hello, world!".
close the grimoire.
```

---

## program structure

every program must follow this structure:

```spellscript
begin the grimoire.
<your code>
close the grimoire.
```

both opening and closing markers are **required**.

---

## syntax rules

### statement terminators

- use `.` to end most statements
- use `:` to end block-starting statements

### whitespace

- whitespace is largely ignored
- statements can span multiple lines
- programs can be written on one line
- indentation is optional (but recommended)

### case sensitivity

- keywords are **case-insensitive**
- variable names are **case-sensitive**

### comments

spellscript does **not** support comments.

---

## variables

### declaration (summon)

**syntax:**
```
summon the <name>.
summon the <name> with essence of <value>.
```

**examples:**
```spellscript
summon the counter.
summon the age with essence of 25.
summon the name with essence of whispers of "alice".
```

### assignment (enchant)

**syntax:**
```
enchant <name> with <value>.
```

**examples:**
```spellscript
enchant counter with 10.
enchant result with x greater by y.
enchant counter with counter greater by 1.
```

### array element assignment

**syntax:**
```
enchant <array> at position <index> with <value>.
```

**example:**
```spellscript
enchant items at position 0 with 99.
```

### deletion (banish)

**syntax:**
```
banish the <name>.
```

**example:**
```spellscript
banish the temp.
```

### variable scope

- variables are **global by default**
- function parameters are **local**
- local parameters **shadow** globals with the same name

---

## data types

### numbers

**integers:**
```spellscript
summon the age with essence of 25.
summon the zero with essence of 0.
```

**floating point:**
use `point` instead of `.` for decimals.
```spellscript
summon the pi with essence of 3point14.
summon the half with essence of 0point5.
```

**negative numbers:**
use `0 lesser by <value>`.
```spellscript
summon the debt with essence of 0 lesser by 100.
```

### strings

use `whispers of "text"`.

**syntax:**
```
whispers of "string content"
```

**examples:**
```spellscript
summon the greeting with essence of whispers of "hello".
summon the empty with essence of whispers of "".
```

### booleans

- `truth` = true
- `falsehood` = false

**truthiness:**
- non-zero numbers are truthy
- zero is falsy

### arrays

see [arrays](#arrays) section.

---

## operators

### arithmetic

**note:** operations evaluate **left-to-right** (no precedence).

**addition:**
```
<a> greater by <b>
```

**subtraction:**
```
<a> lesser by <b>
```

**multiplication:**
```
<a> multiplied by <b>
```

**division:**
```
<a> divided by <b>
```

**chaining:**
```spellscript
summon the result with essence of 2 greater by 3 multiplied by 4.
```
evaluates as `(2 + 3) * 4 = 20`

### comparison

**equals:**
```
<a> equals <b>
```

**greater than:**
```
<a> greater than <b>
```

**less than:**
```
<a> less than <b>
```

### logical

**and:**
```
<condition> and <condition>
```

**or:**
```
<condition> or <condition>
```

**not:**
```
not <condition>
```

---

## conditionals

### if statement

**syntax:**
```
if the signs show <condition> then <statement>.
```

**example:**
```spellscript
if the signs show age greater than 18 then inscribe whispers of "adult".
```

### if-else

**syntax:**
```
if the signs show <condition> then <statement> otherwise <statement>.
```

**example:**
```spellscript
if the signs show score greater than 60 then inscribe whispers of "pass" otherwise inscribe whispers of "fail".
```

### nested conditionals

**syntax:**
```
if the signs show <condition> then <statement> otherwise if the signs show <condition> then <statement> otherwise <statement>.
```

---

## loops

### repeat loop

**inline syntax:**
```
repeat the incantation <number> times do <statement>.
```

**note:** only the first statement is included in the loop body.

**block syntax:**
```
repeat the incantation <number> times to begin:
    <statements>
end loop.
```

**example:**
```spellscript
summon the i with essence of 1.
repeat the incantation 5 times to begin:
    inscribe i.
    enchant i with i greater by 1.
end loop.
```

### traverse loop

**without index:**
```
traverse <array> with each <item> to begin:
    <statements>
end traverse.
```

**with index:**
```
traverse <array> with each <item> at <index> to begin:
    <statements>
end traverse.
```

**examples:**
```spellscript
traverse fruits with each fruit to begin:
    inscribe fruit.
end traverse.

traverse colors with each color at idx to begin:
    inscribe idx bound with whispers of ": " bound with color.
end traverse.
```

---

## arrays

### creating arrays

**syntax:**
```
collection holding <value> and <value> and <value>
```

**examples:**
```spellscript
summon the numbers with essence of collection holding 1 and 2 and 3.
summon the names with essence of collection holding whispers of "alice" and whispers of "bob".
summon the single with essence of collection holding 42.
```

### arrays with function calls

**syntax:**
```
collection holding through ritual <name> with <arg> and through ritual <name> with <arg>
```

**example:**
```spellscript
conjure ritual named double with x to return x multiplied by 2.
summon the doubled with essence of collection holding through ritual double with 1 and through ritual double with 2.
```

### accessing elements

**syntax:**
```
<array> at position <index>
```

arrays are **zero-indexed**.

**example:**
```spellscript
inscribe numbers at position 0.
summon the first with essence of numbers at position 0.
```

### modifying elements

**syntax:**
```
enchant <array> at position <index> with <value>.
```

### appending

**syntax:**
```
append <value> to <array>.
```

**example:**
```spellscript
append 3 to list.
```

### array length

**syntax:**
```
length of <array>
```

**example:**
```spellscript
inscribe length of numbers.
summon the count with essence of length of numbers.
```

---

## functions

### single-line functions

**syntax:**
```
conjure ritual named <name> with <param> and <param> to <statement>.
```

**examples:**
```spellscript
conjure ritual named square with x to return x multiplied by x.
conjure ritual named add with a and b to return a greater by b.
```

### multi-line functions

**syntax:**
```
conjure ritual named <name> with <param> and <param> to begin:
    <statements>
end ritual.
```

**example:**
```spellscript
conjure ritual named findmax with arr to begin:
    summon the max with essence of arr at position 0.
    traverse arr with each element to begin:
        if the signs show element greater than max then enchant max with element.
    end traverse.
    return max.
end ritual.
```

### function parameters

**functions must have at least one parameter.** use a dummy parameter for parameterless functions:

```spellscript
conjure ritual named greet with dummy to begin:
    inscribe whispers of "hello!".
end ritual.
```

### calling functions

**method 1: inline (through ritual)**
```
through ritual <name> with <arg> and <arg>
```

**example:**
```spellscript
summon the result with essence of through ritual square with 7.
```

**method 2: standalone (invoke)**
```
invoke the ritual <name> with <arg> and <arg>.
```

**example:**
```spellscript
invoke the ritual greet with 0.
```

### returning values

**syntax:**
```
return <expression>.
```

**examples:**
```spellscript
return 42.
return x greater by y.
return truth.
```

---

## string operations

### concatenation

**syntax:**
```
<string> bound with <string> bound with <string>
```

**examples:**
```spellscript
summon the combined with essence of whispers of "hello" bound with whispers of " world".
summon the message with essence of whispers of "count: " bound with counter.
```

---

## type conversion

### transmute

**syntax:**
```
transmute <variable> into <type>.
```

**supported types:**
- `number` - converts to integer or float
- `text` - converts to string
- `truth` - converts to boolean

**examples:**
```spellscript
transmute age into text.
transmute input into number.
transmute flag into truth.
```

---

## input/output

### output (inscribe)

**syntax:**
```
inscribe <value>.
inscribe whispers of "<text>".
```

**examples:**
```spellscript
inscribe counter.
inscribe whispers of "hello, world!".
inscribe a greater by b.
inscribe numbers.
```

**array output format:** `[1, 2, 3]`

### input (inquire)

**syntax:**
```
inquire whispers of "<prompt>" into <variable>.
```

**example:**
```spellscript
inquire whispers of "enter your name:" into username.
```

---

## utility commands

### gaze upon (debug)

evaluates and prints a condition.

**syntax:**
```
gaze upon <condition>.
```

**output format:** `gazing reveals: true` or `gazing reveals: false`

### ponder (delay)

pauses execution.

**syntax:**
```
ponder for <seconds> moments.
```

**note:** cannot use `point` directly in ponder. create a variable first:
```spellscript
summon the delay with essence of 0point5.
ponder for delay moments.
```

---

## language behavior

### left-to-right evaluation

operations are evaluated left-to-right **without operator precedence**.

```spellscript
2 greater by 3 multiplied by 4
```
evaluates as `(2 + 3) * 4 = 20`, **not** `2 + (3 * 4) = 14`

**to control order, use intermediate variables:**
```spellscript
summon the product with essence of 3 multiplied by 4.
summon the result with essence of 2 greater by product.
```

### variable scope

- all variables are global by default
- function parameters are local and shadow globals
- modifying parameters doesn't affect globals

---

## limitations

- no nested arrays, must use multiple separate arrays.
- no string indexing, must use arrays of single character strings.
- no modulo operator.
- loops cannot be exited early (besides via function returns).
- comments aren't supported (because the language is read like a book anyways).
- recursive functions can be defined, use iterative approaches instead.
- use a dummy parameter for parameterless functions.

---

## syntax quick reference

| operation | syntax |
|-----------|--------|
| program start | `begin the grimoire.` |
| program end | `close the grimoire.` |
| declare variable | `summon the <name> [with essence of <value>].` |
| assign variable | `enchant <name> with <value>.` |
| assign array element | `enchant <array> at position <index> with <value>.` |
| delete variable | `banish the <name>.` |
| print | `inscribe <value>.` |
| input | `inquire whispers of "<prompt>" into <name>.` |
| if | `if the signs show <condition> then <action>.` |
| if-else | `if the signs show <condition> then <action> otherwise <action>.` |
| repeat (inline) | `repeat the incantation <n> times do <action>.` |
| repeat (block) | `repeat the incantation <n> times to begin: ... end loop.` |
| traverse | `traverse <array> with each <item> [at <index>] to begin: ... end traverse.` |
| define function | `conjure ritual named <name> with <params> to [<statement> \| begin: ... end ritual].` |
| call function (inline) | `through ritual <name> with <args>` |
| call function (standalone) | `invoke the ritual <name> with <args>.` |
| return | `return <value>.` |
| type conversion | `transmute <name> into <type>.` |
| append | `append <value> to <array>.` |
| delay | `ponder for <seconds> moments.` |
| debug | `gaze upon <condition>.` |

### keywords

| keyword | meaning |
|---------|---------|
| `begin the grimoire` | start program |
| `close the grimoire` | end program |
| `summon` | declare variable |
| `enchant` | modify variable |
| `banish` | delete variable |
| `inscribe` | print |
| `inquire` | input |
| `if the signs show` | conditional |
| `then` | conditional action |
| `otherwise` | else |
| `repeat the incantation` | loop |
| `traverse` | for-each |
| `with each` | iterator |
| `conjure ritual named` | define function |
| `invoke the ritual` | call function |
| `through ritual` | inline function call |
| `return` | return value |
| `transmute` | type conversion |
| `append` | add to array |
| `ponder` | delay |
| `gaze upon` | debug |
| `whispers of` | string literal |
| `collection holding` | array literal |
| `essence of` | value source |
| `with essence of` | initialization |
| `at position` | array index |
| `length of` | array length |
| `bound with` | concatenation |
| `greater by` | addition |
| `lesser by` | subtraction |
| `multiplied by` | multiplication |
| `divided by` | division |
| `greater than` | comparison |
| `less than` | comparison |
| `equals` | equality |
| `and` | logical and |
| `or` | logical or |
| `not` | logical not |
| `truth` | true |
| `falsehood` | false |
| `to begin` | block start |
| `end loop` | end repeat |
| `end traverse` | end traverse |
| `end ritual` | end function |
| `moments` | time unit |
| `point` | decimal point |

---
