import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial

import schemdraw
import schemdraw.elements as elm

import matplotlib.pyplot as plt
import numpy as np

import random

import os

from GUI.guiWidgets import *


# class windows(tk.Tk):
#     """
#     Root Class For GUI Window
#     """

#     def __init__(self, _comm_handler, *args, **kwargs):
#         self.comm_handler = _comm_handler

#         self.currentFrame = ""

#         self.touchscreen = True
#         # the entry widget that was clicked on to trigger the keyboard
#         self.keyboardCaller = None
#         self.keyboardActive = False

#         tk.Tk.__init__(self, *args, **kwargs)
#         self.wm_title("Bioreactor")

#         # creating a frame and assigning it to container
#         container = tk.Frame(self, height=400, width=600)
#         # specifying the region where the frame is packed in root
#         container.pack(side="top", fill="both", expand=True)

#         # configuring the location of the container using grid
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         # dictionary of frames {name: page class}
#         if not self.touchscreen:
#             frameDefinitionList = [("Homepage", Homepage), ("Experiment", ExperimentPage), ("Experiment Setup", ExperimentSetupPage),
#                                    ("Control", ControlPage), ("Fossil Record", FossilRecordPage), ("Settings", SettingsPage)]
#         else:

#             frameDefinitionList = [
#                 ("Navscreen1", Homepage1Touchscreen), ("Keyboard", Keyboard)]
#         self.frames = {F[0]: "" for F in frameDefinitionList}
#         for F in frameDefinitionList:
#             self.frames[F[0]] = F[1](container, self)
#             self.frames[F[0]].grid(row=0, column=0, sticky="NSEW")

#         # Using a method to switch frames
#         if not touchscreen:
#             self.show_frame("Homepage")
#         else:
#             self.show_frame("Navscreen1")

#         # getting all sub frames of the window
#         allDescendents = self.winfo_children()

#         # adding to descendants all the sub frames of the 1st level subframes recursively for all frames in window
#         for child in allDescendents:
#             if child.winfo_children():
#                 allDescendents.extend(child.winfo_children())

#         self.updatableDescendents = []
#         self.updatableDescendentsEveryCycle = []

#         # storing a list of all descendants that have update functions so they can be called directly
#         for child in allDescendents:
#             if hasattr(child, "update_data"):
#                 self.updatableDescendents.append(child)
#             if hasattr(child, "update_data_every"):
#                 self.updatableDescendentsEveryCycle.append(child)

#         if self.touchscreen:
#             container.bind_class('Entry', '<Button-1>',
#                                  lambda *args: self.popUpKeyBoard(args[0].widget))

#     def __str__(self):
#         return "root"

#     def popUpKeyBoard(self, widget):
#         if widget["state"] != "normal" or self.keyboardActive:
#             return

#         self.keyboardCaller = widget
#         self.keyboardActive = True
#         self.show_frame("Keyboard")

#     def closeKeyboard(self, isValueEntered, value):
#         if isValueEntered:
#             textvar_name = self.keyboardCaller.cget("textvariable")
#             textvar = self.tk.globalsetvar(textvar_name, value)
#         self.show_frame(self.currentFrame)
#         self.keyboardActive = False

#     def show_frame(self, frameKey):
#         """
#         Brings the requested frame to the top
#         """
#         frame = self.frames[frameKey]
#         if frameKey != "Keyboard":
#             self.currentFrame = frameKey
#         else:
#             frame.displayStringVar.set("")
#         # raises the current frame to the top
#         frame.tkraise()

#     def update_data(self):  # would be better to only do this if that frame is currently on screen
#         """
#         Updates all descendant frames with an update_data function

#         update_data should be used for updates that can be marginally delayed in response
#         """
#         for child in self.updatableDescendents:
#             child.update_data()

#     def update_data_every(self):
#         """
#         Updates all descendant frames with an update_data_every function

#         update_data should be used for updates where response time is essential
#         """
#         for child in self.updatableDescendentsEveryCycle:
#             child.update_data_every()


# class LineGraphWidget(tk.Frame):
#     """
#     Widget for plotting and updating 1 y axis line graph for n updating data series

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     *data -- (data_source, label)
#              -- data_source should be a callable object which returns two lists (list(numeric)), list(numeric))
#                 xData, yData that will be plotted
#              -- label (str) labels series in legend
#     title -- str
#     xAxis -- str
#     yAxis -- str

#     """

#     def __init__(self, parent, controller, *data, title="", xAxis="", yAxis=""):
#         self.title = title
#         self.xAxisLabel = xAxis
#         self.yAxisLabel = yAxis
#         tk.Frame.__init__(self, parent)
#         self.figure1 = plt.Figure(figsize=(6, 3), dpi=100)
#         self.ax3 = self.figure1.add_subplot(111)

#         self.data = data

#         empty_plot = True

#         # go through each data_source, pull the data and plot it
#         for data_source, label in data:
#             xData, yData = data_source()

#             if xData is None or yData is None:
#                 xData = []
#                 yData = []

#             if (xData.shape == yData.shape and
#                     not (np.all(np.isnan(xData)) or np.all(np.isnan(yData)) or xData.shape[0] == 0)):
#                 self.ax3.plot(xData, yData, label=label)
#                 empty_plot = False
#             else:
#                 if (xData.shape[0] != 0):
#                     print("-------------------------------")
#                     print("Plot not plotted")
#                     print(label)
#                     print("x data is nan {}\t{}\t{}".format(
#                         np.all(np.isnan(xData)), xData, yData))
#                     print("y data is nan {}\t{}\t{}".format(
#                         np.all(np.isnan(yData)), xData, yData))
#                     print("x and y data shapes don't match {}\t{}\t{}".format(xData.shape != yData.shape,
#                                                                               xData.shape, yData.shape))
#                     print("-------------------------------")

