import PySimpleGUI as sg

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
