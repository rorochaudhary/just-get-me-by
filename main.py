# main logic for Just Get Me By that integrates algo.py, api.py, and gui.py
from lib.algo import calculate_min_grades
from lib.api import Canvas
import lib.gui as gui
import lib.util as util
import re
import traceback
import PySimpleGUI as sg
# LOW PRIORITY - add PyInstaller to to make .exe without user Python requirement

#set theme
sg.theme('DarkAmber')

# main window creation
layout = gui.get_main_layout()

# Create the Window
window = sg.Window('Just Get Me By', layout)

# Main Event Loop to process "events"
while True:
    event, values = window.read()

    #close program
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    #Show how to get a token
    if event in ("How to get a Token"):
        gui.get_token_help()
    #Select Course Window
    if event in ('Ok'):
        req_items = values

        # Add https:// to url if protocol not found.
        proto = 'https://' if re.search('[^:]+://', req_items['canvasURL']) is None else ''
        req_items['canvasURL'] = proto + req_items['canvasURL'] # right place to format protocol??
        print("req_items:", req_items)

        # get canvas course information
        req_err_prompt = 'Either the token or URL you entered is not valid.\nPlease try again'
        try:
            requestAPI = Canvas(req_items['canvasURL'], req_items['token'])
            courses = requestAPI.get_courses()
            print(courses)
            if 'errors' in courses:
                sg.popup_error(req_err_prompt, title='Token or URL Error')
                continue
        except Exception as e:
            traceback.print_exc()
            sg.popup_error(req_err_prompt, title='Token or URL Error')
            continue

        # user confirm/deny token storage
        if util.search_token()[1] == False:
            store_token_prompt = "In order to simplify future uses of Just Get Me By, do you consent to having your token and school URL stored? If not, you will have to re-enter a token and URL each time."
            confirm = sg.popup_yes_no(store_token_prompt, title='Information Storage Confirmation')
            if confirm == "Yes":
                util.config_access(req_items['token'], req_items['canvasURL'])

        # --------- Select Course Window (within mainloop) --------------
        course_names = []
        course_layout = gui.display_courses(course_names, requestAPI.get_courses())
        course_window = sg.Window('Select Course', course_layout, finalize=True)

        while True:
            course_event, course_values = course_window.read()
            if course_event in (sg.WIN_CLOSED, 'Cancel'):
                break
            if course_event in ('Select'):
                course_chosen = course_values['selected_course'][0]
                # get selected course id
                course_id = 0
                for i in range(len(course_names)):
                    if course_names[i]['name'] == course_chosen:
                        course_id = course_names[i]['id']

                # get selected course assignments/grades
                assignment_data = requestAPI.get_assignments_in_course(course_id)
                group_data = requestAPI.get_assignment_groups_in_course(course_id)
                assignment_dict = {}
                group_dict = {}
                gui.get_assignments_and_groups(assignment_data, assignment_dict, group_data, group_dict)


                # ---------Grade Calculator Window (within Select Course loop)------------
                # layout based on results
                calc_layout = [
                    [sg.Text(f'Course: {course_chosen}')]
                ]

                #add assignment information to layout
                raw_grade_standard = requestAPI.get_grading_standard_in_course(course_id)
                calc_layout += gui.display_known_info(raw_grade_standard, assignment_dict)

                # display window
                calc_window = sg.Window('Grade Calculator', calc_layout, finalize=True)

                while True:
                    calc_event, calc_values = calc_window.read()
                    if calc_event in (sg.WIN_CLOSED, 'Cancel'):
                        break
                    if calc_event in ('Just Get Me By'):
                        target_score = util.input_to_float(calc_values[0])

                        # call algo
                        results_str = ""
                        if target_score == -1.0:  # -1.0 is the sentinel value
                            results_str = "Please enter a valid target grade!"
                        else:
                            results = calculate_min_grades(target_score, assignment_dict, group_dict)
                            print(results)
                            if 'error' in results:
                                results_str += results['error']
                            else:
                                for key, value in results.items():
                                    results_str += f'{key} = {value[0]} out of {value[1]}\n'
                        calc_window['algo_result'].update(results_str)

                calc_window.close()
        course_window.close()
window.close()
