# README

This is a tool to search for the periodic function, showing all the model in the main body of our paper.

### STP Tool Installation and Usage

For information on installing the STP tool, please refer to: 
https://stp.readthedocs.io/en/latest/

For guidance on using the STP tool, please see: 
https://stp.readthedocs.io/en/stable/cvc-input-language.html

## Model

It is provided in `Model`. All our rules are implemented in `operation_7bit_f_k.py`. This script allows users to run various algorithms, generating an output file named `model2.cvc`.

To obtain solutions for the model, run the command `stp model2.cvc`. The results of the model's solutions will be stored in `res.txt`.

Additionally, you can use `process_path.py` to read and interpret the information contained in the solution file.


### Key Variables

- `num_R_color`: Represents the round of Phase 1
- `num_R_head`: Represents the round of Phase 2
- `num_R_linear`: Represents the round of Phase 3
- `num_branch`: the number of tyhe branches of the structure. (no need to modify)

### Usage Instructions

1. Execute `{cipher}.py` to run the desired cipher.
2. Use the command `stp model2.cvc` to solve the model.
3. Access the solutions in `res.txt`.
4. Run `process_path.py` to extract and process the information from the solutions.

### Experiments

The experimental section `Experiments` presents the search for actual periods of various primitives.
In particular, `dec-type1-d-FK.py` provides an example of searching for a period for different branchse, where `num_branch` can be modefied and the round is `R = num_branch**2+1`
