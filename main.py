"""
Insulin Dose Calculator
Written by: Nathan Able
SDEV 140 MW
Professor Ray Storer

Calculate a recommended insulin dose based on both insulin:carb ratio and current BG with correction factoring

"""
# import tkinter module
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from os.path import exists


def setCalculationValues():
    """
    Open the settings file and extract the saved ration and correction values
    :return: tuple (ratio, correction)
    """
    with open('settings.txt') as f:
        ratio = f.readline()
        correction = f.readline()
        calculationsValues = (ratio, correction)
    return calculationsValues


def updateInfoFromSettings():
    """
    Use the saved values to update the label display of those values in the calculations window
    :return: None
    """
    # pull in the values set by settings
    calculationsValues = setCalculationValues()
    ratio = calculationsValues[0]
    correction = calculationsValues[1]
    # Update the labels respectively
    lblCorrection.config(text="1:" + correction)
    lblRatio.config(text="1:" + ratio)


def calculateClick():
    """
    Initiate the calculation and display results in a message box
    :return: None
    """
    # Validate there are values set before continuing
    if calcValidate1.cget("text") == "Not Set" or calcValidate2.cget("text") == "Not Set":
        messagebox.showwarning("No Settings", "Ratio and Correction not set!\n"
                                              "Go to settings to configure before calculating.")
    else:
        try:
            # If the values entered are not Integers an exception is created
            carbs = int(etrCarbs.get())
            bg = int(etrBG.get())
        except:
            # Set dumb values on exception that will trigger a kickout in the next check
            carbs = 0
            bg = 0
        if (carbs > 0) and (bg > 0):
            calculationValues = setCalculationValues()
            ratio = int(calculationValues[0])
            factor = int(calculationValues[1])
            # Calculate the base dose using the Insulin:Carb ratio
            unit1 = round(carbs / ratio, 2)
            # Calculate the correction adjustment using the Correction Factor and ADA standard of 110 ml/dL
            unit2 = round((bg - 110) / factor, 2)
            # Combine for total dose recommendation
            dose = unit1 + unit2
            # Display results
            messagebox.showinfo("Dose Calculation", "Base Dose Calculation - " + str(unit1) + "\n"
                                "Correction Dose Calculation - " + str(unit2) + "\n"
                                "Total Dose - " + str(dose))
        else:
            # Return error message if blank or wrong value type
            messagebox.showwarning("Invalid Data", "Invalid data entered!\n"
                                   "Please use only whole numbers for the Carbs and BG ml/dL")


# Function for Settings window
def openSettingsWindow():
    """
    Open the settings window
    :return: None
    """

    # Nested function for Save button
    def settingsSave():
        """
        Save the settings to a file
        :return: None
        """
        try:
            # If the values entered are not an integer an exception is created
            ratio = int(setrRatio.get())
            factor = int(setrFactor.get())
        except:
            # Creates dumb values to the exception which will allow the program to continue and still alert the user
            # to the issue
            ratio = ""
            factor = ""
            # Verify the values entered were an Integer. If they raised an exception the dumb values will fail check
        if isinstance(ratio, int) and isinstance(factor, int):
            # Create/overwrite the settings file
            f = open('settings.txt', 'w')
            f.write(str(ratio) + '\n' + str(factor))
            f.close()
            messagebox.showinfo("Saved", "Settings have been saved.")
            # Close the settings window
            settingsWindow.destroy()
            # Update any changes made
            updateInfoFromSettings()
        else:
            # Create a warning to the user that the data they entered was not valid in some way
            messagebox.showwarning("Not Saved", "Invalid Entry!\n"
                                                "Please use whole numbers only.\n"
                                                "Please complete both fields.")

    # Attach it to the primary window
    settingsWindow = Toplevel(calculator)
    settingsWindow.title("Settings")
    # Prevents multiple instances of the settings window and returns focus to window on error message
    settingsWindow.grab_set()
    # Labels
    slbl1 = Label(settingsWindow, text="Insulin:Carb Ratio - ", font=("Arial Bold", 12))
    slbl2 = Label(settingsWindow, text="1:", font=("Arial", 12))
    slbl3 = Label(settingsWindow, text="Correction Factor - ", font=("Arial Bold", 12))
    slbl4 = Label(settingsWindow, text="1:", font=("Arial", 12))

    # Data Entry
    setrRatio = Entry(settingsWindow, font=("Arial", 12), width=8)
    setrFactor = Entry(settingsWindow, font=("Arial", 12), width=8)

    # Buttons
    sbtn1 = Button(settingsWindow, text="Save", command=settingsSave)
    sbtn2 = Button(settingsWindow, text="Cancel", command=settingsWindow.destroy)

    # Layout
    slbl1.grid(column=0, row=0, sticky=W, pady=3, padx=(2, 5))
    slbl2.grid(column=2, row=0, sticky=E, pady=3)
    setrRatio.grid(column=3, row=0, sticky=E, pady=3, padx=(0, 3))
    slbl3.grid(column=0, row=1, sticky=W, pady=(10, 0), padx=(2, 5))
    slbl4.grid(column=2, row=1, sticky=E, pady=(10, 0))
    setrFactor.grid(column=3, row=1, sticky=E, pady=(10, 0), padx=(0, 3))
    sbtn1.grid(column=0, row=4, sticky=W, pady=(15, 3), padx=(0, 10))
    sbtn2.grid(column=3, row=4, sticky=E, pady=(15, 3), padx=(10, 0))


