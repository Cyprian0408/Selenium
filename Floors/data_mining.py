import scr as scr
import multiprocessing
import time


# multiprocessing pool object
pool = multiprocessing.Pool()

# pool object with number of element
pool = multiprocessing.Pool(processes=11)

# input list
inputs = [0,6]

# map the function to the list and pass
# function and input list as arguments
outputs = pool.map(scr.web_scraping, inputs)
