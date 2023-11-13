from tkinter import *
from guiPages import *

if __name__ == "__main__":
    testObj = windows()
    loopsPerDataRefresh = 50000
    i = 0
    while True:
        testObj.update_idletasks()
        testObj.update()
        if i > loopsPerDataRefresh:
            testObj.update_data()
            i = 0
        i += 1