# creating main tkinter window/toplevel
calculator = Tk()
calculator.title("Insulin Dose Calculator")

# Labels
lbl1 = Label(calculator, text="Carbs", font=("Arial Bold", 12))
lbl2 = Label(calculator, text="Current BG mg/dL", font=("Arial Bold", 12))
lbl3 = Label(calculator, text="Insulin:Carb Ratio", font=("Arial Bold", 12))
calcValidate1 = lblCorrection = Label(calculator, text="Not Set", font=("Arial", 12))
lbl5 = Label(calculator, text="Correction Factor", font=("Arial Bold", 12))
calcValidate2 = lblRatio = Label(calculator, text="Not Set", font=("Arial", 12))

# Data Entry
etrCarbs = Entry(calculator, font=("Arial", 12), width=8)
etrBG = Entry(calculator, font=("Arial", 12), width=8)

# Buttons
btn1 = Button(calculator, text="Calculate", command=calculateClick)
btn2 = Button(calculator, text="Settings", command=openSettingsWindow)
btn3 = Button(calculator, text="Exit", command=calculator.destroy)

# Images - Impeded to Labels
img = PhotoImage(file="calculator.png")
img1 = img.subsample(20, 20)
calcImage = Label(calculator, image=img1, text="Calculator.png")
settingimg = PhotoImage(file="settingsicon.png")
settingimg1 = settingimg.subsample(15, 15)
setImage = Label(calculator, image=settingimg1, text="settingicon.png")

# Layout
lbl1.grid(column=0, row=0, sticky=W, pady=3, padx=(10, 100))
etrCarbs.grid(column=0, row=1, sticky=W, pady=3, padx=(10, 100))
lbl2.grid(column=0, row=2, sticky=W, pady=3, padx=(10, 100))
etrBG.grid(column=0, row=3, sticky=W, pady=3, padx=(10, 100))
lbl3.grid(column=0, row=4, sticky=W, pady=3, padx=(10, 100))
lblRatio.grid(column=0, row=5, sticky=W, pady=3, padx=(10, 100))
lbl5.grid(column=0, row=6, sticky=W, pady=3, padx=(10, 100))
lblCorrection.grid(column=0, row=7, sticky=W, pady=3, padx=(10, 100))
btn1.grid(column=3, row=2, sticky=E, pady=3, padx=10)
btn2.grid(column=3, row=5, sticky=E, pady=3, padx=10)
btn3.grid(column=3, row=6, sticky=E, pady=3, padx=10)
calcImage.grid(column=2, row=0, columnspan=2, rowspan=2, padx=(5, 0))
setImage.grid(column=2, row=3, columnspan=2, rowspan=2, padx=(5, 0))
# Check for an existing Settings file
hasSettings = exists("settings.txt")
# Update the label display if there is a settings file
if hasSettings:
    updateInfoFromSettings()
else:
    messagebox.showwarning("No Settings", "There are not any settings currently in place.\n"
                                          "Use the 'Settings' button to set your ratio and correction values.")

calculator.mainloop()
