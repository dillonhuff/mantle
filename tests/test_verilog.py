from magma import *
from magma.backend import verilog
from mantle.verilog import *

def bits_binop_test_factory(name, op):
    def _test():
        circ = eval("Define{}(1)".format(name))
        assert verilog.compile(circ) == """
module {}1 (input  I0, input  I1, output  O);
assign O = I0 {} I1
endmodule

""".format(name, op).lstrip()
        circ = eval("Define{}(2)".format(name))
        assert verilog.compile(circ) == """
module {}2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 {} I1
endmodule

""".format(name, op).lstrip()
    return _test

test_and = bits_binop_test_factory("And", "&")
test_or = bits_binop_test_factory("Or", "|")
test_xor = bits_binop_test_factory("Xor", "^")


def test_invert():
    Invert1 = DefineInvert(1)
    assert verilog.compile(Invert1) == """
module Invert1 (input  I, output  O);
assign O = ~I
endmodule

""".lstrip()
    Invert2 = DefineInvert(2)
    assert verilog.compile(Invert2) == """
module Invert2 (input [1:0] I, output [1:0] O);
assign O = ~I
endmodule

""".lstrip()


def shift_factory(direction, op):
    def _test():
        circ = eval("DefineShift{}(2, 1)".format(direction))
        assert verilog.compile(circ) == """
module Shift{}2_1 (input [1:0] I, output [1:0] O);
assign O = I {} 2'd1
endmodule

""".format(direction, op).lstrip()
        circ = eval("DefineShift{}(4, 2)".format(direction))
        assert verilog.compile(circ) == """
module Shift{}4_2 (input [3:0] I, output [3:0] O);
assign O = I {} 4'd2
endmodule

""".format(direction, op).lstrip()

    def _test_dynamic():
        circ = eval("DefineDynamicShift{}(2)".format(direction))
        assert verilog.compile(circ) == """
module DynamicShift{}2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 {} I1
endmodule

""".format(direction, op).lstrip()

    return _test, _test_dynamic

test_shift_left, test_dynamic_shift_left = shift_factory("Left", "<<")
test_shift_right, test_dynamic_shift_right = shift_factory("Right", ">>")

def binop_test_factory(name, op, signed=False):
    signed = "signed " if signed else ""
    def _test():
        circ = eval("Define{}(1)".format(name))
        assert verilog.compile(circ) == """
module {name}1 (input {signed}[0:0] I0, input {signed}[0:0] I1, output {signed}[0:0] O);
assign O = I0 {op} I1
endmodule

""".format(name=name, op=op, signed=signed).lstrip()
        circ = eval("Define{}(2)".format(name))
        assert verilog.compile(circ) == """
module {name}2 (input {signed}[1:0] I0, input {signed}[1:0] I1, output {signed}[1:0] O);
assign O = I0 {op} I1
endmodule

""".format(name=name, op=op, signed=signed).lstrip()
    return _test

test_unsigned_add = binop_test_factory("UnsignedAdd", "+")
test_unsigned_sub = binop_test_factory("UnsignedSub", "-")
test_unsigned_mul = binop_test_factory("UnsignedMul", "*")
test_unsigned_div = binop_test_factory("UnsignedDiv", "/")

test_signed_add = binop_test_factory("SignedAdd", "+", signed=True)
test_signed_sub = binop_test_factory("SignedSub", "-", signed=True)
test_signed_mul = binop_test_factory("SignedMul", "*", signed=True)
test_signed_div = binop_test_factory("SignedDiv", "/", signed=True)

def comparison_test_factory(name, op, signed=False):
    signed = "signed " if signed else ""
    def _test():
        circ = eval("Define{}(1)".format(name))
        assert verilog.compile(circ) == """
module {name}1 (input {signed}[0:0] I0, input {signed}[0:0] I1, output  O);
assign O = I0 {op} I1
endmodule

""".format(name=name, op=op, signed=signed).lstrip()
        circ = eval("Define{}(2)".format(name))
        assert verilog.compile(circ) == """
module {name}2 (input {signed}[1:0] I0, input {signed}[1:0] I1, output  O);
assign O = I0 {op} I1
endmodule

""".format(name=name, op=op, signed=signed).lstrip()
    return _test

test_unsigned_lt = comparison_test_factory("UnsignedLt", "<")
test_unsigned_lte = comparison_test_factory("UnsignedLtE", "<=")
test_unsigned_gt = comparison_test_factory("UnsignedGt", ">")
test_unsigned_gte = comparison_test_factory("UnsignedGtE", ">=")

test_signed_lt = comparison_test_factory( "SignedLt", "<", signed=True)
test_signed_lte = comparison_test_factory("SignedLtE", "<=", signed=True)
test_signed_gt = comparison_test_factory( "SignedGt", ">", signed=True)
test_signed_gte = comparison_test_factory("SignedGtE", ">=", signed=True)
