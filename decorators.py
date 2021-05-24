from typing import Callable
import time
from random import random


def calc_duration(func: Callable) -> Callable:
    def wrapper():
        start = time.perf_counter()
        func()
        stop = time.perf_counter()
        print("elapsed time is about <>  seconds ", stop - start)
    return wrapper


@calc_duration
def long_executing_task():
    for index in range(3):
        print('Iteration ', index)
        time.sleep(random())


def suppress_errors(skip_err: list) -> Callable:
    def outer_wrapper(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except skip_err:
                return 'error is silented'
        return wrapper
    return outer_wrapper


@suppress_errors((
    KeyError,
    ValueError,
))
def potentially_unsafe_func(key: str):
    print(f'Get data by the key {key}')
    data = {'name': 'test', 'age': 30}
    return data[key]


def result_between(value_min, value_max):
    def outer_wrapper(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if not value_min < res < value_max:
                raise ValueError
            return res
        return wrapper
    return outer_wrapper


def len_more_than(s_len):
    def outer_wrapper(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if len(res) < s_len:
                raise ValueError
            return res
        return wrapper
    return outer_wrapper


@result_between(0, 10)
def sum_of_values(numbers):
    return sum(numbers)


@len_more_than(20)
def show_message(message: str) -> str:
    return f'Hi, you sent: {message}'


def replace_commas(func):
    def wrapper(*args, **kwargs):
        res = list(func(*args, **kwargs))
        for i in range(len(res) - 1):
            if res[i] in ',./:;':
                res[i] = ' '
        return ''.join(res)
    return wrapper


def capitalize(s):
    if len(s) > 1:
        return ''.join([s[:1].capitalize(), s[1:-1], (s[-1:].capitalize())])
    return s.capitalize()


def words_title(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs).split(" ")
        for i in range(len(res)):
            res[i] = capitalize(res[i])
        return ' '.join(res)
    return wrapper


@words_title
@replace_commas
def process_text(text: str) -> str:
    return text.replace(':', ',')


@replace_commas
@words_title
def another_process(text: str) -> str:
    return text.replace(':', ',')

def cache_result(func: Callable) -> Callable:
    cache = {}

    def decorated(*args, **kwargs):
        key = args.__str__() + kwargs.__str__()
        if key in cache:
            print("cache:")
            return cache[key]
        res = func(*args, **kwargs)
        cache[key] = res
        return res
    return decorated


@cache_result
def some_func(last_name, first_name, age):
    return f'Hi {last_name} {first_name}, you are {age} years old'


if __name__ == "__main__":
    print(some_func('shulyak', 'dmitry', 30))  # call
    print(some_func('ivanov', 'ivan', 25))  # call
    print(some_func('shulyak', 'dmitry', 30))  # cache
