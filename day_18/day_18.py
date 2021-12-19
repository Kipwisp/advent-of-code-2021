import time
import copy


class Node:
    def __init__(self, value, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.value = value

    def add_child(self, node):
        if self.left:
            self.right = node
        else:
            self.left = node

        node.parent = self

    def explode(self):
        self.value = 0
        self.right = None
        self.left = None

    def split(self):
        left = self.value // 2
        right = self.value - left

        self.add_child(Node(left))
        self.add_child(Node(right))
        self.value = None

    def get_left_most(self):
        left = self.left
        while self.left:
            left = self.left

        return left

    def get_left(self):
        current = self

        if current.parent.left != self and current.parent.left.value is not None:
            return current.parent.left.value

        while current.parent and current.parent.left is current:
            if not current.parent.parent and current.parent.left is current:
                return None
            current = current.parent

        current = current.parent.left

        while not current.value:
            current = current.right

        return current.value

    def get_right(self):
        current = self

        if current.parent.right != self and current.parent.right.value is not None:
            return current.parent.right.value

        while current.parent and current.parent.right is current:
            if not current.parent.parent and current.parent.right is current:
                return None
            current = current.parent

        current = current.parent.right

        while not current.value:
            current = current.left

        return current.value

    def print(self, depth=0):
        if self.left:
            self.left.print(depth + 1)
        print("-" * depth, self.value, "root" if depth == 0 else "")
        if self.right:
            self.right.print(depth + 1)


def traverse(root, depth=0):
    result = []

    if root:
        result += traverse(root.left, depth + 1)
        if root.value is not None:
            result.append((root, depth))
        result += traverse(root.right, depth + 1)

    return result


def build(string):
    open = 0
    mark = 0
    result = []
    for i, char in enumerate(string):
        if char == "[":
            open += 1
        elif char == "]":
            open -= 1

        if open == 2 and char == "[":
            mark = i
        elif open == 1 and char == "]":
            nodes = build(string[mark : i + 1])
            root = Node(None)

            for node in nodes:
                root.add_child(node)

            result.append(root)
        elif char not in {"[", "]", ","} and open == 1:
            result.append(Node(int(char)))

    return result


def get_magnitude(root):
    result = 0

    if root.value is not None:
        result = root.value
    else:
        result = 3 * get_magnitude(root.left) + 2 * get_magnitude(root.right)

    return result


def read_input(path):
    result = []
    with open(path, "r") as file:
        for line in file.readlines():
            nodes = build(line.strip())

            root = Node(None)
            for node in nodes:
                root.add_child(node)

            result.append(root)

    return result


def reduce(root):
    flag = True
    while flag:
        flag = False
        nodes = traverse(root)
        for i, item in enumerate(nodes):
            node, depth = item
            if depth > 4:
                if i > 0:
                    nodes[i - 1][0].value += node.parent.left.value
                if i < len(nodes) - 2:
                    nodes[i + 2][0].value += node.parent.right.value

                node.parent.explode()
                flag = True
                break

        if flag:
            continue

        for i, item in enumerate(nodes):
            node, depth = item
            if node.value >= 10:
                node.split()
                flag = True
                break

    return root


def solve_silver(puzzle):
    puzzle = copy.deepcopy(puzzle)
    while len(puzzle) > 1:
        number = puzzle.pop(0)

        other = puzzle.pop(0)
        root = Node(None)
        root.add_child(number)
        root.add_child(other)

        root = reduce(root)

        puzzle.insert(0, root)

    return get_magnitude(root)


def solve_gold(puzzle):
    best = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if i == j:
                continue

            number = copy.deepcopy(puzzle[i])
            other = copy.deepcopy(puzzle[j])
            root = Node(None)
            root.add_child(number)
            root.add_child(other)

            root = reduce(root)

            magnitude = get_magnitude(root)

            if magnitude > best:
                best = magnitude

    return best


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time()-start}\n")

    start = time.time()
    gold = solve_gold(puzzle)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time()-start}\n")


if __name__ == "__main__":
    main()
