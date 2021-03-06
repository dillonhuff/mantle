import sys
from magma import *
from mantle import *

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

nand2 = NAnd(2)

nand2(main.I0, main.I1)
wire(nand2, main.O)

compile(sys.argv[1], main)


