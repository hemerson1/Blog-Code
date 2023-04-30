"""
Painter's Partition - paint n boards of length {A1, A2, …, An}. 
k painters are available and each takes 1 unit of time to paint 1 unit of the board.
What is the minimum time given painters only paint continuous board segments e.g. {2, 3, 4}? 
"""

import time
     
def partition(arr, n, k):
    """Get the minimum partition sum"""
     
    # if only one painter
    if k == 1: 
        return sum(arr[0:n])
    
    # if only a single board
    if n == 1: 
        return arr[0]
     
    best = 1e5
    for i in range(1, n + 1):

        # calculate sum of new and all previous partitions
        right_part_sum = sum(arr[i:n])
        left_part_sum = partition(arr, i, k-1)

        # select the minimum painter combination
        best = min(best, max(left_part_sum, right_part_sum))

    return best


def dynamic_partition(arr, n, k):
    """Optimise minimum partition sum with dynamic programming."""

    # create table for storing values
    saved_values = [[0 for i in range(n+1)] for j in range(k+1)]

    # if only one painter (set partition values to cumulative sum)
    for i in range(1, n + 1):
        saved_values[1][i] = sum(arr[0:i])
 
    # if only a single board (set painter number to board sum)
    for j in range(1, k + 1):
        saved_values[j][1] = arr[0]

    # iteratively span greater num of boards and painters
    # select the minimum greatest sum of each partition
    # use prior partitions to calculate future partitions
    # storing values in the table
    for i in range(2, n+1): # boards
        for j in range(2, k+1): # painters
            best = 1e5
            for l in range(1, i+1):
                right_part_sum = sum(arr[l:i])
                left_part_sum = saved_values[j-1][l]
                best = min(best, max(left_part_sum, right_part_sum))            
            saved_values[j][i] = best

    return saved_values[k][n]


def timing_wrapper(func):
    """Time function execution"""

    def wrapped_func(*args, **kwargs):
        tic = time.perf_counter()
        output = func(*args, **kwargs)
        toc = time.perf_counter()
        return output, (toc-tic)

    return wrapped_func


if __name__ == "__main__":

    # list [answer, [num_painters, board orientation]]
    test_samples = [
        [20 , [3, [10, 10, 10, 10]]],
        [20, [2, [10, 10, 10, 10]]],
        [60, [2, [10, 20, 30, 40]]],
        [90, [3, [10, 20, 60, 50, 30, 40]]]
    ]

    # initialise function
    painter = timing_wrapper(partition) 
    painter_dyn = timing_wrapper(dynamic_partition) 

    # visualise solution
    for sample in test_samples:

        # unpack samples
        arr = sample[1][1]
        k = sample[1][0]
        n = len(sample[1][1])
        answer = sample[0]

        # test recursive
        algo_answer, algo_time = painter(arr, n, k)
        is_correct = (algo_answer == int(answer))
        print(f'RECURSIVE | Time: {algo_time:.5e} | Answer: {algo_answer:<3} | {is_correct}')

        # test dynamic
        algo_answer, algo_time = painter_dyn(arr, n, k)
        is_correct = (algo_answer == int(answer))
        print(f'DYNAMIC   | Time: {algo_time:.5e} | Answer: {algo_answer:<3} | {is_correct}')




