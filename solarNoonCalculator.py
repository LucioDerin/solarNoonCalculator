# ephemerids calculator library
import ephem
import math as m
# dates and times handler
import datetime as dt
# gui's libraries
import tkinter as tk
from tkinter import messagebox
from functools import partial
# plots' library
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# library for result file path
from pathlib import Path

def coordinatesConverter(latDeg, latPrim, latSec, longDeg, longPrim, longSec):
    '''
    Converts coordinates from deg,primes,seconds to decimal degrees
    Parameters:
        @ latDeg, latPrim, latSec: latitudes degrees, arcprimes and arcsecs;
        @ longDeg, longPrim, longSec: longitude degrees, arcprimes and arcsecs;
    Returns:
        @ lat: float, latitude in decimal degrees;
        @ long: float, longitude in decimal degrees;
    '''
    lat = latDeg + latPrim/60. + latSec/3600.
    long = longDeg + longPrim/60. + longSec/3600.
    return lat, long


def daterange(start_date, end_date):
    '''
    Calculates the dates between a starting date and an end date, with step of 1 day.
    Parameters:
        @ start_date: begin date;
        @ end_date: end date;
    Returns:
        A generator of the list of dates;
    '''
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


def getNoon(d, lat, long):
    '''
    Calculates the solar noon of the desired date in the desired location.
    Parameters:
        @ d: date of the day in which calculate the solar noon;
        @ lat, long: coordinates of the place in which the solar noon has to be evaluated;
    Returns:
        @ noonLocal: a datetime object containing the date and time of the solar noon;
    '''
    o = ephem.Observer()
    o.lat, o.long = lat, long
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=d)
    noon = o.next_transit(sun, start=sunrise)
    noonLocal = ephem.localtime(noon)
    return noonLocal