#         # plot formatting
#         if not empty_plot:
#             self.ax3.legend()
#         self.ax3.set_xlabel(self.xAxisLabel)
#         self.ax3.set_ylabel(self.yAxisLabel)
#         self.figure1.suptitle(title)
#         self.figure1.tight_layout()

#         # converting matpltlib plot to tkinter figure canvas
#         self.canv = FigureCanvasTkAgg(self.figure1, self)
#         self.canv.draw()
#         # converting convas to widget
#         self.canv.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

#     def update_data(self):
#         # clear axis
#         self.ax3.cla()
#         empty_plot = True

#         # for each call data_source to get new data series to plot and plot thems
#         for data_source, label in self.data:
#             xData, yData = data_source()
#             if (xData.shape == yData.shape and
#                     not (np.all(np.isnan(xData)) or np.all(np.isnan(yData)) or xData.shape[0] == 0)):
#                 self.ax3.plot(xData, yData, label=label)
#                 empty_plot = False
#             else:
#                 # if data retrieved is not in a valid format for plotting
#                 if (xData.shape[0] != 0):
#                     print("-------------------------------")
#                     print("Plot not plotted")
#                     print(label)
#                     print("x data is nan {}\t{}\t{}".format(
#                         np.all(np.isnan(xData)), xData, yData))
#                     print("y data is nan {}\t{}\t{}".format(
#                         np.all(np.isnan(yData)), xData, yData))
#                     print("x and y data shapes don't match {}\t{}\t{}".format(xData.shape != yData.shape,
#                                                                               xData.shape, yData.shape))
#                     print("-------------------------------")

#         # plt formatting and conversion
#         if not empty_plot:
#             self.ax3.legend()
#         self.ax3.set_xlabel(self.xAxisLabel)
#         self.ax3.set_ylabel(self.yAxisLabel)
#         self.figure1.tight_layout()
#         self.canv.draw()


# class FlowchartWidget(tk.Frame):
#     # not implemented
#     def __init__(self, parent, controller, *data, title="", xAxis="", yAxis=""):
#         self.title = title
#         self.xAxisLabel = xAxis
#         self.yAxisLabel = yAxis
#         tk.Frame.__init__(self, parent)

#         self.figure1 = plt.Figure(figsize=(6, 3), dpi=100)
#         self.ax = self.figure1.subplots()
#         self.ax.axis("off")

#         self.d = schemdraw.Drawing(canvas=self.ax)
#         self.d += elm.Resistor().label('100KΩ')
#         self.d += elm.Capacitor().down().label('0.1μF', loc='bottom')
#         self.d += elm.Line().left()
#         self.d += elm.Ground()
#         self.d += elm.SourceV().up().label('10V')

#         self.d.draw(canvas=self.ax, show=False)

#         self.canv = FigureCanvasTkAgg(self.figure1, self)
#         self.canv.draw()
#         self.canv.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

#     # def update_data(self):
#     #     self.ax3.cla()

#     #     for data_source, label in self.data:
#     #         xData, yData = data_source()
#     #         self.ax3.plot(xData, yData, label=label)

#     #     self.ax3.legend()
#     #     self.ax3.set_xlabel(self.xAxisLabel)
#     #     self.ax3.set_ylabel(self.yAxisLabel)
#     #     self.figure1.tight_layout()
#     #     self.canv.draw()


# class EntryTableWidget(tk.Frame):
#     """
#     Widget for

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     headings_types_defaults -- (list of len 3 lists) one element for each column. Each element is
#                                a len 3 list of the form (heading, type, default)
#                                -- heading (str) column heading, appears in 1st row
#                                -- type (class) can be any class that can be instanciated as
#                                   type(str) eg int,float etc. Data for this row is converted to this type
#                                   when outputted
#                                -- default value applied if type(str) is invalid at any point also acts as
#                                   the default value if there is no user input
#     """

#     def __init__(self, parent, controller, headings_types_defaults):
#         tk.Frame.__init__(self, parent)

#         self.controller = controller

#         self.headings = [h[0] for h in headings_types_defaults]
#         self.types = [h[1] for h in headings_types_defaults]
#         self.defaults = [h[2] for h in headings_types_defaults]
#         self.rows = 1

#         # creates string vars to hold the value for each grid square
#         self.data = [[tk.StringVar() for h in self.headings]
#                      for i in range(self.rows)]

#         # go through each row and instansiate it
#         for i in range(self.rows + 1):
#             self.rowconfigure(i, weight=1)
#             # go through each cell in a row and instanciate it
#             for j in range(len(self.headings)):

#                 if i == 0:
#                     # heading row
#                     e = tk.Entry(self, width=10,
#                                  font=('Calibri', 12))
#                     self.columnconfigure(j, weight=1)
#                     e.insert(0, self.headings[j])
#                     e.config(state=tk.DISABLED)
#                 else:
#                     # each cell is an entry widget which stores its value in a string var self.data[i][j]
#                     e = tk.Entry(self, textvariable=self.data[i-1][j], width=10,
#                                  font=('Calibri', 12))
#                     self.data[i-1][j].set("")
#                     # add a trace so whenever a value is changed the output function is called
#                     self.data[i -
#                               1][j].trace_add("write", lambda *args: self.output_data())
#                 e.grid(row=i, column=j)

#     def output_data(self):
#         """
#         outputs the data currently in the table to a csv and to the comm_handler
#         also applies specified data types to the data and adds a
#         new row if there is no empty row at the end
#         """

#         # check if there are no empty rows to at the end to type in and add one if there is none
#         self.check_for_table_full()
#         tmp_data = [[self.data[i][j].get() for j in range(len(self.data[0]))]
#                     for i in range(self.rows - 1)]

