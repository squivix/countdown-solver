import random
import itertools
import time
import datetime as dt


BIG_NUMBERS = [25, 50, 75, 100]
MAX_NUMBER = max(BIG_NUMBERS)
MIN_NUMBER = 1


def main():
    starting_numbers = generate_starting_numbers()
    target = random.randint(100, 999)
    start_time = time.time()
    steps = get_steps(starting_numbers, target)
    end_time = time.time()
    elapsed_time = end_time-start_time

    print("\n" * 100)
    print("Time:", str(dt.timedelta(seconds=elapsed_time)))
    if elapsed_time > 30:
        print("Fail.")
    print("Starting numbers:", ", ".join(str(n) for n in starting_numbers))
    print("Target:", target)
    if steps is None:
        print("Unsolvable!")
    else:
        print("\nSolution:")
        print(parse_steps(steps))
        print("Solution is valid." if verify_steps(
            starting_numbers, target, steps) else "Solution is invalid!")


def get_steps(remaining_numbers, target, current=None, steps=None, closest=None):
    if current is None:
        steps = []

    for operand_pair in itertools.permutations(remaining_numbers, 2):
        (operand1, operand2) = operand_pair
        for operation in ['+', '-', '*', '/']:
            if operation == '/' and (operand2 == 0 or not is_integer_result(operand1, operand2)):
                continue
            elif operation == '-' and operand2 > operand1:
                continue
            current = operate(operand1, operand2, operation)
            offby = abs(current - target)
            if current == 0 or len(str(abs(current))) > 4:
                continue
            steps.append([operand1, operation, operand2, current])
            if offby < 10:
                print(f"Off by {offby}:")
                print(parse_steps(steps))
            # print(f'{operand1} {operation} {operand2} = {current}')
            if current == target:
                return steps
            remaining_numbers_copy = remaining_numbers.copy()
            remaining_numbers_copy.remove(operand1)
            remaining_numbers_copy.remove(operand2)
            remaining_numbers_copy.append(current)
            new_steps = get_steps(remaining_numbers_copy,
                                  target, current, steps, closest)
            if new_steps is None:
                steps.pop()
            else:
                return steps


def generate_starting_numbers():
    starting_numbers = []
    big_count = 0
    for i in range(6):
        if random.randint(0, 1) and not big_count >= 4:
            starting_numbers.append(random.choice(BIG_NUMBERS))
            big_count += 1
        else:
            starting_numbers.append(random.randint(1, 10))
    return starting_numbers


def operate(operand1, operand2, operation):
    if operation == '+':
        return operand1 + operand2
    if operation == '-':
        return operand1 - operand2
    if operation == '*':
        return operand1 * operand2
    if operation == '/':
        if not is_integer_result(operand1, operand2):
            raise Exception(
                f"Result of {operand1} / {operand2} is not an integer")
        return operand1 // operand2


def is_integer_result(operand1, operand2):
    return (operand1 / operand2).is_integer()


def verify_steps(starting_numbers, target, steps):
    result: int
    for step in steps:
        (operand1, operation, operand2, r) = step
        if r != operate(operand1, operand2, operation):
            return False
        try:
            starting_numbers.append(r)
            starting_numbers.remove(operand1)
            starting_numbers.remove(operand2)
        except ValueError:
            return False
        result = r
    if result != target:
        return False
    return True


def parse_steps(steps):
    final_string = ""
    for step in steps:
        final_string += f"{step[0]} {step[1]} {step[2]} = {step[3]}\n"
    return final_string


if __name__ == '__main__':
    main()
