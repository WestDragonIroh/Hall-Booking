import time

def elapsed_time(func):
    fname = func.__name__
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Elapsed time by", fname, 'is: ', end - start, '\n')
        return result
    return wrapper

def delay_time(func):
    def wrap(*args, **kwargs):
        val = 0
        time.sleep(val)
        result = func(*args, **kwargs)
        print("Added delay time: ", val)
        return result
    wrap.__name__ = func.__name__
    return wrap