#         # apply types
#         for i in range(len(tmp_data)):
#             for j in range((len(tmp_data[0]))):
#                 try:
#                     tmp_data[i][j] = self.types[j](tmp_data[i][j])
#                 except:
#                     tmp_data[i][j] = self.types[j](self.defaults[j])

#         self.controller.comm_handler._sequance_list = tmp_data.copy()
#         self.controller.comm_handler.save_sequence()

#     def check_for_table_full(self):
#         """
#         checks if there is a trailing empty row and if there isn't one adds it
#         """
#         for tmpStringVar in self.data[-1]:
#             if tmpStringVar.get() != "":
#                 self.rows += 1
#                 self.rowconfigure(self.rows, weight=1)
#                 self.data.append([tk.StringVar() for h in self.headings])
#                 for j in range(len(self.headings)):
#                     e = tk.Entry(self, textvariable=self.data[self.rows-1][j], width=10,
#                                  font=('Calibri', 12))
#                     self.data[self.rows-1][j].set("")
#                     self.data[self.rows -
#                               1][j].trace_add("write", lambda *args: self.output_data())
#                     e.grid(row=self.rows, column=j)

#                 return

#     def update_data(self):
#         """
#         checks if the user has loaded a new sequence and updates the UI accordingly
#         """
#         if self.controller.comm_handler._sequence_loaded:
#             # fetches new sequence
#             tmp_data = self.controller.comm_handler._sequance_list

#             # destroys the current UI elements
#             for widgets in self.winfo_children():
#                 widgets.destroy()

#             self.rows = tmp_data.shape[0]

#             # creats new string var table
#             self.data = [[tk.StringVar() for h in self.headings]
#                          for i in range(self.rows)]

#             # loops  throught the same initialisation process but inserts the value found
#             # in the loaded sequence
#             for i in range(self.rows + 1):
#                 self.rowconfigure(i, weight=1)
#                 for j in range(len(self.headings)):
#                     if i == 0:
#                         e = tk.Entry(self, width=10,
#                                      font=('Calibri', 12))
#                         self.columnconfigure(j, weight=1)
#                         e.insert(0, self.headings[j])
#                         e.config(state=tk.DISABLED)
#                     else:
#                         e = tk.Entry(self, textvariable=self.data[i-1][j], width=10,
#                                      font=('Calibri', 12))
#                         if tmp_data[i-1][j] != self.defaults[j]:
#                             e.insert(0, tmp_data[i-1][j])
#                             self.data[i-1][j].set(tmp_data[i-1][j])
#                         else:
#                             self.data[i-1][j].set("")
#                         self.data[i -
#                                   1][j].trace_add("write", lambda *args: self.output_data())
#                     e.grid(row=i, column=j)

#             self.controller.comm_handler._sequence_loaded = False
#             self.check_for_table_full()


# class PlotDataDisplayWidget(tk.Frame):
#     """
#     forms a grid of labels and values to display updating values and has an associated button
#     to turn on and off plotting on an associated graph

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     *data -- list of 3 element lists each element containing (label, source, button_func)
#              -- label (str)
#              -- source (callable object) a function that returns a singal value to be displayed
#              -- button_func (callable object) the function that gets triggered when the
#                 plotting/not plotting button is pressed
#     columns -- sets how many columns the data will be displayed in, defaults to 1
#     """

#     def __init__(self, parent, controller, *data, columns=1):
#         tk.Frame.__init__(self, parent)
#         rowNum = 0
#         colNum = 0
#         self.rows = {}
#         self.dataSources = {}

#         # configure column sizes
#         for i in range(columns):
#             self.columnconfigure(3*i, weight=1)
#             self.columnconfigure(3*i + 1, weight=1)
#             self.columnconfigure(3*i + 2, weight=1)

#         button_arguments = [[] for i in range(columns)]
#         for label, source, button_func in list(data):

#             # creating the arguments that will later be used to create the button
#             # these are initial text, alternate text, callback function
#             button_arguments[colNum].append(
#                 ("Plotting", "Not Plotting", button_func))

#             # configure each row and add 2 labels for the label and the data
#             self.rowconfigure(rowNum, weight=1)
#             labelTK = tk.Label(self, text=label + ":",  font=("Calibri", 13))
#             dataBoxTK = tk.Label(self, text="{:.2f}".format(
#                 float(source())), font=("Calibri", 13))

#             # set the positions of the label and databox
#             labelTK.grid(row=rowNum, column=3 * colNum, sticky="NSE")
#             dataBoxTK.grid(row=rowNum, column=3 * colNum + 1, sticky="NSW")

#             # save relevant information about each entry
#             self.rows[label] = (labelTK, dataBoxTK)
#             self.dataSources[label] = source
#             colNum += 1
#             if colNum == columns:
#                 colNum = 0
#                 rowNum += 1

#         # create the buttons and place them next to the relevant labels and data
#         for i in range(columns):
#             plotting_buttons = ButtonStackWidget(
#                 self, controller, *button_arguments[i])
#             plotting_buttons.grid(
#                 row=0,  rowspan=int(np.floor(len(list(data))/columns)), column=3 * i + 2, sticky="NSW")

#     def update_data(self):
#         """
#         Fetch new data and refresh all of the data displayed
#         """
#         rowLabels = self.rows.keys()
#         for key in rowLabels:
#             row = self.rows[key]
#             for i, box in enumerate(row[1:]):
#                 box.config(text="{:.2f}".format(float(self.dataSources[key]() if len(
#                     row[1:]) == 1 else self.dataSources[key][i+1]())))


