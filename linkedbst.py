"""
File: linkedbst.py
Author: Ken Lambert
"""
import copy
import time
import timeit
import random

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from datetime import datetime
import sys
sys.setrecursionlimit(20000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while 1:
            if node is None:
                return None
            elif item == node.data:
                return item
            elif item < node.data:
                node = node.left
            else:
                node = node.right
    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def stack_find(base):
            while 1:
                if item < base.data:
                    if base.left == None:
                        base.left = BSTNode(item)
                        break
                    else:
                        base = base.left
                elif item >= base.data:
                    if base.right == None:
                        base.right = BSTNode(item)
                        break
                    else:
                        base = base.right

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            stack_find(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right == None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode == None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left == None \
                and not currentnode.right == None:
            liftMaxInLeftSubtreeToTop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left == None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def get_height(node):
            """
            hekp method for height
            """
            if node is None:
                return 0
            return max(get_height(node.left), get_height(node.right)) + 1

        return max(get_height(self._root) - 1, 0)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < (2 * log(len(self) + 1, 2) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        answer_list = list()
        for i in self.inorder():
            if low <= i <= high:
                answer_list.append(i)
        return answer_list

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build(numbers_list, start, end):
            if start <= end:
                mid = (start + end + 1) // 2
                self.add(numbers_list[mid])
                build(numbers_list, start, mid - 1)
                build(numbers_list, mid + 1, end)
        if not self.is_balanced():
            numbers_list = list(self.inorder())
            numbers_list.sort()
            self.clear()
            build(numbers_list, 0, len(numbers_list) - 1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(node, item):
            """
            help method
            """
            if node != None:
                recurse(node.left, item)
                recurse(node.right, item)
                if item < node.data:
                    answer_number[0] = node.data if answer_number[0] is None\
                        else min(node.data, answer_number[0])
        answer_number = [None]
        recurse(self._root, item)
        return answer_number[0]

    def predecessor(self, item):
        """*
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(node, item):
            """
            help method
            """
            if node != None:
                recurse(node.left, item)
                recurse(node.right, item)
                if item > node.data:
                    answer_number[0] = node.data if answer_number[0] is None \
                        else max(node.data, answer_number[0])
        answer_number = [None]
        recurse(self._root, item)
        return answer_number[0]

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def case1(data: list, random_words: list):
            for elem in random_words:
                for i in data:
                    if elem == i:
                        break

        def case2_3_4(data: LinkedBST, random_words: list):
            for elem in random_words:
                data.find(elem)

        data = []
        bin_ser_tree1 = LinkedBST()
        bin_ser_tree2 = LinkedBST()
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(line[:-1])
        random_data = copy.deepcopy(data)
        random.shuffle(random_data)
        random_words = random.sample(data, 10000)
        for elem in data:
            bin_ser_tree1.add(elem)
        for elem in random_data:
            bin_ser_tree2.add(elem)
        print("Case 1 time: ", timeit.timeit(lambda: case1(data, random_words), number=3))
        print("Case 2 time: ", timeit.timeit(lambda: case2_3_4(bin_ser_tree1, random_words), number=3))
        print("Case 3 time: ", timeit.timeit(lambda: case2_3_4(bin_ser_tree2, random_words), number=3))
        bin_ser_tree2.rebalance()
        print("Case 4 time: ", timeit.timeit(lambda: case2_3_4(bin_ser_tree2, random_words), number=1))

# if __name__ == '__main__':
#     a = LinkedBST()
