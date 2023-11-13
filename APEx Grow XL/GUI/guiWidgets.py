import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial

import schemdraw
import schemdraw.elements as elm

import matplotlib.pyplot as plt
import numpy as np


class LineGraphWidget(tk.Frame):
    """
    Widget for plotting and updating 1 y axis line graph for n updating data series

    parent -- frame for which this widget is the direct child of (ie where it was instantiated)
    controller -- root controller object (windows)
    *data -- (data_source, label) 
             -- data_source should be a callable object which returns two lists (list(numeric)), list(numeric)) 
                xData, yData that will be plotted
             -- label (str) labels series in legend 
    title -- str
    xAxis -- str
    yAxis -- str

    """

    def __init__(self, parent, controller, *data, title="", xAxis="", yAxis=""):
        self.title = title
        self.xAxisLabel = xAxis
        self.yAxisLabel = yAxis
        tk.Frame.__init__(self, parent)
        self.figure1 = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax3 = self.figure1.add_subplot(111)

        self.data = data

        empty_plot = True

        # go through each data_source, pull the data and plot it
        for data_source, label in data:
            xData, yData = data_source()

            if xData is None or yData is None:
                xData = []
                yData = []

            if (xData.shape == yData.shape and
                    not (np.all(np.isnan(xData)) or np.all(np.isnan(yData)) or xData.shape[0] == 0)):
                self.ax3.plot(xData, yData, label=label)
                empty_plot = False
            else:
                if (xData.shape[0] != 0):
                    print("-------------------------------")
                    print("Plot not plotted")
                    print(label)
                    print("x data is nan {}\t{}\t{}".format(
                        np.all(np.isnan(xData)), xData, yData))
                    print("y data is nan {}\t{}\t{}".format(
                        np.all(np.isnan(yData)), xData, yData))
                    print("x and y data shapes don't match {}\t{}\t{}".format(xData.shape != yData.shape,
                                                                              xData.shape, yData.shape))
                    print("-------------------------------")

        # plot formatting
        if not empty_plot:
            self.ax3.legend()
        self.ax3.set_xlabel(self.xAxisLabel)
        self.ax3.set_ylabel(self.yAxisLabel)
        self.figure1.suptitle(title)
        self.figure1.tight_layout()

        # converting matpltlib plot to tkinter figure canvas
        self.canv = FigureCanvasTkAgg(self.figure1, self)
        self.canv.draw()
        # converting convas to widget
        self.canv.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

    def update_data(self):
        # clear axis
        self.ax3.cla()
        empty_plot = True

        # for each call data_source to get new data series to plot and plot thems
        for data_source, label in self.data:
            xData, yData = data_source()
            if (xData.shape == yData.shape and
                    not (np.all(np.isnan(xData)) or np.all(np.isnan(yData)) or xData.shape[0] == 0)):
                self.ax3.plot(xData, yData, label=label)
                empty_plot = False
            else:
                # if data retrieved is not in a valid format for plotting
                if (xData.shape[0] != 0):
                    print("-------------------------------")
                    print("Plot not plotted")
                    print(label)
                    print("x data is nan {}\t{}\t{}".format(
                        np.all(np.isnan(xData)), xData, yData))
                    print("y data is nan {}\t{}\t{}".format(
                        np.all(np.isnan(yData)), xData, yData))
                    print("x and y data shapes don't match {}\t{}\t{}".format(xData.shape != yData.shape,
                                                                              xData.shape, yData.shape))
                    print("-------------------------------")

        # plt formatting and conversion
        if not empty_plot:
            self.ax3.legend()
        self.ax3.set_xlabel(self.xAxisLabel)
        self.ax3.set_ylabel(self.yAxisLabel)
        self.figure1.tight_layout()
        self.canv.draw()