# class DataDisplayWidget(tk.Frame):
#     """
#     forms a grid of labels and values to display updating values and has an associated button
#     to turn on and off plotting on an associated graph

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     *data -- list of 2 element lists each element containing (label, source)
#              -- label (str)
#              -- source (callable object) a function that returns a singal value to be displayed
#     columns (optional) -- sets how many columns the data will be displayed in, defaults to 1
#     """

#     def __init__(self, parent, controller, *data, columns=1):
#         tk.Frame.__init__(self, parent)
#         rowNum = 0
#         colNum = 0
#         self.rows = {}
#         self.dataSources = {}

#         # configure column sizes
#         for i in range(columns):
#             self.columnconfigure(2*i, weight=1)
#             self.columnconfigure(2*i + 1, weight=1)

#         for label, source in list(data):
#             # configure each row and add 2 labels one for the label and one for the data
#             self.rowconfigure(rowNum, weight=1)
#             labelTK = tk.Label(self, text=label + ":",  font=("Calibri", 13))
#             dataBoxTK = tk.Label(self, text="{:.2f}".format(
#                 float(source())), font=("Calibri", 13))

#             # set the positions of the label and databox
#             labelTK.grid(row=rowNum, column=2 * colNum, sticky="NSE")
#             dataBoxTK.grid(row=rowNum, column=2 * colNum + 1, sticky="NSW")

#             # save relevant information about each entry
#             self.rows[label] = (labelTK, dataBoxTK)
#             self.dataSources[label] = source
#             colNum += 1
#             if colNum == columns:
#                 colNum = 0
#                 rowNum += 1

#     def update_data(self):
#         """
#         Fetch new data and refresh all of the data displayed
#         """
#         rowLabels = self.rows.keys()
#         for key in rowLabels:
#             row = self.rows[key]
#             for i, box in enumerate(row[1:]):
#                 box.config(text="{:.2f}".format(float(self.dataSources[key]() if len(
#                     row[1:]) == 1 else self.dataSources[key][i+1]())))


# class OnOffButtonWidget(tk.Button):
#     """
#     Simple toggle button that calls a provided callback function whenever it's triggered

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     onLabel -- (str) label shown on the button when the state is on/true
#     onLabel -- (str) label shown on the button when the state is off/false
#     callback -- (callable object) function called when the button is pressed. It is passed one argument,
#                 the new state as a boolean (on = true, off = false)
#     defaultVal (optional) -- (boolean) sets the startup state of the button, defaults to false if not specified
#     """

#     def __init__(self, parent, onLabel, offLabel, callback, defaultVal=False):
#         # create a button with the appropriate label for the current state and
#         # a callback to the internalCallback function below
#         tk.Button.__init__(
#             self, parent, text=onLabel if defaultVal else offLabel, command=self.internalCallback)
#         self.state = defaultVal
#         self.onLabel = onLabel
#         self.offLabel = offLabel
#         self.callback = callback

#     def internalCallback(self):
#         """
#         toggle the state, update the text displayed and then call the callback function
#         supplied (self.callback)
#         """
#         self.state = not self.state
#         self.config(text=self.onLabel if self.state else self.offLabel)
#         self.callback(self.state)


# class ButtonStackWidget(tk.Frame):
#     """
#     Stack of simple toggle buttons (OnOffButtonWidget)

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     *data -- list of lists with either 3 or 4 elements as shown below
#         onLabel -- (str) label shown on the button when the state is on/true
#         onLabel -- (str) label shown on the button when the state is off/false
#         callback -- (callable object) function called when the button is pressed. It is passed one argument,
#                     the new state as a boolean (on = true, off = false)
#         defaultVal (optional) -- (boolean) sets the startup state of the button, defaults to false if not specified
#     columns (optional) -- sets how many columns the data will be displayed in, defaults to 1
#     """

#     def __init__(self, parent, controller, *data, columns=1):
#         # takes an object with the shape (onLabel, offLabel, output changed callback)
#         tk.Frame.__init__(self, parent)
#         rowNum = 0
#         colNum = 0

#         # loop through all the buttons and create them in turn
#         for buttonArguments in list(data):
#             # set row and column sizes
#             self.columnconfigure(colNum, pad=30, weight=1)
#             self.rowconfigure(rowNum, weight=1)

#             switch = OnOffButtonWidget(self, *buttonArguments)
#             # positon button
#             switch.grid(row=rowNum, column=colNum, sticky="NSEW")
#             colNum += 1
#             # go to the next row is all columns on this row are full
#             if colNum == columns:
#                 colNum = 0
#                 rowNum += 1


# class dataInputStackWidget(tk.Frame):
#     """
#     stack of text inputs with associated label

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     *data -- list of lists with 2 elements as shown below
#              label -- (str)
#              output -- (callable object) Is called when the value in the box is changed and is
#                        passed the new value as a string
#     """

#     def __init__(self, parent, controller, *data):
#         tk.Frame.__init__(self, parent)
#         rowNum = 0

#         # configure the size of the columns
#         self.columnconfigure(0, weight=1)
#         self.columnconfigure(1, weight=1)

#         # dictionary pointing to the string variables associated with each box
#         # the unique name assigned to each tkInter StringVar is used as the key
#         # this is obtained by myStringVar._name and is also passed as the first argument
#         # by tkInter when the text is edited
#         self.outputBoxes = {}

#         # dictionary of the user defined callback functions associated with each input box
#         # the same keys as above are used
#         self.outputFunctions = {}

#         for label, output in list(data):
#             # create a new stringVar and set its initial value to 0
#             tmpStringVar = tk.StringVar()
#             tmpStringVar.set(0)

#             # store the string var in the dictionary
#             self.outputBoxes[tmpStringVar._name] = tmpStringVar

