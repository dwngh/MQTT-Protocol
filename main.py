from tkinter import *
from mqtt import MqttClient


# GUI
root = Tk()
root.title("MQTT Message")
 
FONT = "Courier 12"
FONT_BOLD = "Helvetica 13 bold"

lable1 = Label(root, text="Internal", font=FONT_BOLD, pady=10, width=20, height=1).grid(
    row=0)

lable2 = Label(root, text="External", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0, column=2)



txt = Text(root, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

txt1 = Text(root, font=FONT, width=60)
txt1.grid(row=1, column=2, columnspan=2)

scrollbar1 = Scrollbar(txt1)
scrollbar1.place(relheight=1, relx=0.974)
 
 
e = Entry(root, font=FONT, width=50)
e.grid(row=2, column=0)

# MQTT Init
def intPrint(msg):
    txt.insert(END, "\n" + msg)
def extPrint(msg):
    txt1.insert(END, "\n" + msg)
mqtt = MqttClient(intPrint, extPrint)

def send():
    send = e.get()
    mqtt.publish(send)
    e.delete(0, END)

def connect():
    mqtt.connect()

def subcribe():
    mqtt.subscribe()


conn = Button(root, text="Connect", font=FONT_BOLD,
              command=connect).grid(row=0, column=1)

conn2 = Button(root, text="Subcribe", font=FONT_BOLD,
              command=subcribe).grid(row=0, column=3)

send = Button(root, text="Send", font=FONT_BOLD,
              command=send).grid(row=2, column=1)

def on_closing():
    if mqtt.isConnected():
        mqtt.disconnect()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()