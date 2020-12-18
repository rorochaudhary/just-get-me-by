# add PyInstaller to run gui on windows without user Python requirement
import PySimpleGUI as sg

# change theme string
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

# Event Loop to process "events"
while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    # user clicks Help - display instructions to get token
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
    
    # open window for grade calculator
    if event in ('Ok'):
        req_items = values
        print("req_items:", req_items)
        # calls to /lib/api/api.py here or package req_items to be sent
        results = 'API RESULTS PASSED IN?'

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

window.close()