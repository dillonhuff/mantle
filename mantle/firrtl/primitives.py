from magma import *

_Register = DefineCircuit("Register", "I", In(Bit), "CLK", In(Bit), "O", Out(Bit))
_Register.firrtl = """
reg r : UInt<1>, CLK
r <= I
O <= r
"""
EndCircuit()


def Register(n):
    return join(col(lambda y : _Register(), n))

# TODO: Add decorator to memoize circuit definitions
# add_cache = {}
# def AddN(N):
#     if N not in add_cache:
#         add_cache[N] = DefineCircuit("Add{}".format(N),
#             "I0", In(Array(N, Bit)),
#             "I1", In(Array(N, Bit)),
#             "O", Out(Array(N + 1, Bit)))
#         add_cache[N].firrtl = """
#     O = add(I0, I1)
# """
#         EndCircuit()
#     return add_cache[N]

Add2 = DefineCircuit("Add2",
    "I0", In(Array(2, Bit)),
    "I1", In(Array(2, Bit)),
    "O", Out(Array(2 + 1, Bit)))
Add2.firrtl = """
O <= add(I0, I1)
"""
EndCircuit()
