from .classes import Test, MaxTestAttemptsReached
import lib.util as util
import os


def run():
    print(f'{os.path.basename(__file__)}')
    test = Test(MAX_ATTEMPTS=10)
    try:
        test.set_rand_grade_standard()
    except MaxTestAttemptsReached:
        return
    gsch = test.rand_gstd['grading_scheme']
    result = util.get_target_percentage('A', gsch)
    print(result)


if __name__ == '__main__':
    run()
