import cv2
import numpy as np
import mss


def grab_screen(region=None):

    left, top, width, height = region
    mon = {"top": top, "left": left, "width": width, "height": height}

    sct = mss.mss()
    img = np.asarray(sct.grab(mon))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    return img