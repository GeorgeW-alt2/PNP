import multiprocessing
import itertools

# Function that checks if a subset sums to the target
def subset_sum_worker(subset, target):
    for comb in subset:
        if sum(comb) == target:
            return comb
    return None

# Function to divide the subsets among processes
def distributed_subset_sum(arr, target, num_workers=4):
    # Generate all possible subsets
    all_subsets = []
    for i in range(len(arr) + 1):
        all_subsets.extend(itertools.combinations(arr, i))
    
    # Split the subsets into chunks for each worker
    chunk_size = len(all_subsets) // num_workers
    chunks = [all_subsets[i:i + chunk_size] for i in range(0, len(all_subsets), chunk_size)]

    # Create a pool of workers
    pool = multiprocessing.Pool(processes=num_workers)

    # Run workers on the chunks
    results = pool.starmap(subset_sum_worker, [(chunk, target) for chunk in chunks])

    # Close the pool and wait for all workers to finish
    pool.close()
    pool.join()

    # Check results from each worker
    for result in results:
        if result is not None:
            return result

    return None

if __name__ == "__main__":
    # Example set and target
    arr = [3, 34, 4, 12, 5, 2]
    target = 9

    # Number of workers (processes) to use
    num_workers = multiprocessing.cpu_count()

    result = distributed_subset_sum(arr, target, num_workers)
    
    if result:
        print(f"Subset that sums to {target}: {result}")
    else:
        print(f"No subset found that sums to {target}")
