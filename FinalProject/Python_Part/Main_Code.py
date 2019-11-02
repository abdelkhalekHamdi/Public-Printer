from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tempfile
import win32api
import win32print
import os
from os.path import basename
import time
from win32com.client import Dispatch
from PyPDF2 import PdfFileReader
import wmi
import win32com.client
import serial
import struct
import tkinter.messagebox

arduino = serial.Serial('COM4', 9600)
time.sleep(2)


def Detect_Device(i):
    Device = wmi.WMI()
    wql = "Select * From Win32_USBControllerDevice"
    for item in Device.query(wql):
        i = i + 1  # count nmbr of connected devices
        item.Dependent.Caption
    return i


def Payment_check(pages):
    photo_display.config(image=card)  # display
    root.update()
    arduino.write(struct.pack('>B', pages))
    print("send pages and wait for permission !")
    while True:
        root.permission = len(arduino.readline())
        if root.permission == 3:  # valid card
            return 1
            break
        else:
            return 0
            break


def PDF_page_counter():
    pdf = PdfFileReader(open(root.fileName, 'rb'))
    root.pages = pdf.getNumPages()


def DOC_page_counter():
    word = Dispatch('Word.Application')
    word = word.Documents.Open(root.fileName)
    root.pages = word.ComputeStatistics(2)
    word.Save()
    word.Close()



def Confirm():
    global answer
    photo_display.config(image=confirm)  # display
    answer = tkinter.messagebox.askyesno('PrintF', 'File Name : ' + basename(root.fileName) + '\n'
                                                                                              'Number Of Pages : ' + str(
        root.Number_Of_Pages) + '\n'
                                'Price : ' + str(root.Number_Of_Pages * 5) + ' Da\n'
                                                                             'Do You Want To Confirm ?')


# printing functions

def Print_USB():
    while True:
        usb_det = len(win32api.GetLogicalDriveStrings())  # used to detect usb
        print(usb_det)
        if usb_det > 16:

            photo_display.config(image=USB)  # display
            photo_display.after(2000, lambda: photo_display.config(image=USB))
            root.name = filedialog.askopenfilename(initialdir="G:/")  # choose file from usb
            root.fileName = os.path.abspath(root.name)
            if root.name:  # if a file is chosen
                root.file_path, root.file_format = os.path.splitext(root.fileName)  # file format

                if root.file_format == '.pdf':
                    PDF_page_counter()
                elif root.file_format == '.docx':
                    DOC_page_counter()
                root.Number_Of_Pages = root.pages
                Confirm()
                if answer == True:
                    root.Permission = Payment_check(root.Number_Of_Pages)

                    if root.Permission == 1:
                        win32api.ShellExecute(0, "print", root.fileName, None, None, 0)
                        photo_display.config(image=wait)  # display
                        photo_display.after(root.Number_Of_Pages * 2000,
                                            lambda: photo_display.config(image=Display))  # display
                        break

                    else:
                        photo_display.config(image=recharge)  # display
                        photo_display.after(2000, lambda: photo_display.config(image=Display))
                        break
                else:
                    photo_display.config(image=Display)  # display
                    break




            else:
                photo_display.config(image=NoFile)  # display
                photo_display.after(2000, lambda: photo_display.config(image=Display))  # display
                break

        else:
            photo_display.config(image=NoUSB)
            photo_display.after(3000, lambda: photo_display.config(image=Display))
            break


