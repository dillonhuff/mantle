from magma import *
from magma.backend import verilog
from mantle.verilog import *


def test_and():
    And1 = DefineAnd(1)
    assert verilog.compile(And1) == """
module And1 (input  I0, input  I1, output  O);
assign O = I0 & I1
endmodule

""".lstrip()
    And2 = DefineAnd(2)
    assert verilog.compile(And2) == """
module And2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 & I1
endmodule

""".lstrip()


def test_or():
    Or1 = DefineOr(1)
    assert verilog.compile(Or1) == """
module Or1 (input  I0, input  I1, output  O);
assign O = I0 | I1
endmodule

""".lstrip()
    Or2 = DefineOr(2)
    assert verilog.compile(Or2) == """
module Or2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 | I1
endmodule

""".lstrip()


def test_xor():
    Xor1 = DefineXor(1)
    assert verilog.compile(Xor1) == """
module Xor1 (input  I0, input  I1, output  O);
assign O = I0 ^ I1
endmodule

""".lstrip()
    Xor2 = DefineXor(2)
    assert verilog.compile(Xor2) == """
module Xor2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 ^ I1
endmodule

""".lstrip()


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


def test_unsigned_add():
    Add1 = DefineUnsignedAdd(1)
    assert verilog.compile(Add1) == """
module UnsignedAdd1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
assign O = I0 + I1
endmodule

""".lstrip()
    Add2 = DefineUnsignedAdd(2)
    assert verilog.compile(Add2) == """
module UnsignedAdd2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 + I1
endmodule

""".lstrip()


def test_unsigned_sub():
    Sub1 = DefineUnsignedSub(1)
    assert verilog.compile(Sub1) == """
module UnsignedSub1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
assign O = I0 - I1
endmodule

""".lstrip()
    Sub2 = DefineUnsignedSub(2)
    assert verilog.compile(Sub2) == """
module UnsignedSub2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 - I1
endmodule

""".lstrip()


def test_unsigned_mul():
    Mul1 = DefineUnsignedMul(1)
    assert verilog.compile(Mul1) == """
module UnsignedMul1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
assign O = I0 * I1
endmodule

""".lstrip()
    Mul2 = DefineUnsignedMul(2)
    assert verilog.compile(Mul2) == """
module UnsignedMul2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 * I1
endmodule

""".lstrip()


def test_unsigned_div():
    Div1 = DefineUnsignedDiv(1)
    assert verilog.compile(Div1) == """
module UnsignedDiv1 (input [0:0] I0, input [0:0] I1, output [0:0] O);
assign O = I0 / I1
endmodule

""".lstrip()
    Div2 = DefineUnsignedDiv(2)
    assert verilog.compile(Div2) == """
module UnsignedDiv2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 / I1
endmodule

""".lstrip()


def test_shift_left():
    ShiftLeft2_1 = DefineUnsignedShiftLeft(2, 1)
    assert verilog.compile(ShiftLeft2_1) == """
module UnsignedShiftLeft2_1 (input [1:0] I, output [1:0] O);
assign O = I << 1'd1
endmodule

""".lstrip()
    ShiftLeft4_2 = DefineUnsignedShiftLeft(4, 2)
    assert verilog.compile(ShiftLeft4_2) == """
module UnsignedShiftLeft4_2 (input [3:0] I, output [3:0] O);
assign O = I << 2'd2
endmodule

""".lstrip()


def test_dynamic_shift_left():
    DynamicShiftLeft2 = DefineUnsignedDynamicShiftLeft(2)
    assert verilog.compile(DynamicShiftLeft2) == """
module UnsignedDynamicShiftLeft2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 << I1
endmodule

""".lstrip()


def test_shift_right():
    ShiftRight2_1 = DefineUnsignedShiftRight(2, 1)
    assert verilog.compile(ShiftRight2_1) == """
module UnsignedShiftRight2_1 (input [1:0] I, output [1:0] O);
assign O = I >> 1'd1
endmodule

""".lstrip()
    ShiftRight4_2 = DefineUnsignedShiftRight(4, 2)
    assert verilog.compile(ShiftRight4_2) == """
module UnsignedShiftRight4_2 (input [3:0] I, output [3:0] O);
assign O = I >> 2'd2
endmodule

""".lstrip()


def test_dynamic_shift_right():
    DynamicShiftRight2 = DefineUnsignedDynamicShiftRight(2)
    assert verilog.compile(DynamicShiftRight2) == """
module UnsignedDynamicShiftRight2 (input [1:0] I0, input [1:0] I1, output [1:0] O);
assign O = I0 >> I1
endmodule

""".lstrip()
