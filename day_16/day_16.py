import time
import math
from functools import reduce
from io import StringIO


def read_input(path):
    with open(path, "r") as file:
        return file.read().strip()


def convert_to_binary(stream):
    result = ""
    for digit in stream:
        result += format(int(digit, 16), "04b")

    return result


def parse_packets(input, subpackets=math.inf):
    stream = StringIO(input)
    version_sum = 0
    packet = 0
    buffer = []
    while stream.tell() < len(input) - 10 and packet < subpackets:
        version = int(stream.read(3), 2)
        type = int(stream.read(3), 2)

        version_sum += version

        if type == 4:
            bitstring = ""
            while True:
                group = int(stream.read(1), 2)
                value = stream.read(4)
                bitstring += value

                if group == 0:
                    break

            buffer.append(int(bitstring, 2))
        else:
            inner_buffer = []
            length_type = stream.read(1)

            if length_type == "0":
                length = int(stream.read(15), 2)
                s, _, inner_buffer = parse_packets(
                    input[stream.tell() : stream.tell() + length]
                )
                stream.seek(stream.tell() + length)
                version_sum += s
            else:
                length = int(stream.read(11), 2)
                s, l, inner_buffer = parse_packets(
                    input[stream.tell() :], subpackets=length
                )
                stream.seek(stream.tell() + l)
                version_sum += s

            if type == 0:
                buffer += [sum(inner_buffer)]
            elif type == 1:
                buffer += [reduce(lambda x, y: x * y, inner_buffer)]
            elif type == 2:
                buffer += [min(inner_buffer)]
            elif type == 3:
                buffer += [max(inner_buffer)]
            elif type == 5:
                buffer += [inner_buffer[0] > inner_buffer[1]]
            elif type == 6:
                buffer += [inner_buffer[0] < inner_buffer[1]]
            elif type == 7:
                buffer += [inner_buffer[0] == inner_buffer[1]]

        packet += 1

    return version_sum, stream.tell(), buffer


def solve_silver(puzzle):
    stream = convert_to_binary(puzzle)
    result, _, _ = parse_packets(stream)
    return result


def solve_gold(puzzle):
    stream = convert_to_binary(puzzle)
    _, _, result = parse_packets(stream)
    return result.pop()


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(puzzle)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
