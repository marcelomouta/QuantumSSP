# QuantumSSP
A quantum circuit that solves a variation of the Subset Sum Problem (SSP) in which all the inputs are positive and all the subsets are found.

More specifically, it finds the subsets where the sum is equal to the value 16 in the vector [5, 7, 8, 9, 1], being easily generalized for different vectors and values.

To do this, it assumes a representation using 5 qubits for the indices of the vector and then performs a Grover search over all the possible combinations of indices. In order to detect which indices should make the cut, an oracle is constructed which only flips the phase of the quantum state when a specific combination of indices has values which sum to the desired value.

This implementation assumes the number of solutions is known beforehand, although a more generalized solution can be obtained by performing a Quantum Counting to obtain the number of solutions before performing the search.[^count]

## Oracle

The constructed oracle for the subset search uses n + n + 1 qubits, where n is the length of the binary representation of the desired value. It uses the first n qubits as an auxiliary space to set the vector value corresponding to an index. It then sums that value to the following n qubits and resets the first n qubits in order to be able to sum over the remaining indices of the subset, while economizing space. Once all the values given by the selected indices are summed, a phase flip is then applied to the last qubit controlled on whether the subset sum equals the desired value.

## Draper Adder
The Draper Adder[^1] was used to perform the sum of the possible subset values, and the implementation was based on the description provided by Ruiz-Perez et al. (2017)[^2] 

The following exemplifies the obtained circuit for adding 10 and 6, represented as |01010> and |00110>, respectively:
```
 0: ───────────╭ControlledPhaseShift(3.14)───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤       
 1: ──X────────│────────────────────────────╭ControlledPhaseShift(1.57)────────────────────────────────╭ControlledPhaseShift(3.14)───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤       
 2: ───────────│────────────────────────────│────────────────────────────╭ControlledPhaseShift(0.785)──│──────────────────────────────────────────────────────────╭ControlledPhaseShift(1.57)──────────────────────────────────────────────────────────────╭ControlledPhaseShift(3.14)───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤       
 3: ──X────────│────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────╭ControlledPhaseShift(0.393)──│──────────────────────────────────────────────────────────╭ControlledPhaseShift(0.785)──│──────────────────────────────────────────────────────────╭ControlledPhaseShift(1.57)────────────────────────────────╭ControlledPhaseShift(3.14)─────────────────────────────────────────────────────────────────────┤       
 4: ───────────│────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────╭ControlledPhaseShift(0.196)──│─────────────────────────────│────────────────────────────╭ControlledPhaseShift(0.393)──│────────────────────────────╭ControlledPhaseShift(0.785)──│────────────────────────────╭ControlledPhaseShift(1.57)──╭ControlledPhaseShift(3.14)───────────┤       
 5: ─────╭QFT──│────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│────────────────────────────╰ControlledPhaseShift(3.14)──╭QFT⁻¹──╭┤ Probs 
 6: ─────├QFT──│────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────╰ControlledPhaseShift(3.14)──╰ControlledPhaseShift(1.57)───────────────────────────────├QFT⁻¹──├┤ Probs 
 7: ──X──├QFT──│────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│────────────────────────────│─────────────────────────────│─────────────────────────────╰ControlledPhaseShift(3.14)──│─────────────────────────────╰ControlledPhaseShift(1.57)──╰ControlledPhaseShift(0.785)─────────────────────────────────────────────────────────────────────────────────────────├QFT⁻¹──├┤ Probs 
 8: ──X──├QFT──│────────────────────────────│────────────────────────────│─────────────────────────────╰ControlledPhaseShift(3.14)──│─────────────────────────────╰ControlledPhaseShift(1.57)──│─────────────────────────────╰ControlledPhaseShift(0.785)───────────────────────────────╰ControlledPhaseShift(0.393)────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────├QFT⁻¹──├┤ Probs 
 9: ─────╰QFT──╰ControlledPhaseShift(3.14)──╰ControlledPhaseShift(1.57)──╰ControlledPhaseShift(0.785)───────────────────────────────╰ControlledPhaseShift(0.393)───────────────────────────────╰ControlledPhaseShift(0.196)─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╰QFT⁻¹──╰┤ Probs 
    
```
This is achieved by transforming the states |01010>|00110> into |01010>**|10000>** and measuring qubits 5 to 9, yelding the desired 16 in binary representation.


[^count]: https://qiskit.org/textbook/ch-labs/Lab06_Grover_search_with_an_unknown_number_of_solutions.html

[^1]: T. G. Draper, Addition on a Quantum Computer, 2000. [arXiv:quant-ph/0008033](https://arxiv.org/pdf/quant-ph/0008033.pdf)

[^2]: Ruiz-Perez et al., Quantum arithmetic with the Quantum Fourier Transform, 2017. [arXiv:1411.5949](https://arxiv.org/pdf/1411.5949.pdf)
