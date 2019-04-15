#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import TextIOWrapper
from pathlib import PureWindowsPath, PurePosixPath
from typing import List, Union
import argparse


class TreeItem:
    def __init__(self, name: str,
                 readable: bool = False,
                 writable: bool = False) -> None:
        """
        Tree structure with folder name and children sub-folders
        :param name: folder name
        :param readable: set to True if folder is readable
        :param writable: set to True if folder is writable (it will also set readable flag)
        """
        self._name = name
        self._writable = writable
        self._readable = readable
        self._children = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def writable(self) -> bool:
        return self._writable

    @property
    def readable(self) -> bool:
        return self._writable or self._readable

    @readable.setter
    def readable(self, value: bool) -> None:
        self._readable = value

    @writable.setter
    def writable(self, value: bool) -> None:
        self._writable = value

    @property
    def children(self) -> List['TreeItem']:
        """
        Children for the TreeItem
        :return: List of TreeItem children
        """
        return list(self._children.values())

    def add_child(self, child: 'TreeItem') -> 'TreeItem':
        """
        Add child to the children list, updated existing child if exists
        :param child: TreeItem child
        :return: TreeItem child added/updated in the list of children
        """
        key = child.name
        if key in self._children:
            self._children[key].update(child)
        else:
            self._children[key] = child
        return self._children[key]

    def remove_child(self, child: 'TreeItem') -> Union['TreeItem', None]:
        """
        Remove particular child from the list of children
        :param child: child to remove
        :return: TreeItem removed child or None if child is not in list of children
        """
        return self._children.pop(child.name, None)

    def __repr__(self, depth: int = 1) -> str:
        """
        String representation of the tree
        :param depth: depth level
        :return: textual representation of the tree
        """
        result = [self.name]
        depth += 1
        for child in self.children:
            result.extend(["\n", "  " * depth, child.__repr__(depth)])
        return "".join(result)

    def update(self, other: 'TreeItem') -> None:
        """
        Update current node with other node with the same name, from folder permissions those with wider access
        would be used, children list would be merged via add_child to the current node.
        :param other: TreeItem other node to merge with
        """
        if self.name != other.name:
            return
        self.readable = self.readable or other.readable
        self.writable = self.writable or other.writable
        for child in other.children:
            self.add_child(child)


def build_writable_folders_tree(readable_folders: List[str],
                                writable_folders: List[str],
                                system: str = 'posix') -> TreeItem:
    """
    Function builds tree with writable folders leafs (accessible from the root via at least readable ones),
    posix and windows like paths supported
    :param readable_folders: List of readable absolute paths
    :param writable_folders: List of writable absolute paths
    :param system: 'posix' or 'windows' - depending on absolute paths system
    :return: TreeItem with writable folders leafs (nodes could be readable or readable/writable)
    """
    system_flavour = {'posix': PurePosixPath, 'windows': PureWindowsPath}

    if system not in system_flavour:
        raise ValueError(f'System \'{system}\' is not supported, should be one of: {", ".join(system_flavour.keys())}')

    def populate_tree(folders: List[str], readable=False, writable=False) -> None:
        for folder in folders:
            path = system_flavour[system](folder)
            parents = list(reversed(path.parents))
            tree = root.add_child(TreeItem(parents[0].as_posix(), readable=True))
            for parent in parents[1:]:
                tree = tree.add_child(TreeItem(parent.name))
            tree.add_child(TreeItem(path.name, readable, writable))

    def keep_only_writable(tree: 'TreeItem') -> None:
        for child in tree.children:
            keep_only_writable(child)
            if not child.readable or (not child.children and not child.writable):
                tree.remove_child(child)

    root = TreeItem("")
    populate_tree(readable_folders, readable=True)
    populate_tree(writable_folders, writable=True)
    keep_only_writable(root)
    return root


def _read_files(files: List[TextIOWrapper]) -> List[str]:
    content = []
    for file in files:
        with file:
            content += [l.strip() for l in file.readlines()]
    return content


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Lists accessible for write folders.')
    parser.add_argument('-r', '--readable', required=True, nargs='*', type=argparse.FileType('r'),
                        help='Files with newline separated readable folders list')
    parser.add_argument('-w', '--writable', required=True, nargs='*', type=argparse.FileType('r'),
                        help='Files with newline separated writable folders list')
    parser.add_argument('-s', '--system', choices=['posix', 'windows'], nargs=1, type=str, default='posix',
                        help='Type of system paths (windows or posix)')
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    print(build_writable_folders_tree(_read_files(args.readable), _read_files(args.writable), args.system))


if __name__ == '__main__':
    main()
