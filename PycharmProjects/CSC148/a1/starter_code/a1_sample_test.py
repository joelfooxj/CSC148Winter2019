
from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists

from application import *
from data import tiny_data

# def test_len_empty() -> None:
#     """Test LinkedList.__len__ for an empty linked list."""
#     lst = LinkedList()
#     assert len(lst) == 0
#
#
# def test_len_three() -> None:
#     """Test LinkedList.__len__ on a linked list of length 3."""
#     lst = LinkedList()
#     node1 = _Node(10)
#     node2 = _Node(20)
#     node3 = _Node(30)
#     node1.next = node2
#     node2.next = node3
#     lst._first = node1
#
#     assert len(lst) == 3
#
#
# def test_contains_doctest() -> None:
#     """Test LinkedList.__contains__ on the given doctest."""
#     lst = LinkedList()
#     node1 = _Node(1)
#     node2 = _Node(2)
#     node3 = _Node(3)
#     node1.next = node2
#     node2.next = node3
#     lst._first = node1
#
#     assert 2 in lst
#     assert not (4 in lst)


def test_something() -> None:
    customer_list = create_customers(tiny_data)
    process_event_history(tiny_data, customer_list)
    print('complete')



if __name__ == '__main__':
    import pytest
    pytest.main(['a1_sample_test.py'])
