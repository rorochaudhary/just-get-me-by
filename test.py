from lib.algo.algo import algo
from lib.api.api import Canvas
import tests.gstd_select
import re
import toml

# GUI test
tests.gs_select.run()

# # Canvas API test
# my_token = toml.load('config/config.toml')['secret']['manual_token']
# canvas = Canvas('https://canvas.oregonstate.edu', my_token)

# COURSE_ID = 1784009

# def calculate_grades(target_grade, course_id) -> dict:
#     assignment_dict = {}
#     group_dict = {}
#     assignment_data = canvas.get_assignments_in_course(course_id)
#     group_data = canvas.get_assignment_groups_in_course(course_id)

#     #creates a dict holding group ids: 'group_id': [group_weight]
#     for group in group_data:
#         assignment_list = []
#         assignment_list.append(group['group_weight'])
#         group_dict[group['id']] = assignment_list

#     #creates a dict holding assigenment_data: 'name': [score, max_score]
#     #appends assignment names to the dict holding group ids
#     for assignment in assignment_data:
#         data_list = []
#         data_list.append(assignment['submission']['score'])
#         data_list.append(assignment['points_possible'])
#         assignment_dict[assignment['name']] = data_list

#         #append assignment to group
#         group_dict[assignment['assignment_group_id']].append(assignment['name'])

#     #uses the grade algorithm
#     return algo(target_grade, assignment_dict, group_dict)


# print(calculate_grades(93, COURSE_ID))