class FlowchartWidget(tk.Frame):
    # not implemented
    def __init__(self, parent, controller, *data, title="", xAxis="", yAxis=""):
        self.title = title
        self.xAxisLabel = xAxis
        self.yAxisLabel = yAxis
        tk.Frame.__init__(self, parent)

        self.figure1 = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax = self.figure1.subplots()
        self.ax.axis("off")

        self.d = schemdraw.Drawing(canvas=self.ax)
        self.d += elm.Resistor().label('100KΩ')
        self.d += elm.Capacitor().down().label('0.1μF', loc='bottom')
        self.d += elm.Line().left()
        self.d += elm.Ground()
        self.d += elm.SourceV().up().label('10V')

        self.d.draw(canvas=self.ax, show=False)

        self.canv = FigureCanvasTkAgg(self.figure1, self)
        self.canv.draw()
        self.canv.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

    # def update_data(self):
    #     self.ax3.cla()

    #     for data_source, label in self.data:
    #         xData, yData = data_source()
    #         self.ax3.plot(xData, yData, label=label)

    #     self.ax3.legend()
    #     self.ax3.set_xlabel(self.xAxisLabel)
    #     self.ax3.set_ylabel(self.yAxisLabel)
    #     self.figure1.tight_layout()
    #     self.canv.draw()


class EntryTableWidget(tk.Frame):
    """
    Widget for 

    parent -- frame for which this widget is the direct child of (ie where it was instantiated)
    controller -- root controller object (windows)
    headings_types_defaults -- (list of len 3 lists) one element for each column. Each element is 
                               a len 3 list of the form (heading, type, default)
                               -- heading (str) column heading, appears in 1st row
                               -- type (class) can be any class that can be instanciated as 
                                  type(str) eg int,float etc. Data for this row is converted to this type 
                                  when outputted
                               -- default value applied if type(str) is invalid at any point also acts as
                                  the default value if there is no user input
    """

    def __init__(self, parent, controller, headings_types_defaults):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.headings = [h[0] for h in headings_types_defaults]
        self.types = [h[1] for h in headings_types_defaults]
        self.defaults = [h[2] for h in headings_types_defaults]
        self.rows = 1

        # creates string vars to hold the value for each grid square
        self.data = [[tk.StringVar() for h in self.headings]
                     for i in range(self.rows)]

        # go through each row and instansiate it
        for i in range(self.rows + 1):
            self.rowconfigure(i, weight=1)
            # go through each cell in a row and instanciate it
            for j in range(len(self.headings)):

                if i == 0:
                    # heading row
                    e = tk.Entry(self, width=10,
                                 font=('Calibri', 12))
                    self.columnconfigure(j, weight=1)
                    e.insert(0, self.headings[j])
                    e.config(state=tk.DISABLED)
                else:
                    # each cell is an entry widget which stores its value in a string var self.data[i][j]
                    e = tk.Entry(self, textvariable=self.data[i-1][j], width=10,
                                 font=('Calibri', 12))
                    self.data[i-1][j].set("")
                    # add a trace so whenever a value is changed the output function is called
                    self.data[i -
                              1][j].trace_add("write", lambda *args: self.output_data())
                e.grid(row=i, column=j)

    def output_data(self):
        """
        outputs the data currently in the table to a csv and to the comm_handler
        also applies specified data types to the data and adds a 
        new row if there is no empty row at the end
        """

        # check if there are no empty rows to at the end to type in and add one if there is none
        self.check_for_table_full()
        tmp_data = [[self.data[i][j].get() for j in range(len(self.data[0]))]
                    for i in range(self.rows - 1)]

        # apply types
        for i in range(len(tmp_data)):
            for j in range((len(tmp_data[0]))):
                try:
                    tmp_data[i][j] = self.types[j](tmp_data[i][j])
                except:
                    tmp_data[i][j] = self.types[j](self.defaults[j])

        self.controller.comm_handler._sequance_list = tmp_data.copy()
        self.controller.comm_handler.save_sequence()

    def check_for_table_full(self):
        """
        checks if there is a trailing empty row and if there isn't one adds it
        """
        for tmpStringVar in self.data[-1]:
            if tmpStringVar.get() != "":
                self.rows += 1
                self.rowconfigure(self.rows, weight=1)
                self.data.append([tk.StringVar() for h in self.headings])
                for j in range(len(self.headings)):
                    e = tk.Entry(self, textvariable=self.data[self.rows-1][j], width=10,
                                 font=('Calibri', 12))
                    self.data[self.rows-1][j].set("")
                    self.data[self.rows -
                              1][j].trace_add("write", lambda *args: self.output_data())
                    e.grid(row=self.rows, column=j)

                return

    def update_data(self):
        """
        checks if the user has loaded a new sequence and updates the UI accordingly
        """
        if self.controller.comm_handler._sequence_loaded:
            # fetches new sequence
            tmp_data = self.controller.comm_handler._sequance_list

            # destroys the current UI elements
            for widgets in self.winfo_children():
                widgets.destroy()

            self.rows = tmp_data.shape[0]

            # creats new string var table
            self.data = [[tk.StringVar() for h in self.headings]
                         for i in range(self.rows)]

            # loops  throught the same initialisation process but inserts the value found
            # in the loaded sequence
            for i in range(self.rows + 1):
                self.rowconfigure(i, weight=1)
                for j in range(len(self.headings)):
                    if i == 0:
                        e = tk.Entry(self, width=10,
                                     font=('Calibri', 12))
                        self.columnconfigure(j, weight=1)
                        e.insert(0, self.headings[j])
                        e.config(state=tk.DISABLED)
                    else:
                        e = tk.Entry(self, textvariable=self.data[i-1][j], width=10,
                                     font=('Calibri', 12))
                        if tmp_data[i-1][j] != self.defaults[j]:
                            e.insert(0, tmp_data[i-1][j])
                            self.data[i-1][j].set(tmp_data[i-1][j])
                        else:
                            self.data[i-1][j].set("")
                        self.data[i -
                                  1][j].trace_add("write", lambda *args: self.output_data())
                    e.grid(row=i, column=j)

            self.controller.comm_handler._sequence_loaded = False
            self.check_for_table_full()


