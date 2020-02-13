from tkinter import *
from tkinter import messagebox


class application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_hand_state_frame(self):
        hand_state_frame = Frame(self)
        hand_state_frame.grid(row=0, column=0)

        self.connection_state_info_label = Label(hand_state_frame, text="Connection state: ")
        self.connection_state_info_label.grid(row=0, column=0)
        self.connection_actual_state_label = Label(hand_state_frame, text="not connected", fg="red")
        self.connection_actual_state_label.grid(row=0, column=1)

        self.hand_action_state_info_label = Label(hand_state_frame, text="Hand's process state: ")
        self.hand_action_state_info_label.grid(row=1, column=0)
        self.hand_actual_action_state_label = Label(hand_state_frame, text="ready", fg="green")
        self.hand_actual_action_state_label.grid(row=1, column=1)

    def create_current_hand_command_frame(self):
        current_hand_command_frame = Frame(self)
        current_hand_command_frame.grid(row=0, column=1)

        self.current_hand_command_label = Label(current_hand_command_frame, text="Current command:")
        self.current_hand_command_label.grid(row=0, column=0)

        temporary_img = PhotoImage(file=r"C:\Users\davep\Unisherbrooke"
                                        r"\Session4\Projet\Project-SLEARH\Image_Library\temporary_img.png")
        # temporary_img1 = temporary_img.subsample(2, 2)
        self.temporary_img_ui = Label(current_hand_command_frame, image=temporary_img)
        self.temporary_img_ui.image = temporary_img
        self.temporary_img_ui.grid(row=1, column=0, columnspan=3)

    def create_hand_control_frame(self):
        hand_control_frame = Frame(self)

        text_entry_frame = Frame(hand_control_frame)
        text_entry_frame.grid(row=1, column=0)
        self.text_entry_label = Label(hand_control_frame, text="Enter text here:", anchor=W)
        self.text_entry_label.grid(row=0, column=0)
        self.text_entry = Entry(text_entry_frame)
        self.text_entry.grid(row=1, column=0, sticky=W, padx=10)

        hand_control_buttons_frame = Frame(hand_control_frame)
        hand_control_buttons_frame.grid(row=0, column=1, padx=50)

        self.stop_button = Button(hand_control_buttons_frame)
        self.stop_button["text"] = "stop"
        self.stop_button["command"] = self.say_stoped
        self.stop_button.grid(row=1, column=1)

        self.pause_button = Button(hand_control_buttons_frame)
        self.pause_button["text"] = "pause",
        self.pause_button["command"] = self.say_paused
        self.pause_button.grid(row=1, column=0)

        self.send_button = Button(hand_control_buttons_frame)
        self.send_button["text"] = "send"
        self.send_button["command"] = self.send_text
        self.send_button.grid(row=0, column=0, columnspan=2)

        hand_control_frame.grid(row=2, column=0, columnspan=2, pady=20)

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
        self.create_hand_state_frame()
        self.create_options_frame()
        self.create_hand_control_frame()
        self.create_current_hand_command_frame()

    def connect(self, widget, signal, event):
        widget.bind(signal, event)

    def send_text(self):
        # TODO: Add sending message to the TextAnalyser and sending message to the arduino here (and wait for the
        #  "message received" before showing info)
        messagebox.showinfo("Sended", "Text is being analyse.")

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
