from lib.api.api import Canvas
import re

# # Regex test
# re_test_str = '''<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="current",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="next",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=1&per_page=10>; rel="first",<https://canvas.oregonstate.edu/api/v1/courses/1784184/assignments?include=submission&page=2&per_page=10>; rel="last"'''
# pattern = '<([^>]+)>; rel="next"'
# print(re.search(pattern, re_test_str).group(1))

# # Canvas API test
test = Canvas('config/config.toml')

# print("---Courses---")
# print(test.get_courses())

# print("---Assignments---")
# print(test.get_assignments_in_course(1784184))

print("---Ungraded assignments---")
print(test.get_assignments_in_course(
    1784184,
    # refer to https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index for more info on what params/args we could pass
    params={
        'include': ['submission'],  # includes score
        'bucket': 'ungraded',
        'order_by': 'due_at',  # possible values are position, name, and due_at
    }
))

print("---Assignments---")
for assignment in test.get_assignments_in_course(1784184):
    print(
        f"name: {assignment['name']}\n"
        f"id: {assignment['id']}\n"
        f"assignment_group_id: {assignment['assignment_group_id']}\n"
        f"points_possible: {assignment['points_possible']}\n"
        # grade for int, score for float
        f"grade: {assignment['submission']['grade']}\n"
        f"score: {assignment['submission']['score']}\n\n"
    )

print("---Assignment Groups---")
for assignment_group in test.get_assignment_groups_in_course(1784184):
    print(
        f"name: {assignment_group['name']}\n"
        f"id: {assignment_group['id']}\n"
        f"group_weight: {assignment_group['group_weight']}\n\n"
    )

# Looks like there can be more than one per class??
print("---Grading Standard---")
for gs in test.get_grading_standard_in_course(1784184):
    print(
        f"id: {gs['id']}\n"
        f"title: {gs['title']}\n"
        f"grading_scheme: {gs['grading_scheme']}\n"
    )
print('')
