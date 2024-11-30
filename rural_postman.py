#!/usr/bin/env python3
import sys
import subprocess
import os
from itertools import combinations

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    n, m, k = map(int, lines[0].strip().split())
    edges = []
    for i in range(1, m+1):
        u, v = map(int, lines[i].strip().split())
        edge = tuple(sorted((u, v)))  # Ensure edges are stored consistently
        edges.append(edge)

    f_line = m + 1
    f_count = int(lines[f_line].strip())
    F = []
    for i in range(f_line+1, f_line+1+f_count):
        u, v = map(int, lines[i].strip().split())
        edge = tuple(sorted((u, v)))  # Ensure edges are stored consistently
        F.append(edge)

    return n, edges, F, k

def encode_sum_leq_k(vars_list, k):
    clauses = []
    if k < len(vars_list):
        for subset in combinations(vars_list, k+1):
            clause = ' '.join([f"-{var}" for var in subset]) + " 0"
            clauses.append(clause)
    return clauses


def encode_sum_geq_k(vars_list, k):
    clauses = []
    if k > 0:
        for subset in combinations(vars_list, len(vars_list) - k + 1):
            clause = ' '.join([f"{var}" for var in subset]) + " 0"
            clauses.append(clause)
    return clauses

def write_cnf(n, edges, F, k, cnf_file):
    var_mapping = {}
    clauses = []
    num_vars = len(edges)
    num_clauses = 0

    # Assign variable numbers to edges
    for idx, edge in enumerate(edges):
        var_mapping[edge] = idx + 1

    # Edge Inclusion Constraints for edges in F
    for edge in F:
        var = var_mapping[edge]
        clauses.append(f"{var} 0")
        num_clauses += 1

    # Edge Count Constraints: sum x_e = k
    all_vars = list(var_mapping.values())
    clauses += encode_sum_leq_k(all_vars, k)
    num_clauses += len(encode_sum_leq_k(all_vars, k))
    
    clauses += encode_sum_geq_k(all_vars, k)
    num_clauses += len(encode_sum_geq_k(all_vars, k))

    # Degree Constraints for each node
    for v in range(1, n+1):
        incident_edges = [edge for edge in edges if v in edge]
        vars_incident = [var_mapping[edge] for edge in incident_edges]

        # Exactly-2 Constraints for incident edges at node v
        # At-Least-2 Constraints
        for pair in combinations(vars_incident, 2):
            clauses.append(f"{pair[0]} {pair[1]} 0")
            num_clauses += 1

        # At-Most-2 Constraints
        for triplet in combinations(vars_incident, 3):
            clauses.append(f"-{triplet[0]} -{triplet[1]} -{triplet[2]} 0")
            num_clauses += 1

    # Write clauses to the CNF file
    with open(cnf_file, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(f"{clause}\n")

    return var_mapping



def call_sat_solver(cnf_file, solver_path='glucose', output_file='solver_output.txt'):
    command = [solver_path, cnf_file]
    with open(output_file, 'w') as outfile:
        subprocess.run(command, stdout=outfile)


def parse_solver_output(output_file, var_mapping):
    with open(output_file, 'r') as f:
        lines = f.readlines()

    satisfiable = False
    model_vars = []
    for line in lines:
        line = line.strip()
        if line.startswith('s SATISFIABLE'):
            satisfiable = True
        elif line.startswith('v '):
            vars_in_line = map(int, line[2:].strip().split())
            model_vars.extend(vars_in_line)

    if not satisfiable:
        return None  # No solution

    selected_edges = []
    inv_var_mapping = {v: e for e, v in var_mapping.items()}
    for var in model_vars:
        if var > 0:
            edge = inv_var_mapping.get(var)
            if edge:
                selected_edges.append(edge)

    return selected_edges


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rural_postman.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    n, edges, F, k = read_input(input_file)

    cnf_file = 'problem.cnf'
    var_mapping = write_cnf(n, edges, F, k, cnf_file)

    # Ensure Glucose solver is available
    solver_path = 'glucose/simp/glucose_release'  # Adjust the path to your Glucose solver executable
    if not os.path.exists(solver_path):
        print("Error: Glucose SAT solver not found at the specified path.")
        sys.exit(1)

    output_file = 'solver_output.txt'
    call_sat_solver(cnf_file, solver_path, output_file)

    selected_edges = parse_solver_output(output_file, var_mapping)

    if selected_edges is None:
        print("No solution exists.")
    else:
        print("Cycle found with the following edges:")
        for edge in selected_edges:
            print(f"{edge[0]} -- {edge[1]}")

if __name__ == '__main__':
    main()