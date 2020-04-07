from Backend_Scripts import TextAnalyser
from Backend_Scripts import Configuration
from Backend_Scripts import EventHandler
from Backend_Scripts import Communication
from tkinter import *
from tkinter import messagebox
from enum import Enum
import os
import glob


current_directory = os.getcwd()
images_directory = None
quiz_purpose_img_dir = None
education_purpose_img_dir = None

if sys.platform.startswith('win'):
    images_directory = str(current_directory) + "\\Image_Library\\"
    quiz_purpose_img_dir = "Quiz_purpose_img\\sign_"
    education_purpose_img_dir = "Education_purpose_img\\letter_"
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    images_directory = str(current_directory) + "/Image_Library/"
    quiz_purpose_img_dir = "Quiz_purpose_img/sign_"
    education_purpose_img_dir = "Education_purpose_img/letter_"
elif sys.platform.startswith('darwin'):
    images_directory = str(current_directory) + "/Image_Library/"
    quiz_purpose_img_dir = "Quiz_purpose_img/sign_"
    education_purpose_img_dir = "Education_purpose_img/letter_"
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')

class ModeEnum(Enum):
    Automatic = 1
    Step = 2


class PurposeEnum(Enum):
    Education = 1
    Quiz = 2


class application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.__mode_option_state__ = IntVar()
        self.__purpose_option_state__ = IntVar()
        EventHandler.Instance.set_ui_adress(self)
        Communication.Instance.set_ui_adress(self)
        Communication.Instance.start_thread()

    def change_connected_state(self, state):
        if state:
            try:
                self.connection_actual_state_label["text"] = "connected"
                self.connection_actual_state_label["fg"] = "green"
            except:
                return
        else:
            try:
                self.connection_actual_state_label["text"] = "not connected"
                self.connection_actual_state_label["fg"] = "red"
            except:
                return

    def change_hand_ready_state(self, state):
        if state:
            try:
                self.hand_actual_action_state_label["text"] = "ready"
                self.hand_actual_action_state_label["fg"] = "green"
            except:
                return
        else:
            try:
                self.hand_actual_action_state_label["text"] = "not ready"
                self.hand_actual_action_state_label["fg"] = "red"
            except:
                return

    def change_state_picture(self, accepted_command, command):
        if self.__purpose_option_state__ == PurposeEnum.Education:
            if accepted_command:
                if os.path.exists(images_directory+education_purpose_img_dir+str(command)):
                    current_operation_img = PhotoImage(file=images_directory+education_purpose_img_dir+str(command))
                    self.temporary_img_ui.configure(image=current_operation_img)
                    self.temporary_img_ui.image = current_operation_img
                else:
                    no_img_found_img = PhotoImage(file=images_directory + "no_img_found_img.png")
                    self.temporary_img_ui.configure(image=no_img_found_img)
                    self.temporary_img_ui.image = no_img_found_img

            else:
                no_current_operation_img = PhotoImage(file=images_directory + "no_operation_img.png")
                self.temporary_img_ui.configure(image=no_current_operation_img)
                self.temporary_img_ui.image = no_current_operation_img

        elif self.__purpose_option_state__ == PurposeEnum.Quiz:
            if accepted_command:
                if os.path.exists(images_directory+quiz_purpose_img_dir+str(command)):
                    current_operation_img = PhotoImage(file=images_directory+quiz_purpose_img_dir+str(command))
                    self.temporary_img_ui.configure(image=current_operation_img)
                    self.temporary_img_ui.image = current_operation_img
                else:
                    no_img_found_img = PhotoImage(file=images_directory + "no_img_found_img.png")
                    self.temporary_img_ui.configure(image=no_img_found_img)
                    self.temporary_img_ui.image = no_img_found_img

            else:
                no_current_operation_img = PhotoImage(file=images_directory + "no_operation_img.png")
                self.temporary_img_ui.configure(image=no_current_operation_img)
                self.temporary_img_ui.image = no_current_operation_img

    def get_mode_option_state(self):
        return self.__mode_option_state__

    def get_purpose_option_state(self):
        return self.__purpose_option_state__

    def set_mode_option_state(self, new_value):
        if new_value == ModeEnum.Automatic or ModeEnum.Step:
            self.__mode_option_state__ = new_value

    def set_purpose_option_state(self, new_value):
        if new_value == PurposeEnum.Education or PurposeEnum.Quiz:
            self.__purpose_option_state__ = new_value

    def create_hand_state_frame(self):
        hand_state_frame = Frame(self)
        hand_state_frame.grid(row=0, column=0, stick=W)

        self.connection_state_info_label = Label(hand_state_frame, text="Connection state: ")
        self.connection_state_info_label.grid(row=0, column=0, stick=W)
        self.connection_actual_state_label = Label(hand_state_frame, text="not connected", fg="red")
        self.connection_actual_state_label.grid(row=0, column=1)

        self.hand_action_state_info_label = Label(hand_state_frame, text="Hand's process state: ")
        self.hand_action_state_info_label.grid(row=1, column=0, stick=W)
        self.hand_actual_action_state_label = Label(hand_state_frame, text="ready", fg="green")
        self.hand_actual_action_state_label.grid(row=1, column=1)

    def create_current_hand_command_frame(self):
        current_hand_command_frame = Frame(self)
        current_hand_command_frame.grid(row=1, column=1)

        self.current_hand_command_label = Label(current_hand_command_frame, text="Current command:")
        self.current_hand_command_label.grid(row=0, column=0, stick=W)

        no_current_operation_img = PhotoImage(file=images_directory+"no_operation_img.png")
        self.temporary_img_ui = Label(current_hand_command_frame, image=no_current_operation_img)
        self.temporary_img_ui.image = no_current_operation_img
        self.temporary_img_ui.grid(row=1, column=0, columnspan=3)

    def create_hand_control_frame(self):
        hand_control_frame = Frame(self)

        self.line_between_control_options_canvas = Canvas(hand_control_frame, bg='black', height=1.5, width=556)
        self.line_between_control_options_canvas.grid(stick=W, row=0, column=0, columnspan=3)

        text_entry_frame = Frame(hand_control_frame)
        text_entry_frame.grid(row=2, column=0)
        self.text_entry_label = Label(hand_control_frame, text="Enter text here:", anchor=W)
        self.text_entry_label.grid(row=1, column=0, stick=W)
        self.text_entry = Entry(text_entry_frame, width=60)
        self.text_entry.grid(row=0, column=0, sticky=W, padx=10)

        hand_control_buttons_frame = Frame(hand_control_frame)
        hand_control_buttons_frame.grid(row=1, column=1, padx=50)

        self.stop_button = Button(hand_control_buttons_frame)
        self.stop_button["text"] = "stop"
        self.stop_button["command"] = self.do_stop
        self.stop_button.grid(row=1, column=1, pady=5)

        self.pause_button = Button(hand_control_buttons_frame)
        self.pause_button["text"] = "pause",
        self.pause_button["command"] = self.do_pause
        self.pause_button.grid(row=1, column=0)

        self.send_button = Button(hand_control_buttons_frame)
        self.send_button["text"] = "send"
        self.send_button["command"] = self.send_text
        self.send_button.grid(row=0, column=0, columnspan=2)

        self.move_motor_1 = Button(hand_control_buttons_frame)
        self.move_motor_1["text"] = "move 1"
        self.move_motor_1["command"] = self.send_movement_motor_1
        self.move_motor_1.grid(row=2, column=0)

        self.move_motor_2 = Button(hand_control_buttons_frame)
        self.move_motor_2["text"] = "move 2"
        self.move_motor_2["command"] = self.send_movement_motor_2
        self.move_motor_2.grid(row=2, column=1)

        hand_control_frame.grid(row=2, column=0, columnspan=2, pady=20, stick=W)

    def create_options_frame(self):
        options_frame = Frame(self)
        self.set_purpose_option_state(PurposeEnum.Education)
        self.set_mode_option_state(ModeEnum.Automatic)

        # Configuration and placement for the "Options:" label
        self.options_label = Label(options_frame, text="Options:")
        self.options_label.grid(row=0, column=0, pady=2)

        # Configuration and placement for the "Purpose:" section
        self.purpose_label = Label(options_frame, text="Purpose:")
        self.purpose_label.grid(row=1, column=0, pady=2, stick=W)
        options_purpose_choices_frame = Frame(options_frame)
        options_purpose_choices_frame.grid(row=2, column=1, padx=2)
        self.purpose_choices_education = Radiobutton(options_purpose_choices_frame, text="Education",
                                                     var=self.__purpose_option_state__, value=PurposeEnum.Education,
                                                     command=self.send_new_purpose_option)
        self.purpose_choices_education.select()
        self.purpose_choices_education.grid(row=0, column=0)
        self.purpose_choices_quiz = Radiobutton(options_purpose_choices_frame, text="Quiz",
                                                var=self.__purpose_option_state__, value=PurposeEnum.Quiz,
                                                command=self.send_new_purpose_option)
        self.purpose_choices_quiz.deselect()
        self.purpose_choices_quiz.grid(row=0, column=1)

        # Configuration and placement for the "Mode:" section
        self.mode_label = Label(options_frame, text="Mode:")
        self.mode_label.grid(row=3, column=0, pady=2, stick=W)
        options_mode_choices_frame = Frame(options_frame)
        options_mode_choices_frame.grid(row=4, column=1, padx=2)
        self.mode_choices_automatic = Radiobutton(options_mode_choices_frame, text="Automatic",
                                                  var=self.__mode_option_state__, value=ModeEnum.Automatic,
                                                  command=self.set_mode_option_automatic)
        # command=self.send_new_mode_option)
        self.mode_choices_automatic.select()
        self.mode_choices_automatic.grid(row=0, column=0)
        self.mode_choices_step = Radiobutton(options_mode_choices_frame, text="Step", var=self.__mode_option_state__,
                                             value=ModeEnum.Step,
                                             command=self.set_mode_option_step)
        # command=self.send_new_mode_option)
        self.mode_choices_step.deselect()
        self.mode_choices_step.grid(row=0, column=1)

        # Configuration and placement for the Glider section
        self.next_letter_speed_glider = Scale(options_frame, label="Second(s) passed on one sign", orient=HORIZONTAL,
                                              to=10.0, from_=1.0, tickinterval=0.25, length=169)
        self.next_letter_speed_glider["command"] = self.send_new_speed_on_letter
        self.next_letter_speed_glider.grid(row=5, column=1, pady=2)

        options_frame.grid(row=1, column=0, stick=W)

    def create_widgets(self):
        self.create_hand_state_frame()
        self.create_options_frame()
        self.create_hand_control_frame()
        self.create_current_hand_command_frame()

    def connect(self, widget, signal, event):
        widget.bind(signal, event)

    def send_movement_motor_1(self):
        Communication.Instance.update_stream(ord('a'))
        Communication.Instance.send_stream()

    def send_movement_motor_2(self):
        Communication.Instance.update_stream(ord('b'))
        Communication.Instance.send_stream()

    def send_text(self):
        # TODO: Add sending message to the TextAnalyser and sending message to the arduino here (and wait for the
        #  "message received" before showing info)
        if self.connection_actual_state_label["text"] == "not connected":
            self.no_connection_window()
        else:
            message_to_send = self.text_entry.get()
            self.text_entry.delete(0, END)
            self.text_entry.config(state="disabled")
            TextAnalyser.instance.parse_char(message_to_send)
            messagebox.showinfo("Sent", message_to_send)

    def do_stop(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        EventHandler.Instance.clear_queue()
        messagebox.showinfo("Stopped", "Hand has been stopped.")

    def do_pause(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("Paused", "Hand has been paused.")

    def send_new_speed_on_letter(self, new_time_value):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        Configuration.Instance.set_wait_time(new_time_value)
        print("New on_letter_time_value: " + new_time_value)

    def set_mode_option_step(self):
        self.set_mode_option_state(ModeEnum.Step)
        self.send_new_mode_option()

    def set_mode_option_automatic(self):
        self.set_mode_option_state(ModeEnum.Automatic)
        self.send_new_mode_option()

    def send_new_mode_option(self):
        if self.get_mode_option_state() == ModeEnum.Automatic:
            if Configuration.Instance.is_semi_auto():
                Configuration.Instance.toggle_semi_auto()
            else:
                return
        elif not Configuration.Instance.is_semi_auto():
            Configuration.Instance.toggle_semi_auto()
        else:
            return

        messagebox.showinfo("New mode", "Mode option has been changed to " + str(self.get_mode_option_state()))

    def send_new_purpose_option(self):
        # TODO: Add sending message to the arduino here (and wait for the "message received" before showing info)
        messagebox.showinfo("New purpose", "Purpose option has been changed to " + str(self.get_purpose_option_state()))

    def no_connection_window(self):
        messagebox.showinfo("Warning!", "No connection to the hand.")

    def enable_entry(self):
        self.text_entry.config(state="normal")


def on_closing():
    EventHandler.Instance.end_thread()
    Communication.Instance.end_thread()
    root.destroy()


if __name__ == "__main__":
    Configuration.Instance.set_debug(TRUE, 1)
    root = Tk()
    app = application(master=root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
