import functools
import time

def time_profile(logger):
    def concrete_decorator(function):
        @functools.wraps(function)
        def wrapped(*args, **kw):
            start_time = time.time()
            result = function(*args, **kw)
            end_time = time.time()
            logger.info(f"{function.__name__}, time lapsed {end_time - start_time} seconds")
            return result
        return wrapped
    return concrete_decorator