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
import datetime
from typing import Optional, Tuple
from math import ceil
from bill import Bill
from call import Call

# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.datetime
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class MTMContract(Contract):
    """
    A month-to-month contract for a phoneline

    === Public Attributes ===
    start:
         Starting date for the contract
    bill:
         Bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.datetime
    bill: Optional[Bill]

    def __init__(self, start: datetime.datetime) -> None:
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("MTM", MTM_MINS_COST)
        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)


class TermContract(Contract):
    """
    A term contract for a phoneline

    === Public Attributes ===
    start:
         Starting date for the contract
    bill:
         Bill for this contract for the last month of call records loaded from
         the input dataset
    end_date:
        Termination/end date for the contract
    free_minutes:
        The number of free calling minutes for this contract
    current_date:
        The date of the latest month that is added

    === Private Attributes ===
    _term_deposit:
        The fixed deposit that is added to the first bill
        when the contract is first instantiated

    There are several conditions for this contract:
    - This contract has a start date and end date
    - A contract deposit is added to the initial month's bill
    - If cancel_contract is called before end date, the deposit is forfeited.
    - If cancel_contract is called after end date,
      the deposit is returned minus that month's bill
    - Free minutes are refreshed per month, with calls using all
      free minutes first before being billed

    === Representation invariants ===
    term_deposit >= 0
    start > current_date > end_date
    free_minutes > 0
    """
    start: datetime.datetime
    _term_deposit: float
    end_date: datetime.datetime
    free_minutes: int
    current_date: Tuple[int, int]
    bill: Optional[Bill]

    def __init__(self, start: datetime.datetime,
                 end: datetime.datetime) -> None:
        Contract.__init__(self, start)
        self._term_deposit = TERM_DEPOSIT
        self.end_date = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.current_date = (month, year)
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)
        if self.current_date == (self.start.month, self.start.year):
            self.bill.add_fixed_cost(self._term_deposit)
        else:
            pass
        self.free_minutes = TERM_MINS
        self.bill.free_min = 0
        self.bill.add_fixed_cost(TERM_MONTHLY_FEE)

    def bill_call(self, call: Call) -> None:
        call_mins = ceil(call.duration / 60.0)
        if self.free_minutes > call_mins:
            self.free_minutes -= call_mins
            self.bill.add_free_minutes(call_mins)
        else:
            call_mins -= self.free_minutes
            self.bill.add_billed_minutes(call_mins)

    def cancel_contract(self) -> float:
        if self.current_date > (self.end_date.month, self.end_date.year):
            self.bill.add_fixed_cost(-self._term_deposit)
        else:
            pass
        return self.bill.get_cost()


class PrepaidContract(Contract):
    """
    A pre-paid contract for a phoneline

    There are several conditions for this contract:
    - The contract is initialized with bill credits
    - Every month, if credit amount falls below 10,
      the contract will automatically add 25 credits
    - If contract contains negative credits, then
      cancelling the contract will bill the customer
      for these remaining credits

    === Public Attributes ===
    start:
         Starting date for the contract
    bill:
         Bill for this contract for the last month of call records loaded from
         the input dataset
    balance:
        The amount of credits that this contract has left.
    """

    start: datetime.datetime
    balance: float
    bill: Optional[Bill]

    def __init__(self, start: datetime.datetime, balance: float) -> None:
        Contract.__init__(self, start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        if self.balance > -10:
            self.balance += -25
        self.bill = bill
        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
        self.bill.add_fixed_cost(self.balance)

    def bill_call(self, call: Call) -> None:
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))
        self.balance = self.bill.get_cost()

    def cancel_contract(self) -> float:
        self.start = None
        if self.balance > 0:
            return self.balance
        else:
            return 0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
