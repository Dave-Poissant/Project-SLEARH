from Backend_Scripts import TextAnalyser
from Backend_Scripts import Configuration
from Backend_Scripts import EventHandler
from Backend_Scripts import Communication
from Backend_Scripts import Purpose
from Backend_Scripts import Quiz
from tkinter import *
from tkinter import messagebox
from enum import Enum
import os
import glob
import time

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
        self.__mode_option_state__ = IntVar()
        self.__purpose_option_state__ = IntVar()
        self.create_widgets()
        Quiz.Instance.set_ui_adress(self)
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
                if os.path.exists(images_directory+education_purpose_img_dir+str(command)+".png"):
                    current_operation_img = PhotoImage(file=images_directory+education_purpose_img_dir+str(command)+".png")
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
                if os.path.exists(images_directory+quiz_purpose_img_dir+str(command)+".png"):
                    current_operation_img = PhotoImage(file=images_directory+quiz_purpose_img_dir+str(command)+".png")
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

        self.clear_button = Button(hand_control_buttons_frame)
        self.clear_button["text"] = "clear"
        self.clear_button["command"] = self.clear_actions
        self.clear_button.grid(row=1, column=1, pady=5)

        self.send_button = Button(hand_control_buttons_frame)
        self.send_button["text"] = "send"
        self.send_button["command"] = self.send_text
        self.send_button.grid(row=0, column=0, columnspan=2)

        self.next = Button(hand_control_buttons_frame)
        self.next["text"] = "next"
        self.next["command"] = self.next_action
        self.next.grid(row=1, column=0, pady=5)

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
                                                     command=self.set_purpose_option_education)
        self.purpose_choices_education.select()
        self.purpose_choices_education.grid(row=0, column=0)
        self.purpose_choices_quiz = Radiobutton(options_purpose_choices_frame, text="Quiz (Score = 0)",
                                                var=self.__purpose_option_state__, value=PurposeEnum.Quiz,
                                                command=self.set_purpose_option_quiz)
        self.purpose_choices_quiz.deselect()
        self.purpose_choices_quiz.grid(row=0, column=1)
        self.set_purpose_option_education()

        # Configuration and placement for the "Mode:" section
        self.mode_label = Label(options_frame, text="Mode:")
        self.mode_label.grid(row=3, column=0, pady=2, stick=W)
        options_mode_choices_frame = Frame(options_frame)
        options_mode_choices_frame.grid(row=4, column=1, padx=2)
        self.mode_choices_automatic = Radiobutton(options_mode_choices_frame, text="Automatic",
                                                  var=self.__mode_option_state__, value=ModeEnum.Automatic,
                                                  command=self.set_mode_option_automatic)
        self.mode_choices_automatic.select()
        self.set_mode_option_automatic()
        self.mode_choices_automatic.grid(row=0, column=0)
        self.mode_choices_step = Radiobutton(options_mode_choices_frame, text="Step", var=self.__mode_option_state__,
                                             value=ModeEnum.Step,
                                             command=self.set_mode_option_step)
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
        self.create_current_hand_command_frame()
        self.create_options_frame()
        self.create_hand_control_frame()

    def wait_arduino_ready_state(self):
        ready = False
        while not ready:  # Wait for the Arduino to send a ready state
            string_state = Communication.Instance.read_stream()
            if string_state == "true":
                ready = True
            elif string_state == "false":
                ready = False
            elif string_state == "none":
                EventHandler.Instance.clear_queue()
                self.no_connection_window()
                self.enable_entry()
                self.change_hand_ready_state(True)
                self.change_state_picture(False, '')
                break
            time.sleep(0.1)

    def send_text(self):
        if self.connection_actual_state_label["text"] == "not connected":
            self.no_connection_window()
        else:
            message_to_send = self.text_entry.get()
            self.text_entry.delete(0, END)
            self.text_entry.config(state="disabled")
            if TextAnalyser.instance.parse_char(message_to_send):
                if self.get_mode_option_state() == ModeEnum.Step:
                    EventHandler.Instance.next_letter()

                if self.get_purpose_option_state() == PurposeEnum.Education:
                    self.mode_choices_automatic.config(state="disable")
                    self.mode_choices_step.config(state="disable")
                    self.purpose_choices_education.config(state="disable")
                    self.purpose_choices_quiz.config(state="disable")
                    messagebox.showinfo("Sent", message_to_send)
            else:
                messagebox.showinfo("Invalid input", "Enter only one character for a quiz answer")
                self.text_entry.config(state="normal")

    def next_action(self):
        if self.hand_actual_action_state_label["text"] == "ready":
            if self.__purpose_option_state__ == PurposeEnum.Quiz:
                Quiz.Instance.get_new_letter()

                Communication.Instance.update_stream(ord(Quiz.Instance.get_current_letter()),
                                                     Configuration.Instance.get_purpose_string(),
                                                     Configuration.Instance.get_wait_time())
                Communication.Instance.send_stream()
                self.change_state_picture(True, Quiz.Instance.get_current_letter())
                self.change_hand_ready_state(False)

                self.wait_arduino_ready_state()

                self.enable_entry()
                self.change_hand_ready_state(True)
            else:
                EventHandler.Instance.next_letter()
        else:
            messagebox.showinfo("Warning !", "Hand is not ready.")

    def clear_actions(self):
        EventHandler.Instance.clear_queue()
        messagebox.showinfo("Warning !", "All actions have been cleared.")

    def send_new_speed_on_letter(self, new_time_value):
        Configuration.Instance.set_wait_time(new_time_value)

    def set_mode_option_step(self):
        self.set_mode_option_state(ModeEnum.Step)
        self.send_new_mode_option()

    def set_mode_option_automatic(self):
        self.set_mode_option_state(ModeEnum.Automatic)
        self.send_new_mode_option()
        self.change_state_picture(False, '')

    def set_purpose_option_education(self):
        self.set_purpose_option_state(PurposeEnum.Education)
        self.send_new_purpose_option()
        self.change_state_picture(False, '')

    def set_purpose_option_quiz(self):
        self.set_purpose_option_state(PurposeEnum.Quiz)
        self.send_new_purpose_option()

    def send_new_mode_option(self):
        if self.get_mode_option_state() == ModeEnum.Automatic:
            if Configuration.Instance.is_semi_auto():
                Configuration.Instance.toggle_semi_auto()
            else:
                return
            messagebox.showinfo("New mode", "Mode option has been changed to automatic")
        elif not Configuration.Instance.is_semi_auto():
            Configuration.Instance.toggle_semi_auto()
            messagebox.showinfo("New mode", "Mode option has been changed to step")
        else:
            return



    def send_new_purpose_option(self):
        if self.get_purpose_option_state() == PurposeEnum.Quiz:
            if Configuration.Instance.get_purpose() == Purpose.Purpose.Quiz:
                return
            else:
                Configuration.Instance.set_purpose(Purpose.Purpose.Quiz)
                Quiz.Instance.reset()
            messagebox.showinfo("New purpose",
                                "Purpose option has been changed to quiz. Press next to start the quiz.")
        elif self.get_purpose_option_state() == PurposeEnum.Education:
            if Configuration.Instance.get_purpose() == Purpose.Purpose.Education:
                return
            else:
                Configuration.Instance.set_purpose(Purpose.Purpose.Education)
            self.modify_quiz_score()
            messagebox.showinfo("New purpose", "Purpose option has been changed to education.")

    def no_connection_window(self):
        messagebox.showinfo("Warning!", "No connection to the hand.")

    def enable_entry(self):
        self.text_entry.config(state="normal")

    def enable_radiobuttons(self):
        self.mode_choices_automatic.config(state="normal")
        self.mode_choices_step.config(state="normal")
        self.purpose_choices_education.config(state="normal")
        self.purpose_choices_quiz.config(state="normal")

    def modify_quiz_score(self):
        self.purpose_choices_quiz["text"] = "Quiz (Score = " + str(Quiz.Instance.get_score()) + ")"

    def quiz_answer_conclusion(self, answer_verification):
        if answer_verification:
            messagebox.showinfo("Well done!", "That was the correct answer.")
        else:
            messagebox.showinfo("Wrong!", "That was not the correct answer.")


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
