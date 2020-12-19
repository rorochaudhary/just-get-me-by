from .test_util import print_title, Test, MaxTestAttemptsReached
import os
import re


def run():
    print_title(os.path.basename(__file__))

    # Regex test for api get all pages
    re_test_str = '''<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="current",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="next",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="first",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="last"'''
    pattern = '<([^>]+)>; rel="next"'
    assert(re.search(pattern, re_test_str).group(1) == "https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10")

    # Regex test for protocol search
    re_test_str = '''https://canvas.oregonstate.edu'''
    pattern = '[^:]+://'
    assert(re.search(pattern, re_test_str) is not None)

    print('passed\n')


if __name__ == '__main__':
    run()
