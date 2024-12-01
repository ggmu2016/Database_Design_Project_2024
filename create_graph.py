import matplotlib.pyplot as plt
from queries import time_queries

def create_scatterplot(times):
    """
    Creates a scatterplot for the given array of times.

    Parameters:
    times (list of float): Array of times it takes a function to complete.

    Returns:
    None
    """
    plt.scatter(range(len(times)), times)
    plt.title('Query Completion Times')
    plt.xlabel('Query Number')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.show()

times = time_queries()
create_scatterplot(times)