#             # configure the size of the row and create the label and entry box objects
#             self.rowconfigure(rowNum, weight=1)
#             labelTK = tk.Label(self, text="" if label ==
#                                "" else label + ":",  font=("Calibri", 13))
#             dataBoxTK = tk.Entry(self, textvariable=self.outputBoxes[tmpStringVar._name], font=(
#                 "Calibri", 13), width=5)

#             # add a trace to the entry box so that whenever the value is edited the user provided callback
#             # function is called and passed the current value of the entry box
#             self.outputBoxes[tmpStringVar._name].trace_add(
#                 "write", lambda *args: self.outputFunctions[args[0]](self.outputBoxes[args[0]].get()))

#             # store the callback function in the associated dictionary
#             self.outputFunctions[tmpStringVar._name] = output
#             labelTK.grid(row=rowNum, column=0, sticky="NSE")
#             dataBoxTK.grid(row=rowNum, column=1, sticky="NSW")
#             rowNum += 1


# class pumpControlWidget(tk.Frame):
#     """
#     widget for displaying the current state of all the pumps and giving the ability
#     to overide the speed to a desired state.
#     Has the overall form of pumpName|pumpSpeed|overideToggle|overideSpeed

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     """

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         # configure column and row sizes
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=1)

#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         # create title row of labels
#         labelSpeed = tk.Label(self, text="Speed")
#         labelSpeed.grid(row=0, column=0, sticky="NSEW")

#         labelOveride = tk.Label(self, text="Override")
#         labelOveride.grid(row=0, column=1, sticky="NSEW")

#         labelOverideSpeed = tk.Label(self, text="Override Speed")
#         labelOverideSpeed.grid(row=0, column=2, sticky="NSEW")

#         # create a data display widget with the pump names as the labels and the current pump speed as the data
#         pumpSpeed = DataDisplayWidget(self, controller, ("Media OD Sensor Pump", lambda: controller.comm_handler._Pump[0, -1]),
#                                       ("Media Inlet Pump",
#                                        lambda: controller.comm_handler._Pump[1, -1]),
#                                       ("Media Transfer Pump",
#                                        lambda: controller.comm_handler._Pump[2, -1]),
#                                       ("Main OD Sensor Pump",
#                                        lambda: controller.comm_handler._Pump[3, -1]),
#                                       ("Waste Pump",
#                                        lambda: controller.comm_handler._Pump[4, -1]),
#                                       ("Sterilzation Input Pump",
#                                        lambda: controller.comm_handler._Pump[5, -1]),
#                                       ("Fossil Record Pump",
#                                        lambda: controller.comm_handler._Pump[6, -1]),
#                                       ("Main Mixer",
#                                        lambda: controller.comm_handler._Pump[7, -1]),
#                                       ("Media Mixer", lambda: controller.comm_handler._Pump[8, -1]))

#         # position this display widget in the first column
#         pumpSpeed.grid(row=1, column=0, sticky="NSEW")

#         # generate a button stack to act as the overide toggle for each pump and place it in the 2nd column
#         pumpOverideButtons = ButtonStackWidget(self, controller,
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    0, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    1, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    2, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    3, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    4, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    5, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    6, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
#                                                    7, bool(x))),
#                                                ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(8, bool(x))))
#         pumpOverideButtons.grid(row=1, column=1, sticky="NSEW")

#         # create a data input stack to take in the desired overide speeds and place it in the 3rd column
#         # the inbuilt label is set to "" to be empty
#         pumpOverideSpeeds = dataInputStackWidget(self, controller, ("", lambda x: controller.comm_handler.set_pump_speed(0, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      1, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      2, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      3, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      4, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      5, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      6, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(
#                                                      7, x)),
#                                                  ("", lambda x: controller.comm_handler.set_pump_speed(8, x)))
#         pumpOverideSpeeds.grid(row=1, column=2, sticky="NSEW", padx=10)


# class groupParameterUpdateWidget(tk.Frame):
#     """
#     widget the groups together a series of variables and groups them with a singular button to act as a
#     callback of somekind

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     title -- (str) title of the group
#     callback -- function to call then the update function is called
#     *data -- arguments passed to the dataDisplayWidget, list of lists with 2 elements as shown below
#              label -- (str)
#              output -- (callable object) Is called when the value in the box is changed and is
#                        passed the new value as a string
#     """

#     def __init__(self, parent, controller, title, callback, *data):
#         tk.Frame.__init__(
#             self, parent, highlightbackground="black", highlightthickness=2)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)

#         self.grid_rowconfigure(0, weight=0, minsize=10, pad=10)

#         self.title = title

#         self.callback = callback

#         title_label = tk.Label(self, text=self.title,
#                                font=("Calibri", 13, "bold"))
#         title_label.grid(row=0, column=0, sticky="NSW", padx=20)

#         upload_button = tk.Button(
#             self, text="Upload", command=self.callback, bg="green", fg="white")

#         upload_button.grid(column=1, row=0, sticky="NSE", padx=20, pady=20)

#         input_widget = dataInputStackWidget(
#             self, controller, *data)
#         input_widget.grid(column=0, row=1, columnspan=2)


# class MenuBarWidget(tk.Frame):
#     """
#     widget that displays the menu bar at the top of each page and changes the displayed page
#     if another tab is selected

#     parent -- frame for which this widget is the direct child of (ie where it was instantiated)
#     controller -- root controller object (windows)
#     """

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.grid_rowconfigure(0, weight=1)

#         pageNames = controller.frames.keys()
#         self.labels = []

#         colNum = 0
#         for pageName in pageNames:
#             # create a lable with a callback function attached which calls the
#             # show frame function in the windows class with the appropriate pageName
#             tmplabel = tk.Button(self, text=pageName, command=partial(
#                 controller.show_frame, pageName))
#             tmplabel.grid(row=0, column=colNum, sticky="NSEW")
#             self.labels.append(tmplabel)
#             colNum += 1


