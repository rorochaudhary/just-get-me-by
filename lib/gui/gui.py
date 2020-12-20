import lib.util as util
import PySimpleGUI as sg

def get_main_layout() -> list:
    return [
        [sg.Text('Hello! Let\'s get you by. First we need a couple things.')],
        [sg.Text('School Canvas URL (ex. canvas.oregonstate.edu):'), sg.InputText(util.search_url()[0], key="canvasURL")],
        [sg.Text('Your Canvas Token:'), sg.InputText(util.search_token()[0], key='token')],
        [sg.Button('Ok'), sg.Cancel(), sg.Button("How to get a Token")]
    ]

def get_grade_scale(raw_grade_standard) -> list:
    display_grade_scale = False

    if len(raw_grade_standard) == 1:
        grade_scale = raw_grade_standard[0]['grading_scheme']
        display_grade_scale = True
    elif len(raw_grade_standard) > 1:
        selected_gstd = grade_standard_selection(raw_grade_standard)
        if len(selected_gstd) == 0:  # empty list returned if canceled
            display_grade_scale = False
        else:
            grade_scale = selected_gstd['grading_scheme']
            display_grade_scale = True

    add_layout = []

    if display_grade_scale is True:
        # display grading scale
        add_layout += [sg.Text('Your course\'s current grade scale:')],
        grade_list = []
        for obj in grade_scale:
            grade_list.append(sg.Text(f'{obj["name"]} = {obj["value"]}'))
        add_layout += [grade_list[i] for i in range(len(grade_list))],

    return add_layout

def display_courses(course_names, courses) -> list:
    # just need course id and name
    for i in range(len(courses)):
        # print(f"Course {i}: {courses[i]}\n")
        # print(f'id: {courses[i]["id"]}, name: {courses[i]["name"]}')
        try:
            course_names.append({'id': courses[i]["id"], 'name': courses[i]["name"]})
        except:
            pass
    # print(f"current courses:\n{course_names}")
    # print([course_names[i]['name'] for i in range(len(course_names))])

    add_layout = [
        [sg.Listbox(values=[course_names[i]['name'] for i in range(len(course_names))], size=(75, 12), key='selected_course')],
        [sg.Button('Select'), sg.Button('Cancel')]
    ]

    return add_layout


def get_token_help():
    get_token_txt = "In order to calculate your grades, I will need a token:\n" + \
                "1. Login to your institution Canvas site.\n" + \
                "2. On the left vertical taskbar, click 'Account'\n" + \
                "3. Click Profile -> Settings\n" + \
                "4. In the Approved Integrations section, click '+New Access Token'\n" + \
                "5. Give a Purpose (ex. Just Get Me By) and click 'Generate Token'\n" + \
                "6. Copy/Paste the Token (including the leading number and ~ sign) into the Your Canvas Token field and you're done!\n\n" + \
                "Screenshots of token generation are available at the GitHub repo - https://github.com/rorochaudhary/just-get-me-by"
    sg.popup_scrolled(get_token_txt, title="Getting a User Token")

def get_assignments_and_groups(assignment_data, assignment_dict, group_data, group_dict):
    # process group data
    for group in group_data:
        assignment_list = []
        assignment_list.append(group['group_weight'])
        group_dict[group['id']] = assignment_list

    # process assignments
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

def display_known_info(raw_grade_standard, assignment_dict) -> list:
    calc_layout = []

    #find a grade standard to use
    add_layout = get_grade_scale(raw_grade_standard)
    calc_layout += add_layout

    # select target grade and execute grade calc
    calc_layout += [sg.Text('Target Grade?'), sg.InputText(size=(10, 1))],
    calc_layout += [sg.Button('Just Get Me By'), sg.Cancel()],

    # display assignments
    calc_layout += [sg.Text("Your current assignments:")],
    assignments_str = ""
    for key, val in assignment_dict.items():
        assignments_str += f'{key} = {val[0]} out of {val[1]}\n'
    # print(assignments_str)
    calc_layout += [sg.Multiline(assignments_str, size=(45, 10))],
    calc_layout += [sg.Text('Your target scores needed:')],
    calc_layout += [sg.Multiline(size=(45, 10), key='algo_result')],

    return calc_layout

def grade_standard_selection(grade_standards: list) -> list:
    """Opens a new window for the user to choose one of the GradingStandards.

    Returns the selected GradingStandard as a list.
    Returns an empty list if no GradingStandards are found or if canceled.
    """
    if len(grade_standards) < 1:
        return []

    layout = [
        [sg.Listbox(
            values=[gstd['title'] for gstd in grade_standards],
            size=(75, 12),
            key='selected'
        )],
        [sg.Button('Select'), sg.Button('Details'), sg.Button('Cancel')]
    ]
    window = sg.Window('Select Grade Scale', layout)#, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            return []
        if event in ('Select', 'Details'):
            selected_title = values['selected'][0]
            for gstd in grade_standards:
                if gstd['title'] == selected_title:
                    if event == 'Select':
                        window.close()
                        return gstd
                    if event == 'Details':
                        popup_text = 'Letter Grade: Minimum Percentage\n'
                        for grade in gstd['grading_scheme']:
                            popup_text += \
                                f"{grade['name']}: {grade['value'] * 100}\n"
                        sg.popup_scrolled(popup_text, title='Details')
                    break  # out of the for loop, not the while
