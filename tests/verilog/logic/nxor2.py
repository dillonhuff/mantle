import sys
from magma import *
from mantle import *

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

nxor2 = NXOr(2)

nxor2(main.I0, main.I1)
wire(nxor2, main.O)

compile(sys.argv[1], main)


