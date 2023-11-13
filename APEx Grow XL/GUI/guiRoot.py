from GUI.guiPages import *
from GUI.guiPagesTouchscreen import *

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial

import schemdraw
import schemdraw.elements as elm

import matplotlib.pyplot as plt
import numpy as np


class windows(tk.Tk):
    """
    Root Class For GUI Window
    """

    def __init__(self, _comm_handler, *args, **kwargs):
        self.comm_handler = _comm_handler

        self.currentFrame = ""

        self.touchscreen = False
        # the entry widget that was clicked on to trigger the keyboard
        self.keyboardCaller = None
        self.keyboardActive = False

        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Bioreactor")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary of frames {name: page class}
        if not self.touchscreen:
            frameDefinitionList = [("Homepage", Homepage), ("Experiment", ExperimentPage), ("Experiment Setup", ExperimentSetupPage),
                                   ("Control", ControlPage), ("Fossil Record", FossilRecordPage), ("Settings", SettingsPage)]
        else:

            frameDefinitionList = [
                ("Navscreen1", NavPage1Touchscreen), ("ExperimentStp",
                                                      ExperimentStpTouchscreen), ("ExperimentRun", ExperimentRunTouchscreen),
                ("ExperimentPrep", ExperimentPrepTouchscreen), ("Overides",
                                                                OveridesTouchscreen), ("Control", ControlTouchscreen),
                ("Fossilrecord", FossilRecordTouchscreen), ("Settings", SettingsTouchscreen), ("Keyboard", Keyboard)]
        self.frames = {F[0]: "" for F in frameDefinitionList}
        for F in frameDefinitionList:
            self.frames[F[0]] = F[1](container, self)
            self.frames[F[0]].grid(row=0, column=0, sticky="NSEW")

        # Using a method to switch frames
        if not self.touchscreen:
            self.show_frame("Homepage")
        else:
            self.show_frame("Navscreen1")

        # getting all sub frames of the window
        allDescendents = self.winfo_children()

        # adding to descendants all the sub frames of the 1st level subframes recursively for all frames in window
        for child in allDescendents:
            if child.winfo_children():
                allDescendents.extend(child.winfo_children())

        self.updatableDescendents = []
        self.updatableDescendentsEveryCycle = []

        # storing a list of all descendants that have update functions so they can be called directly
        for child in allDescendents:
            if hasattr(child, "update_data"):
                self.updatableDescendents.append(child)
            if hasattr(child, "update_data_every"):
                self.updatableDescendentsEveryCycle.append(child)

        if self.touchscreen:
            container.bind_class('Entry', '<Button-1>',
                                 lambda *args: self.popUpKeyBoard(args[0].widget))

    def __str__(self):
        return "root"

    def popUpKeyBoard(self, widget):
        if widget["state"] != "normal" or self.keyboardActive:
            return

        self.keyboardCaller = widget
        self.keyboardActive = True
        self.show_frame("Keyboard")

    def closeKeyboard(self, isValueEntered, value):
        if isValueEntered:
            textvar_name = self.keyboardCaller.cget("textvariable")
            textvar = self.tk.globalsetvar(textvar_name, value)
        self.show_frame(self.currentFrame)
        self.keyboardActive = False

    def show_frame(self, frameKey):
        """
        Brings the requested frame to the top
        """
        frame = self.frames[frameKey]
        if frameKey != "Keyboard":
            self.currentFrame = frameKey
        else:
            frame.displayStringVar.set("")
        # raises the current frame to the top
        frame.tkraise()

    def update_data(self):  # would be better to only do this if that frame is currently on screen
        """
        Updates all descendant frames with an update_data function

        update_data should be used for updates that can be marginally delayed in response 
        """
        for child in self.updatableDescendents:
            child.update_data()

    def update_data_every(self):
        """
        Updates all descendant frames with an update_data_every function

        update_data should be used for updates where response time is essential 
        """
        for child in self.updatableDescendentsEveryCycle:
            child.update_data_every()
