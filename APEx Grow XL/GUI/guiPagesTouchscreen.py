from GUI.guiWidgets import *

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial

import schemdraw
import schemdraw.elements as elm

import matplotlib.pyplot as plt
import numpy as np


class SubpageScafoldTouchscreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        homeButton = ButtonStackWidget(
            self, controller, ("Home", "Home", lambda x: controller.show_frame("Navscreen1")))
        homeButton.grid(row=2, column=4, sticky="NSEW")


class NavPage1Touchscreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)

        frameKeys = ["ExperimentStp", "ExperimentPrep",
                     "Overides", "Control", "Fossilrecord", "Settings"]
        navButtons = ButtonStackWidget(
            self, controller, *[(k, k, lambda x: controller.show_frame(k)) for k in frameKeys], columns=3)
        navButtons.grid(row=0, column=0, sticky="NSEW")


class ExperimentStpTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class ExperimentRunTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class ExperimentPrepTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class OveridesTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class ControlTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class FossilRecordTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class SettingsTouchscreen(SubpageScafoldTouchscreen):
    def __init__(self, parent, controller):
        SubpageScafoldTouchscreen.__init__(self, parent, controller)


class Keyboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.displayStringVar = tk.StringVar()
        display = tk.Entry(self, textvariable=self.displayStringVar, font=(
            "Calibri", 13), width=5)

        display.grid(row=0, column=0, columnspan=5, sticky="NSEW")

        def stingAppend(val):
            self.displayStringVar.set(self.displayStringVar.get() + val)

        numpad = ButtonStackWidget(self, controller,
                                   ("1", "1", lambda x: stingAppend("1")), ("2", "2",
                                                                            lambda x: stingAppend("2")), ("3", "3", lambda x: stingAppend("3")),
                                   ("4", "4", lambda x: stingAppend("4")), ("5", "5",
                                                                            lambda x: stingAppend("5")), ("6", "6", lambda x: stingAppend("6")),
                                   ("7", "7", lambda x: stingAppend("7")), ("8", "8",
                                                                            lambda x: stingAppend("8")), ("9", "9", lambda x: stingAppend("9")),
                                   (".", ".", lambda x: stingAppend(".")), ("0", "0",
                                                                            lambda x: stingAppend("0")), ("-", "-", lambda x: stingAppend("-")),
                                   columns=3)
        numpad.grid(column=0, row=1, columnspan=4, rowspan=4, sticky="NSEW")

        entrybuttons = ButtonStackWidget(self, controller,
                                         ("<-", "<-", lambda x: self.displayStringVar.set(self.displayStringVar.get()[:-1])), ("Enter", "Enter", lambda x: controller.closeKeyboard(True, self.displayStringVar.get())), ("Cancel", "Cancel", lambda x: controller.closeKeyboard(False, "")))
        entrybuttons.grid(column=4, row=1, rowspan=4, sticky="NSEW")
