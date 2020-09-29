import json
import tkinter as tk
from pathlib import Path
from Quiz import QuizBook, QuizQuestion


class App():
    def __init__(self, master):
        self.master = master
        self.main_font = "Bahnschrift"
        self.symbol = "Wingdings 3"
        self.header_bg = ["#101820", "#000810", "#202830"]
        self.body_bg = ["#f2aa4c", "#e28a3c", "#ffba5c"]
        self.accent_bg = ["#302daf", "#201d8f", "#403dbf"]
        self.Overlay()

    def Overlay(self):
        self.header = tk.Frame(self.master, bg=self.header_bg[0], height=50)
        self.header.pack(side="top", fill="x")
        self.body = tk.Frame(self.master, bg=self.body_bg[0])
        self.body.pack(side="top", fill="both", expand=1)
        self.master.update_idletasks()
        self.header_content(self.header)
        self.body_content(self.body)

    def header_content(self, parent_frame):
        header_frame = tk.Frame(parent_frame, bg=self.header_bg[0])
        header_frame.pack(side="top", fill="both")

        self.header_title = tk.Label(header_frame, text="Python Quiz", fg=self.body_bg[0], bg=self.header_bg[0], font=(self.main_font, 20, "bold"))
        self.header_title.pack(side="top", pady=10)

        header_buttons_frame = tk.Frame(header_frame, bg=self.header_bg[0])
        header_buttons_frame.pack(side="top", fill="both")

        header_button_names = {"Contents": self._go_contents, "Add": None, "Settings": None}
        self.header_indicator = []
        for key, val in header_button_names.items():
            indicator = self._generate_header_buttons(header_buttons_frame, key, val)
            indicator.config(bg=self.header_bg[0])
            self.header_indicator.append(indicator)
            self.master.update_idletasks()
            self.master.update()

        self.header_indicator[0].config(bg=self.body_bg[0])
        self.master.update_idletasks()
        self.master.update()

    def body_content(self, parent_frame):
        # Scrollable Frame
        self.body_frame = tk.Frame(parent_frame, bg=self.header_bg[0])
        self.canvas_frame = tk.Frame(self.body_frame, bg=self.header_bg[0])   # Canvas Holder
        self.body_canvas = tk.Canvas(self.canvas_frame, bd=0, relief="flat", highlightthickness=0, bg=self.header_bg[0])    # Canvas
        body_scroll_bar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.body_canvas.yview)  # Scroll Bar
        display_frame = tk.Frame(self.body_canvas, bg=self.body_bg[0])   # Frame Holder
        body_scroll_bar.bind("<Configure>", lambda e: self.body_canvas.config(scrollregion=self.body_canvas.bbox("all")))   # Scrollbar Updater
        self.item = self.body_canvas.create_window(0, 0, window=display_frame, anchor="nw")     # Create Scrollable Frame window
        self.body_canvas.config(yscrollcommand=body_scroll_bar.set)     # Set scroll command to scroll bar

        # Display Widgets
        self.body_frame.pack(side="top", fill="both", expand=1)
        self.canvas_frame.pack(side="top", fill="both", expand=1)
        body_scroll_bar.pack(side="right", fill="y")
        self.body_canvas.pack(side="top", fill="both", expand=1)
        self.master.update_idletasks()  # Update Display

        # Get recent Quiz Book in QuizList.json
        quizzes = QuizBook("covergroup").getRecent()
        quiz_book = []
        for quiz in quizzes:
            quiz_book_name = Path(quiz).name
            quiz_book.append(QuizBook(quiz_book_name))  # save recent Quiz Book in quiz_book
            self.master.update_idletasks()  # Update Display
            self.master.update()    # Update User Input

        # Iterate over quiz_book
        for quiz in quiz_book:
            self.body_canvas.config(scrollregion=self.body_canvas.bbox("all"))  # Update Scroll Bar
            self._generate_content(display_frame, quiz)
            self.master.update_idletasks()  # Update Display
            self.master.update()     # Update User Input
        self.body_canvas.bind("<Configure>", self.resize)   # Resize x axis of widgets in display_frame
        self.master.update_idletasks()  # Update Display
        self.master.update()    # Update User Input

    def open_quiz_book(self, quizbook):
        self.canvas_frame.forget()
        self.header_title.config(text=quizbook.title)

        self.quiz_book_border = tk.Frame(self.body_frame, bg=self.body_bg[0], bd=1)
        self.quiz_book_border.pack(side="top", expand=1, padx=50, pady=50, fill="both")
        quiz_book_frame = tk.Frame(self.quiz_book_border, height=100, width=200, bg=self.header_bg[0])
        quiz_book_frame.pack(side="top", expand=1, fill="both")

        num_quiz = len(quizbook)
        num_quiz_label = tk.Label(quiz_book_frame, text=f'Number of Quiz:\t{num_quiz}', fg=self.body_bg[0], bg=self.header_bg[0], font=(self.main_font, 24))
        num_quiz_label.pack(side="top", expand=1, fill="both", pady=10)

        start_button = tk.Label(quiz_book_frame, text="Start Quiz", font=(self.main_font, 30, "bold"), fg=self.header_bg[0], bg=self.body_bg[0])
        start_button.pack(side="bottom", fill="x")
        start_button.bind("<Enter>", lambda e: self._change_color(e, self.body_bg[2]))
        start_button.bind("<Button-1>", lambda e: self._press_content(e, lambda: self.start_quiz(quizbook), bg=self.body_bg[1]))
        start_button.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.body_bg[0]))
        start_button.bind("<Leave>", lambda e: self._change_color(e, self.body_bg[0]))

    def start_quiz(self, quizbook):
        questions = quizbook.AllQuestions()
        self.quiz_book_border.destroy()
        self.question_frame = tk.Frame(self.body_frame, bg=self.header_bg[0])
        self.question_frame.pack(side="top", fill="both", expand=1)
        question_border = tk.Frame(self.question_frame, bg=self.body_bg[0], bd=1)
        hold_question = tk.Frame(question_border, bg=self.header_bg[0])
        hold_choices = tk.Frame(question_border, bg=self.header_bg[2])
        question_border.pack(fill="both", expand=1, padx=10, pady=10)
        hold_question.pack(fill="both", expand=1)
        hold_choices.pack(fill="both")
        self.master.update_idletasks()
        for key, val in questions.items():
            question_label = tk.Label(hold_question, text=str(key), bg=self.header_bg[0], fg=self.body_bg[0], font=(self.main_font, 30, "bold"))
            question_label.pack(side="top", expand=1, fill="both")
            choices = val[0]["choices"]
            answer = val[0]["answerIndex"]
            x = 0
            for y, choice in enumerate(choices):
                self._generate_choices(hold_choices, choice, answer, x, y % 2)
                if y % 2 == 1:
                    x += 1

            break

    def _generate_choices(self, parent, choice, answer, x, y):
        hold_choice = tk.Frame(parent, bg=self.body_bg[0])
        choice_shadow_side = tk.Frame(hold_choice, bg=self.header_bg[0])
        choice_shadow_side.pack(side="right", fill="y")
        if y == 0:
            choice_shadow_side = tk.Frame(hold_choice, bg=self.header_bg[0])
            choice_shadow_side.pack(side="left", fill="y")
        choice_name = tk.Label(hold_choice, bg=self.body_bg[0], text=choice, font=(self.main_font, 20), height=2, width=10)
        choice_name.pack(side="top", fill="both", expand=1)
        choice_shadow = tk.Frame(hold_choice, bg=self.header_bg[0])
        choice_shadow.pack(side="bottom", expand=1, fill="x")
        choice_name.bind("<Enter>", lambda e: self._change_color(e, self.body_bg[2]))
        choice_name.bind("<Button-1>", lambda e: self._press_content(e, bg=self.body_bg[1]))
        choice_name.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.body_bg[0]))
        choice_name.bind("<Leave>", lambda e: self._change_color(e, self.body_bg[0]))
        parent.rowconfigure(x, weight=1)
        parent.columnconfigure(y, weight=1)
        hold_choice.grid(row=x, column=y, sticky=tk.NSEW)
        self.master.update_idletasks()
        self.master.update()
        return hold_choice

    def _generate_content(self, parent_frame, quizbook):
        content_frame = tk.Frame(parent_frame, bg=self.header_bg[0])
        content_frame.pack(side="top", fill="x")

        content_shadow = tk.Frame(content_frame, bg=self.body_bg[0], height=1)
        content_shadow.pack(side="bottom", fill="x")

        content_label = tk.Label(content_frame, fg=self.body_bg[0], text=quizbook.title, font=(self.main_font, 17), bg=self.header_bg[0], height=2, width=37, bd=4)  # Add font
        content_label.pack(side="top", fill="x", expand=1)
        content_label.bind("<Enter>", lambda e: self._change_color(e, self.header_bg[2]))
        content_label.bind("<Button-1>", lambda e: self._press_content(e, lambda: self.open_quiz_book(quizbook), bg=self.header_bg[1]))  # Add OpenQuizFunc
        content_label.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.header_bg[0]))
        content_label.bind("<Leave>", lambda e: self._change_color(e, self.header_bg[0]))
        self.master.update_idletasks()
        self.master.update()

    def _generate_header_buttons(self, parent, title, command=None):
        header_content_frame = tk.Frame(parent, bg=self.header_bg[0])
        header_content_frame.pack(side="left", fill="x", expand=1)

        header_content_button = tk.Label(header_content_frame, text=title, fg=self.body_bg[0], bg=self.header_bg[0], font=(self.main_font, 17, "bold"))
        header_content_button.pack(side="top", fill="x", expand=1)
        header_content_button.bind("<Enter>", lambda e: self._change_color(e, self.header_bg[2]))
        header_content_button.bind("<Button-1>", lambda e: self._press_content(e, command, bg=self.header_bg[1]))
        header_content_button.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.header_bg[0]))
        header_content_button.bind("<Leave>", lambda e: self._change_color(e, self.header_bg[0]))

        header_content_shadow = tk.Frame(header_content_frame, bg=self.body_bg[0], height=1)
        header_content_shadow.pack(side="bottom", fill="x")
        header_content_indicator = tk.Frame(header_content_frame, height=2, bg=self.body_bg[0])
        header_content_indicator.pack(side="bottom", fill="x", expand=1)

        return header_content_indicator

    def _disable_all_indicator(self):
        for indicater in self.header_indicator:
            indicater.config(bg=self.header_bg[0])

    def _go_contents(self):
        if "quiz_book_border" in self.__dict__:
            self.quiz_book_border.destroy()
        self.canvas_frame.pack(side="top", fill="both", expand=1)

    def _disable_all_frames(self):
        self.header.destroy()
        self.body.destroy()

    def resize(self, event):
        self.body_canvas.itemconfig(self.item, width=event.width)

    def _change_color(self, event=None, color="#6d6d6d"):
        event.widget.config(bg=color)

    def _press_content(self, event=None, func=None, bg="#4d4d4d"):
        event.widget.config(bg=bg)
        if func is not None:
            func()

    def _dummy(self):
        print("I'm a dummy")
        x = 10 + 10
        print(x)


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.update_idletasks()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
