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


@lru_cache(maxsize=None)
def DefineUnsignedShiftLeft(N, amount):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = UInt(N)

    class _UnsignedShiftLeft(Circuit):
        name = "UnsignedShiftLeft{}_{}".format(N, amount)
        IO = ["I", In(T), "O", Out(T)]

    _UnsignedShiftLeft.verilog = "assign O = I << {}'d{}".format((N-1).bit_length(), amount)
    return _UnsignedShiftLeft


@lru_cache(maxsize=None)
def DefineUnsignedDynamicShiftLeft(N):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = UInt(N)

    class _UnsignedDynamicShiftLeft(Circuit):
        name = "UnsignedDynamicShiftLeft{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedDynamicShiftLeft.verilog = "assign O = I0 << I1"
    return _UnsignedDynamicShiftLeft


@lru_cache(maxsize=None)
def DefineUnsignedShiftRight(N, amount):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = UInt(N)

    class _UnsignedShiftRight(Circuit):
        name = "UnsignedShiftRight{}_{}".format(N, amount)
        IO = ["I", In(T), "O", Out(T)]

    _UnsignedShiftRight.verilog = "assign O = I >> {}'d{}".format((N-1).bit_length(), amount)
    return _UnsignedShiftRight


@lru_cache(maxsize=None)
def DefineUnsignedDynamicShiftRight(N):
    assert N > 1, "TODO: Should we support shift left on a single bit?"
    T = UInt(N)

    class _UnsignedDynamicShiftRight(Circuit):
        name = "UnsignedDynamicShiftRight{}".format(N)
        IO = ["I0", In(T), "I1", In(T), "O", Out(T)]

    _UnsignedDynamicShiftRight.verilog = "assign O = I0 >> I1"
    return _UnsignedDynamicShiftRight
