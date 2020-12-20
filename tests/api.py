from .test_util import print_title
from lib.api import Canvas
import os
import random
import toml


def run():
    print_title(os.path.basename(__file__))

    # Feed url and token into Canvas API.
    my_token = toml.load('config/config.toml')['secret']['manual_token']
    canvas = Canvas('https://canvas.oregonstate.edu', my_token)

    print("---Courses---")
    courses = canvas.get_courses()
    for course in courses:
        print(
            f"id: {course['id']}\n"
            f"name: {course['name']}\n"
        )
    print('')

    # Get random course id.
    random.seed()
    rand_course_id = courses[random.randrange(len(courses))]['id']

    # print("---Assignments---")
    assignments = canvas.get_assignments_in_course(rand_course_id)
    # print(assignments)

    print("---Ungraded assignments---")
    print(canvas.get_assignments_in_course(
        rand_course_id,
        # refer to https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index for more info on what params/args we could pass
        params={
            'include': ['submission'],  # includes score
            'bucket': 'ungraded',
            'order_by': 'due_at',  # possible values are position, name, and due_at
        }
    ))
    print('\n')

    print("---Assignments---")
    for assignment in assignments:
        print(
            f"name: {assignment['name']}\n"
            f"id: {assignment['id']}\n"
            f"assignment_group_id: {assignment['assignment_group_id']}\n"
            f"points_possible: {assignment['points_possible']}\n"
            # grade for int, score for float
            #f"grade: {assignment['submission']['grade']}\n"
            #f"score: {assignment['submission']['score']}\n"
        )
    print('')

    print("---Assignment Groups---")
    for assignment_group in canvas.get_assignment_groups_in_course(rand_course_id):
        print(
            f"name: {assignment_group['name']}\n"
            f"id: {assignment_group['id']}\n"
            f"group_weight: {assignment_group['group_weight']}\n"
        )
    print('')

    print("---Grading Standard---")
    for gs in canvas.get_grading_standard_in_course(rand_course_id):
        print(
            f"id: {gs['id']}\n"
            f"title: {gs['title']}\n"
            f"grading_scheme: {gs['grading_scheme']}\n"
        )
    print('')

    print('passed\n')


if __name__ == '__main__':
    run()
