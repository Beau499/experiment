"""
This is a tkinter implementation for a computer administered, paired-choice, reaction-time task.
It was used by Beau Fonville (b.d.fonville@student.rug.nl) for an experiment on ADHD and mindfulness meditation.
Please use it as you like as long as it isn't for commercial ends.
"""

import tkinter as tk
import random
from random import choice
from datetime import datetime
import pandas as pd


"""
Note that I used a timer for 4 minutes. That is the time participants had to do the task.
"""
class ReactionTimeTask:
    def __init__(self, root, answers):
        self.digit_show_time = 300
        self.pause_time = 1200
        self.root = root
        self.root.title("Choice Reaction-Time Task")
        self.root.geometry("1200x1200")
        self.create_widgets()
        self.no1 = 0
        self.no2 = 0
        self.answers = answers
        self.index = 0


    def create_widgets(self):
        self.input_label = tk.Label(self.root, text="Enter your number:", font=("Arial", 14))
        self.input_label.pack(pady=20)

        self.number_entry = tk.Entry(self.root, font=("Arial", 38))
        self.number_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Task", font=("Arial", 14), command=self.start_task)
        self.start_button.pack(pady=20)

        self.label = tk.Label(self.root, font=("Arial", 40))
        self.label.pack(pady=20)

    def increase_index(self):
        self.index += 1
    def start_task(self):
        user_input = self.number_entry.get()
        try:
            self.no1 = int(user_input)
        except ValueError:
            self.label.config(text="Invalid input. Please enter a number.")
            return
        self.answers.append(self.no1)
        self.increase_index()
        # get the date and time as to put in the dataframe (nice to have if I mix up conditions)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.answers.append(dt_string)
        self.increase_index()
        self.input_label.pack_forget()
        self.number_entry.pack_forget()
        self.start_button.pack_forget()
        self.show_blank_screen1()


    def get_current_time(self):
        return self.root.winfo_fpixels('1i') * 1000

    def show_white_screen(self):
        self.label.config(text="")

    def show_blank_screen1(self):
        self.label.config(text=' \nYou will see 2 numbers quickly after one another. \nAs quickly as possible press A when the first number shown was\n larger, otherwise press L.\n You will now begin the test. press any button to start.')
        self.wait_for_input()

    def show_blank_screen(self):
        self.no1 = random.randint(1, 99)
        self.no2 = choice([i for i in range(1, 99) if i not in [self.no1]])
        self.show_white_screen()
        self.root.after(500, self.label.config(text=f"{self.no1}"))
        self.root.after(self.digit_show_time, self.show_white_screen)
        self.root.after(self.pause_time, self.show_second_number)

    def show_second_number(self):
        self.label.config(text=f'{self.no2}')
        self.root.after(150, lambda: self.label.config(text="Press A if the first number was larger\n and L if the second was larger."))
        self.wait_for_input()


    def wait_for_input(self):
        self.root.bind("<Key>", self.check_answer)

    def check_answer(self, event):
        key_pressed = event.keysym.upper()
        if (key_pressed == "A" and self.no1 > self.no2) or \
                (key_pressed == "L" and self.no2 > self.no1):
            print("Correct!")
            self.answers.append(1)
        else:
            print("Incorrect!")
            self.answers.append(2)
        self.increase_index()
        self.show_blank_screen()

    def end_task(self):
        self.label.config(text="Task Completed")

if __name__ == "__main__":
    answers_participant = []
    root = tk.Tk()
    app = ReactionTimeTask(root, answers_participant)

    root.mainloop()
    # if there are already other participants that filled in, then take that dataframe as to append to it.
    try:
        df = pd.read_excel("RESULTS.xlsx")
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        columns = ["number", "date and time"] + [str(i) for i in range(1, 199)]
        df = pd.DataFrame(columns=columns)

    # remove the first answer of the participant because for some reason it captures that and says it's false.
    answers_participant.pop(2)
    # add the data to the  and save it again
    num_columns = len(df.columns)
    answers_participant.extend([-1] * (num_columns - len(answers_participant)))

    # Append the padded answers_participant list to the DataFrame
    df.loc[len(df)] = answers_participant

    # Save the updated DataFrame to RESULTS.xlsx
    df.to_excel("RESULTS.xlsx", index=False)
