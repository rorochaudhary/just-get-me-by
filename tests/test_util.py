from lib.api.api import Canvas
import random
import toml


def print_title(title: str) -> None:
    """Prints a formatted title in the standard output."""
    print(
        f"{len(title) * '='}\n"
        f'{title}\n'
        f"{len(title) * '='}"
    )


class MaxTestAttemptsReached(Exception):
    """"""
    pass


class Test:
    def __init__(self, MAX_ATTEMPTS=10):
        self.MAX_ATTEMPTS: int = MAX_ATTEMPTS
        self.current_attempts: int = 0
        self.canvas: Canvas = None
        self.courses: list = []
        self.rand_course_id: int = -1  # sentinel
        self.gstds: list = []
        self.rand_gstd: dict = {}
        self.assignments: list = []
        self.assignment_grps: list = []
        random.seed()

    def init_canvas(self, config='') -> None:
        """Feed url and token into Canvas API."""
        if config == '':
            path = 'config/config.toml'
        else:
            path = config
        my_token = toml.load(path)['secret']['manual_token']
        self.canvas = Canvas('https://canvas.oregonstate.edu', my_token)

    def set_courses(self) -> None:
        """Stores the courses in the Test object"""
        if self.canvas is None:
            self.init_canvas()
        self.courses = self.canvas.get_courses()

    def set_rand_course_id(self) -> None:
        """Stores a random course id."""
        if len(self.courses) == 0:
            self.set_courses()
        self.rand_course_id = self.courses[random.randrange(len(self.courses))]['id']

    def set_grade_standards(self, course_id: int = -1) -> None:
        """Stores the grade standards for the given course id.

        If a course id isn't specified, uses the random course id stored.
        """
        if len(self.courses) == 0:
            self.set_courses()
        if course_id == -1:  # default
            if self.rand_course_id == -1:
                self.set_rand_course_id()
            course_id = self.rand_course_id
        self.gstds = self.canvas.get_grading_standard_in_course(course_id)
        while True:
            if self._is_max_attempts_reached():
                raise MaxTestAttemptsReached()
            if len(self.gstds) > 0:
                return
            self.current_attempts += 1
            # Try a different course.
            self.set_rand_course_id()
            self.gstds = self.canvas.get_grading_standard_in_course(self.rand_course_id)

    def set_rand_grade_standard(self) -> None:
        """Stores a random grade standard."""
        if len(self.gstds) == 0:
            self.set_grade_standards()
        self.rand_gstd = self.gstds[random.randrange(len(self.gstds))]
        while True:
            if self._is_max_attempts_reached():
                raise MaxTestAttemptsReached()
            if 'grading_scheme' in self.rand_gstd:
                return
            self.current_attempts += 1
            # Try finding a grade scheme elsewhere.
            self.set_rand_course_id()
            self.set_grade_standards()
            self.rand_gstd = self.gstds[random.randrange(len(self.gstds))]

    def set_assignments(self, course_id: int = -1) -> None:
        """Stores assignments from the given course id.

        If a course id isn't specified, uses the random course id stored.
        """
        if len(self.courses) == 0:
            self.set_courses()
        if course_id == -1:  # default
            if self.rand_course_id == -1:
                self.set_rand_course_id()
            course_id = self.rand_course_id
        self.assignments = self.canvas.get_assignments_in_course(course_id)

    def set_assignment_groups(self, course_id: int = -1) -> None:
        """Stores assignment groups from the given course id.

        If a course id isn't specified, uses the random course id stored.
        """
        if len(self.courses) == 0:
            self.set_courses()
        if course_id == -1:  # default
            if self.rand_course_id == -1:
                self.set_rand_course_id()
            course_id = self.rand_course_id
        self.assignment_grps = self.canvas.get_assignment_groups_in_course(course_id)

    def _is_max_attempts_reached(self) -> bool:
        """Returns True if current attempts is equal to max attempts."""
        if self.current_attempts == self.MAX_ATTEMPTS:
            print(f'Reached max attempts: {self.MAX_ATTEMPTS}')
            return True
        return False
