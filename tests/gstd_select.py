from .test_util import print_title, Test, MaxTestAttemptsReached
from lib.api import Canvas
import lib.gui as gui
import os
import random
import toml


def run():
    print_title(os.path.basename(__file__))

    test = Test(MAX_ATTEMPTS=10)
    test.set_rand_course_id()
    test.set_grade_standards()
    grade_scale = gui.grade_standard_selection(test.gstds)
    print(f'--------------\ngrade_standard\n--------------\n{grade_scale}')

    print('passed\n')


if __name__ == '__main__':
    run()
