import textwrap
import inspect
import ast
import astor

def to_source(tree):
    return astor.to_source(tree).rstrip()


class Source:
    def __init__(self):
        self._source = ""

    def add_line(self, line, tab=""):
        self._source += tab + line + "\n"

    def add_lines(self, lines, tab=""):
        for line in lines:
            self.add_line(line, tab)
    
    def __str__(self):
        return self._source


class ExprVisitor(ast.NodeVisitor):
    def __init__(self, clock=True):
        super().__init__()
        self.clock = clock
        self.source = Source()
        self.source.add_line("from magma import *")
        self.source.add_line("from mantle import *")
        self.__unique_id = -1  # Starts at -1 so first instance is 0
        self.args = []
        self.width_table = {}
        self.name = None

    def unique_id(self):
        self.__unique_id += 1
        return "inst{}".format(self.__unique_id)

    def visit_FunctionDef(self, node):
        args = []
        for arg in node.args.args:
            self.args.append(arg.arg)
            args.append("\"" + arg.arg + "\"")
            typ = arg.annotation
            args.append(to_source(typ))
            if isinstance(typ, ast.Call):
                assert typ.func.id in ["In", "Out"]
                assert len(typ.args) == 1
                if isinstance(typ.args[0], ast.Name) and typ.args[0].id == "Bit":
                    self.width_table[arg.arg] = 1
                elif isinstance(typ.args[0], ast.Call) and typ.args[0].func.id == "Array":
                    self.width_table[arg.arg] = typ.args[0].args[0].n
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError(ast.dump(typ))
        if self.clock:
            args.append("\"CLK\"")
            args.append("In(Bit)")
        self.name = node.name
        self.source.add_line(
                "{name} = DefineCircuit(\"{name}\", {args})".format(
                    name=node.name, args=", ".join(args)))
        for s in node.body:
            if isinstance(s, ast.Expr) and \
               isinstance(s.value, ast.Call) and \
               s.value.func.id == "wire":
                arg1 = self.visit(s.value.args[0])
                arg2 = self.visit(s.value.args[1])
                self.source.add_line("wire({}, {})".format(arg1, arg2))
            else:
                self.visit(s)
        self.source.add_line("EndCircuit()")

    def get_width(self, node):
        if isinstance(node, ast.Name):
            return self.width_table[node.id]
        elif isinstance(node, ast.Num):
            return max(1, node.n.bit_length())  # max because (0).bit_length() == 1
        elif isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.LShift, ast.RShift)):
                return self.get_width(node.left)
            elif isinstance(node.op, (ast.And, ast.Eq)):
                return 1  # Boolean output
            left_width = self.get_width(node.left)
            right_width = self.get_width(node.right)
            return max(left_width, right_width)
        elif isinstance(node, ast.Compare):
            return 1
        elif isinstance(node, ast.UnaryOp):
            return self.get_width(node.operand)
        elif isinstance(node, ast.Attribute):
            return self.width_table[to_source(node)]
        elif isinstance(node, ast.BoolOp):
            return 1  # Logic boolean op returns 1 or 0
        elif isinstance(node, ast.Subscript):
            if isinstance(node.slice, ast.Index):
                return 1  # TODO: Do we have to worry about multidimensional subscripting?
            raise NotImplementedError(ast.dump(node), type(node))
        raise NotImplementedError(ast.dump(node), type(node))

    def visit_Name(self, node):
        if node.id in self.args:
            return "{}.{}".format(self.name, node.id)
        return node.id + ".O"

    def visit_Num(self, node):
        return node.n

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["int2seq", "array"]:
                return to_source(node)
            elif len(node.args) == 1:
                val = self.visit(node.args[0])
                circ_width = self.get_width(node.func)
                if isinstance(val, int) and val.bit_length() < circ_width:
                    val = "int2seq({}, {})".format(val, circ_width)
                circ = to_source(node.func)
                self.source.add_line("wire({}.I, {})".format(circ, val))
                return 
        raise NotImplementedError(to_source(node))

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call):
            if node.value.func.id == "Register":
                self.width_table[node.targets[0].id] = node.value.args[0].n
                self.width_table[node.targets[0].id + ".I"] = node.value.args[0].n
                self.width_table[node.targets[0].id + ".O"] = node.value.args[0].n
            elif node.value.func.id in {"Mux", "Or", "And"}:
                for i in range(node.value.args[0].n):
                    self.width_table[node.targets[0].id + ".I{}".format(i)] = node.value.args[1].n
                self.width_table[node.targets[0].id + ".O"] = node.value.args[1].n
            else:
                raise NotImplementedError(to_source(node))
            self.source.add_line(to_source(node))
            return

        value = self.visit(node.value)
        if len(node.targets) > 1:
            raise NotImplementedError(to_source(node))
        target = self.visit(node.targets[0])
        if isinstance(value, int):
            value = "int2seq({}, {})".format(value, self.get_width(node.targets[0]))
        assert target is not None, type(node.targets[0])
        assert value is not None, to_source(node.value)
        self.source.add_line("wire({}, {})".format(value, target))
        self.width_table[to_source(node.targets[0])] = self.get_width(node.value)

    def visit_Attribute(self, node):
        return to_source(node)

    def visit_Compare(self, node):
        """
        Convert to a tree of BinOps, then reuse BinOp logic
        TODO: Is this legal?
        """
        curr_node = node.left
        for op, comparator in zip(node.ops, node.comparators):
            curr_node = ast.BinOp(curr_node, op, comparator)
        return self.visit(curr_node)

    def visit_BoolOp(self, node):
        """
        Convert to a tree of BinOps, then reuse BinOp logic
        TODO: Is this legal?
        """
        curr_node = node.values[0]
        for value in node.values[1:]:
            curr_node = ast.BinOp(curr_node, node.op, value)
        return self.visit(curr_node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        left_width = self.get_width(node.left)
        if not isinstance(node.op, (ast.LShift, ast.RShift)):
            right_width = self.get_width(node.right)
            if isinstance(left, int):
                left = "int2seq({}, {})".format(left, max(left_width, right_width))
            if isinstance(right, int):
                right = "int2seq({}, {})".format(right, max(left_width, right_width))
            width = max(left_width, right_width)
        else:
            width = left_width
        binop_map = {
            ast.Add: "Add",
            ast.Sub: "Sub",
            ast.BitAnd: "And",
            ast.BitOr: "Or",
            ast.BitXor: "Xor",
            ast.LShift: "LeftShift",
            ast.RShift: "RightShift",
            ast.Lt: "ULT",  # TODO: Should we default to unsigned?
            ast.LtE: "ULE",  # TODO: Should we default to unsigned?
            ast.Eq: "EQ"
        }
        if node.op.__class__ in binop_map:
            op_str = binop_map[node.op.__class__]
            inst_id = self.unique_id()
            if op_str in ["And", "Or", "Xor"]:
                self.source.add_line("{} = {}(2, width={})({}, {})".format(inst_id, op_str, width, left, right))
            elif op_str in ["LeftShift", "RightShift"]:
                self.source.add_line("{} = {}({}, {})({})".format(inst_id, op_str, width, right, left))
            else:
                self.source.add_line("{} = {}({})({}, {})".format(inst_id, op_str, width, left, right))
            return inst_id
        elif isinstance(node.op, ast.And):
            inst_id0 = self.unique_id()
            self.source.add_line("{} = And(2, width={})({}, {})".format(inst_id0, width, left, right))
            inst_id1 = self.unique_id()
            self.source.add_line("{} = AndN({})({})".format(inst_id1, width, inst_id0))
            return inst_id1
        elif isinstance(node.op, ast.Or):
            inst_id0 = self.unique_id()
            self.source.add_line("{} = Or(2, width={})({}, {})".format(inst_id0, width, left, right))
            inst_id1 = self.unique_id()
            self.source.add_line("{} = OrN({})({})".format(inst_id1, width, inst_id0))
            return inst_id1
        raise NotImplementedError(ast.dump(node))

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        operand_width = self.get_width(node.operand)
        unop_map = {
            ast.Not: "NorN",
            ast.Invert: "Invert",
            ast.USub: "Negate"
        }
        if node.op.__class__ in unop_map:
            op_str = unop_map[node.op.__class__]
            inst_id = self.unique_id()
            self.source.add_line("{} = {}({})({})".format(inst_id, op_str, operand_width, operand))
            return inst_id
        raise NotImplementedError(ast.dump(node))

    def visit_Subscript(self, node):
        """
        Subscript(value, slice, ctx)
        """
        value = self.visit(node.value)
        if isinstance(node.slice, ast.Index):
            _slice = self.visit(node.slice.value)
        elif isinstance(node.slice, ast.Slice):
            # Constant slice, emit a select on the Bit Array
            return "{}[{}]".format(value, to_source(node.slice))
        elif isinstance(node.slice, ast.ExtSlice):
            raise NotImplementedError

        if isinstance(_slice, int):
            return "{}[{}]".format(value, _slice)
        else:
            inst_id = self.unique_id()
            self.source.add_line("{} = MuxN({})({}, {})".format(inst_id, self.get_width(node.value), value, _slice))
            return inst_id


def process_circuit_ast(tree, clock=True):
    visitor = ExprVisitor(clock)
    visitor.visit(tree)
    return str(visitor.source), visitor.name

def process_circuit(fn, clock=True):
    tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    source, name = process_circuit_ast(tree, clock=clock)
    for i, line in enumerate(source.splitlines()):
        print("{} {}".format(i + 1, line))
    _globals = inspect.stack()[1][0].f_globals
    _locals = inspect.stack()[1][0].f_locals
    exec(source, _globals, _locals)
    func = _locals[name]
    func.__magma_source = source
    return func

def circuit(fn=None, clock=True):
    if fn is None:
        def wrapped(fn):
            return process_circuit(fn, clock)
        return wrapped
    return process_circuit(fn, clock)

