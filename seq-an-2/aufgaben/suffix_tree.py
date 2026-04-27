from typing import Dict, List, Optional, Tuple


class SuffixTree:
    """A simple suffix tree built using a naive WOTD-style construction."""

    def __init__(self, string: str) -> None:
        self.base_string: str = string
        self.root: SuffixTreeNode = wotd(string)

    def __repr__(self) -> str:
        return (
            f"SuffixTree of string {self.base_string}:\n"
            f"{self.root.represent_tree(self.base_string, 0, '')}"
        )

    def search_prefix(self, string: str) -> str:
        """Return the longest prefix of `string` found in the suffix tree."""
        curr_pos = 0
        curr_node = self.root

        while curr_pos < len(string):
            char = string[curr_pos]

            if char not in curr_node.children:
                break

            curr_node = curr_node.children[char]
            start, end = curr_node.edge_substring

            for sc in self.base_string[start:end]:
                if string[curr_pos] != sc:
                    break

                curr_pos += 1
                if curr_pos >= len(string):
                    break

        return string[:curr_pos]


class SuffixTreeNode:
    """A node of the suffix tree storing edge interval information."""

    def __init__(self, ij : Optional[Tuple[int,int]]) -> None:
        self.children: Dict[str, "SuffixTreeNode"] = {}
        self.edge_substring: Optional[Tuple[int, int]] = ij

    def represent_tree(
        self,
        base_string: str,
        depth: int,
        incoming_char: str,
    ) -> str:
        """Return a readable string representation of the subtree."""
        
        if self.edge_substring is None:
            result = "Root\n"
        else:
            start, end = self.edge_substring
            substring = base_string[start:end]
            result = (
                f"{' ' * depth}"
                f"{incoming_char}:{start},{end}:{substring}\n"
            )

        for char, child in self.children.items():
            result += child.represent_tree(base_string, depth + 1, char)

        return result


def wotd(string: str) -> SuffixTreeNode:
    """Construct the suffix tree root using naive WOTD recursion."""
    suffixes = [i for i in range(len(string))]
    root = SuffixTreeNode(None)
    wotd_(string, suffixes, root)
    return root


def wotd_(
    base_string: str,
    suffixes: List[int],
    root: SuffixTreeNode,
) -> None:
    """Recursive helper for WOTD suffix tree construction."""
    if len(suffixes) == 1:
        return

    for char, group_suffixes in group(suffixes, base_string).items():
        depth = lcp(group_suffixes, base_string)
        shifted_suffixes = [i + depth for i in group_suffixes]

        start_index = group_suffixes[0]
        node = SuffixTreeNode((start_index, start_index + depth))

        wotd_(base_string, shifted_suffixes, node)
        root.children[char] = node


def group(suffixes: List[int], base_str: str) -> Dict[str, List[int]]:
    """Group suffix indices by their current leading character."""
    groupings: Dict[str, List[int]] = {}

    for index in suffixes:
        char = base_str[index]
        if char not in groupings:
            groupings[char] = []
        groupings[char].append(index)

    return groupings


def lcp(suffixes: List[int], base_str: str) -> int:
    """Return the length of the longest common prefix of given suffixes."""
    equal = True

    max_depth = min(len(base_str) - i for i in suffixes)

    for depth in range(max_depth):
        char = base_str[suffixes[0] + depth]

        for index in suffixes[1:]:
            if base_str[index + depth] != char:
                equal = False
                break

        if not equal:
            break

    if equal:
        depth += 1

    return depth

