import sys
import pandas as pd 
import numpy as np
from simulate import sample_size_calculator as sp 

def run():

    pd.set_option('display.max_rows', 1000)
    
    init = sp(
        p1 = np.float(sys.argv[1]),
        min_size = np.float(sys.argv[2]),
        max_size = np.float(sys.argv[3]),
        volume = np.float(sys.argv[4])
    )
    print(init.simulate())

if __name__ == "__main__":
    run()