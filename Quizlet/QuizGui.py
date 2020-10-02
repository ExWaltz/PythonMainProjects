import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from Quiz import QuizBook, QuizQuestion


class App():
    """
        Number 1 of my: Let's make 12 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects
    """

    def __init__(self, master):
        self.master = master
        self.main_font = "Bahnschrift"
        # [Base, Highlight, Shadow]
        self.header_bg = ("#101820", "#000810", "#202830")
        self.body_bg = ("#f2aa4c", "#e28a3c", "#ffba5c")
        self.overlay()

    def overlay(self):
        # Divide the app into header and body
        self.header = tk.Frame(self.master, bg=self.header_bg[0], height=50)
        self.header.pack(side="top", fill="x")
        self.body = tk.Frame(self.master, bg=self.body_bg[0])
        self.body.pack(side="top", fill="both", expand=1)
        self.master.update_idletasks()  # Update root
        self.header_content(self.header)
        self.body_content(self.body)

    def header_content(self, parent_frame):
        header_frame = tk.Frame(parent_frame, bg=self.header_bg[0])
        header_frame.pack(side="top", fill="both")

        self.header_title = tk.Label(header_frame,
                                     text="Python Quiz",
                                     fg=self.body_bg[0],
                                     bg=self.header_bg[0],
                                     font=(self.main_font, 20, "bold"))
        self.header_title.pack(side="top", pady=10)

        header_buttons_frame = tk.Frame(header_frame, bg=self.header_bg[0])
        header_buttons_frame.pack(side="top", fill="both")

        # {Name: Function}
        header_button_names = {"Contents": self._go_contents,
                               "Add": self._go_add,
                               "Settings": None}
        self.header_indicator = []  # Indicate which button is active
        for key, val in header_button_names.items():
            indicator = self._generate_header_buttons(header_buttons_frame,
                                                      key,
                                                      val)
            indicator.config(bg=self.header_bg[0])
            self.header_indicator.append(indicator)
            self.master.update_idletasks()
            self.master.update()

        self.header_indicator[0].config(bg=self.body_bg[0])
        self.master.update_idletasks()
        self.master.update()

    def body_content(self, parent_frame):
        # Scrollable Frame
        self.body_frame = tk.Frame(parent_frame,
                                   bg=self.header_bg[0])
        self.canvas_frame = tk.Frame(self.body_frame,
                                     bg=self.header_bg[0])   # Canvas Holder

        self.body_canvas = tk.Canvas(self.canvas_frame,
                                     bd=0,
                                     relief="flat",
                                     highlightthickness=0,
                                     bg=self.header_bg[0])    # Canvas

        body_scroll_bar = tk.Scrollbar(self.canvas_frame,
                                       orient="vertical",
                                       command=self.body_canvas.yview)  # Scroll Bar

        display_frame = tk.Frame(self.body_canvas, bg=self.body_bg[0])   # Frame Holder

        body_scroll_bar.bind("<Configure>",
                             lambda e: self.body_canvas.config(
                                 scrollregion=self.body_canvas.bbox("all")))   # Scrollbar Updater
        self.item = self.body_canvas.create_window(0, 0,
                                                   window=display_frame,
                                                   anchor="nw")     # Create Scrollable Frame window
        self.body_canvas.config(yscrollcommand=body_scroll_bar.set)     # Set scroll command to scroll bar

        # Display Widgets
        self.body_frame.pack(side="top",
                             fill="both",
                             expand=1)

        self.canvas_frame.pack(side="top",
                               fill="both",
                               expand=1)

        body_scroll_bar.pack(side="right",
                             fill="y")

        self.body_canvas.pack(side="top",
                              fill="both",
                              expand=1)

        self.master.update_idletasks()  # Update Display

        # Get recent Quiz Book in QuizList.json
        quizzes = QuizBook.getRecent()
        quiz_book = []
        for quiz in quizzes:
            quiz_book_name = Path(quiz).name
            quiz_book.append(QuizBook(quiz_book_name))  # save recent Quiz Book in quiz_book
            self.master.update_idletasks()  # Update Display
            self.master.update()    # Update User Input

        # Iterate over quiz_book
        for quiz in quiz_book:
            self.body_canvas.config(scrollregion=self.body_canvas.bbox("all"))  # Update Scroll Bar
            self._generate_content(display_frame, quiz)     # Make and display Quiz Books in QuizList.json
            self.master.update_idletasks()  # Update Display
            self.master.update()     # Update User Input
        self.body_canvas.bind("<Configure>", self.resize)   # Resize x axis of widgets in display_frame
        self.master.update_idletasks()  # Update Display
        self.master.update()    # Update User Input

    def open_quiz_book(self, quizbook):
        self.canvas_frame.forget()  # disable canvas
        self.header_title.config(text=quizbook.title)   # change Header title to quiz book title

        self.quiz_book_border = tk.Frame(self.body_frame,
                                         bg=self.body_bg[0],
                                         bd=1)  # Add a border effect on Quiz Info
        # Display Widgets
        self.quiz_book_border.pack(side="top",
                                   expand=1,
                                   padx=50,
                                   pady=50,
                                   fill="both")

        quiz_book_frame = tk.Frame(self.quiz_book_border,
                                   height=100,
                                   width=200,
                                   bg=self.header_bg[0])

        quiz_book_frame.pack(side="top",
                             expand=1,
                             fill="both")

        num_quiz = len(quizbook)    # Get the total amount of quizzes in quizbook
        num_quiz_label = tk.Label(quiz_book_frame,
                                  text=f'Number of Quiz:\t{num_quiz}',
                                  fg=self.body_bg[0],
                                  bg=self.header_bg[0],
                                  font=(self.main_font, 24))    # Display amount of quizzes
        num_quiz_label.pack(side="top",
                            expand=1,
                            fill="both",
                            pady=10)
        self._label_button(quiz_book_frame,
                           text="Start Quiz",
                           font=(self.main_font, 30, "bold"),
                           fg=self.header_bg,
                           bg=self.body_bg,
                           side="bottom",
                           fill="x",
                           func=lambda: self._go_start_quiz(quizbook))

    def start_quiz(self, quizbook):
        questions = quizbook.AllQuestions()     # Get all the questions in the quizbook
        self.question_frame = tk.Frame(self.body_frame,
                                       bg=self.header_bg[0])    # Frame holder for quizzes
        question_border = tk.Frame(self.question_frame,
                                   bg=self.body_bg[0],
                                   bd=1)    # Border effect on quiz frame
        hold_question = tk.Frame(question_border,
                                 bg=self.header_bg[0])  # question frame
        hold_choices = tk.Frame(question_border,
                                bg=self.header_bg[0])   # choices frame
        # Display Widgets
        self.question_frame.pack(side="top",
                                 fill="both",
                                 expand=1)
        question_border.pack(fill="both",
                             expand=1,
                             padx=10,
                             pady=10)
        hold_question.pack(fill="both",
                           expand=1)
        hold_choices.pack(fill="both")
        self.master.update_idletasks()
        question_label = tk.Label(hold_question,
                                  bg=self.header_bg[0],
                                  fg=self.body_bg[0],
                                  font=(self.main_font, 30, "bold"))    # Question Text
        question_label.pack(side="top",
                            expand=1,
                            fill="both")
        score = 0   # total score in quiz
        for key, val in questions.items():  # iterate over questions
            # start of quiz
            question_label.config(text=str(key))    # change question text
            choices = val[0]["choices"]     # Get choices list
            choices = [str(c) for c in choices]     # convert to items in list to str
            answerIndex = val[0]["answerIndex"]     # get answer index
            answer = choices[answerIndex]           # Get answer from choices
            choice_frame = {}                       # Hold Choice and choice frame
            self.iscorrect = None   # if correct answer is choosen (see self._answer)
            x = 0   # row grid
            for y, choice in enumerate(choices):
                h_frame, r_choice = self._generate_choices(hold_choices,
                                                           choice,
                                                           answer,
                                                           x,
                                                           y % 2)   # Make and display choices
                choice_frame[r_choice] = h_frame
                # nested for loops are slow so I did this version
                if y % 2 == 1:
                    x += 1
            addScore = True     # if user got the correct answer
            while True:
                # Loop until answer is choosen
                if self.iscorrect is True:
                    if addScore is True:
                        score += 1  # add score
                    [f.destroy() for f in choice_frame.values()]
                    break
                elif self.iscorrect is False:
                    addScore = False    # incorrect answer
                    for ck, cv in choice_frame.items():
                        if ck != answer:
                            # cv.destroy()    # destroy all wrong answer
                            label = cv.children["!label"]
                            label.unbind("<Enter>")
                            label.unbind("<Button-1>")
                            label.unbind("<ButtonRelease-1>")
                            label.unbind("<Leave>")
                            label.config(bg=self.header_bg[0])
                        else:
                            # cv.grid_forget()    # Reset grid settings
                            # cv.grid(row=0,
                            #         column=0,
                            #         columnspan=2,
                            #         sticky="nsew")
                            pass
                self.master.update_idletasks()
                self.master.update()
                # next quiz
        # End of quiz
        question_label.config(text=f"Total Score:\t{score}")
        self._label_button(hold_choices,
                           fg=self.header_bg,
                           bg=self.body_bg,
                           text="Go Back",
                           font=(self.main_font, 20),
                           height=2,
                           width=10,
                           side="top",
                           fill="both",
                           expand=1,
                           func=lambda: self._go_quiz_book(quizbook))

    def add_quiz_book(self):
        self.canvas_frame.forget()
        self.add_quiz_frame = tk.Frame(self.body_frame,
                                       bg=self.header_bg[0])
        self.add_quiz_frame.pack(fill="both",
                                 expand=1)
        border_open_file = tk.Frame(self.add_quiz_frame, bg=self.body_bg[0], bd=1)
        border_open_file.pack(fill="both", pady=5, padx=5)
        open_file_frame = tk.Frame(border_open_file, bg=self.header_bg[0])
        open_file_frame.pack(fill="x")
        self._label_button(open_file_frame,
                           fg=self.body_bg,
                           bg=self.header_bg,
                           text="Open File",
                           font=(self.main_font, 20, "bold"),
                           height=2,
                           width=10,
                           side="top",
                           fill="both",
                           expand=1,
                           func=self._add_quiz_path)
        self._shadow_effect(self.add_quiz_frame, bg=self.body_bg[0], height=2, side="top", pady=3)

    def _add_quiz_path(self):
        paths = filedialog.askopenfilenames()
        file_names = [Path(f).stem for f in paths]
        for file_name, path in zip(file_names, paths):
            if QuizBook.isValid(path):
                QuizBook(file_name, path)
            else:
                messagebox.showwarning("Warning", "Invalid Quiz Book")
                return
        answer = messagebox.askokcancel("Restart?", "Restart to show new Quiz Book")
        answer_switch = {True: self._reset_program, False: lambda: None}
        ans = answer_switch[answer]
        ans()

    def _generate_choices(self, parent, choice, answer, x, y):
        # Make and display choices
        hold_choice = tk.Frame(parent, bg=self.body_bg[0])  # hold choices

        self._shadow_effect(hold_choice, bg=self.header_bg[0], side="right", fill="y")

        if y == 0:
            self._shadow_effect(hold_choice, bg=self.header_bg[0], side="left", fill="y")

        self._label_button(hold_choice,
                           fg=self.header_bg,
                           bg=self.body_bg,
                           text=choice,
                           font=(self.main_font, 20),
                           height=2,
                           width=10,
                           side="top",
                           fill="both",
                           expand=1,
                           func=lambda: self._answer(choice, answer))

        self._shadow_effect(hold_choice, bg=self.header_bg[0], expand=1)

        parent.rowconfigure(x, weight=1)        # Make row expandable
        parent.columnconfigure(y, weight=1)     # Make column expandable
        hold_choice.grid(row=x,
                         column=y,
                         sticky=tk.NSEW)        # Display Choice button
        self.master.update_idletasks()
        self.master.update()
        return hold_choice, choice              # Return holder frame and choice

    def _answer(self, choice, answer):
        # if choice choosen is correct
        if choice == answer:
            self.iscorrect = True
            return
        self.iscorrect = False

    def _generate_content(self, parent_frame, quizbook):
        # Make and display Quiz Book in QuizList.json
        content_frame = tk.Frame(parent_frame,
                                 bg=self.header_bg[0])      # hold Quiz Book
        content_frame.pack(side="top",
                           fill="x")

        self._shadow_effect(content_frame, bg=self.body_bg[0])
        self._label_button(content_frame,
                           fg=self.body_bg,
                           bg=self.header_bg,
                           text=quizbook.title,
                           font=(self.main_font, 17),
                           height=2,
                           width=37,
                           bd=4,
                           side="top",
                           fill="x",
                           expand=1,
                           func=lambda: self._go_quiz_book(quizbook))
        self.master.update_idletasks()
        self.master.update()

    def _generate_header_buttons(self, parent, title, command=None):
        # Make and display header contents
        header_content_frame = tk.Frame(parent,
                                        bg=self.header_bg[0])       # hold header contents
        header_content_frame.pack(side="left",
                                  fill="x",
                                  expand=1)
        self._label_button(header_content_frame,
                           text=title,
                           fg=self.body_bg,
                           bg=self.header_bg,
                           font=(self.main_font, 17, "bold"),
                           side="top",
                           fill="x",
                           expand=1,
                           func=command)
        self._shadow_effect(header_content_frame, bg=self.body_bg[0])
        header_content_indicator = self._shadow_effect(header_content_frame, bg=self.body_bg[0], height=2, expand=1)

        return header_content_indicator

    def _label_button(self, parent, **kwarg):
        label_button = tk.Label(parent,
                                fg=kwarg.get("fg", ("#000000"))[0],
                                bg=kwarg.get("bg", ("#ffffff"))[0],
                                text=kwarg.get("text", " "),
                                font=kwarg.get("font", ("Century Gothic", 12)),
                                height=kwarg.get("height", 1),
                                width=kwarg.get("width", 1),
                                bd=kwarg.get("bd", 1))
        label_button.pack(side=kwarg.get("side", "top"), fill=kwarg.get("fill", "both"), expand=kwarg.get("expand", 0))
        label_button = self._button_properties(label_button, kwarg.get("bg", ("#2e2e2e", "#6a6a6a", "#161616")), kwarg.get("func", None))
        return label_button

    def _button_properties(self, label, color, command):
        # Button properties
        label.bind("<Enter>", lambda e: self._change_color(e, color[2]))    # when mouse is over widget
        label.bind("<Button-1>", lambda e: self._press_content(e, command, bg=color[1]))    # when widget is clicked
        label.bind("<ButtonRelease-1>", lambda e: self._change_color(e, color[2]))  # when mouse button is released
        label.bind("<Leave>", lambda e: self._change_color(e, color[0]))    # when mouse is not on widget
        return label

    def _shadow_effect(self, parent, **kwarg):
        shadow_effect = tk.Frame(parent,
                                 bg=kwarg.get("bg", "#ffffff"),
                                 height=kwarg.get("height", 1))      # Shadow effects
        shadow_effect.pack(side=kwarg.get("side", "bottom"),
                           fill=kwarg.get("fill", "x"),
                           expand=kwarg.get("expand", 0),
                           padx=kwarg.get("padx", 0),
                           pady=kwarg.get("pady", 0))
        return shadow_effect

    def _reset_program(self):
        python = sys.executable
        filePath = (sys.argv[0])
        os.execl(python, python, f'"{filePath}"')

    def _disable_all_indicator(self):
        # disable all header indicator
        for indicater in self.header_indicator:
            indicater.config(bg=self.header_bg[0])

    def _on_header(self, index):
        self._disable_all_indicator()
        self.header_indicator[index].config(bg=self.body_bg[0])

    def _go_add(self):
        self._disable_all_frames()
        self._on_header(1)
        self.add_quiz_book()

    def _go_start_quiz(self, quizbook):
        self._disable_all_frames()
        self._on_header(0)
        self.start_quiz(quizbook)

    def _go_quiz_book(self, quizbook):
        # Open Quiz Book Wrapper
        self._disable_all_frames()
        self._on_header(0)
        self.open_quiz_book(quizbook)

    def _go_contents(self):
        # Go back to Quiz Book List (startup page)
        self._disable_all_frames()
        self._on_header(0)
        self.canvas_frame.pack(side="top", fill="both", expand=1)
        self.header_title.config(text="Python Quiz")

    def _disable_all_frames(self):
        # disable all import parent frame
        if "quiz_book_border" in self.__dict__:
            self.quiz_book_border.destroy()
        if "question_frame" in self.__dict__:
            self.question_frame.destroy()
        if "add_quiz_frame" in self.__dict__:
            self.add_quiz_frame.destroy()
        self.master.update_idletasks()

    def resize(self, event):
        # resize Quiz Book List to fit the screen
        self.body_canvas.itemconfig(self.item, width=event.width)

    def _change_color(self, event=None, color="#6d6d6d"):
        # Change color of a widget
        event.widget.config(bg=color)

    def _press_content(self, event=None, func=None, bg="#4d4d4d"):
        # Change color of a widget and excute a function
        event.widget.config(bg=bg)
        if func is not None:
            func()


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.update_idletasks()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
