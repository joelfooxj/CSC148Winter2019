"""Lab 6: Recursion

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union, List


def add_n(obj: Union[int, List], n: int) -> Union[int, List]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """

    if isinstance(obj, int):
        return obj + n
    else:
        for i in range(len(obj)):
            if isinstance(obj[i], int):
                obj[i] += n
            else:
                add_n(obj[i], n)
        return obj


def nested_list_equal(obj1: Union[int, List], obj2: Union[int, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    # HINT: You'll need to modify the basic pattern to loop over indexes,
    # so that you can iterate through both obj1 and obj2 in parallel.

    if type(obj1) != type(obj2):
        return False
    else:
        if isinstance(obj1, int):
            if obj1 == obj2:
                return True
            else:
                return False
        else:
            for i in range(len(obj1)):
                if not nested_list_equal(obj1[i], obj2[i]):
                    return False
                else:
                    pass
            return True


def duplicate(obj: Union[int, List]) -> Union[int, List]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    # HINT: in the recursive case, you'll need to distinguish between
    # a <sublist> that is an int and a <sublist> that is a list
    # (put an isinstance check inside the loop).

    newlist = []
    if isinstance(obj, int):
        return [obj, obj]
    else:
        for sublist in obj:
            # print('instance is of type: ' + str(type(sublist)))
            if isinstance(sublist, int):
                newlist.append(sublist)
                newlist.append(sublist)
            else:
                newlist.append(duplicate(sublist))
    return newlist


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all()
