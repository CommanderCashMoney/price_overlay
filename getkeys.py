# coding=utf-8
import win32api as wapi
import win32con

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)

    if wapi.GetAsyncKeyState(win32con.VK_F1):
        keys.append('F1')
    if wapi.GetAsyncKeyState(win32con.VK_F2):
        keys.append('F2')
    if wapi.GetAsyncKeyState(win32con.VK_F3):
        keys.append('F3')
    if wapi.GetAsyncKeyState(win32con.VK_F4):
        keys.append('F4')
    if wapi.GetAsyncKeyState(win32con.VK_F5):
        keys.append('F5')
    if wapi.GetAsyncKeyState(win32con.VK_F6):
        keys.append('F6')
    return keys