class PageScafold(tk.Frame):
    """
    Generic page scafold that all pages should inherit from
    Adds a menu bar and configures the top row 

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=0, minsize=20)

        label = MenuBarWidget(self, controller)
        label.grid(row=0, column=0, columnspan=2, sticky="NEW")


class Homepage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1, pad=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        communicationsDataView = DataDisplayWidget(self, controller, ("PC Status", lambda: controller.comm_handler._Status),
                                                   ("Device Status", lambda: controller.comm_handler._DeviceStatus), columns=2)
        communicationsDataView.grid(row=1, column=0, sticky="NSEW")

        ODDataView = PlotDataDisplayWidget(self, controller,
                                           ("OD1",
                                            lambda: controller.comm_handler._OD[0, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 0, bool(x))),
                                           ("Media OD1",
                                            lambda: controller.comm_handler._OD_media[0, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 0, bool(x))),
                                           ("OD2",
                                            lambda: controller.comm_handler._OD[1, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 1, bool(x))),
                                           ("Media OD2",
                                            lambda: controller.comm_handler._OD_media[1, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 1, bool(x))),
                                           ("OD3",
                                            lambda: controller.comm_handler._OD[2, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 2, bool(x))),
                                           ("Media OD3",
                                            lambda: controller.comm_handler._OD_media[2, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 2, bool(x))),
                                           ("OD4",
                                            lambda: controller.comm_handler._OD[3, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 3, bool(x))),
                                           ("Media OD4",
                                            lambda: controller.comm_handler._OD_media[3, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 3, bool(x))),
                                           ("OD5",
                                            lambda: controller.comm_handler._OD[4, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 4, bool(x))),
                                           ("Media OD5",
                                            lambda: controller.comm_handler._OD_media[4, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 4, bool(x))),
                                           ("OD6",
                                            lambda: controller.comm_handler._OD[5, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD", 5, bool(x))),
                                           ("Media OD6",
                                            lambda: controller.comm_handler._OD_media[5, -1],
                                            lambda x: controller.comm_handler.set_plot_bools("OD Media", 5, bool(x))),
                                           columns=2)
        ODDataView.grid(row=2, column=0, sticky="NSEW")

        tempDataView = PlotDataDisplayWidget(self, controller,
                                             ("Temperature IR",
                                              lambda: controller.comm_handler._TempIR[-1] if len(
                                                  controller.comm_handler._TempIR) > 0 else "nan",
                                              lambda x: controller.comm_handler.set_plot_bools("Temp", 0, bool(x))),
                                             ("Temperature Immersed",
                                              lambda: controller.comm_handler._Temp[-1] if len(
                                                  controller.comm_handler._Temp) > 0 else "nan",
                                              lambda x: controller.comm_handler.set_plot_bools("Temp", 1, bool(x))),
                                             ("Media Temperature IR",
                                              lambda: controller.comm_handler._TempIR_media[-1] if len(
                                                  controller.comm_handler._TempIR_media) > 0 else "nan",
                                              lambda x: controller.comm_handler.set_plot_bools("Temp Media", 0, bool(x))),
                                             ("Media Temperature Immersed",
                                              lambda: controller.comm_handler._Temp_media[-1] if len(
                                                  controller.comm_handler._Temp_media) > 0 else "nan",
                                              lambda x: controller.comm_handler.set_plot_bools("Temp Media", 1, bool(x))),
                                             columns=2)
        tempDataView.grid(row=3, column=0, sticky="NSEW")

        pumpControl = pumpControlWidget(self, controller)
        pumpControl.grid(row=4, column=0, sticky="NSEW", pady=10)

        ODGraph = LineGraphWidget(self, controller,
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[0]
                                            else np.array([]),
                                            controller.comm_handler._OD[0, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD1"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[1]
                                            else np.array([]),
                                            controller.comm_handler._OD[1, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD2"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[2]
                                            else np.array([]),
                                            controller.comm_handler._OD[2, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD3"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[3]
                                            else np.array([]),
                                            controller.comm_handler._OD[3, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD4"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[4]
                                            else np.array([]),
                                            controller.comm_handler._OD[4, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD5"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[5]
                                            else np.array([]),
                                            controller.comm_handler._OD[5, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD6"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[0]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[0, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD1"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[1]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[1, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD2"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[2]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[2, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD3"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[3]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[3, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD4"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[4]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[4, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD5"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[5]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[5, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD6"),
                                  title="Optical Density", xAxis="Time(s)", yAxis="Optical Density")

        ODGraph.grid(row=1, column=1, rowspan=2, sticky="NSW")

        tempGraph = LineGraphWidget(self, controller,
                                    (lambda: (controller.comm_handler._Temp_times[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable[0]
                                     else np.array([]),
                                     controller.comm_handler._TempIR[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]), "Temp IR"),
                                    (lambda: (controller.comm_handler._Temp_times[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable[1]
                                     else np.array([]),
                                     controller.comm_handler._Temp[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]), "Analogue Temp"),
                                    (lambda: (controller.comm_handler._Temp_times_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable_media[0]
                                     else np.array([]),
                                     controller.comm_handler._TempIR_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]), "Media Temp IR"),
                                    (lambda: (controller.comm_handler._Temp_times_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable_media[1]
                                     else np.array([]),
                                     controller.comm_handler._Temp_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]), "Media Analogue Temp"),
                                    title="Temperature", xAxis="Time(s)", yAxis="Temperature(°C)")

        tempGraph.grid(row=3, column=1, rowspan=2, sticky="NSW")


class ExperimentPage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        ODGraph = LineGraphWidget(self, controller,
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[0]
                                            else np.array([]),
                                            controller.comm_handler._OD[0, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD1"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[1]
                                            else np.array([]),
                                            controller.comm_handler._OD[1, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD2"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[2]
                                            else np.array([]),
                                            controller.comm_handler._OD[2, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD3"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[3]
                                            else np.array([]),
                                            controller.comm_handler._OD[3, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD4"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[4]
                                            else np.array([]),
                                            controller.comm_handler._OD[4, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD5"),
                                  (lambda: (controller.comm_handler._OD_times[controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable[5]
                                            else np.array([]),
                                            controller.comm_handler._OD[5, :][controller.comm_handler._OD_times > controller.comm_handler._OD_plot_min_t]), "OD6"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[0]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[0, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD1"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[1]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[1, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD2"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[2]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[2, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD3"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[3]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[3, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD4"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[4]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[4, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD5"),
                                  (lambda: (controller.comm_handler._OD_times_media[controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]
                                            if controller.comm_handler._OD_plot_enable_media[5]
                                            else np.array([]),
                                            controller.comm_handler._OD_media[5, :][controller.comm_handler._OD_times_media > controller.comm_handler._OD_plot_min_t]), "Media OD6"),
                                  title="Optical Density", xAxis="Time(s)", yAxis="Optical Density")
        ODGraph.grid(row=1, column=0, sticky="NSW")

        tempGraph = LineGraphWidget(self, controller,
                                    (lambda: (controller.comm_handler._Temp_times[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable[0]
                                     else np.array([]),
                                     controller.comm_handler._TempIR[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]), "Temp IR"),
                                    (lambda: (controller.comm_handler._Temp_times[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable[1]
                                     else np.array([]),
                                     controller.comm_handler._Temp[controller.comm_handler._Temp_times > controller.comm_handler._Temp_plot_min_t]), "Analogue Temp"),
                                    (lambda: (controller.comm_handler._Temp_times_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable_media[0]
                                     else np.array([]),
                                     controller.comm_handler._TempIR_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]), "Media Temp IR"),
                                    (lambda: (controller.comm_handler._Temp_times_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]
                                     if controller.comm_handler._Temp_plot_enable_media[1]
                                     else np.array([]),
                                     controller.comm_handler._Temp_media[controller.comm_handler._Temp_times_media > controller.comm_handler._Temp_plot_min_t]), "Media Analogue Temp"),
                                    title="Temperature", xAxis="Time(s)", yAxis="Temperature(°C)")

        tempGraph.grid(row=1, column=1, sticky="NSW")


class ExperimentSetupPage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=0, minsize=20)
        self.grid_rowconfigure(2, weight=1)

        # should add a scrollable element but it can only act on a canvas so would have to stack the table frame inside the canvas.

        buttons = ButtonStackWidget(self, controller,
                                    ("Upload Sequence", "Upload Sequence",
                                     lambda x: controller.comm_handler.set_Status(32)),
                                    ("Stop Run", "Start Run",
                                     lambda x: controller.comm_handler.set_Status(
                                         2)
                                     if x else controller.comm_handler.set_Status(3)),
                                    ("Referance OD", "Referance OD",
                                     lambda x: controller.comm_handler.set_Status(68)),
                                    ("Referance Media OD", "Referance Media OD",
                                     lambda x: controller.comm_handler.set_Status(69)),
                                    ("Save Sequence", "Save Sequence",
                                     lambda x: controller.comm_handler.save_sequence(
                                         tk.filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                                         title="Select a File",
                                                                         filetypes=(("Sequnce files",
                                                                                    "*.csv*"),
                                                                                    ("All files",
                                                                                    "*.*"))))),
                                    ("Load Sequence", "Load Sequence",
                                     lambda x: controller.comm_handler.load_sequence(
                                         tk.filedialog.askopenfilename(initialdir=os.getcwd(),
                                                                       title="Select a File",
                                                                       filetypes=(("Sequnce files",
                                                                                  "*.csv*"),
                                                                                  ("All files",
                                                                                  "*.*"))))),
                                    columns=6)

        buttons.grid(row=1, column=0, columnspan=2, sticky="NSEW")

        sequenceTable = EntryTableWidget(
            self, controller, [("No", int, 0), ("Time Trigger", float, 5000000), ("Temp Trigger", float, 200), ("OD", float, 200),
                               ("", float, 200), ("T", float, 200), ("ri", float,
                                                                     200), ("gg", float, 200), ("er", float, 200),
                               ("Target Temp", float, 0), ("OD Sensor", int, 2), ("Target OD", float, 200), ("OD Drift", float, 0), ("Next", int, 0)])
        sequenceTable.grid(row=2, column=0, columnspan=2, sticky="NEW")


class ControlPage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        OD_calibration = groupParameterUpdateWidget(
            self, controller, "OD Calibration", lambda: controller.comm_handler.set_Status(64), ("Gradient", lambda x: controller.comm_handler.set_OD_calibration_gradient(x)), ("Offset", lambda x: controller.comm_handler.set_OD_calibration_offset(x)), ("Reference Absorbance", lambda x: controller.comm_handler.set_OD_reference_absorbance(x)))
        OD_calibration.grid(column=0, row=1, sticky="NSEW", padx=20, pady=20)

        OD_target = groupParameterUpdateWidget(
            self, controller, "OD Target", lambda: controller.comm_handler.set_Status(65), ("Target", lambda x: controller.comm_handler.set_OD_target(x)))
        OD_target.grid(column=0, row=2, sticky="NSEW", padx=20, pady=20)

        OD_Control = groupParameterUpdateWidget(
            self, controller, "OD Control", lambda: controller.comm_handler.set_Status(66), ("k_P", lambda x: controller.comm_handler.set_OD_P(x)), ("k_I", lambda x: controller.comm_handler.set_OD_I(x)), ("k_D", lambda x: controller.comm_handler.set_OD_D(x)))
        OD_Control.grid(column=0, row=3, sticky="NSEW", padx=20, pady=20)

        Temp_calibration = groupParameterUpdateWidget(
            self, controller, "Temperature Calibration", lambda: controller.comm_handler.set_Status(48), ("Gradient", lambda x: controller.comm_handler.set_temp_calibration_gradient(x)), ("Offset", lambda x: controller.comm_handler.set_temp_calibration_offset(x)))
        Temp_calibration.grid(column=1, row=1, sticky="NSEW", padx=20, pady=20)

        Temp_target = groupParameterUpdateWidget(
            self, controller, "Temperature Target", lambda: controller.comm_handler.set_Status(49), ("Target", lambda x: controller.comm_handler.set_temp_target(x)))
        Temp_target.grid(column=1, row=2, sticky="NSEW", padx=20, pady=20)

        Temp_Control = groupParameterUpdateWidget(
            self, controller, "Temperature Control", lambda: controller.comm_handler.set_Status(50), ("k_P", lambda x: controller.comm_handler.set_temp_P(x)), ("k_I", lambda x: controller.comm_handler.set_temp_I(x)), ("k_D", lambda x: controller.comm_handler.set_temp_D(x)))
        Temp_Control.grid(column=1, row=3, sticky="NSEW", padx=20, pady=20)


class SettingsPage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=1)

        settingsStack = dataInputStackWidget(
            self, controller, ("OD Plots Start Time",
                               lambda x: controller.comm_handler.set_od_plot_start_time(x)),
            ("Temperature Plots Start Time", lambda x: controller.comm_handler.set_temp_plot_start_time(x)))
        settingsStack.grid(row=1, column=0, sticky="NEW")


class FossilRecordPage(PageScafold):
    def __init__(self, parent, controller):
        PageScafold.__init__(self, parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=1)

        moveSizes = dataInputStackWidget(
            self, controller, ("Axis 1 Movement",
                               lambda x: controller.comm_handler.set_distance_to_move(0, x)),
            ("Axis 2 Movement", lambda x: controller.comm_handler.set_distance_to_move(1, x)))

        moveSizes.grid(column=0, row=1)

        buttons = ButtonStackWidget(self, controller,
                                    ("Execute Move", "Execute Move",
                                     lambda x: controller.comm_handler.set_Status(81)),
                                    ("Set As First Well", "Set As First Well",
                                     lambda x: controller.comm_handler.set_set_well_as_first_flag(True)),
                                    ("Set As Last Well", "Set As Last Well",
                                     lambda x: controller.comm_handler.set_set_well_as_first_flag(False)),
                                    ("Dry Run", "Dry Run",
                                     lambda x: controller.comm_handler.set_Status(89)))
        buttons.grid(column=1, row=1)


# class Homepage1Touchscreen(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         self.grid_columnconfigure(0, weight=1)

#         self.grid_rowconfigure(0, weight=1)

#         navButtons = ButtonStackWidget(
#             self, controller, *[(str(i), str(i), lambda x: i) for i in range(6)], columns=3)
#         navButtons.grid(row=0, column=0, sticky="NSEW")


# class Keyboard(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=1)
#         self.grid_columnconfigure(3, weight=1)
#         self.grid_columnconfigure(4, weight=1)

#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)
#         self.grid_rowconfigure(2, weight=1)
#         self.grid_rowconfigure(3, weight=1)
#         self.grid_rowconfigure(4, weight=1)

#         self.displayStringVar = tk.StringVar()
#         display = tk.Entry(self, textvariable=self.displayStringVar, font=(
#             "Calibri", 13), width=5)

#         display.grid(row=0, column=0, columnspan=5, sticky="NSEW")

#         def stingAppend(val):
#             self.displayStringVar.set(self.displayStringVar.get() + val)

#         numpad = ButtonStackWidget(self, controller,
#                                    ("1", "1", lambda x: stingAppend("1")), ("2", "2",
#                                                                             lambda x: stingAppend("2")), ("3", "3", lambda x: stingAppend("3")),
#                                    ("4", "4", lambda x: stingAppend("4")), ("5", "5",
#                                                                             lambda x: stingAppend("5")), ("6", "6", lambda x: stingAppend("6")),
#                                    ("7", "7", lambda x: stingAppend("7")), ("8", "8",
#                                                                             lambda x: stingAppend("8")), ("9", "9", lambda x: stingAppend("9")),
#                                    (".", ".", lambda x: stingAppend(".")), ("0", "0",
#                                                                             lambda x: stingAppend("0")), ("<-", "<-", lambda x: self.displayStringVar.set(self.displayStringVar.get()[:-1])),
#                                    columns=3)
#         numpad.grid(column=0, row=1, columnspan=4, rowspan=4, sticky="NSEW")

#         entrybuttons = ButtonStackWidget(self, controller,
#                                          ("Enter", "Enter", lambda x: controller.closeKeyboard(True, self.displayStringVar.get())), ("Cancel", "Cancel", lambda x: controller.closeKeyboard(False, "")))
#         entrybuttons.grid(column=4, row=1, rowspan=4, sticky="NSEW")


def tmpRandomNumGen():
    return random.randint(0, 100)


def tmpGraphDataGen():
    xData = []
    yData = []
    for i in range(6):
        xData.append(tmpRandomNumGen())
        yData.append(tmpRandomNumGen())

    tmpX = [0, 1, 2, 3, 4, 5, 6]
    tmpY = [0, 1, 2, 3, 4, 5, 6]
    # return (tmpX,tmpY)
    return (xData, yData)
