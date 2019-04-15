#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from typing import List

from permission_resolver import TreeItem, build_writable_folders_tree


def get_leafs(tree: TreeItem) -> List[str]:
    leafs = []
    for child in tree.children:
        leafs += get_leafs(child)
    if not leafs:
        leafs = [tree.name]
    return sorted(leafs)


class TestPermissionResolver(unittest.TestCase):

    @unittest.expectedFailure
    def test_incorrect_system(self):
        build_writable_folders_tree([], [], system='fail')

    def test_posix_path_not_empty(self) -> None:
        readable = ['/var', '/var/log/', '/var/log/my application', '/var/log/my application/b/v']
        writable = ['/var/log/resolver', '/usr/secret/folder', '/var/log/my application/b']
        self.assertEqual(['b', 'resolver'], get_leafs(build_writable_folders_tree(readable, writable)))

    def test_posix_path_not_empty_with_skipped_level(self) -> None:
        readable = ['/var', '/var/log', "var/log/my application", '/var/log/', '/var/log/my application/b/v']
        writable = ['/var/log/resolver', '/usr/secret/folder', '/var/log/my application/b']
        self.assertEqual(['resolver'], get_leafs(build_writable_folders_tree(readable, writable)))

    def test_windows_path_not_empty(self) -> None:
        readable = ['d:\\var', 'd:\\var\\log', 'd:\\var\\log\\application']
        writable = ['d:\\var\\log\\one', 'c:\\var\\log\\application']
        self.assertEqual(['one'], get_leafs(build_writable_folders_tree(readable, writable, system='windows')))

    def test_windows_path_two_disks(self) -> None:
        readable = ['d:\\var', 'd:\\var\\log', 'd:\\var\\log\\application', 'c:\\app']
        writable = ['d:\\var\\log\\one', 'c:\\app\\my x']
        self.assertEqual(['my x', 'one'], get_leafs(build_writable_folders_tree(readable, writable, system='windows')))

    def test_path_only_writable(self) -> None:
        readable = []
        writable = ['/var', '/var/log', '/var/log/resolver', '/usr/secret/folder', '/var/log/application/b']
        self.assertEqual(['resolver'], get_leafs(build_writable_folders_tree(readable, writable)))

    def test_posix_path_empty(self) -> None:
        readable = ['/usr', '/var/log', '/var/log/application']
        writable = ['/var/log/resolver', '/usr/secret/folder', '/var/log/application/b']
        self.assertEqual([''], get_leafs(build_writable_folders_tree(readable, writable)))

    def test_windows_path_empty(self) -> None:
        readable = ['d:\\var', 'd:\\var\\log', 'd:\\var\\log\\application']
        writable = ['c:\\var\\log\\application']
        self.assertEqual([''], get_leafs(build_writable_folders_tree(readable, writable, system='windows')))

    def test_readable_empty(self) -> None:
        readable = []
        writable = ['/var/log/resolver', '/usr/secret/folder', '/var/log/application/b']
        self.assertEqual([''], get_leafs(build_writable_folders_tree(readable, writable)))

    def test_all_empty(self) -> None:
        readable = []
        writable = []
        self.assertEqual([''], get_leafs(build_writable_folders_tree(readable, writable)))


if __name__ == '__main__':
    unittest.main()
