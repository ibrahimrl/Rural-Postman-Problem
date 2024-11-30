# Rural Postman Problem Solver

This project provides a solver for the **Rural Postman Problem (RPP)** using **SAT encoding** and the **Glucose SAT solver**. The solver reads a graph, encodes the RPP into a CNF formula, calls the Glucose SAT solver, and decodes the solution to output the required cycle.

---

## Table of Contents

- [Rural Postman Problem Solver](#rural-postman-problem-solver)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Problem Description](#problem-description)
  - [SAT Encoding](#sat-encoding)
    - [Propositional Variables](#propositional-variables)
    - [Constraints](#constraints)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the repository:](#1-clone-the-repository)
    - [2. Navigate to the project directory:](#2-navigate-to-the-project-directory)
    - [3. Install Glucose SAT Solver](#3-install-glucose-sat-solver)
    - [4. Modify Glucose Source Code](#4-modify-glucose-source-code)
      - [**Steps to Modify `Main.cc`:**](#steps-to-modify-maincc)
    - [5. Compile Glucose](#5-compile-glucose)
    - [6. Update Solver Path in Script](#6-update-solver-path-in-script)
  - [Usage](#usage)
    - [Input File Format](#input-file-format)
    - [Running the Solver](#running-the-solver)
  - [Experimental Results](#experimental-results)
    - [Testing Environment](#testing-environment)
    - [Results](#results)
    - [Observations](#observations)
    - [Conclusion](#conclusion)
  - [Code Structure](#code-structure)

---

## Introduction

The **Rural Postman Problem (RPP)** is a variation of the classic Postman Problem. Given a graph and a subset of required edges, the goal is to find a closed walk (cycle) of minimal total cost that traverses all the required edges.

This project implements a solver for the RPP by:

- Encoding the problem as a Boolean satisfiability problem (SAT).
- Using the **Glucose SAT solver** to find a solution.
- Decoding and presenting the solution in terms of the original graph.

---

## Problem Description

Given:

- A graph $G = (V, E)$ with:
  - $V$: A set of vertices.
  - $E$: A set of undirected edges.
- A subset of required edges $F \subseteq E$.
- An integer $k$ representing the maximum number of edges allowed in the cycle.

**Objective:**

Find a closed walk (cycle) $C$ in $G$ such that:

- **All required edges are included**: Every edge in $F$ is traversed exactly once in $C$.
- **Edge usage**: Each edge in $E$ is used at most once in $C$.
- **Cycle constraint**: The walk starts and ends at the same vertex.
- **Edge limit**: The total number of edges in $C$ does not exceed $k$.

**Constraints:**

- The graph may be disconnected; however, it's only possible to find a solution if all required edges are in the same connected component.
- Nodes can be revisited multiple times, but edges are traversed at most once.

---

## SAT Encoding

### Propositional Variables

- **Edge Variables**: For each edge $e \in E$, introduce a propositional variable $x_e$:
  - $x_e = \text{True}$ if edge $e$ is included in the cycle.
  - $x_e = \text{False}$ otherwise.

### Constraints

1. **Edge Inclusion Constraints**:

   - For every required edge $e \in F$:
     - $x_e$ must be **True**.
     - Encoded as: $x_e$.

2. **Edge Count Constraint**:

   - The total number of selected edges must be exactly $k$:
     - $$ \sum_{e \in E} x_e = k. $$

   - Encoded using cardinality constraints.

3. **Degree Constraints**:

   - For each vertex $v \in V$:
     - If $v$ is part of the cycle (i.e., incident to any selected edge), it must have **degree 2** in the cycle.

     - **At-Least-2 Constraint**:
       - At least two incident edges are selected.
       - Encoded as:
         - For each vertex $v$ with incident edges $\{ x_{e_1}, x_{e_2}, \dots, x_{e_n} \}$:
           - $$ \sum_{i=1}^{n} x_{e_i} \geq 2. $$

     - **At-Most-2 Constraint**:
       - At most two incident edges are selected.
       - Encoded as:
         - $$ \sum_{i=1}^{n} x_{e_i} \leq 2. $$

4. **Connectivity Constraints**:

   - Ensures the selected edges form a single connected cycle.
   - Simplified by pre-processing to check if all required edges are in the same connected component.

---

## Prerequisites

- **Python 3.x**: The script is written in Python 3.
- **Glucose SAT Solver**: The solver requires the Glucose SAT solver executable.

---

## Setup Instructions

### 1. Clone the repository:
   
  ```bash
  git clone https://github.com/ibrahimrl/Rural-Postman-Problem.git
  ```
  
### 2. Navigate to the project directory:
   ```bash
    cd Rural-Postman-Problem
   ```

### 3. Install Glucose SAT Solver

Download the Glucose SAT solver source code:

```bash
git clone https://github.com/audemard/glucose.git
```


### 4. Modify Glucose Source Code

To ensure that Glucose outputs the model (variable assignments) when a solution is found, you need to modify the `Main.cc` file in the Glucose source code.

#### **Steps to Modify `Main.cc`:**

1. **Navigate to the Glucose Source Directory:**
   

    ```bash
    cd glucose/simp
    ```
  

2. **Open `Main.cc` for Editing:**

    Use your preferred text editor to open `Main.cc`.

    ```bash
    vim Main.cc
    ```

3. **Locate the Code Block Responsible for Printing the Model:**

    Find the following code near the end of the `main` function:

    ```bash
    if(S.showModel && ret==l_True) {
        printf("v ");
        for (int i = 0; i < S.nVars(); i++)
            if (S.model[i] != l_Undef)
                printf("%s%s%d", (i==0)?"":" ", (S.model[i]==l_True)?"":"-", i+1);
        printf(" 0\n");
    }
    ```


4. **Modify the Code to Always Print the Model:**

    Press `i` and replace the above code block with:


    ```bash
    if(ret == l_True) {
        printf("v ");
        for (int i = 0; i < S.nVars(); i++)
            if (S.model[i] != l_Undef)
                printf("%s%s%d", (i==0)?"":" ", (S.model[i]==l_True)?"":"-", i+1);
        printf(" 0\n");
    }
    ```

    This change removes the condition `S.showModel &&`, ensuring that the model is always printed when a solution is found.



5. **Save and Close the File:**

    If you use `vim`, press `ESC` then type `:x`.

### 5. Compile Glucose

  After modifying the source code, compile the Glucose solver. Make sure you are still inside the `simp` direcotry.

  1. **Clean Previous Builds:**

      ```bash
      make clean
      ```

  2. **Compile the Solver:**

      ```bash
      make r
      ```
      This will generate the executable `glucose_release` in the `simp` directory.

  3. **Verify the Compilation:**

      Ensure that the `glucose_release` executable is created:
      
      ```bash
      chmod +x glucose_release
      ```

### 6. Update Solver Path in Script

  In the `rural_postman.py` script, update the `solver_path` variable to point to the compiled Glucose executable.

  ```bash
  solver_path = '/path/to/glucose_release'
  ```

---


## Usage

### Input File Format

The input file should be a text file containing:

1. **First Line**: Three integers `n m k`
   - `n`: Number of nodes in the graph.
   - `m`: Number of edges in the graph.
   - `k`: Maximum number of edges allowed in the cycle.

2. **Next `m` Lines**: Edges of the graph
   - Each line contains two integers `u v`, representing an undirected edge between nodes `u` and `v`.

3. **Next Line**: An integer `f`
   - `f`: Number of edges in subset **F** (edges that must be included in the cycle).

4. **Next `f` Lines**: Edges in subset **F**
   - Each line contains two integers `u v`, representing an edge that must be included in the cycle.


### Running the Solver

  To run the solver, use the following command:

  ```bash
  python3 rural_postman.py <input_file>
  ```

## Experimental Results


### Testing Environment

- **Processor**: Intel Core i5
- **RAM**: 8 GB
- **Operating System**: MacOS
- **Python Version**: 3.12
- **Glucose Version**: 4.2, Modified.

### Results

| Instance                | Nodes | Edges | Required Edges | k   | Runtime    | Result       |
|-------------------------|-------|-------|----------------|-----|------------|--------------|
| input_small_positive.txt| 6     | 7     | 3              | 6   | <1 second  | Solution found|
| input_small_negative.txt| 4     | 3     | 2              | 4   | <1 second  | No solution  |
| large_instance.txt      | 30    | 115   | 10             | 50  | ~7 minutes | Solution found|

### Observations

- **Small Instances**: The solver handles small graphs efficiently, with runtimes under a second.
- **Large Instances**: For graphs with up to 30 nodes and over 100 edges, the solver takes several minutes.
- **Scalability**: The runtime increases significantly with the size of the graph due to the exponential growth in the number of clauses.
- **Limitations**: For very large graphs (e.g., over 50 nodes and several hundred edges), the solver may run out of memory or take an impractically long time.


### Conclusion

The solver is suitable for small to medium-sized instances of the RPP. For larger instances, optimizations to the CNF encoding or alternative solving methods may be necessary.

---

## Code Structure

- **`rural_postman.py`**: The main script containing the solver implementation.
  
  **Functions:**
  
  - `read_input(file_path)`: Reads and parses the input file.
    - **Purpose**: Reads the graph structure, subset **F**, and the value of **k** from the input file.
    - **Input**: Path to the input file.
    - **Output**: Returns `n` (number of nodes), `edges` (list of edges), `F` (list of required edges), and `k` (maximum number of edges in the cycle).
  
  - `encode_sum_leq_k(vars_list, k)`: Encodes the constraint that the sum of selected edges is less than or equal to **k**.
    - **Purpose**: Generates CNF clauses to enforce that at most **k** edges are selected.
    - **Input**: List of variables (`vars_list`), integer **k**.
    - **Output**: List of CNF clauses representing the constraint.
  
  - `encode_sum_geq_k(vars_list, k)`: Encodes the constraint that the sum of selected edges is greater than or equal to **k**.
    - **Purpose**: Generates CNF clauses to enforce that at least **k** edges are selected.
    - **Input**: List of variables (`vars_list`), integer **k**.
    - **Output**: List of CNF clauses representing the constraint.
  
  - `check_connectivity(n, edges, F)`: Checks if all required edges are in the same connected component.
    - **Purpose**: Ensures that it's possible to form a cycle including all required edges.
    - **Input**: Number of nodes (`n`), list of edges (`edges`), list of required edges (`F`).
    - **Output**: Returns `True` if all required edges are connected; otherwise, `False`.
  
  - `write_cnf(n, edges, F, k, cnf_file)`: Encodes the problem into CNF format.
    - **Purpose**: Generates the CNF file that represents the SAT encoding of the RPP.
    - **Input**: Number of nodes (`n`), list of edges (`edges`), list of required edges (`F`), integer **k**, output CNF file path (`cnf_file`).
    - **Output**: Returns a mapping of variables to edges (`var_mapping`).
  
  - `call_sat_solver(cnf_file, solver_path='glucose', output_file='solver_output.txt')`: Calls the Glucose SAT solver.
    - **Purpose**: Executes the Glucose SAT solver on the CNF file.
    - **Input**: CNF file path (`cnf_file`), path to the Glucose solver executable (`solver_path`), output file path (`output_file`).
    - **Output**: None (the solver's output is written to the specified output file).
  
  - `parse_solver_output(output_file, var_mapping)`: Parses the solver's output to extract the solution.
    - **Purpose**: Reads the SAT solver's output and determines which edges are included in the solution.
    - **Input**: Output file path (`output_file`), variable-to-edge mapping (`var_mapping`).
    - **Output**: Returns a list of selected edges if a solution exists; otherwise, `None`.
  
  - `main()`: The main function that orchestrates the execution of the solver.
    - **Purpose**: Coordinates the entire solving process, from reading input to outputting the result.
