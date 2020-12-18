# main logic for Just Get Me By that integrates algo.py, api.py, and gui.py
from lib.algo.algo import algo
from lib.api.api import Canvas
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
        req_items['canvasURL'] = 'https://' + req_items['canvasURL'] # right place to format protocol??
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
            course_names.append({'id': courses[i]["id"], 'name': courses[i]["name"]})
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
                # get selected course id
                id = 0
                for i in range(len(course_names)):
                    if course_names[i]['name'] == course_values['selected_course'][0]:
                        id = course_names[i]['id']
                # print("selected:", id)

                # ---------Grade Calculator Window (within Select Course loop)------------
                # layout based on results
                calc_layout = [
                    [sg.Text('Your Canvas course:')]
                ]
                
                # display assignments
                for i in range(0, 6):
                    calc_layout += [sg.Text(f'assignment {i} here'), sg.Text(f'score {i} here'), sg.Text(f'total {i} here')],

                # display grade weights
                calc_layout += [sg.Text('canvas grade breakdown:')],
                for i in range(0, 6):
                    calc_layout += [sg.Text(f'assignment group {i}'), sg.Text(f'group weight {i}'), sg.Text('total here')],

                # display grading standard
                calc_layout += [sg.Text('course grading standard:')],
                for i in range(0, 6):
                    calc_layout += [sg.Text(f'grade title {i}'), sg.Text(f'grading scheme {i}')],

                # select target grade and execute grade calc
                calc_layout += [sg.Text('Target Grade?'), sg.Combo(["A", "B", "C", "D", "E", "F"], size=(3, 1))],
                calc_layout += [sg.Button('Just Get Me By'), sg.Cancel()],

                # display window
                calc_window = sg.Window('Grade Calculator', calc_layout, finalize=True)

                while True:
                    calc_event, calc_values = calc_window.read()
                    if calc_event in (sg.WIN_CLOSED, 'Cancel'):
                        break
                    if calc_event in ('Just Get Me By'):
                        # pop up showing calculator results? or manipulate/add to current window?
                        break

                calc_window.close()
        course_window.close()
window.close()