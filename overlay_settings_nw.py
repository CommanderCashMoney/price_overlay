import PySimpleGUI as sg

class detail_overlay():


    def __init__(self):

        col1 = [
            [
                sg.Text('---------------------------------------------------------', key='name', text_color='#FFFFFF', background_color='#1d1d1d', font=("Helvetica", 15)),
            ],
            [
                sg.Text('---------------', key='price', text_color='#FFFFFF', background_color='#1d1d1d',
                        font=("Helvetica", 25)),
                sg.Text('----------------------------------------------------------', key='price_change', text_color='#FFFFFF',
                        background_color='#1d1d1d',
                        font=("Helvetica", 10)),
            ],
            [
                sg.Text('--------------------------------------------------------------', key='last_checked', text_color='#FFFFFF',
                        background_color='#1d1d1d',
                        font=("Helvetica", 10)),
            ],

        ]



        layout = [
            [sg.Column(col1, background_color='#1d1d1d', justification="left")]


        ]

        # Create the Window
        window = sg.Window('Window Title',
                           layout,
                           no_titlebar=True,
                           keep_on_top=True,
                           location=(0, 0),
                           background_color='#1d1d1d',
                           element_justification='Center',
                           finalize=True,
                           use_default_focus=False,
                           element_padding=None,


                           size=(475,125)

                           )
        self.win = window

    def read(self):
        event, values = self.win.read(timeout=0)
        return event, values

    def updatetext(self, element, val):
        self.win[element].Update(value=val)

    def hide(self):
        self.win.Hide()
    def show(self):
        self.win.UnHide()
    def move(self, x, y):
        self.win.move(x, y)





# details = detail_overlay()
# #
# # enabled=False
# while True:
#
#     event, values = details.read()
    # details.updatetext('name', 'Asmodeum')
    # if event != '__TIMEOUT__':
    #     overlay.save_settings(values)
    #     print(event)
    #print(values)