class PlotDataDisplayWidget(tk.Frame):
    """
    forms a grid of labels and values to display updating values and has an associated button 
    to turn on and off plotting on an associated graph

    parent -- frame for which this widget is the direct child of (ie where it was instantiated)
    controller -- root controller object (windows)
    *data -- list of 3 element lists each element containing (label, source, button_func)
             -- label (str) 
             -- source (callable object) a function that returns a singal value to be displayed
             -- button_func (callable object) the function that gets triggered when the 
                plotting/not plotting button is pressed
    columns -- sets how many columns the data will be displayed in, defaults to 1
    """

    def __init__(self, parent, controller, *data, columns=1):
        tk.Frame.__init__(self, parent)
        rowNum = 0
        colNum = 0
        self.rows = {}
        self.dataSources = {}

        # configure column sizes
        for i in range(columns):
            self.columnconfigure(3*i, weight=1)
            self.columnconfigure(3*i + 1, weight=1)
            self.columnconfigure(3*i + 2, weight=1)

        button_arguments = [[] for i in range(columns)]
        for label, source, button_func in list(data):

            # creating the arguments that will later be used to create the button
            # these are initial text, alternate text, callback function
            button_arguments[colNum].append(
                ("Plotting", "Not Plotting", button_func))

            # configure each row and add 2 labels for the label and the data
            self.rowconfigure(rowNum, weight=1)
            labelTK = tk.Label(self, text=label + ":",  font=("Calibri", 13))
            dataBoxTK = tk.Label(self, text="{:.2f}".format(
                float(source())), font=("Calibri", 13))

            # set the positions of the label and databox
            labelTK.grid(row=rowNum, column=3 * colNum, sticky="NSE")
            dataBoxTK.grid(row=rowNum, column=3 * colNum + 1, sticky="NSW")

            # save relevant information about each entry
            self.rows[label] = (labelTK, dataBoxTK)
            self.dataSources[label] = source
            colNum += 1
            if colNum == columns:
                colNum = 0
                rowNum += 1

        # create the buttons and place them next to the relevant labels and data
        for i in range(columns):
            plotting_buttons = ButtonStackWidget(
                self, controller, *button_arguments[i])
            plotting_buttons.grid(
                row=0,  rowspan=int(np.floor(len(list(data))/columns)), column=3 * i + 2, sticky="NSW")

    def update_data(self):
        """
        Fetch new data and refresh all of the data displayed
        """
        rowLabels = self.rows.keys()
        for key in rowLabels:
            row = self.rows[key]
            for i, box in enumerate(row[1:]):
                box.config(text="{:.2f}".format(float(self.dataSources[key]() if len(
                    row[1:]) == 1 else self.dataSources[key][i+1]())))


