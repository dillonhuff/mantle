from magma import *
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


@lru_cache(maxsize=None)
def DefineAnd(N):
    if N == 1:
        T = Bit
    else:
        assert N > 1
        T = Bits(N)

    class _And(Circuit):
        name = "And{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _And.verilog = "assign O = I0 & I1"
    return _And


@lru_cache(maxsize=None)
def DefineOr(N):
    if N == 1:
        T = Bit
    else:
        assert N > 1
        T = Bits(N)

    class _Or(Circuit):
        name = "Or{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _Or.verilog = "assign O = I0 | I1"
    return _Or


@lru_cache(maxsize=None)
def DefineXor(N):
    if N == 1:
        T = Bit
    else:
        assert N > 1
        T = Bits(N)

    class _Xor(Circuit):
        name = "Xor{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _Xor.verilog = "assign O = I0 ^ I1"
    return _Xor


@lru_cache(maxsize=None)
def DefineInvert(N):
    if N == 1:
        T = Bit
    else:
        assert N > 1
        T = Bits(N)

    class _Invert(Circuit):
        name = "Invert{}".format(N)
        IO = ["I", In(T), "O", Out(T)]

    _Invert.verilog = "assign O = ~I"
    return _Invert


@lru_cache(maxsize=None)
def DefineShiftLeft(N, amount):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = Bits(N)

    class _ShiftLeft(Circuit):
        name = "ShiftLeft{}_{}".format(N, amount)
        IO = ["I", In(T), "O", Out(T)]

    _ShiftLeft.verilog = "assign O = I << {}'d{}".format((N-1).bit_length(), amount)
    return _ShiftLeft


@lru_cache(maxsize=None)
def DefineDynamicShiftLeft(N):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = Bits(N)

    class _DynamicShiftLeft(Circuit):
        name = "DynamicShiftLeft{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _DynamicShiftLeft.verilog = "assign O = I0 << I1"
    return _DynamicShiftLeft


@lru_cache(maxsize=None)
def DefineShiftRight(N, amount):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = Bits(N)

    class _ShiftRight(Circuit):
        name = "ShiftRight{}_{}".format(N, amount)
        IO = ["I", In(T), "O", Out(T)]

    _ShiftRight.verilog = "assign O = I >> {}'d{}".format((N-1).bit_length(), amount)
    return _ShiftRight


@lru_cache(maxsize=None)
def DefineDynamicShiftRight(N):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = Bits(N)

    class _DynamicShiftRight(Circuit):
        name = "DynamicShiftRight{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _DynamicShiftRight.verilog = "assign O = I0 >> I1"
    return _DynamicShiftRight


@lru_cache(maxsize=None)
def DefineUnsignedAdd(N):
    T = UInt(N)

    class _UnsignedAdd(Circuit):
        name = "UnsignedAdd{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedAdd.verilog = "assign O = I0 + I1"
    return _UnsignedAdd


@lru_cache(maxsize=None)
def DefineUnsignedSub(N):
    T = UInt(N)

    class _UnsignedSub(Circuit):
        name = "UnsignedSub{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedSub.verilog = "assign O = I0 - I1"
    return _UnsignedSub


@lru_cache(maxsize=None)
def DefineUnsignedMul(N):
    T = UInt(N)

    class _UnsignedMul(Circuit):
        name = "UnsignedMul{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedMul.verilog = "assign O = I0 * I1"
    return _UnsignedMul


@lru_cache(maxsize=None)
def DefineUnsignedDiv(N):
    T = UInt(N)

    class _UnsignedDiv(Circuit):
        name = "UnsignedDiv{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedDiv.verilog = "assign O = I0 / I1"
    return _UnsignedDiv
