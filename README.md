# language_esolang ![](https://github.com/danzhechen/language_esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.

## Examples

### Conditionals

Showcasing comparison operators and conditional logic:

```python
# Simple comparison
>>> interpreter.visit(parser.parse("a = 5; b = 3; (a + 2) > b"))
True

# Ternary conditional statements
>>> interpreter.visit(parser.parse("0 ? 1 : 2"))
1
>>> interpreter.visit(parser.parse("1 ? 1 : 2"))
2
>>> interpreter.visit(parser.parse("{1 - 1} ? 1 : 2"))
1
>>> interpreter.visit(parser.parse("{1 - 1} ? {z = 2; z + 2} : 2"))
4

# Nested conditional logic
>>> interpreter.visit(parser.parse("{{{1}}} ? {10} : 3"))
3

>>> interpreter.visit(parser.parse("1 ? {x = 5; x + 2} : {y = 3; y * 2}"))
6

>>> interpreter.visit(parser.parse("a = 2; b = 4; 1 ? {c = a + b; c + b} : {d = 3; d * a}"))
6

>>> interpreter.visit(parser.parse("x = 5; y = 10; 0 ? {a = x + 2} : {b = y - 3}"))
7
```

### Loops

This section demonstrates for loops and their usage with mathematical computations:

```python
# Sum integers in a range
>>> interpreter.visit(parser.parse("a=0; for i in range(5+5) {a = a + i}"))
45

# Use a variable in the range
>>> interpreter.visit(parser.parse("n = 4; a = 0; for i in range(n) {a = a + i}; a"))
6

# Modify the range variable within the loop
>>> interpreter.visit(parser.parse("n = 4; a = 0; for i in range(n) {n = n + 1; a = a + i}; a"))
6

# Nested loops
>>> interpreter.visit(parser.parse("a = 0; for i in range(3) {for j in range(i + 1) {a = a + j}}; a"))
4
```

### While Loops

Demonstrating while loops with various conditions:

```python
# Basic while loop
>>> interpreter.visit(parser.parse("a=0; while a < 10 {a = a + 1}; a"))
10

# Conditional inside while loop
>>> interpreter.visit(parser.parse("a=0; n=4; while a + n < 10 {a = a + 1}; a"))
6

# Multiplicative growth
>>> interpreter.visit(parser.parse("a=1; while a < 4 {a = a * 2}; a"))
4
```

### Prime Number Computation

Below are examples that demonstrate how to check and generate prime numbers:

```python
# Check if a single number is prime
>>> interpreter.visit(parser.parse("prime(2) ? 0 : print(2);"))
2

# Print all prime numbers in a range
>>> interpreter.visit(parser.parse("for i in range(10) {prime(i) ? 0 : print(i)};"))
2
3
5
7

>>> interpreter.visit(parser.parse("for i in range(5) {prime(i) ? 0 : print(i)};"))
2
3

>>> interpreter.visit(parser.parse("for i in range(30) {prime(i) ? 0 : print(i)};"))
2
3
5
7
11
13
17
19
23
29
```

