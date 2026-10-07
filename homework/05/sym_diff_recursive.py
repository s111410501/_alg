def is_number(e):
    return isinstance(e, (int, float)) and not isinstance(e, bool)


def is_var(e):
    return e == 'x'


def sym_diff(expr):
    if is_number(expr):
        return 0

    if is_var(expr):
        return 1

    if not isinstance(expr, tuple):
        raise ValueError(f"Unsupported expression type: {expr}")

    op = expr[0]

    if op == '+':
        _, u, v = expr
        du = sym_diff(u)
        dv = sym_diff(v)
        return ('+', du, dv)

    if op == '-':
        _, u, v = expr
        du = sym_diff(u)
        dv = sym_diff(v)
        return ('-', du, dv)

    if op == '*':
        _, u, v = expr
        du = sym_diff(u)
        dv = sym_diff(v)
        return ('+', ('*', du, v), ('*', u, dv))

    if op == '/':
        _, u, v = expr
        du = sym_diff(u)
        dv = sym_diff(v)
        num = ('-', ('*', du, v), ('*', u, dv))
        den = ('^', v, 2)
        return ('/', num, den)

    if op == '^' or op == '**':
        _, u, n = expr
        du = sym_diff(u)

        if is_number(n):
            return ('*', ('*', n, ('^', u, n - 1)), du)

        return ('*', ('^', u, n), ('+', ('*', ('/', n, u), du), ('*', ('ln', u), sym_diff(n))))

    if op == 'neg':
        _, u = expr
        return ('neg', sym_diff(u))

    if op == 'sin':
        _, u = expr
        du = sym_diff(u)
        return ('*', ('cos', u), du)

    if op == 'cos':
        _, u = expr
        du = sym_diff(u)
        return ('neg', ('*', ('sin', u), du))

    if op == 'tan':
        _, u = expr
        du = sym_diff(u)
        cos_u = ('cos', u)
        return ('*', ('/', 1, ('^', cos_u, 2)), du)

    if op == 'exp':
        _, u = expr
        du = sym_diff(u)
        return ('*', ('exp', u), du)

    if op == 'ln':
        _, u = expr
        du = sym_diff(u)
        return ('*', ('/', 1, u), du)

    if op == 'sqrt':
        _, u = expr
        du = sym_diff(u)
        return ('*', ('/', 1, ('*', 2, ('sqrt', u))), du)

    raise ValueError(f"Unsupported operator: {op}")


def _prec(op):
    if op == 'neg':
        return 5
    if op in ('^', '**'):
        return 4
    if op == '*' or op == '/':
        return 3
    if op == '+' or op == '-':
        return 2
    return 0


def expr_to_str(expr):
    if is_number(expr):
        if isinstance(expr, float) and expr.is_integer():
            return str(int(expr))
        return str(expr)

    if is_var(expr):
        return 'x'

    if isinstance(expr, tuple):
        op = expr[0]

        if op == 'neg' and len(expr) == 2:
            u = expr[1]
            if isinstance(u, tuple) and _prec(u[0]) >= _prec('neg'):
                return f"-({expr_to_str(u)})"
            return f"-{expr_to_str(u)}"

        if len(expr) == 2:
            u = expr[1]
            return f"{op}({expr_to_str(u)})"

        if len(expr) == 3:
            u, v = expr[1], expr[2]
            if op == '^' or op == '**':
                if isinstance(v, tuple):
                    vstr = f"({expr_to_str(v)})"
                else:
                    vstr = expr_to_str(v)
                if isinstance(u, tuple) and _prec(u[0]) >= _prec(op):
                    return f"({expr_to_str(u)})^{vstr}"
                return f"{expr_to_str(u)}^{vstr}"

            left = expr_to_str(u)
            right = expr_to_str(v)
            if isinstance(u, tuple) and _prec(u[0]) < _prec(op):
                left = f"({left})"
            if isinstance(v, tuple) and _prec(v[0]) < _prec(op):
                right = f"({right})"
            if op == '*':
                return f"{left}*{right}"
            if op == '/':
                return f"{left}/{right}"
            if op == '+':
                return f"{left}+{right}"
            if op == '-':
                return f"{left}-{right}"
            return f"{left}{op}{right}"

    return str(expr)


def sym_diff_str(expr):
    return expr_to_str(sym_diff(expr))


if __name__ == '__main__':
    examples = [
        'x',
        ('^', 'x', 2),
        ('^', 'x', 3),
        ('*', 'x', 5),
        ('+', ('^', 'x', 2), ('*', 3, 'x')),
        ('*', ('sin', 'x'), ('cos', 'x')),
        ('sin', ('^', 'x', 2)),
        ('ln', 'x'),
        ('exp', 'x'),
        ('/', ('sin', 'x'), 'x'),
        ('sqrt', 'x'),
    ]
    for e in examples:
        print(f"d/dx {expr_to_str(e)} = {sym_diff_str(e)}")
