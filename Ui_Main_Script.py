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

        hand_control_frame.grid(row=2, column=1, columnspan=2)

    def create_options_frame(self):
        options_frame = Frame(self)

        # Configuration and placement for the "Options:" label
        self.options_label = Label(options_frame, text="Options:")
        self.options_label.grid(row=0, column=0, pady=2)

        # Configuration and placement for the "Purpose:" section
        self.purpose_label = Label(options_frame, text="Purpose:")
        self.purpose_label.grid(row=1, column=1, pady=2)
        options_purpose_choices_frame = Frame(options_frame)
        options_purpose_choices_frame.grid(row=2, column=1, padx=2)
        self.purpose_choices_education = Radiobutton(options_purpose_choices_frame, text="Education")
        self.purpose_choices_education.grid(row=0, column=0)
        self.purpose_choices_quiz = Radiobutton(options_purpose_choices_frame, text="Quiz")
        self.purpose_choices_quiz.grid(row=0, column=1)

        # Configuration and placement for the "Mode:" section
        self.mode_label = Label(options_frame, text="Mode:")
        self.mode_label.grid(row=3, column=1, pady=2)
        options_mode_choices_frame = Frame(options_frame)
        options_mode_choices_frame.grid(row=4, column=1, padx=2)
        self.mode_choices_automatic = Radiobutton(options_mode_choices_frame, text="Automatic")
        self.mode_choices_automatic.grid(row=0, column=0)
        self.mode_choices_quiz = Radiobutton(options_mode_choices_frame, text="Quiz")
        self.mode_choices_quiz.grid(row=0, column=1)

        # Configuration and placement for the Glider section
        self.next_letter_speed_glider = Scale(options_frame, label="Second(s) passed on one sign", orient=HORIZONTAL,
                                              to=5.0, from_=1.0, tickinterval=0.25, length=169)
        self.next_letter_speed_glider.grid(row=5, column=1, pady=2)

        options_frame.grid(row=1, column=0)

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
    app.mainloop()
    root.destroy()
