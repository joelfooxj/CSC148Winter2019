"""Lab 7: Recapping -- Linked Lists

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

This is the same as the starter code from Lab 5, except that we've added some
new guidelines for supporting for-loop iteration at the bottom of this file.
"""
from __future__ import annotations

from typing import Any, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]
    _last: Optional[_Node]
    _length: int

    def __init__(self, items: list) -> None:
        """Initialize a new empty linked list containing the given items.

        Note: this is the inefficient version of the initializer from the
        lecture notes. Feel free to replace it with your own version from Lab 5!
        """
        self._length = 0
        self._first = None
        self._last = None
        for item in items:
            self.append(item)

    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        for i in self:
            items.append(str(i))
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        if index >= len(self):
            raise IndexError
        count = 0
        for item in self:
            if count == index:
                return item
            else:
                count += 1

    def append(self, item: Any) -> None:
        """Append <item> to the end of this list.

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        >>> lst.append(4)
        >>> str(lst)
        '[1 -> 2 -> 3 -> 4]'
        """
        if self._first is None:
            self._first = _Node(item)
        elif self._last is None:
            self._last = _Node(item)
            self._first.next = self._last
        else:
            newnode = _Node(item)
            self._last.next = newnode
            self._last = newnode
        self._length += 1

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
        else:
            # Iterate to (index-1)-th node.
            count = 0
            for node_item in self:
                if count == index:
                    pass
                else:
                    count += 1



            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next

    def __contains__(self, item):
        for node_item in self:
            if node_item == item:
                return True
        return False

    def count(self, item):
        """
        Return the number of times <item> occurs in the list


        """
        count = 0
        for node_item in self:
            if node_item == item:
                count += 1
        return count

    def index(self, item):
        """
        Return the index of the first occurance of <item> in the list

        """
        if item not in self:
            raise ValueError
        index = 0
        for node_item in self:
            if node_item == item:
                return index
            else:
                index += 1

    def __len__(self):
        return self._length

    # TODO: Implement this method!
    def __iter__(self) -> LinkedListIterator:
        """Return an iterator for this linked list.

        It should be straightforward to initialize the iterator here
        (see the class documentation below). Just remember to initialize
        it to the first node in this linked list.
        """
        return LinkedListIterator(self._first)


# TODO: Implement this class!
class LinkedListIterator:
    """An object responsible for iterating through a linked list.

    This enables linked lists to be used inside for loops!

    >>> lst = LinkedList([1, 2, 3])
    >>> for x in lst:
    ...     print(x)
    ...
    1
    2
    3
    """
    # === Private attributes ===
    # _curr:
    #   The current node for this iterator.
    #   This should start as the first node in a linked list,
    #   and update to the "next" node every time __next__ is called.
    _curr: Optional[_Node]

    def __init__(self, first_node: Optional[_Node]) -> None:
        """Initialize a new linked list iterator with the given node."""
        self._curr = first_node

    def __next__(self) -> Any:
        """Return the next item in the iteration.

        Raise StopIteration if there are no more items to return.

        Hint: If you have an attribute keeping track of the where the iteration
        is currently at in the list, it should be straight-forward to return
        the current item, and update the attribute to be the next node in
        the list.

        >>> lst = LinkedList([1, 2, 3])
        >>> iterator = lst.__iter__()
        >>> iterator.__next__()
        1
        >>> iterator.__next__()
        2
        >>> iterator.__next__()
        3
        """

        if not self._curr:
            raise StopIteration
        else:
            curr_item = self._curr.item
            curr = self._curr
            self._curr = curr.next
            return curr_item


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
