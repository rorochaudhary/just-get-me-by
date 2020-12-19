from .test_util import print_title, Test, MaxTestAttemptsReached
from lib.algo.algo import calculate_min_grades
from lib.api.api import Canvas
import lib.gui.gui as gui
import os
import random
import re
import toml


def run():
    print_title(os.path.basename(__file__))

    # Set up data.
    test = Test(MAX_ATTEMPTS=10)
    test.set_rand_course_id()
    test.set_assignments()
    test.set_assignment_groups()

    assignment_dict = {}
    group_dict = {}
    gui.get_assignments_and_groups(
        test.assignments, assignment_dict, test.assignment_grps, group_dict
    )
    print(calculate_min_grades(-1, assignment_dict, group_dict))
    print(calculate_min_grades(0, assignment_dict, group_dict))
    print(calculate_min_grades(50, assignment_dict, group_dict))
    print(calculate_min_grades(80, assignment_dict, group_dict))
    print(calculate_min_grades(90, assignment_dict, group_dict))
    print(calculate_min_grades(95, assignment_dict, group_dict))
    print(calculate_min_grades(100, assignment_dict, group_dict))
    print(calculate_min_grades(105, assignment_dict, group_dict))

    print('passed\n')

if __name__ == '__main__':
    run()
