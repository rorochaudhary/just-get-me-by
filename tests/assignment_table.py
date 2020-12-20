from .test_util import print_title, Test, MaxTestAttemptsReached
import lib.gui as gui
import lib.util as util
import PySimpleGUI as sg
import os


def run():
    print_title(os.path.basename(__file__))

    test = Test(MAX_ATTEMPTS=10)
    try:
        test.set_rand_grade_standard()
    except MaxTestAttemptsReached:
        return
    test.set_assignments()
    test.set_assignment_groups()
    assignment_dict = {}
    group_dict = {}
    gui.get_assignments_and_groups(test.assignments, assignment_dict, test.assignment_grps, group_dict)
    layout = gui.get_assign_table_layout(assignment_dict)
    window = sg.Window('Current Assignments', layout)
    event, values = window.read()

    print('passed\n')


if __name__ == '__main__':
    run()
