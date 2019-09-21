"""
CSC148, Winter 2019
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import time
import datetime
from typing import List, Tuple
from call import Call
from customer import Customer


class Filter:
    """ A class for filtering customer data on some criterion. A filter is
    applied to a set of calls.

    This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data>, which match the filter
        specified in <filter_string>.

        The <filter_string> is provided by the user through the visual prompt,
        after selecting this filter.
        The <customers> is a list of all customers from the input dataset.

         If the filter has
        no effect or the <filter_string> is invalid then return the same calls
        from the <data> input.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        - all calls included in <data> are valid calls from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """
    A class for resetting all previously applied filters, if any.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Reset all of the applied filters. Return a List containing all the
        calls corresponding to <customers>.
        The <data> and <filter_string> arguments for this type of filter are
        ignored.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        """
        filtered_calls = []
        for c in customers:
            customer_history = c.get_history()
            # only take outgoing calls, we don't want to include calls twice
            filtered_calls.extend(customer_history[0])
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Reset all of the filters applied so far, if any"


class CustomerFilter(Filter):
    """
    A class for selecting only the calls from a given customer.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data> made or received by the
         customer with the id specified in <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains a valid
        customer ID.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """
        # Input checking
        cust_id = 0
        try:
            cust_id = int(filter_string)
        except ValueError:
            return data

        if cust_id not in [customer.get_id() for customer in customers]:
            return data
        else:
            pass

        # Filtered calls
        filtered_calls = []
        for c in customers:
            if c.get_id() == int(filter_string):
                filtered_calls.extend(c.get_history()[0])
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """
    A class for selecting only the calls lasting either over or under a
    specified duration.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data> with a duration of under or
        over the time indicated in the <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains the following
        input format: either "Lxxx" or "Gxxx", indicating to filter calls less
        than xxx or greater than xxx seconds, respectively.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """
        # Input checking
        seconds = 0
        try:
            specifier = filter_string[0]
            if specifier in ('L', 'G'):
                pass
            else:
                return data
        except IndexError:
            return data
        try:
            seconds = int(filter_string[1:])
            if seconds < 0:
                return data
        except ValueError:
            return data

        # Filtering
        filtered_calls = []
        for call in data:
            if call.duration < seconds and specifier == 'L':
                filtered_calls.append(call)
            elif call.duration > seconds and specifier == 'G':
                filtered_calls.append(call)
            else:
                pass
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls based on duration; " \
               "L### returns calls less than specified length, G### for greater"


class LocationFilter(Filter):
    """
    A class for selecting only the calls that took place within a specific area
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data>, which took place within
        a location specified by the <filter_string> (at least the source or the
        destination of the event was in the range of coordinates from the
        <filter_string>).

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains four valid
        coordinates within the map boundaries.
        These coordinates represent the location of the lower left corner
        and the upper right corner of the search location rectangle,
        as 2 pairs of longitude/latitude coordinates, each separated by
        a comma and a space:
          lowerLong, lowerLat, upperLong, upperLat
        Calls that fall exactly on the boundary of this rectangle are
        considered a match as well.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """
        # Map boundaries
        maxlower = [-79.697878, 43.576959]
        maxupper = [-79.196382, 43.799568]

        # test input = -79.5, 43.63, -79.4, 43.67
        lowercoord = []
        uppercoord = []
        split_string = filter_string.split(',')
        if len(split_string) != 4:
            return data
        else:
            try:
                coordinates = [float(coord) for coord in split_string]
                lowercoord = [coordinates[0], coordinates[1]]
                uppercoord = [coordinates[2], coordinates[3]]
            except ValueError:
                return data

        if lowercoord < maxlower or uppercoord > maxupper:
            return data

        filtered_calls = []
        for call in data:
            src_coords = list(call.src_loc)
            dst_coords = list(call.dst_loc)
            if uppercoord >= src_coords >= lowercoord:
                filtered_calls.append(call)
            elif uppercoord >= dst_coords >= lowercoord:
                filtered_calls.append(call)
            else:
                pass
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls made or received in a given rectangular area. " \
               "Format: \"lowerLong, lowerLat, " \
               "upperLong, upperLat\" (e.g., -79.6, 43.6, -79.3, 43.7)"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'time', 'datetime', 'call', 'customer'
        ],
        'max-nested-blocks': 4,
        'allowed-io': ['apply', '__str__'],
        'disable': ['W0611', 'W0703'],
        'generated-members': 'pygame.*'
    })
