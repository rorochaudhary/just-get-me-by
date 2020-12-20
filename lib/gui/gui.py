import PySimpleGUI as sg


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