class DataDisplayWidget(tk.Frame):
    """
    forms a grid of labels and values to display updating values and has an associated button 
    to turn on and off plotting on an associated graph

    parent -- frame for which this widget is the direct child of (ie where it was instantiated)
    controller -- root controller object (windows)
    *data -- list of 2 element lists each element containing (label, source)
             -- label (str) 
             -- source (callable object) a function that returns a singal value to be displayed
    columns (optional) -- sets how many columns the data will be displayed in, defaults to 1
    """

    def __init__(self, parent, controller, *data, columns=1):
        tk.Frame.__init__(self, parent)
        rowNum = 0
        colNum = 0
        self.rows = {}
        self.dataSources = {}

        # configure column sizes
        for i in range(columns):
            self.columnconfigure(2*i, weight=1)
            self.columnconfigure(2*i + 1, weight=1)

        for label, source in list(data):
            # configure each row and add 2 labels one for the label and one for the data
            self.rowconfigure(rowNum, weight=1)
            labelTK = tk.Label(self, text=label + ":",  font=("Calibri", 13))
            dataBoxTK = tk.Label(self, text="{:.2f}".format(
                float(source())), font=("Calibri", 13))

            # set the positions of the label and databox
            labelTK.grid(row=rowNum, column=2 * colNum, sticky="NSE")
            dataBoxTK.grid(row=rowNum, column=2 * colNum + 1, sticky="NSW")

            # save relevant information about each entry
            self.rows[label] = (labelTK, dataBoxTK)
            self.dataSources[label] = source
            colNum += 1
            if colNum == columns:
                colNum = 0
                rowNum += 1

    def update_data(self):
        """
        Fetch new data and refresh all of the data displayed
        """
        rowLabels = self.rows.keys()
        for key in rowLabels:
            row = self.rows[key]
            for i, box in enumerate(row[1:]):
                box.config(text="{:.2f}".format(float(self.dataSources[key]() if len(
                    row[1:]) == 1 else self.dataSources[key][i+1]())))


class OnOffButtonWidget(tk.Button):
    """
    Simple toggle button that calls a provided callback function whenever it's triggered

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    onLabel -- (str) label shown on the button when the state is on/true
    onLabel -- (str) label shown on the button when the state is off/false
    callback -- (callable object) function called when the button is pressed. It is passed one argument, 
                the new state as a boolean (on = true, off = false)
    defaultVal (optional) -- (boolean) sets the startup state of the button, defaults to false if not specified
    """

    def __init__(self, parent, onLabel, offLabel, callback, defaultVal=False):
        # create a button with the appropriate label for the current state and
        # a callback to the internalCallback function below
        tk.Button.__init__(
            self, parent, text=onLabel if defaultVal else offLabel, command=self.internalCallback)
        self.state = defaultVal
        self.onLabel = onLabel
        self.offLabel = offLabel
        self.callback = callback

    def internalCallback(self):
        """
        toggle the state, update the text displayed and then call the callback function 
        supplied (self.callback) 
        """
        self.state = not self.state
        self.config(text=self.onLabel if self.state else self.offLabel)
        self.callback(self.state)


