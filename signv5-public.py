from Tkinter import *
import tkFont
import RPi.GPIO as GPIO
import tkSimpleDialog
import time
import os
from slackclient import SlackClient

# Valve Initialization Code Start

valve_1_close = 6
valve_1_open = 5
valve_2_close = 13
valve_2_open = 19

GPIO.setmode(GPIO.BCM) # BCM style pins
chan_list = [5,6,13,19]
GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)

# # Ensure valves are closed on boot

#GPIO.output(valve_1_close, GPIO.HIGH)
#GPIO.output(valve_2_close, GPIO.HIGH)
#GPIO.output(valve_1_close, GPIO.LOW)
#GPIO.output(valve_2_close, GPIO.LOW)

# Valve Initialization Code End

slack_token = os.environ["SLACK_BOT_TOKEN"]

sc = SlackClient(slack_token)

sc.api_call(
        "chat.postMessage",
        channel="CGPUM0V98",
        text="BURP!"
        )

win = Tk()
win.overrideredirect(1)

myFont = tkFont.Font(family = "Helvetica", size = 128, weight = 'bold')

barState = 0;
passcodes = {"<RFID NUMBERS>":"<DISPLAYED NAME>"}

def barOpen(event=None):
    print("Drinking Station: One State Toggled")
    global barState
    global passcodes
    
    if barState == 1:
        barButton["text"] = "Bar Closed"
        barState = 0
        barButton["activebackground"] = "red"
        barButton["bg"] = "red"
        sc.api_call(
            "chat.postMessage",
            channel="CGPUM0V98",
            text="Drinking Station: One is closed. :crying_cat_face:"
        )
        # Close valves
        GPIO.output(valve_1_open, GPIO.LOW)
        GPIO.output(valve_2_open, GPIO.LOW)
        GPIO.output(valve_1_close, GPIO.HIGH)
        GPIO.output(valve_2_close, GPIO.HIGH)
        # time.sleep(5)
        # GPIO.output(valve_1_close, GPIO.LOW)
        # GPIO.output(valve_2_close, GPIO.LOW)
    else:
        barButton["text"] = "Enter Password:"
        win.update();
        password = tkSimpleDialog.askstring("Login", "What's the Password")
        if(password == "exit"):
            exitProgram()                
        if(passcodes.has_key(password)):
            bartender = passcodes.get(password)
            barButton["text"] = "Bar Open \n\n"+bartender+" is Bartending!"
            barState = 1
            barButton["activebackground"] = "green"
            barButton["bg"] = "green"
            
            sc.api_call(
                "chat.postMessage",
                channel="CGPUM0V98",
                text="Drinking Station: One is open! "+bartender+" is bartending! :cheers:"
            )
            # Open the valves!
	    GPIO.output(valve_1_close, GPIO.LOW)
            GPIO.output(valve_2_close, GPIO.LOW)
            GPIO.output(valve_1_open, GPIO.HIGH)
            GPIO.output(valve_2_open, GPIO.HIGH)
            #  time.sleep(5)
            # GPIO.output(valve_1_open, GPIO.LOW)
            # GPIO.output(valve_2_open, GPIO.LOW)
        else:
            barButton["text"] = "Incorrect Password"
            win.update()
            time.sleep(1)
            barButton["text"] = "Bar Closed"
            
            if(password != "exit"):
                sc.api_call(
                    "chat.postMessage",
                    channel="CGPUM0V98",
                    text="Intruder Alert!!! Intruder Alert!!! :alien:"
                )

def exitProgram():
    print("Exiting")
    #GPIO.cleanup()
    win.quit()

#win.bind('<Enter>',barOpen)
win.title("Drinking Station: One")
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.bind('<Return>',barOpen)


#exitButton = Button(win, text = "EXIT", font = myFont, command = exitProgram, height = 2, width = 6)
#exitButton.pack(side = BOTTOM);

barButton = Button(win,wraplength=win.winfo_screenwidth(), text = "Bar Closed",command = barOpen, bg="red",activebackground="red",  font = myFont, height = win.winfo_screenheight(), width = win.winfo_screenwidth())
#barButton.bind('<Button-1>',barOpen)
barButton.pack()
mainloop()





