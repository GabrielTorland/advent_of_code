from collections import defaultdict
from itertools import product

import numpy as np
import sympy


def create_equations(M_rref, pivot_cols):
    none_pivot_cols = [i for i in range(M_rref.shape[1] - 1) if i not in pivot_cols]
    free_variables = {}
    number = 97
    for i in none_pivot_cols:
        free_variables[i] = sympy.symbols(chr(number))
        number += 1

    variables = {}
    for i in pivot_cols:
        variables[i] = sympy.symbols(f"x_{i+1}")

    equations = {}
    for i in range(M_rref.shape[0]):
        if i >= len(pivot_cols):
            break

        rhs = M_rref[i, M_rref.shape[1] - 1]
        for j in range(pivot_cols[i] + 1, M_rref.shape[1] - 1):
            if M_rref[i, j] == 0:
                continue

            coefficient = M_rref[i, j]

            aVariable = free_variables[j] if j in free_variables else variables[j]
            rhs += (-1) * coefficient * aVariable
        equations[pivot_cols[i]] = rhs

    return equations, free_variables, variables


def is_valid_result(result, buttons, joltages):
    result_clicks = defaultdict(int)
    for i, val in result.items():
        if val < 0:
            return False

        if not val.is_integer:
            return False

        for button in buttons[i]:
            result_clicks[button] += val

    for button, clicks in result_clicks.items():
        if clicks > joltages[button]:
            return False

    return True


def is_valid_comb(comb, free_variables, buttons, joltages):
    current_joltages = defaultdict(int)
    for i, val in zip(free_variables.keys(), comb):
        for button in buttons[i]:
            current_joltages[button] += val
            if current_joltages[button] > joltages[button]:
                return False
    return True


def p2(input_file="Inputs/10.txt"):
    min_clicks = []
    for idx, line in enumerate(open(input_file, "r").readlines()):
        segments = line.strip().split(" ")

        buttons = []
        for button_raw in segments[1:-1]:
            buttons.append(list(map(int, button_raw[1:-1].split(","))))

        unique_buttons = set(
            [button for sub_buttons in buttons for button in sub_buttons]
        )

        joltages = {
            i: joltage
            for i, joltage in enumerate(map(int, segments[-1][1:-1].split(",")))
        }

        m = []
        for sub_buttons in buttons:
            row = np.array([0] * len(joltages))
            for button in sub_buttons:
                row[button] = 1
            m.append(row)
        m.append(np.array(list(joltages.values())))

        m = np.array(m).T
        M = sympy.Matrix(m)

        M_rref, pivot_cols = M.rref()
        equations, free_variables, variables = create_equations(M_rref, pivot_cols)

        valid_results = []
        for comb in product(range(max(joltages.values())), repeat=len(free_variables)):
            if not is_valid_comb(comb, free_variables, buttons, joltages):
                continue
            free_variable_values = {}
            for free_variable, val in zip(free_variables.values(), comb):
                free_variable_values[free_variable] = val

            result = {}
            for i, equation in equations.items():
                answer = equation

                while any(
                    [
                        variable in answer.free_symbols
                        for variable in list(variables.values())
                        + list(free_variables.values())
                    ]
                ):
                    for j, variable in variables.items():
                        if i == j:
                            continue
                        if variable in answer.free_symbols:
                            answer = answer.subs(variable, equations[j])

                    for free_variable, value in free_variable_values.items():
                        answer = answer.subs(free_variable, value)

                result[i] = answer

            for i, val in zip(free_variables.keys(), comb):
                result[i] = val

            if is_valid_result(result, buttons, joltages):
                valid_results.append(result)

        best_result = min(valid_results, key=lambda x: sum(x.values()))

        min_clicks.append(sum(best_result.values()))
        print(sum(best_result.values()))
        print(sum(min_clicks))
        print()


if __name__ == "__main__":
    p2()