class gui:
    '''
    Implements the GUI of the calculator
    '''

    def __init__(self):
        # window
        self.window = tk.Tk()
        self.window.geometry("400x600")
        self.window.title("Solar Noon Calculator")

        # title
        row = 0
        column = 0
        self.title = tk.StringVar()
        self.title.set("Solar Noon Calculator")
        self.titleLabel = tk.Label(textvariable=self.title)
        self.titleLabel.grid(row=row, column=column, columnspan=10)

        # lat long

        # decimal deg checkbox
        row += 1
        self.decCheckboxState = tk.IntVar()
        self.decCheckbox = tk.Checkbutton(text="Use decimal degrees coordinates",
                                          var=self.decCheckboxState, onvalue=1, offvalue=0,
                                          command=partial(self.__manageCheckbox, "dec"))
        self.decCheckbox.grid(row=row, column=column,
                              columnspan=10, sticky='W')

        # decimal deg input box
        # latitude
        row += 1
        self.latString = tk.StringVar()
        self.latString.set("Lat: ")
        self.latString = tk.Label(textvariable=self.latString)
        self.latString.grid(row=row, column=column)
        column += 1
        self.lat = tk.Entry(width="10", state='disabled')
        self.lat.grid(row=row, column=column)
        # longitude
        column += 1
        self.longString = tk.StringVar()
        self.longString.set("Long: ")
        self.longString = tk.Label(textvariable=self.longString)
        self.longString.grid(row=row, column=column)
        column += 1
        self.long = tk.Entry(width="10", state='disabled')
        self.long.grid(row=row, column=column)

        # deg prim sec checkbox
        column = 0
        row += 1
        self.degCheckboxState = tk.IntVar()
        self.degCheckbox = tk.Checkbutton(text="Use deg prim sec coordinates",
                                          var=self.degCheckboxState, onvalue=1, offvalue=0,
                                          command=partial(self.__manageCheckbox, "deg"))
        self.degCheckbox.grid(row=row, column=column,
                              columnspan=10, sticky='W')
        # deg prim sec input box
        # latitude degs
        row += 1
        column = 0
        self.latString = tk.StringVar()
        self.latString.set("Lat: ")
        self.latString = tk.Label(textvariable=self.latString)
        self.latString.grid(row=row, column=column)
        column += 1
        self.latDeg = tk.Entry(width="5", state='disabled')
        self.latDeg.grid(row=row, column=column)
        column += 1
        self.degString = tk.StringVar()
        self.degString.set("°")
        self.degString = tk.Label(textvariable=self.degString)
        self.degString.grid(row=row, column=column)
        # latitude primes
        column += 1
        self.latPrim = tk.Entry(width="5", state='disabled')
        self.latPrim.grid(row=row, column=column)
        column += 1
        self.primString = tk.StringVar()
        self.primString.set("'")
        self.primString = tk.Label(textvariable=self.primString)
        self.primString.grid(row=row, column=column)
        # latitude seconds
        column += 1
        self.latSec = tk.Entry(width="10", state='disabled')
        self.latSec.grid(row=row, column=column)
        column += 1
        self.secString = tk.StringVar()
        self.secString.set("''")
        self.secString = tk.Label(textvariable=self.secString)
        self.secString.grid(row=row, column=column)
        row += 1
        # longitude degs
        column = 0
        self.longString = tk.StringVar()
        self.longString.set("Long: ")
        self.longString = tk.Label(textvariable=self.longString)
        self.longString.grid(row=row, column=column)
        column += 1
        self.longDeg = tk.Entry(width="5", state='disabled')
        self.longDeg.grid(row=row, column=column)
        column += 1
        self.degString = tk.StringVar()
        self.degString.set("°")
        self.degString = tk.Label(textvariable=self.degString)
        self.degString.grid(row=row, column=column)
        # longitude primes
        column += 1
        self.longPrim = tk.Entry(width="5", state='disabled')
        self.longPrim.grid(row=row, column=column)
        column += 1
        self.primString = tk.StringVar()
        self.primString.set("'")
        self.primString = tk.Label(textvariable=self.primString)
        self.primString.grid(row=row, column=column)
        # longitude seconds
        column += 1
        self.longSec = tk.Entry(width="10", state='disabled')
        self.longSec.grid(row=row, column=column)
        column += 1
        self.secString = tk.StringVar()
        self.secString.set("''")
        self.secString = tk.Label(textvariable=self.secString)
        self.secString.grid(row=row, column=column)

        # Mode dropdown menu
        row += 1
        column = 0
        self.modeString = tk.StringVar()
        self.modeString.set("Select a mode:")
        self.modeLabel = tk.Label(textvariable=self.modeString)
        self.modeLabel.grid(row=row, column=column, columnspan=10)

        row += 1
        column = 0
        self.modes = ['Today Solar Noon', 'Solar Noon up to a certain date']
        self.selectedMode = tk.StringVar()
        self.selectedMode.set('Options')
        self.modeMenu = tk.OptionMenu(self.window, self.selectedMode, *self.modes,
                                      command=partial(self._manageModes, row))
        self.modeMenu.grid(row=row, column=column, columnspan=10)

    def __manageCheckbox(self, value):
        '''
        Manages the checkboxes' states, since they are mutually exclusive.
        Parameters:
            @ value: the value of the checkbox the user has just flagged;
        '''
        # if dec are selected and deg were previously selected
        # unflag deg, disable deg input boxes, enable dec input boxes
        if value == 'dec' and self.degCheckboxState.get():
            self.degCheckboxState.set(0)
            self.latDeg.config(state='disabled')
            self.latPrim.config(state='disabled')
            self.latSec.config(state='disabled')
            self.longDeg.config(state='disabled')
            self.longPrim.config(state='disabled')
            self.longSec.config(state='disabled')
            self.lat.config(state='normal')
            self.long.config(state='normal')
        # if deg are selected and dec were previously selected
        # unflag dec, disable dec input boxes, enable deg input boxes
        elif value == 'deg' and self.decCheckboxState.get():
            self.decCheckboxState.set(0)
            self.lat.config(state='disabled')
            self.long.config(state='disabled')
            self.latDeg.config(state='normal')
            self.latPrim.config(state='normal')
            self.latSec.config(state='normal')
            self.longDeg.config(state='normal')
            self.longPrim.config(state='normal')
            self.longSec.config(state='normal')
        # if dec are selected and there were no previous selections
        # enable dec input boxes
        elif value == 'dec':
            self.lat.config(state='normal')
            self.long.config(state='normal')
        # if deg are selected and there were no previous selections
        # enable deg input boxes
        else:
            self.latDeg.config(state='normal')
            self.latPrim.config(state='normal')
            self.latSec.config(state='normal')
            self.longDeg.config(state='normal')
            self.longPrim.config(state='normal')
            self.longSec.config(state='normal')

    def _manageModes(self, row, value):
        '''
        Manages the modes selected through the dropdown menu: if 'Today Solar Noon' mode is selected,
        just draws the calculate button; if 'Solar Noon up to a certain date' mode is selected,
        draws the end date input box and the calculate button.
        If mode is changed and there was a previous selection/result, it cleans them.
        Parameters:
            @ row: last row occupied by the widgets;
            @ value: mode selected through the dropdown menu;
        '''
        row += 1
        column = 0
        # check if previous selection/results were displayed
        # and, if so, clear them
        try:
            self.calcButton.destroy()
        except:
            pass
        try:
            self.date.destroy()
        except:
            pass
        try:
            self.string.destroy()
        except:
            pass
        try:
            self.result.destroy()
        except:
            pass
        try:
            self.canvas.get_tk_widget().destroy()
        except:
            pass

        # mode distinction
        if value == 'Solar Noon up to a certain date':
            # create the end date input box
            self.string = tk.StringVar()
            self.string.set(
                'Insert the date up to which calculate the solar noons\n(yyyy/mm/dd):')
            self.string = tk.Label(textvariable=self.string)
            self.string.grid(row=row, column=column, columnspan=10)
            row += 1
            column = 0
            self.date = tk.Entry(width=20)
            self.date.grid(row=row, column=column, columnspan=10)
            row += 1
            # create the calculate button
            self.calcButton = tk.Button(
                text='Calculate', bg='green', command=partial(self._getNoon, row))
            self.calcButton.grid(row=row, column=0, columnspan=10)
        elif value == 'Today Solar Noon':
            # create the calculate button
            self.calcButton = tk.Button(
                text='Calculate', bg='green', command=partial(self._getNoon, row))
            self.calcButton.grid(row=row, column=0, columnspan=10)
        # might catch some unwanted dropdown menu's behavior
        else:
            pass

    def _getNoon(self, row):
        '''
        Calculates the solar noon from the input data and mode selection, then displays the result 
        (and saves them in a file if the mode is solar noon up to a certain date).
        Parameters:
            @ row: last row occupied by the widgets;
        '''
        row += 1
        # check if coordinates are given as input
        # if not, raise an error box
        if not self.decCheckboxState.get() and not self.degCheckboxState.get():
            messagebox.showerror(
                "Error!", message="You must insert the coordinates!")
        # if coordinates are given as decimal degrees, directly read them
        if self.decCheckboxState.get():
            lat = str(self.lat.get())
            long = str(self.long.get())
        # if coordinates are given in dec,prime,sec read them and convert them
        else:
            # read input dec,prime,sec
            latDeg = float(self.latDeg.get())
            latPrim = float(self.latPrim.get())
            latSec = float(self.latSec.get())
            longDeg = float(self.longDeg.get())
            longPrim = float(self.longPrim.get())
            longSec = float(self.longSec.get())
            # convert coordinates
            lat, long = coordinatesConverter(
                latDeg, latPrim, latSec, longDeg, longPrim, longSec)
            lat = str(lat)
            long = str(long)

        # if 'Today Solar Noon' mode: calculate today solar noon and display the result
        if self.selectedMode.get() == 'Today Solar Noon':
            # get today date
            d = ephem.now()
            # get solar noon
            noon = getNoon(d, lat, long)
            # if a previous result was displayed, clear it
            try:
                self.result.destroy()
                self.canvas.get_tk_widget().destroy()
            except:
                pass
            # display the result
            self.result = tk.StringVar()
            temp = "The solar noon will be at: " + \
                str(noon.time().strftime('%Hh %Mm %S.%f')[:-4]) + "s; "
            self.result.set(temp)
            self.result = tk.Label(textvariable=self.result)
            self.result.grid(row=row, column=0, columnspan=10)
        # if 'Solar Noon up to a certain date' mode, calculate all the solar noons,
        # write them in a file and display the time equation graph
        else:
            # check if end date was given correctly
            # if not, return
            if not self.date.get():
                messagebox.showerror(
                    "Error!", message="You must specify the date!")
                return
            # iterate over the dates and store the date and respective solar noons (and store also decimal hours for the graph):
            # lists
            dates = []
            times = []
            hours = []
            # read the end date
            stopDate = self.date.get()
            stopDate = dt.date(int(stopDate.split(
                "/")[0]), int(stopDate.split("/")[1]), int(stopDate.split("/")[2]))
            # get today date
            today = ephem.now()
            today = ephem.localtime(today).date()
            # iterate over the dates
            for day in daterange(today, stopDate+dt.timedelta(1)):
                # store values
                dateStr = str(day)
                dates.append(dateStr)
                dateStr += " 9:00"
                dayEphem = ephem.date(dateStr)
                times.append(
                    str(getNoon(dayEphem, lat, long).time().strftime('%Hh %Mm %S.%fs')))
                # convert hour/min/sec to decimal hours for the graph
                graphValues = str(getNoon(day, lat, long).time())
                h = float(graphValues.split(":")[0])
                mins = float(graphValues.split(":")[1])
                secs = float(graphValues.split(":")[2])
                h = h + mins/60. + secs/3600.
                hours.append(h)
            # print the results in a csv file
            path = Path(__file__).with_name('result.csv')
            with path.open('w') as ofile:
                print("Date,SolarNoon", file=ofile)
                for d, t in zip(dates, times):
                    print(d, ",", t, file=ofile)
            
            # if a previous result was displayed, clear it
            try:
                self.result.destroy()
                self.canvas.get_tk_widget().destroy()
            except:
                pass
            # display the success message
            # and the results' file's name
            self.result = tk.StringVar()
            self.result.set(
                "Results have been written in the file 'result.csv'")
            self.result = tk.Label(textvariable=self.result)
            self.result.grid(row=row, column=0, columnspan=10)

            # get rid of the discontinuity due to the legal hour in
            # the time dependance of the solar noons
            for i in range(1, len(hours)):
                if abs(hours[i] - hours[i-1]) > 0.2:
                    hours[i] = m.floor(hours[i-1]) + hours[i] % 1

            # plot the solar noon time dependance (time equation)
            self.figure = Figure(figsize=(3, 3), dpi=80)
            self.subplot = self.figure.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(
                self.figure, master=self.window)
            self.subplot.set_title("Solar Noon\nTime dependance")
            self.subplot.set_xlabel("Time [days]")
            self.subplot.set_ylabel("Solar Noon Hour")
            self.subplot.plot(
                [i for i in range(0, (stopDate-today).days+1)], hours)
            self.canvas.draw_idle()
            self.canvas.get_tk_widget().grid(row=13, columnspan=10)
            self.figure.tight_layout()

    def run(self):
        '''
        Runs the GUI of the program;
        '''
        self.window.mainloop()


if __name__ == "__main__":
    # create an instance of the GUI
    calculator = gui()
    # run the GUI
    calculator.run()
