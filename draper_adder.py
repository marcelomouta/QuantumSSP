import pennylane as qml
import math


def adder(wires_a, wires_b):
    """
    Drapper adder that transforms the states |a>|b> into |a>|a+b>

    wires_a: indices of the wires containing value a
    wires_a: indices of the wires containing value b

    For further details see:
      Ruiz-Perez et al., Quantum arithmetic with the Quantum Fourier Transform, 2017. https://arxiv.org/pdf/1411.5949.pdf
    """

    qml.QFT(wires=wires_b)

    n = len(wires_b)

    for j in range(n):
        for k in range(n - j):
            phi = math.pi / (2 ** k)
            qml.ControlledPhaseShift(phi, wires=[wires_a[j + k], wires_b[-j - 1]])

    qml.QFT(wires=wires_b).inv()