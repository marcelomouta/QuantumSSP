"""
Example usage of quantum addition with Draper Adder
"""

import pennylane as qml

from draper_adder import adder
from utils import plot_results


# number of qubits to represent value
value_len = 5  # 16 = 0b10000 (5 bits)

n_wires = 2 * value_len
wires = list(range(n_wires))

# create quantum device
dev = qml.device("default.qubit", wires=wires)


def set_value(value, value_wires):
    binary_value = "{:05b}".format(value)

    for bit_index in range(len(binary_value)):

        if binary_value[bit_index] == "1":
            qml.PauliX(value_wires[bit_index])


@qml.qnode(dev)
def Add(a, b):

    wires_a = wires[:value_len]
    wires_b = wires[value_len:]

    set_value(a, wires_a)
    set_value(b, wires_b)

    adder(wires_a, wires_b)

    return qml.probs(wires[value_len:])


def main():

    a = 10
    b = 6

    result_probs = Add(a, b)

    # Draw resulting circuit
    drawer = qml.draw(Add)
    print(drawer(a, b))

    # Plot histogram with resulting probabilities
    plot_results(result_probs, value_len)


if __name__ == "__main__":
    main()