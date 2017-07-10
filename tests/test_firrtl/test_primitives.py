from magma import *
from mantle.firrtl.primitives import Register, Add2

def test():
    main = DefineCircuit('main', 'CLK', In(Bit))
    reg = Register(2)
    add = Add2()
    wire(reg.O, add.I0)
    wire(int2seq(1, 2), add.I1)
    wire(add.O[:2], reg.I)
    EndCircuit()
    compile('main', main, output="firrtl")


if __name__ == "__main__":
    test()
