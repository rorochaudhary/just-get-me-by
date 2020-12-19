from .test_util import print_title, Test, MaxTestAttemptsReached
from lib.algo.algo import calculate_min_grades
from lib.api.api import Canvas
import lib.gui.gui as gui
import os
import random
import re
import toml
import traceback


def run():
    print_title(os.path.basename(__file__))

    test = Test(MAX_ATTEMPTS=10)
    for _ in range(5):
        # Set up data.
        test.set_rand_course_id()
        test.set_assignments()
        test.set_assignment_groups()
        assignment_dict = {}
        group_dict = {}
        gui.get_assignments_and_groups(
            test.assignments, assignment_dict, test.assignment_grps, group_dict
        )
        try:
            # print(calculate_min_grades(-1, assignment_dict, group_dict))
            # print(calculate_min_grades(0, assignment_dict, group_dict))
            # print(calculate_min_grades(50, assignment_dict, group_dict))
            # print(calculate_min_grades(80, assignment_dict, group_dict))
            print(calculate_min_grades(90, assignment_dict, group_dict))
            # print(calculate_min_grades(95, assignment_dict, group_dict))
            # print(calculate_min_grades(100, assignment_dict, group_dict))
            # print(calculate_min_grades(105, assignment_dict, group_dict))
            print('passed\n')
        except:
            traceback.print_exc()

            the_course_name = "not found?"
            for course in test.courses:
                if course['id'] == test.rand_course_id:
                    the_course_name = course['name']
            print(f"{13 * '-'}\nthe course id\n{13 * '-'}\n{test.rand_course_id}")
            print(f"{15 * '-'}\nthe course name\n{15 * '-'}\n{the_course_name}")
            print(f"{15 * '-'}\nassignment_dict\n{15 * '-'}\n{assignment_dict}")
            print(f"{10 * '-'}\ngroup_dict\n{10 * '-'}\n{group_dict}")


if __name__ == '__main__':
    run()
