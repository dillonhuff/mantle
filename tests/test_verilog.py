from magma import *
from magma.backend import verilog
from mantle.verilog import *


def test_and():
    And1 = DefineAnd(1)
    assert verilog.compile(And1) == """
module And1 (input  I0, input  I1, output  O);
O = I0 & I1
endmodule

""".lstrip()
    And2 = DefineAnd(2)
    assert verilog.compile(And2) == """
module And2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 & I1
endmodule

""".lstrip()


def test_or():
    Or1 = DefineOr(1)
    assert verilog.compile(Or1) == """
module Or1 (input  I0, input  I1, output  O);
O = I0 | I1
endmodule

""".lstrip()
    Or2 = DefineOr(2)
    assert verilog.compile(Or2) == """
module Or2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 | I1
endmodule

""".lstrip()


def test_xor():
    Xor1 = DefineXor(1)
    assert verilog.compile(Xor1) == """
module Xor1 (input  I0, input  I1, output  O);
O = I0 ^ I1
endmodule

""".lstrip()
    Xor2 = DefineXor(2)
    assert verilog.compile(Xor2) == """
module Xor2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 ^ I1
endmodule

""".lstrip()


def test_invert():
    Invert1 = DefineInvert(1)
    assert verilog.compile(Invert1) == """
module Invert1 (input  I, output  O);
O = ~I
endmodule

""".lstrip()
    Invert2 = DefineInvert(2)
    assert verilog.compile(Invert2) == """
module Invert2 (input [1:0] I, output [1:0] O);
O = ~I
endmodule

""".lstrip()


def test_unsigned_add():
    Add1 = DefineUnsignedAdd(1)
    assert verilog.compile(Add1) == """
module UnsignedAdd1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
O = I0 + I1
endmodule

""".lstrip()
    Add2 = DefineUnsignedAdd(2)
    assert verilog.compile(Add2) == """
module UnsignedAdd2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 + I1
endmodule

""".lstrip()


def test_unsigned_sub():
    Sub1 = DefineUnsignedSub(1)
    assert verilog.compile(Sub1) == """
module UnsignedSub1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
O = I0 - I1
endmodule

""".lstrip()
    Sub2 = DefineUnsignedSub(2)
    assert verilog.compile(Sub2) == """
module UnsignedSub2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 - I1
endmodule

""".lstrip()


def test_unsigned_mul():
    Mul1 = DefineUnsignedMul(1)
    assert verilog.compile(Mul1) == """
module UnsignedMul1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
O = I0 * I1
endmodule

""".lstrip()
    Mul2 = DefineUnsignedMul(2)
    assert verilog.compile(Mul2) == """
module UnsignedMul2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 * I1
endmodule

""".lstrip()


def test_unsigned_div():
    Div1 = DefineUnsignedDiv(1)
    assert verilog.compile(Div1) == """
module UnsignedDiv1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
O = I0 / I1
endmodule

""".lstrip()
    Div2 = DefineUnsignedDiv(2)
    assert verilog.compile(Div2) == """
module UnsignedDiv2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
O = I0 / I1
endmodule

""".lstrip()