def Print_Mobile():
    while True:

        usb_det = len(win32api.GetLogicalDriveStrings())  # used to detect usb
        mobile_det = Detect_Device(0)
        print(mobile_det)
        if usb_det < 17 and mobile_det > 12:
            photo_display.config(image=Phone)  # display
            photo_display.after(1000, lambda: photo_display.config(image=Phone))  # display
            root.name = filedialog.askopenfilename(initialdir="C:/Users/IDRIS/Desktop")  # choose file from usb
            root.fileName = os.path.abspath(root.name)
            if root.name:  # if a file is chosen

                root.file_path, root.file_format = os.path.splitext(root.fileName)  # file format

                if root.file_format == '.pdf':
                    PDF_page_counter()
                elif root.file_format == '.docx':
                    DOC_page_counter()
                root.Number_Of_Pages = root.pages

                Confirm()

                if answer == True:
                    root.Permission = Payment_check(root.Number_Of_Pages)

                    if root.Permission == 1:
                        win32api.ShellExecute(0, "print", root.fileName, None, None, 0)
                        photo_display.config(image=wait)  # display
                        photo_display.after(root.Number_Of_Pages * 3000,
                                            lambda: photo_display.config(image=Display))  # display
                        break

                    else:
                        photo_display.config(image=recharge)  # display
                        photo_display.after(2000, lambda: photo_display.config(image=Display))
                        break
                else:
                    photo_display.config(image=Display)  # display
                    break
            else:
                photo_display.config(image=NoFile)  # display
                photo_display.after(3000, lambda: photo_display.config(image=Display))  # display
                break

        else:
            photo_display.config(image=NoPhone)
            photo_display.after(3000, lambda: photo_display.config(image=Display))
            break


def Print_HardDisk():
    photo_display.config(image=hard_disk)  # display
    root.name = filedialog.askopenfilename(initialdir="C:/Users/IDRIS/Desktop/PrintF")  # choose file from usb
    root.fileName = os.path.abspath(root.name)

    if root.name:  # if a file is chosen

        root.file_path, root.file_format = os.path.splitext(root.fileName)  # file format

        if root.file_format == '.pdf':
            PDF_page_counter()
        elif root.file_format == '.docx':
            DOC_page_counter()
        root.Number_Of_Pages = root.pages
        print(root.Number_Of_Pages)
        Confirm()

        if answer == True:

            root.Permission = Payment_check(root.Number_Of_Pages)
            if root.Permission == 1:
                win32api.ShellExecute(0, "print", root.fileName, None, None, 0)
                photo_display.config(image=wait)  # display
                photo_display.after(root.Number_Of_Pages * 3000, lambda: photo_display.config(image=Display))  # display

            else:
                photo_display.config(image=recharge)  # display
                photo_display.after(2000, lambda: photo_display.config(image=Display))

        else:
            photo_display.config(image=Display)  # display


    else:
        photo_display.config(image=NoFile)  # display
        photo_display.after(3000, lambda: photo_display.config(image=Display))  # display


root = Tk()  # empty window
# for full screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.bind("<Escape>", lambda e: e.widget.quit())  # click échap to quit

# Photos
Display = PhotoImage(file="First.png")
BackGround = PhotoImage(file="BG.png")

# Labels contain photo to display
photo_BG = Label(root, image=BackGround)
photo_BG.pack()
photo_display = Label(root, image=Display)
photo_display.place(x=74.5, y=198)

Phone = PhotoImage(file="Phone.png")
USB = PhotoImage(file="USB.png")
NoUSB = PhotoImage(file="NoUSB.png")
NoPhone = PhotoImage(file="NoPhone.png")
hard_disk = PhotoImage(file="PC.png")
NoFile = PhotoImage(file="NoFile.png")
confirm = PhotoImage(file="confirm.png")
card = PhotoImage(file="card.png")
valid = PhotoImage(file="valid.png")
wait = PhotoImage(file="wait.png")
recharge = PhotoImage(file="recharge.png")

# icons
Mobile_icon = PhotoImage(file="phone_icon.png")
scanner_icon = PhotoImage(file="scanner_icon.png")
USB_Icon = PhotoImage(file="usb_icon.png")
folder_icon = PhotoImage(file="folder_icon.png")

# frames
Payment_frame = Frame(root, height="618", width="480")

button1 = Button(root, image=USB_Icon, command=Print_USB)
button1.place(x=850, y=235)
button2 = Button(root, image=Mobile_icon, command=Print_Mobile)
button2.place(x=1100, y=235)
button3 = Button(root, image=folder_icon, command=Print_HardDisk)
button3.place(x=850, y=465)
button4 = Button(root, image=scanner_icon)
button4.place(x=1100, y=465)

root.lift()
root.attributes('-topmost', True)
root.mainloop()
