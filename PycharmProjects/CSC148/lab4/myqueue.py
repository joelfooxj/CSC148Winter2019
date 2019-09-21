"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will develop an implementation of the Queue ADT.
It will be helpful to review the stack implementation from lecture.

After you've implemented the Queue, you'll write two different functions that
operate on a queue, paying attention to whether or not the queue should be
modified.
"""
from typing import Any, List, Optional


# TODO: implement this class! Note that you'll need at least one private
# attribute to store items.
class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.
    """

    # -> Description of class
    # -> Private Attributes
    # -> Representational invariants
    # -> type list

    # Private Attributes
    # _items is a List of items in the stack

    _items: List[Any]

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """

        return not bool(self._items)

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """

        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """

        return self._items.pop(0)


def product(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Remove all items from the queue.

    Precondition: integer_queue contains only integers.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    q = integer_queue
    if q.is_empty():
        raise Exception('Integer queue is empty')
    else:
        num = 1
        while not q.is_empty():
            num *= q.dequeue()
        return num


def product_star(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Precondition: integer_queue contains only integers.

    >>> primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> prime_line = Queue()
    >>> for prime in primes:
    ...     prime_line.enqueue(prime)
    ...
    >>> product_star(prime_line)
    6469693230
    >>> prime_line.is_empty()
    False
    """

    q = integer_queue
    new_q = Queue()
    if q.is_empty():
        raise Exception('Integer queue is empty')
    else:
        num = 1
        while not q.is_empty():
            temp_var = q.dequeue()
            num *= temp_var
            new_q.enqueue(temp_var)
        while not new_q.is_empty():
            q.enqueue(new_q.dequeue())
        return num


if __name__ == '__main__':
    import doctest
    doctest.testmod()
