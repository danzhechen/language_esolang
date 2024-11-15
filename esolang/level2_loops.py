import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop | whileloop | comparison | "(" comparison ")" 

    forloop: "for" NAME "in" range block
    whileloop: "while" comparison block
    
    range: "range" "(" start ("," start)? ")"

    comparison: start COMPARISON_OPERATOR start

    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined
    
    >>> interpreter.visit(parser.parse("a=0; for i in range(5+5)     {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("n = 4; a = 0; for i in range(n) {a = a + i}; a"))
    6
    >>> interpreter.visit(parser.parse("n = 4; a = 0; for i in range(n) {n = n + 1; a = a + i}; a"))
    6
    >>> interpreter.visit(parser.parse("a = 0; for i in range(3) {for j in range(i + 1) {a = a + j}}; a"))
    4
    >>> interpreter.visit(parser.parse("a = 5; b = 3; (a + 2) > b"))
    True
    >>> interpreter.visit(parser.parse("a=0; while a < 10 {a = a + 1}; a"))
    10
    >>> interpreter.visit(parser.parse("a=0; n=4; while a + n < 10 {a = a + 1}; a"))
    6
    >>> interpreter.visit(parser.parse("a=1; while a < 4 {a = a * 2}; a"))
    4
    '''
    def range(self, tree):
        return range(int(self.visit(tree.children[0])))

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])
        self.stack.append({})
        result = None
        for x in xs:
            self.stack[-1][varname] = x
            result = self.visit(tree.children[2])
        self.stack.pop()
        return result

    def whileloop(self, tree):
        while self.visit(tree.children[0]) != 0:
            self.visit(tree.children[1])

    def comparison(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[2])
        op = tree.children[1].value
        if op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right 
