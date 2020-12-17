# add PyInstaller to run gui on windows without user Python requirement
import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a little color to your windows

# All the stuff inside your window. This is the PSG magic code compactor...
layout = [  [sg.Text('Hello! Let\'s get you by. First we need a few things.')],
            [sg.Text('School Canvas URL (ex. canvas.oregonstate.edu):'), sg.InputText(key="canvasURL")],
            [sg.Text('Your Canvas Token:'), sg.InputText(key='token')],
            [sg.OK(), sg.Cancel(), sg.Button("How to get a Token")]]

# Create the Window
window = sg.Window('Just Get Me By', layout)

# Event Loop to process "events"
while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    
    # user clicks Ok, gather url and token from input
    req_items = values
    print("req_items:", req_items)

    # user click token help, display instructions on getting a token
    if event in ("How to get a Token"):
        get_token_txt = "In order to calculate your grades, I will need a token:\n" + \
                        "1. Login in your institution Canvas site.\n" + \
                        "2. On the left vertical taskbar, click 'Account'\n" + \
                        "3. Click Profile -> Settings\n" + \
                        "4. In the Approved Integrations section, click '+New Access Token'\n" + \
                        "5. Give a Purpose (ex. Just Get Me By) and click 'Generate Token'\n" + \
                        "6. Copy/Paste the Token (including the leading number and ~ sign) into the Your Canvas Token field and you're done!\n\n" + \
                        "Screenshots of token generation are available at the GitHub repo for this project - https://github.com/rorochaudhary/just-get-me-by"
        sg.popup_scrolled(get_token_txt)

window.close()