class ButtonStackWidget(tk.Frame):
    """
    Stack of simple toggle buttons (OnOffButtonWidget)

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    *data -- list of lists with either 3 or 4 elements as shown below
        onLabel -- (str) label shown on the button when the state is on/true
        onLabel -- (str) label shown on the button when the state is off/false
        callback -- (callable object) function called when the button is pressed. It is passed one argument, 
                    the new state as a boolean (on = true, off = false)
        defaultVal (optional) -- (boolean) sets the startup state of the button, defaults to false if not specified
    columns (optional) -- sets how many columns the data will be displayed in, defaults to 1
    """

    def __init__(self, parent, controller, *data, columns=1):
        # takes an object with the shape (onLabel, offLabel, output changed callback)
        tk.Frame.__init__(self, parent)
        rowNum = 0
        colNum = 0

        # loop through all the buttons and create them in turn
        for buttonArguments in list(data):
            # set row and column sizes
            self.columnconfigure(colNum, pad=30, weight=1)
            self.rowconfigure(rowNum, weight=1)

            switch = OnOffButtonWidget(self, *buttonArguments)
            # positon button
            switch.grid(row=rowNum, column=colNum, sticky="NSEW")
            colNum += 1
            # go to the next row is all columns on this row are full
            if colNum == columns:
                colNum = 0
                rowNum += 1


class dataInputStackWidget(tk.Frame):
    """
    stack of text inputs with associated label

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    *data -- list of lists with 2 elements as shown below
             label -- (str)
             output -- (callable object) Is called when the value in the box is changed and is 
                       passed the new value as a string
    """

    def __init__(self, parent, controller, *data):
        tk.Frame.__init__(self, parent)
        rowNum = 0

        # configure the size of the columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # dictionary pointing to the string variables associated with each box
        # the unique name assigned to each tkInter StringVar is used as the key
        # this is obtained by myStringVar._name and is also passed as the first argument
        # by tkInter when the text is edited
        self.outputBoxes = {}

        # dictionary of the user defined callback functions associated with each input box
        # the same keys as above are used
        self.outputFunctions = {}

        for label, output in list(data):
            # create a new stringVar and set its initial value to 0
            tmpStringVar = tk.StringVar()
            tmpStringVar.set(0)

            # store the string var in the dictionary
            self.outputBoxes[tmpStringVar._name] = tmpStringVar

            # configure the size of the row and create the label and entry box objects
            self.rowconfigure(rowNum, weight=1)
            labelTK = tk.Label(self, text="" if label ==
                               "" else label + ":",  font=("Calibri", 13))
            dataBoxTK = tk.Entry(self, textvariable=self.outputBoxes[tmpStringVar._name], font=(
                "Calibri", 13), width=5)

            # add a trace to the entry box so that whenever the value is edited the user provided callback
            # function is called and passed the current value of the entry box
            self.outputBoxes[tmpStringVar._name].trace_add(
                "write", lambda *args: self.outputFunctions[args[0]](self.outputBoxes[args[0]].get()))

            # store the callback function in the associated dictionary
            self.outputFunctions[tmpStringVar._name] = output
            labelTK.grid(row=rowNum, column=0, sticky="NSE")
            dataBoxTK.grid(row=rowNum, column=1, sticky="NSW")
            rowNum += 1


