from lib.api.api import Canvas
import lib.util as util
import os
import random
import toml


def run():
    print(f'{os.path.basename(__file__)}')
    test = Test(MAX_ATTEMPTS=10)

    # Feed url and token into Canvas API.

    # # Get random course id.

    # # Get grading standards from course.
    # gstds = get_grade_standards(rand_course_id)

    # # Get a random grade standard from course.

    # rand_gstd = get_rand_grade_standard(gstds)
    # gsch = rand_gstd['grade_scheme']

    # result = util.get_target_percentage('A', gsch)
    # print(result)





class Test:
    def __init__(self, MAX_ATTEMPTS):
        self.MAX_ATTEMPTS: int = MAX_ATTEMPTS
        self.current_attempts: int = 0
        self.canvas: object = None
        self.courses: list = []
        self.rand_course_id: int = -1  # sentinel
        self.gstds: list = []
        random.seed()

    def init_canvas(self) -> None:
        my_token = toml.load('config/config.toml')['secret']['manual_token']
        self.canvas = Canvas('https://canvas.oregonstate.edu', my_token)

    def set_courses(self) -> None:
        if self.canvas is None:
            self.init_canvas()
        self.courses = self.canvas.get_courses()

    def set_rand_course_id(self) -> None:
        if self.canvas is None:
            self.init_canvas()
        if len(self.courses) == 0:
            self.set_courses()
        self.rand_course_id = self.courses[random.randrange(len(self.courses))]['id']

    def set_grade_standards(self) -> None:
        if self.canvas is None:
            self.init_canvas()
        if len(self.courses) == 0:
            self.set_courses()
        if self.rand_course_id == -1:
            self.set_rand_course_id()
        self.gstds = self.canvas.get_grading_standard_in_course(self.rand_course_id)
        while True:
            if self.current_attempts == self.MAX_ATTEMPTS:
                print(f"Reached max attempts: {self.MAX_ATTEMPTS}")
                return False
            if len(self.gstds) > 0:
                return True
            self.current_attempts += 1
            # Try a different course.
            self.set_rand_course_id()
            self.gstds = self.canvas.get_grading_standard_in_course(self.rand_course_id)

    # def set_rand_grade_standard(self):
    #     rand_gstd = gstds[random.randrange(len(gstds))]
    #     while True:
    #         if current_attempts == MAX_ATTEMPTS:
    #             print(f"Reached max attempts: {MAX_ATTEMPTS}")
    #             return
    #         if 'grade_scheme' in rand_gstd:
    #             break
    #         current_attempts += 1
    #         # Try finding a grade scheme somewhere else.
    #         gstds = canvas.get_grading_standard_in_course(rand_course_id)
    #         rand_gstd = gstds[random.randrange(len(gstds))]

    def is_max_attempts_reached(self) -> bool:
        if self.current_attempts == self.MAX_ATTEMPTS:
            print(f"Reached max attempts: {self.MAX_ATTEMPTS}")
            return True
        return False

if __name__ == '__main__':
    run()
