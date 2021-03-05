import itertools
import numpy as np
import math
import random
from typing import List

from zquantum.core.bitstring_distribution import BitstringDistribution, save_bitstring_distribution

def get_bars_and_stripes_target_distribution(nrows, ncols, fraction=1., method="zigzag"):
    ''' Generates bars and stripes (BAS) data in zigzag pattern
    Args: 
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset 
        fraction (float): maximum fraction of patterns to include (at least one pattern will always be included)
        method (string): the method to use to label the qubits
    Returns: 
        Array of list of BAS pattern. 
    '''
    if method == "zigzag":
        print("^"*1000)
        print("calling ip_dataset with nrows", nrows)
        data = ip_dataset(nrows, ncols)
        print(data)
        #data = bars_and_stripes_zigzag(nrows, ncols)
        print("^"*1000)
    else:
        raise RuntimeError("Method: {} is not supported for generated a target distribution for bars and stripes".format(method))

    # Remove patterns until left with a subset that has cardinality less than or equal to the percentage * total number of patterns
    num_desired_patterns = int(len(data) * fraction)
    num_desired_patterns = max(num_desired_patterns, 1)
    data = random.sample(list(data), num_desired_patterns)

    distribution_dict = {}
    for pattern in data: 
        bitstring = ""
        for qubit in pattern:
            bitstring += str(qubit)

        distribution_dict[bitstring] = 1.
    print("*"*1000)
    print(distribution_dict)
    print("*"*1000)

    save_bitstring_distribution(BitstringDistribution(distribution_dict), "distribution.json")


# Generate BAS with specified rows and columns in zigzag pattern (taken from Vicente's code, would be careful about ownership of code)
def bars_and_stripes_zigzag(nrows, ncols):
    ''' Generates bars and stripes data in zigzag pattern
    Args: 
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset
    Returns: 
        Array of list of BAS pattern. 
    '''

    data = [] 
    
    for h in itertools.product([0,1], repeat=ncols):
        pic = np.repeat([h], nrows, 0)
        data.append(pic.ravel().tolist())
          
    for h in itertools.product([0,1], repeat=nrows):
        pic = np.repeat([h], ncols, 1)
        data.append(pic.ravel().tolist())
    
    data = np.unique(np.asarray(data), axis=0)
    return data

def ip_dataset(nrows, ncols):
    ''' Generates bars and stripes data in zigzag pattern
    Args: 
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset
    Returns: 
        Array of list of BAS pattern. 
    '''
    #data = [
    #    [0,1,0,1],
    #    [0,1,1,1],
    #    [1,0,1,0],
    #    [1,0,1,1],
    #    [1,1,0,1],
    #    [1,1,1,0],
    #]

    print("building IP dataset with nrows", nrows)
    data = IP(nrows)
    print(data)
    data = np.unique(np.asarray(data), axis=0)
    print(data)
    return data

def IP(n):
    n_2 = int(n/2)
    first_half = [dec_to_bin_array(i, n_2) for i in range(2**(n_2))]
    second_half = [dec_to_bin_array(i, n_2) for i in range(2**(n_2))]
    result = []
    for i in first_half:
        for j in second_half:
            if np.dot(i, j) % 2 == 1:
                result.append(np.concatenate([i, j]))
    print("IP: returning data with n", n)
    print(result)
    return result

def dec_to_bin_array(dec, num_digits = 4):
    result = [int(i) for i in bin(dec)[2:]]
    return [0]*(num_digits-len(result)) + result

def get_num_bars_and_stripes_patterns(nrows, ncols) -> int:
    ''' Get the number of bars and stripes patters for a 2-dimensional grid.
    Args:
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset 
    Returns: 
        (int): number of bars and stripes patterns
    '''
    # Always have all blank and all filled
    num_patterns = 2

    for dimension in [nrows, ncols]: 
        for num_choices in range(1, dimension):
            # nCr = n! / (n-r)! * r!
            num_patterns += math.factorial(dimension) // (math.factorial(dimension-num_choices) * math.factorial(num_choices))

    return num_patterns

#get_bars_and_stripes_target_distribution(6,6)
