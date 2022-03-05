import cv2
from getkeys import key_check
import time
import overlay_settings_nw
from win32gui import GetWindowText, GetForegroundWindow
from my_timer import Timer
import pynput
from grabscreen import grab_screen
import pytesseract
import requests
import json
import re
import webbrowser
from name_cleanup import text_cleanup
import pyperclip
import ctypes
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

cleaner = re.compile('<.*?>')

# os.putenv("TESSDATA_PREFIX", 'tesseract\\tessdata')
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = resource_path('tesseract\\tesseract.exe')

details = overlay_settings_nw.detail_overlay()
app_timer = Timer('app timer')
app_timer.start()
mouse = pynput.mouse.Controller()
price_timer = Timer('price_timer')

keyboard = pynput.keyboard.Controller

def ra_x(x):
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x_adjust = screensize[0] / 2560

    # print(screensize)
    return round(x*x_adjust)
def ra_y(y):
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    y_adjust = screensize[1] / 1440
    # print(screensize)
    return round(y*y_adjust)


def open_web():
    global item_id_for_web
    if item_id_for_web:
        print('Opening browser for {}'.format(item_id_for_web))
        url = 'https://nwmarketprices.com/{}'.format(item_id_for_web)
        webbrowser.open_new_tab(url)
        time.sleep(0.4)
def copy_text():
    global text_for_copy
    if text_for_copy:
        pyperclip.copy(text_for_copy)
        spam = pyperclip.paste()
        print(spam)

listener = pynput.keyboard.GlobalHotKeys({
        '<alt>+d': open_web,
        '<ctrl>+<alt>+c': copy_text})

listener.start()


def cleanhtml(raw_html):
    cleantext = re.sub(cleaner, '', raw_html)
    return cleantext
def process_image(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    res = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return res


def get_price_from_web(name_id):

    # name_id = 1152
    url = 'https://nwmarketprices.com/'
    params = {'cn_id': name_id}
    header = {"X-Requested-With": "XMLHttpRequest"}
    r = requests.get(url=url, params=params, headers=header)
    data = r.json()
    return data


def get_name_ids():
    url = 'https://nwmarketprices.com/cn'

    header = {"X-Requested-With": "XMLHttpRequest"}
    r = requests.get(url=url, headers=header)
    data = r.json()
    data_str = data['cn']
    data_list = json.loads(data_str)

    names = {sub[0]: sub[1] for sub in data_list}
    return names

def lookup_nameid(item_name, names):
    if item_name in names:
        name_id = names[item_name]
    else:
        name_id = None
    return name_id


def ocr(img):
    f_txt = ''
    custom_config = """-c tessedit_char_whitelist="0123456789,.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:- \\"\\'" """
    txt = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng')
    for count, text in enumerate(txt['text']):
        text = text.strip()
        if len(text) > 1:
            if f_txt == '':
                f_txt = text
            else:
                f_txt = '{} {}'.format(f_txt, text)

    return f_txt

item_id_for_web = None
text_for_copy = None

def main():

    global item_id_for_web, text_for_copy
    price_overlay = False
    price_timer.start()
    details.hide()
    last_item_checked = None
    names = get_name_ids()
    while True:
        keys = key_check()
        if keys:
            for key in keys:
                if key == 'F6':
                    price_overlay = not price_overlay
                    print('Price Overlay Active: ', price_overlay)
                    time.sleep(0.2)
        # if price_overlay and GetWindowText(GetForegroundWindow()) == "New World":
        if price_overlay:

            mouse_pos = mouse.position

            x = mouse_pos[0] - ra_x(320)
            y = mouse_pos[1] - ra_y(356)
            if mouse_pos[0] < ra_x(320):
                x = 0
            if mouse_pos[1] < ra_y(356):
                y = 0

            aoi = (x, y, ra_x(580), ra_y(406))
            img_grab = grab_screen(aoi)
            reference_image_file = resource_path('actions.png')
            reference_img = cv2.imread(reference_image_file)
            width = reference_img.shape[1]
            height = reference_img.shape[0]
            dim = (ra_x(width), ra_y(height))
            reference_img = cv2.resize(reference_img, dim)
            res = cv2.matchTemplate(img_grab, reference_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # print(max_val)
            if max_val > 0.5:
                # we found the action image. Now figure out what side it's on

                if max_loc[0] > ra_x(300):
                    #details on the right
                    x1 = max_loc[0] + ra_x(350) + x
                    y1 = max_loc[1] + y

                else:
                    #details on the left
                    x1 = max_loc[0] - ra_x(370) + x
                    y1 = max_loc[1] + y

                aoi1 = (x1, y1, ra_x(356), ra_y(75))
                img_grab2 = grab_screen(aoi1)
                img_grab2 = process_image(img_grab2)
                detail_x = x1 - ra_x(120)
                detail_y = y1 - 140
                #extract text
                text = ocr(img_grab2)
                text_for_copy = text
                text = text_cleanup(text)
                #get name id
                name_id = lookup_nameid(text, names)
                if name_id:

                    if not last_item_checked or name_id != last_item_checked:
                        item_details = get_price_from_web(name_id)
                        last_item_checked = name_id
                        last_checked = 'Lowest price as of {}'.format(item_details['last_checked'])
                        recent_price = item_details['recent_lowest_price']
                        price_change = cleanhtml(item_details['price_change'])

                        details.show()
                        details.updatetext('name', text)
                        details.updatetext('price', recent_price)
                        details.updatetext('last_checked', last_checked)
                        details.updatetext('price_change', price_change)

                        details.move(detail_x, detail_y)
                        event, values = details.read()
                        item_id_for_web = name_id
                        print('Received item info for: {}'.format(text))
                    else:
                        # we just searched that item. Don't do it again

                        details.move(detail_x, detail_y)
                        event, values = details.read()
                else:
                    item_id_for_web = None
                    item_details = '{} - Not Found'.format(text)
                    details.updatetext('name',text)
                    details.updatetext('price', 'Not Found')
                    details.updatetext('last_checked', '--')
                    details.updatetext('price_change', '--')

                    details.show()
                    details.move(detail_x, detail_y)
                    event, values = details.read()
                    # details.hide()
                    # print(item_details)

                # cv2.imshow('win2', img_grab2)
                # cv2.moveWindow('win2', 3200, 0)
            else:
                item_id_for_web = None
                details.hide()
                last_item_checked = None
                details.read()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
