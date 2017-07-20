from magma import *
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

def bits_binop_factory(name, op):
    @lru_cache(maxsize=None)
    def DefineCirc(N):
        if N == 1:
            T = Bit
        else:
            assert N > 1
            T = Bits(N)

        circuit = DefineCircuit("{}{}".format(name, N), "I0", In(T), "I1", In(T), "O", Out(T))
        circuit.verilog = "assign O = I0 {} I1".format(op)
        EndCircuit()
        return circuit
    return DefineCirc

def bits_unop_factory(name, verilog):
    @lru_cache(maxsize=None)
    def DefineCirc(N):
        if N == 1:
            T = Bit
        else:
            assert N > 1
            T = Bits(N)

        circuit = DefineCircuit("{}{}".format(name, N), "I", In(T), "O", Out(T))
        circuit.verilog = verilog
        EndCircuit()
        return circuit
    return DefineCirc

DefineAnd = bits_binop_factory("And", "&")
DefineOr  = bits_binop_factory("Or",  "|")
DefineXor = bits_binop_factory("Xor", "^")
DefineInvert = bits_unop_factory("Invert", "assign O = ~I")

def shift_factory(direction, op):
    @lru_cache(maxsize=None)
    def DefineShift(N, amount):
        assert N > 1, "TODO: Should we support shift left on a single bit?"
        T = Bits(N)

        circuit = DefineCircuit("Shift{}{}_{}".format(direction, N, amount), "I", In(T), "O", Out(T))
        circuit.verilog = "assign O = I {} {}'d{}".format(op, N, amount)
        return circuit

    @lru_cache(maxsize=None)
    def DefineDynamicShift(N):
        assert N > 1, "TODO: Should we support shift left on a single bit?"
        T = Bits(N)

        circuit = DefineCircuit("DynamicShift{}{}".format(direction, N), "I0", In(T), "I1", In(T), "O", Out(T))
        circuit.verilog = "assign O = I0 {} I1".format(op)
        return circuit
    return DefineShift, DefineDynamicShift

DefineShiftLeft, DefineDynamicShiftLeft = shift_factory("Left", "<<")
DefineShiftRight, DefineDynamicShiftRight = shift_factory("Right", ">>")


def binop_factory(name, T, op):
    @lru_cache(maxsize=None)
    def DefineCirc(N):
        _type = T(N)
        circuit = DefineCircuit("{}{}".format(name, N), "I0", In(_type), "I1", In(_type), "O", Out(_type))
        circuit.verilog = "assign O = I0 {} I1".format(op)
        EndCircuit()
        return circuit
    return DefineCirc

DefineUnsignedAdd = binop_factory("UnsignedAdd", UInt, "+")
DefineUnsignedSub = binop_factory("UnsignedSub", UInt, "-")
DefineUnsignedMul = binop_factory("UnsignedMul", UInt, "*")
DefineUnsignedDiv = binop_factory("UnsignedDiv", UInt, "/")

DefineSignedAdd = binop_factory("SignedAdd", SInt, "+")
DefineSignedSub = binop_factory("SignedSub", SInt, "-")
DefineSignedMul = binop_factory("SignedMul", SInt, "*")
DefineSignedDiv = binop_factory("SignedDiv", SInt, "/")


def comparison_factory(name, T, op):
    @lru_cache(maxsize=None)
    def DefineCirc(N):
        _type = T(N)
        circuit = DefineCircuit("{}{}".format(name, N), "I0", In(_type), "I1", In(_type), "O", Out(Bit))
        circuit.verilog = "assign O = I0 {} I1".format(op)
        EndCircuit()
        return circuit
    return DefineCirc

DefineUnsignedLt = comparison_factory("UnsignedLt", UInt, "<")
DefineUnsignedLtE = comparison_factory("UnsignedLtE", UInt, "<=")
DefineUnsignedGt = comparison_factory("UnsignedGt", UInt, ">")
DefineUnsignedGtE = comparison_factory("UnsignedGtE", UInt, ">=")

DefineSignedLt = comparison_factory( "SignedLt",  SInt, "<")
DefineSignedLtE = comparison_factory("SignedLtE", SInt, "<=")
DefineSignedGt = comparison_factory( "SignedGt",  SInt, ">")
DefineSignedGtE = comparison_factory("SignedGtE", SInt, ">=")