class pumpControlWidget(tk.Frame):
    """
    widget for displaying the current state of all the pumps and giving the ability 
    to overide the speed to a desired state. 
    Has the overall form of pumpName|pumpSpeed|overideToggle|overideSpeed

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # configure column and row sizes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create title row of labels
        labelSpeed = tk.Label(self, text="Speed")
        labelSpeed.grid(row=0, column=0, sticky="NSEW")

        labelOveride = tk.Label(self, text="Override")
        labelOveride.grid(row=0, column=1, sticky="NSEW")

        labelOverideSpeed = tk.Label(self, text="Override Speed")
        labelOverideSpeed.grid(row=0, column=2, sticky="NSEW")

        # create a data display widget with the pump names as the labels and the current pump speed as the data
        pumpSpeed = DataDisplayWidget(self, controller, ("Media OD Sensor Pump", lambda: controller.comm_handler._Pump[0, -1]),
                                      ("Media Inlet Pump",
                                       lambda: controller.comm_handler._Pump[1, -1]),
                                      ("Media Transfer Pump",
                                       lambda: controller.comm_handler._Pump[2, -1]),
                                      ("Main OD Sensor Pump",
                                       lambda: controller.comm_handler._Pump[3, -1]),
                                      ("Waste Pump",
                                       lambda: controller.comm_handler._Pump[4, -1]),
                                      ("Sterilzation Input Pump",
                                       lambda: controller.comm_handler._Pump[5, -1]),
                                      ("Fossil Record Pump",
                                       lambda: controller.comm_handler._Pump[6, -1]),
                                      ("Main Mixer",
                                       lambda: controller.comm_handler._Pump[7, -1]),
                                      ("Media Mixer", lambda: controller.comm_handler._Pump[8, -1]))

        # position this display widget in the first column
        pumpSpeed.grid(row=1, column=0, sticky="NSEW")

        # generate a button stack to act as the overide toggle for each pump and place it in the 2nd column
        pumpOverideButtons = ButtonStackWidget(self, controller,
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   0, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   1, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   2, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   3, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   4, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   5, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   6, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(
                                                   7, bool(x))),
                                               ("On", "Off", lambda x: controller.comm_handler.set_pump_overide(8, bool(x))))
        pumpOverideButtons.grid(row=1, column=1, sticky="NSEW")

        # create a data input stack to take in the desired overide speeds and place it in the 3rd column
        # the inbuilt label is set to "" to be empty
        pumpOverideSpeeds = dataInputStackWidget(self, controller, ("", lambda x: controller.comm_handler.set_pump_speed(0, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     1, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     2, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     3, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     4, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     5, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     6, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(
                                                     7, x)),
                                                 ("", lambda x: controller.comm_handler.set_pump_speed(8, x)))
        pumpOverideSpeeds.grid(row=1, column=2, sticky="NSEW", padx=10)


class groupParameterUpdateWidget(tk.Frame):
    """
    widget the groups together a series of variables and groups them with a singular button to act as a
    callback of somekind

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    title -- (str) title of the group
    callback -- function to call then the update function is called
    *data -- arguments passed to the dataDisplayWidget, list of lists with 2 elements as shown below
             label -- (str)
             output -- (callable object) Is called when the value in the box is changed and is 
                       passed the new value as a string
    """

    def __init__(self, parent, controller, title, callback, *data):
        tk.Frame.__init__(
            self, parent, highlightbackground="black", highlightthickness=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10, pad=10)

        self.title = title

        self.callback = callback

        title_label = tk.Label(self, text=self.title,
                               font=("Calibri", 13, "bold"))
        title_label.grid(row=0, column=0, sticky="NSW", padx=20)

        upload_button = tk.Button(
            self, text="Upload", command=self.callback, bg="green", fg="white")

        upload_button.grid(column=1, row=0, sticky="NSE", padx=20, pady=20)

        input_widget = dataInputStackWidget(
            self, controller, *data)
        input_widget.grid(column=0, row=1, columnspan=2)


class MenuBarWidget(tk.Frame):
    """
    widget that displays the menu bar at the top of each page and changes the displayed page 
    if another tab is selected 

    parent -- frame for which this widget is the direct child of (ie where it was instantiated) 
    controller -- root controller object (windows)
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)

        pageNames = controller.frames.keys()
        self.labels = []

        colNum = 0
        for pageName in pageNames:
            # create a lable with a callback function attached which calls the
            # show frame function in the windows class with the appropriate pageName
            tmplabel = tk.Button(self, text=pageName, command=partial(
                controller.show_frame, pageName))
            tmplabel.grid(row=0, column=colNum, sticky="NSEW")
            self.labels.append(tmplabel)
            colNum += 1
