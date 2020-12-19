from .test_util import print_title, Test, MaxTestAttemptsReached
from lib.api.api import Canvas
import os
import random
import re
import toml
from lib.algo.algo import algo


def run():
    print_title(os.path.basename(__file__))

    # Set up data.
    test = Test(MAX_ATTEMPTS=10)
    test.set_rand_course_id()
    test.set_assignments()
    test.set_assignment_groups()

    def calculate_grades(target_grade, assignment_data, group_data) -> dict:
        assignment_dict = {}
        group_dict = {}

        #creates a dict holding group ids: 'group_id': [group_weight]
        for group in group_data:
            assignment_list = []
            assignment_list.append(group['group_weight'])
            group_dict[group['id']] = assignment_list

        #creates a dict holding assigenment_data: 'name': [score, max_score]
        #appends assignment names to the dict holding group ids
        for assignment in assignment_data:
            data_list = []
            try:
                data_list.append(assignment['submission']['score'])
            except KeyError:
                data_list.append(None)
            finally:
                data_list.append(assignment['points_possible'])
                assignment_dict[assignment['name']] = data_list

                # append assignment to group
                group_dict[assignment['assignment_group_id']].append(assignment['name'])

        #uses the grade algorithm
        return algo(target_grade, assignment_dict, group_dict)

    print(calculate_grades(93, test.assignments, test.assignment_grps))

    print('passed\n')

if __name__ == '__main__':
    run()
