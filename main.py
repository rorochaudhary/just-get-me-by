# main logic for Just Get Me By that integrates algo.py, api.py, and gui.py
from lib.algo.algo import algo
from lib.api.api import Canvas
import lib.util as util
import re
import PySimpleGUI as sg
# LOW PRIORITY - add PyInstaller to to make .exe without user Python requirement

sg.theme('DarkAmber')

# main/opening window layout
layout = [
            [sg.Text('Hello! Let\'s get you by. First we need a couple things.')],
            [sg.Text('School Canvas URL (ex. canvas.oregonstate.edu):'), sg.InputText(key="canvasURL")],
            [sg.Text('Your Canvas Token:'), sg.InputText(key='token')],
            [sg.Button('Ok'), sg.Cancel(), sg.Button("How to get a Token")]
        ]

# Create the Window
window = sg.Window('Just Get Me By', layout)

# Main Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    # -------------Help Get Token Window (within mainloop)-----------
    if event in ("How to get a Token"):
        get_token_txt = "In order to calculate your grades, I will need a token:\n" + \
                        "1. Login to your institution Canvas site.\n" + \
                        "2. On the left vertical taskbar, click 'Account'\n" + \
                        "3. Click Profile -> Settings\n" + \
                        "4. In the Approved Integrations section, click '+New Access Token'\n" + \
                        "5. Give a Purpose (ex. Just Get Me By) and click 'Generate Token'\n" + \
                        "6. Copy/Paste the Token (including the leading number and ~ sign) into the Your Canvas Token field and you're done!\n\n" + \
                        "Screenshots of token generation are available at the GitHub repo - https://github.com/rorochaudhary/just-get-me-by"
        sg.popup_scrolled(get_token_txt, title="Getting a User Token")

    # -------Select Course Window (within mainloop)-------------
    if event in ('Ok'):
        req_items = values
        # Add https:// to url if protocol not found.
        proto = 'https://' if re.search('[^:]+://', req_items['canvasURL']) is None else ''
        req_items['canvasURL'] = proto + req_items['canvasURL'] # right place to format protocol??
        print("req_items:", req_items)

        # get Canvas information
        requestAPI = Canvas(req_items['canvasURL'], req_items['token'])
        courses = requestAPI.get_courses()
        # print(courses)

        # just need course id and name
        course_names = []
        for i in range(len(courses)):
            # print(f"Course {i}: {courses[i]}\n")
            # print(f'id: {courses[i]["id"]}, name: {courses[i]["name"]}')
            try:
                course_names.append({'id': courses[i]["id"], 'name': courses[i]["name"]})
            except:
                pass
        print(f"current courses:\n{course_names}")
        # print([course_names[i]['name'] for i in range(len(course_names))])

        course_layout = [
            [sg.Listbox(values=[course_names[i]['name'] for i in range(len(course_names))], size=(75, 12), key='selected_course')],
            [sg.Button('Select'), sg.Button('Cancel')]
        ]

        course_window = sg.Window('Select Course', course_layout, finalize=True)

        while True:
            course_event, course_values = course_window.read()
            if course_event in ('Cancel'):
                break
            if course_event in ('Select'):
                # print('user chose:', course_values['selected_course'][0])
                course_chosen = course_values['selected_course'][0]
                # get selected course id
                course_id = 0
                for i in range(len(course_names)):
                    # if course_names[i]['name'] == course_values['selected_course'][0]:
                    if course_names[i]['name'] == course_chosen:
                        course_id = course_names[i]['id']
                # print("selected:", id)

                # get selected course assignments/grades
                assignment_data = requestAPI.get_assignments_in_course(course_id)
                group_data = requestAPI.get_assignment_groups_in_course(course_id)
                raw_grade_standard = requestAPI.get_grading_standard_in_course(course_id)
                grade_scale = raw_grade_standard[0]['grading_scheme']
                assignment_dict = {}
                group_dict = {}
                # grade_standard = {}

                # process group data
                for group in group_data:
                    assignment_list = []
                    assignment_list.append(group['group_weight'])
                    group_dict[group['id']] = assignment_list
                # print(f"group dict:\n{group_dict}")

                # process assignments
                # print(f'assignment data:\n{assignment_data}')
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

                # print(f"assignment dict:\n{assignment_dict}")

                # process grade_standard to get users target
                print(grade_scale)

                # ---------Grade Calculator Window (within Select Course loop)------------
                # layout based on results
                calc_layout = [
                    [sg.Text(f'Course: {course_chosen}')]
                ]

                # display grading scale
                calc_layout += [sg.Text('Your course\'s current grade scale:')],
                grade_list = []
                for obj in grade_scale:
                    grade_list.append(sg.Text(f'{obj["name"]} = {obj["value"]}'))
                calc_layout += [grade_list[i] for i in range(len(grade_list))],

                # select target grade and execute grade calc
                calc_layout += [sg.Text('Target Grade?'), sg.Combo(["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"], size=(3, 1))],
                calc_layout += [sg.Button('Just Get Me By'), sg.Cancel()],

                # display assignments
                calc_layout += [sg.Text("Your current assignments:")],
                assignments_str = ""
                for key, val in assignment_dict.items():
                    assignments_str += f'{key} = {val[0]} out of {val[1]}\n'
                # print(assignments_str)
                calc_layout += [sg.Multiline(assignments_str, size=(45, 10))],

                calc_layout += [sg.Text('Your target scores needed:')],
                calc_layout += [sg.Multiline(size=(45, 12), key='algo_result')],

                # display window
                calc_window = sg.Window('Grade Calculator', calc_layout, finalize=True)

                while True:
                    calc_event, calc_values = calc_window.read()
                    if calc_event in (sg.WIN_CLOSED, 'Cancel'):
                        break
                    if calc_event in ('Just Get Me By'):
                        print(util.get_target_percentage(calc_values[0], grade_scale))  # TODO: remove later
                        target_score = util.get_target_percentage(calc_values[0], grade_scale)

                        # call algo
                        results = algo(target_score, assignment_dict, group_dict)
                        print(results)

                        # display algo results
                        print(calc_values)
                        calc_window['algo_result'].update(results)

                calc_window.close()
        course_window.close()
window.close()
