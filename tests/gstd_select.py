from lib.api.api import Canvas
import lib.gui.gui as gui
import random
import toml


def run():
    # Feed url and token into the Canvas API.
    my_token = toml.load('config/config.toml')['secret']['manual_token']
    canvas = Canvas('https://canvas.oregonstate.edu', my_token)

    # Select a random course.
    random.seed()
    courses = canvas.get_courses()
    rand_course_id = courses[random.randrange(len(courses))]['id']

    # Open the grade selection.
    grade_standards = canvas.get_grading_standard_in_course(rand_course_id)
    grade_scale = gui.grade_standard_selection(grade_standards)
    print(f'--------------\ngrade_standard\n--------------\n{grade_scale}')


if __name__ == '__main__':
    run()
