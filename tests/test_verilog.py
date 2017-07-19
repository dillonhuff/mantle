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
