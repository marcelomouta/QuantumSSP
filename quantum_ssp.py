"""
Implementation of a quantum circuit solving a variant of the Subset Sum Problem (SSP)

More specifically, it finds the subsets where the sum is equal to the value 16 in the given vector
"""

import pennylane as qml
import matplotlib.pyplot as plt
from draper_adder import adder


n_wires = 4
wires = list(range(n_wires))

# create quantum device
dev = qml.device("default.qubit", wires=wires)


def subset_sum():
    # TODO
    # set value for each index (using CNOTs)
    # sum all values
    return


def oracle():

    # sum over subset
    subset_sum()

    # qml.Hadamard(wires[-1])
    qml.MultiControlledX(control_wires=[0, 1, 2], wires=3, control_values="010")
    # qml.Hadamard(wires[-1])

    # uncomputation of subset_sum
    # qml.adjoint(subset_sum)()


@qml.qnode(dev)
def GroverSearch(num_iterations=2):
    """
    Grover Search algorithm for finding the subsets that sum to the desired value
    in the given vector

    adapted from:
        https://pennylane.readthedocs.io/en/stable/code/api/pennylane.GroverOperator.html
    """
    for wire in wires:
        qml.Hadamard(wire)

    # set output qubit to |->
    qml.PauliX(wires[-1])
    qml.Hadamard(wires[-1])

    # num_iterations is given by .... we need to count first
    #  see https://qiskit.org/textbook/ch-labs/Lab06_Grover_search_with_an_unknown_number_of_solutions.html
    #
    # USE 2 sols for initial test --> |01101> and |01010>
    for _ in range(num_iterations):
        oracle()
        qml.templates.GroverOperator(wires=wires[:-1])
    return qml.probs(wires[:-1])


def plot_results(result_probs, f_index):
    ticks = range(len(result_probs))
    plt.bar(ticks, height=result_probs)
    plt.xlabel("Subsets")
    plt.ylabel("Probabilities")

    labels = [f_index.format(i) for i in ticks]
    plt.xticks(ticks=ticks, labels=labels)

    plt.show()


def main():
    vector = [5, 7, 8, 9, 1]

    # Format string for binary representation of the indexes
    f_index = "{:0" + str(len(vector)) + "b}"

    # Format string for binary representation of the values
    f_value = "{:05b}"  # 16 = 0b10000 (5 bits)

    # Search for the desired subsets
    result_probs = GroverSearch()
    drawer = qml.draw(GroverSearch)
    print(drawer())

    plot_results(result_probs, f_index)


if __name__ == "__main__":
    main()