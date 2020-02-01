from tkinter import *
from tkinter import messagebox


class application(Frame):
    def createWidgets(self):
        self.options_label = Label(self, text="Options:")
        self.options_label.pack()

        self.stop_button = Button(self)
        self.stop_button["text"] = "stop"
        self.stop_button["command"] = self.say_stoped
        self.stop_button.pack()

        self.pause_button = Button(self)
        self.pause_button["text"] = "pause",
        self.pause_button["command"] = self.say_paused
        self.pause_button.pack(side=LEFT, pady=5, padx=5)

    def connect(self, widget, signal, event):
        widget.bind(signal, event)

    def say_stoped(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("Stoped", "Hand has been stoped.")

    def say_paused(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("Paused", "Hand has been paused.")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


if __name__ == "__main__":
    root = Tk("")
    app = application(master=root)
    app.mainloop()
    root.destroy()
