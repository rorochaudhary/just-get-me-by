from lib.api.api import Canvas
import re
import toml
from lib.algo.algo import algo

# # Regex test
# re_test_str = '''<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="current",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="next",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="first",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="last"'''
# pattern = '<([^>]+)>; rel="next"'
# print(re.search(pattern, re_test_str).group(1))

# # Canvas API test
my_token = toml.load('config/config.toml')['secret']['manual_token']
test = Canvas('https://canvas.oregonstate.edu', my_token)

# print("---Courses---")
# for course in test.get_courses():
    # print(
        # f"id: {course['id']}\n"
        # f"name: {course['name']}\n"
    # )
# print('')

COURSE_ID = 1784009

# print("---Assignments---")
# print(test.get_assignments_in_course(COURSE_ID))

# print("---Ungraded assignments---")
# print(test.get_assignments_in_course(
#     COURSE_ID,
#     # refer to https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index for more info on what params/args we could pass
#     params={
#         'include': ['submission'],  # includes score
#         'bucket': 'ungraded',
#         'order_by': 'due_at',  # possible values are position, name, and due_at
#     }
# ))
# print('\n')

# print("---Assignments---")
# for assignment in test.get_assignments_in_course(COURSE_ID):
#     print(
#         f"name: {assignment['name']}\n"
#         f"id: {assignment['id']}\n"
#         f"assignment_group_id: {assignment['assignment_group_id']}\n"
#         f"points_possible: {assignment['points_possible']}\n"
#         # grade for int, score for float
#         #f"grade: {assignment['submission']['grade']}\n"
#         #f"score: {assignment['submission']['score']}\n"
#     )
# print('')

# print("---Assignment Groups---")
# for assignment_group in test.get_assignment_groups_in_course(COURSE_ID):
#     print(
#         f"name: {assignment_group['name']}\n"
#         f"id: {assignment_group['id']}\n"
#         f"group_weight: {assignment_group['group_weight']}\n"
#     )
# print('')

# # Looks like there can be more than one per class??
# print("---Grading Standard---")
# for gs in test.get_grading_standard_in_course(COURSE_ID):
#     print(
#         f"id: {gs['id']}\n"
#         f"title: {gs['title']}\n"
#         f"grading_scheme: {gs['grading_scheme']}\n"
#     )
# print('')


def calculate_grades(target_grade, course_id) -> dict:
    assignment_dict = {}
    group_dict = {}
    assignment_data = test.get_assignments_in_course(course_id)
    group_data = test.get_assignment_groups_in_course(course_id)

    #creates a dict holding group ids: 'group_id': [group_weight]
    for group in group_data:
        assignment_list = []
        assignment_list.append(group['group_weight'])
        group_dict[group['id']] = assignment_list

    #creates a dict holding assigenment_data: 'name': [score, max_score]
    #appends assignment names to the dict holding group ids
    for assignment in assignment_data:
        data_list = []
        data_list.append(assignment['submission']['score'])
        data_list.append(assignment['points_possible'])
        assignment_dict[assignment['name']] = data_list

        #append assignment to group
        group_dict[assignment['assignment_group_id']].append(assignment['name'])

    #uses the grade algorithm
    return algo(target_grade, assignment_data, group_data)