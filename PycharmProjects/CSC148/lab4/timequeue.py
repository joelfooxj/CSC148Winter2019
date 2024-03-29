"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module runs timing experiments to determine how the time taken
to enqueue or dequeue grows as the queue size grows.
"""
from timeit import timeit
from typing import List, Tuple

from myqueue import Queue
import matplotlib.pyplot as plt


###############################################################################
# Task 3: Running timing experiments
###############################################################################
# TODO: implement this function
def _setup_queues(qsize: int, n: int) -> List[Queue]:
    """Return a list of <n> queues, each of the given size."""
    # Experiment preparation: make a list containing <n> queues,
    # each of size <qsize>.
    # You can "cheat" here and set your queue's _items attribute directly
    # to a list of the appropriate size by writing something like
    #
    #     queue._items = list(range(qsize))
    #
    # to save a bit of time in setting up the experiment.

    q_list = []
    for i in range(n):
        new_q = Queue()
        new_q._items = list(range(qsize))
        q_list.append(new_q)
    return q_list


def time_queue() -> None:
    """Run timing experiments for Queue.enqueue and Queue.dequeue."""
    # The queue sizes to try.
    queue_sizes = [10000, 20000, 40000, 80000, 160000]

    # The number of times to call a single enqueue or dequeue operation.
    trials = 200

    # This loop runs the timing experiment. Its three steps are:
    #   1. Initialize the sample queues.
    #   2. For each one, calling the function "timeit", takes three arguments:
    #        - a *string* representation of a piece of code to run
    #        - the number of times to run it (just 1 for us)
    #        - globals is a technical argument that you DON'T need to care about
    #   3. Report the total time taken to do an enqueue on each queue.
    for queue_size in queue_sizes:
        queues = _setup_queues(queue_size, trials)
        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1, globals=locals())
        print(f'enqueue: Queue size {queue_size:>7}, time {time}')

    # TODO: using the above loop as an analogy, write a second timing
    # experiment here that runs dequeue on the given queues, and reports the
    # time taken. Note that you can reuse most of the same code.
    for queue_size in queue_sizes:
        queues = _setup_queues(queue_size, trials)
        time = 0
        for queue in queues:
            time += timeit('queue.dequeue()', number=1, globals=locals())
        print(f'dequeue: Queue size {queue_size:>7}, time {time}')


# TODO: implement this function
def time_queue_lists() -> Tuple[List[int], List[float], List[float]]:
    """Run timing experiments for Queue.enqueue and Queue.dequeue.

    Return lists storing the results of the experiments.  See the lab
    handout for further details.
    """

    print('Queue list running')

    # The queue sizes to try.
    queue_sizes = [10000, 20000, 40000, 80000, 160000]

    # The number of times to call a single enqueue or dequeue operation.
    trials = 200
    en_timelist = []
    de_timelist = []
    for queue_size in queue_sizes:
        queues = _setup_queues(queue_size, trials)

        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1, globals=locals())
        en_timelist.append(time)
        time = 0
        for queue in queues:
            time += timeit('queue.dequeue()', number=1, globals=locals())
        de_timelist.append(time)
    return (queue_sizes, en_timelist, de_timelist)


if __name__ == '__main__':
    # time_queue()
    size, en_list, de_list = time_queue_lists()
    # red dashes, blue squares and green triangles
    plt.plot(size, en_list, size, de_list)
    plt.show()