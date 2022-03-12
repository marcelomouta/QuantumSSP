"""
Implementation of a quantum circuit solving a variant of the Subset Sum Problem (SSP)

More specifically, it finds the subsets where the sum is equal to the value 16 in the given vector
"""

import math
import pennylane as qml

from draper_adder import adder
from utils import plot_results


vector = [5, 7, 8, 9, 1]
target_value = 16

# number of qubits to represent vector indices
n = len(vector)
# number of qubits to represent value
value_len = math.floor(math.log2(target_value)) + 1

# Circuit stores the following qubits:
# |indices>|aux_value>|summed_value>|oracle_output>
n_wires = n + value_len + value_len + 1

# create quantum device
wires = list(range(n_wires))
dev = qml.device("default.qubit", wires=wires)


def set_index_value(index_wire, index_value):
    """
    Set auxiliary qubits with the value corresponding to a vector index

    index_wire: wire representing the index
    index_value: value of the vector in this index
    """

    for bit_index in range(len(index_value)):
        if index_value[bit_index] == "1":
            bit_wire = wires[n + bit_index]
            qml.CNOT(wires=[index_wire, bit_wire])


def subset_sum(f_value):
    """
    Performs a sum over all values represented by current indices selected
    on the Grover search using the Draper Adder
    """

    oracle_wires = wires[n:]
    aux_value_wires = oracle_wires[:value_len]
    summed_value_wires = oracle_wires[value_len:-1]

    # sum value corresponding to each index
    for index in range(n):
        index_wire = wires[index]
        index_value = f_value.format(vector[index])

        # set auxiliary value from current index
        set_index_value(index_wire, index_value)
        # add current value to total sum
        adder(aux_value_wires, summed_value_wires)

        # reset current auxiliary value for next sum
        qml.adjoint(set_index_value)(index_wire, index_value)


def oracle(value=16):
    """
    Apply an oracle which performs a phase flip whenever the subset
    represented by vector indices sums to the target value
    """

    # Format string for binary representation of the values
    f_value = "{:0" + str(value_len) + "b}"

    # sum over subset
    subset_sum(f_value)

    # Apply phase change to last qubit if subset sum equals desired value
    binary_value = f_value.format(value)
    sum_result_wires = wires[len(vector) + value_len : -1]
    qml.MultiControlledX(
        control_wires=sum_result_wires, wires=wires[-1], control_values=binary_value
    )

    # uncomputation of subset_sum
    qml.adjoint(subset_sum)(f_value)


@qml.qnode(dev)
def GroverSearch(target_value, num_iterations=1):
    """
    Grover Search algorithm for finding the subsets that sum to the desired value
    in the given vector

    adapted from:
        https://pennylane.readthedocs.io/en/stable/code/api/pennylane.GroverOperator.html
    """
    n = len(vector)
    for wire in wires[:n]:
        qml.Hadamard(wire)

    # set oracle output qubit to |->
    qml.PauliX(wires[-1])
    qml.Hadamard(wires[-1])

    for _ in range(num_iterations):
        oracle(target_value)
        qml.templates.GroverOperator(wires=wires[:n])

    return qml.probs(wires[:n])


def calculate_num_Grover_iters(n, k):
    """
    Calculate optimal number of Grover search iterations

    n: number of qubits
    k: number of solutions
    """
    num_iters = (math.pi / 4) * math.sqrt(2 ** n / k)
    return math.floor(num_iters)


def main():

    # Assume the number of solutions is known --> |01010> and |01101>
    # In a more general solution we would need to count k first, see:
    # https://qiskit.org/textbook/ch-labs/Lab06_Grover_search_with_an_unknown_number_of_solutions.html
    k = 2

    # Find optimal number of iterations for Grover search
    num_iters = calculate_num_Grover_iters(n, k)

    # Search for the subsets that sum to the target value
    result_probs = GroverSearch(target_value, num_iters)

    # Plot histogram with resulting probabilities
    plot_results(result_probs, n)


if __name__ == "__main__":
    main()