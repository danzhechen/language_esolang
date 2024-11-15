'''

The following tests show example strings in the language.
There are no meaningful commands at this point,
only a block structure.

>>> tree = parser.parse("")
>>> tree = parser.parse(";")
>>> tree = parser.parse(";;;;")
>>> tree = parser.parse("{{}}")
>>> tree = parser.parse(";{};{;;}")
>>> tree = parser.parse(";{{}{{}}};{;{}{;};}")

The following tests check that unbalanced blocks correctly raise exceptions.

>>> tree = parser.parse("{") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{{}{}{{{}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{;;;}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedCharacters:
    
The following checks test that comments work.

>>> tree = parser.parse(";{};#")
>>> tree = parser.parse(";{};#{")
>>> tree = parser.parse(";{#}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

'''

import lark
import esolang.level0_arithmetic


grammar = esolang.level0_arithmetic.grammar + r"""
    %extend start: start (";" start)*
        | assign_var
        | block
        | /#.*/                -> comment
        | if_statement
        |

    if_statement: condition "?" start ":" start 

    ?condition: start

    block: "{" start* "}"

    assign_var: NAME "=" start

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

    %extend atom: NAME -> access_var
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level0_arithmetic.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a = 2"))
    2
    >>> interpreter.visit(parser.parse("a + 2"))
    4
    >>> interpreter.visit(parser.parse("a = a + 3"))
    5
    >>> interpreter.visit(parser.parse("b = 3"))
    3
    >>> interpreter.visit(parser.parse("a * b"))
    15
    >>> interpreter.visit(parser.parse("a = 3; {a+5}"))
    8
    >>> interpreter.visit(parser.parse("a = 3; {a=5; a+5}"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {a=5}; a+5"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {c=5}; c+5")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable c undefined
    
    >>> interpreter.visit(parser.parse("0 ? 1 : 2"))
    1
    >>> interpreter.visit(parser.parse("1 ? 1 : 2"))
    2
    >>> interpreter.visit(parser.parse("{1 - 1} ? 1 : 2"))
    1
    >>> interpreter.visit(parser.parse("{1 - 1} ? {z = 2; z + 2} : 2"))
    4
    >>> interpreter.visit(parser.parse("{{{1}}} ?  { 10 } : 3"))
    3
    >>> interpreter.visit(parser.parse("1 ? {x = 5; x + 2} : {y = 3; y * 2}"))
    6
    >>> interpreter.visit(parser.parse("a = 2; b = 4; 1 ? {c = a + b; c + b} : {d = 3; d * a}"))
    6
    >>> interpreter.visit(parser.parse("x = 5; y = 10; 0 ? {a = x + 2} : {b = y - 3}"))
    7

    '''
    def __init__(self):
        self.stack = [{}]

    def _get_from_stack(self, name):
        for d in reversed(self.stack):
            if name in d:
                return d[name]
        raise ValueError(f"Variable {name} undefined")

    def _assign_to_stack(self, name, value):
        for d in reversed(self.stack):
            if name in d:
                d[name] = value
                return value
        self.stack[-1][name] = value
        return value

    def if_statement(self, tree):
        condition = self.visit(tree.children[0])
        if condition == 0:
            return self.visit(tree.children[1])
        else:
            return self.visit(tree.children[2])

    def assign_var(self, tree):
        name = tree.children[0].value
        value = self.visit(tree.children[1])
        self._assign_to_stack(name, value)
        return value

    def access_var(self, tree):
        name = tree.children[0].value
        return self._get_from_stack(name)

    def block(self, tree):
        self.stack.append({})
        for child in tree.children:
            result = self.visit(child)
        self.stack.pop()
        return result
