from multiprocessing import Pool
import walkscore as wlk

# multiprocessing pool object
pool = Pool()

# input list
inputs = [0,1,2,3,4,5,6,7,8,9,10]

# map the function to the list and pass
# function and input list as arguments
pool.map(wlk.walkscore_function, inputs)