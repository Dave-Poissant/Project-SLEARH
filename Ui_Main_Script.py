from tkinter import *
from tkinter import messagebox


class application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_hand_control_frame(self):
        hand_control_frame = Frame(self)

        self.stop_button = Button(hand_control_frame)
        self.stop_button["text"] = "stop"
        self.stop_button["command"] = self.say_stoped
        self.stop_button.pack(side=LEFT)

        self.pause_button = Button(hand_control_frame)
        self.pause_button["text"] = "pause",
        self.pause_button["command"] = self.say_paused
        self.pause_button.pack(side=LEFT)

        hand_control_frame.pack(side=LEFT)

    def create_options_frame(self):
        options_frame = Frame(self)
        option_label_frame = Frame(options_frame)
        option_label_frame.pack(side=TOP)

        self.options_label = Label(option_label_frame, text="Options:")
        self.options_label.pack(side=LEFT)

        self.next_letter_speed_glider = Scale(options_frame, label="Second(s) passed on one sign", orient=HORIZONTAL,
                                              to=5.0, from_=1.0, tickinterval=0.25, length=169)
        self.next_letter_speed_glider.pack(side=TOP, pady=10)

        options_frame.pack(side=TOP)

    def create_widgets(self):
        self.create_options_frame()
        self.create_hand_control_frame()

    def connect(self, widget, signal, event):
        widget.bind(signal, event)

    def say_stoped(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("Stoped", "Hand has been stoped.")

    def say_paused(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("Paused", "Hand has been paused.")


if __name__ == "__main__":
    root = Tk("")
    app = application(master=root)
    root.geometry('640x640')
    app.mainloop()
    root.destroy()
