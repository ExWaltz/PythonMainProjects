import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
from Quiz import QuizBook, QuizQuestion


class App():
    """
        Number 1 of my: Let's make 12 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects
    """

    def __init__(self, master):
        self.master = master
        self.main_font = "Bahnschrift"
        self.git_img_file = Image.open("Images/github.png")
        self.git_img_file = self.git_img_file.resize((60, 60), Image.ANTIALIAS)
        self.git_img_file = ImageTk.PhotoImage(self.git_img_file)
        # [Base, Shadow, Highlight]
        self.header_bg = ("#101820", "#0d131a", "#282f36")
        self.body_bg = ("#f2aa4c", "#c2883d", "#f3b35e")
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
                               "About": self._go_about}
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

        self.display_frame = tk.Frame(self.body_canvas,
                                      bg=self.body_bg[0])   # Frame Holder

        body_scroll_bar.bind("<Configure>",
                             lambda e: self.body_canvas.config(
                                 scrollregion=self.body_canvas.bbox("all")))   # Scrollbar Updater
        self.item = self.body_canvas.create_window(0, 0,
                                                   window=self.display_frame,
                                                   anchor="nw")     # Create Scrollable Frame window
        # Set scroll command to scroll bar
        self.body_canvas.config(yscrollcommand=body_scroll_bar.set)

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
        self.update_quiz_book_list(self.display_frame)

    def update_quiz_book_list(self, parent):
        # Get recent Quiz Book in QuizList.json
        for prev_quiz_book in list(parent.children.values()):
            prev_quiz_book.destroy()

        quizzes = QuizBook.getRecent()
        quiz_book = []
        if quizzes == None:
            quizzes = QuizBook.getRecent()
        for quiz in quizzes:
            quiz_book_name = Path(quiz).name
            # save recent Quiz Book in quiz_book
            quiz_book.append(QuizBook(quiz_book_name))
            self.master.update_idletasks()  # Update Display
            self.master.update()    # Update User Input

        # Iterate over quiz_book
        for quiz in quiz_book:
            self.body_canvas.config(
                scrollregion=self.body_canvas.bbox("all"))  # Update Scroll Bar
            # Make and display Quiz Books in QuizList.json
            self._generate_content(parent, quiz)
            self.master.update_idletasks()  # Update Display
            self.master.update()     # Update User Input
        # Resize x axis of widgets in self.display_frame
        self.body_canvas.bind("<Configure>", self.resize)
        self.master.update_idletasks()  # Update Display
        self.master.update()    # Update User Input

    def open_quiz_book(self, quizbook):
        # change Header title to quiz book title
        self.header_title.config(text=quizbook.title)

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

        # Get the total amount of quizzes in quizbook
        num_quiz = len(quizbook)
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
            # convert to items in list to str
            choices = [str(c) for c in choices]
            answerIndex = val[0]["answerIndex"]     # get answer index
            answer = choices[answerIndex]           # Get answer from choices
            choice_frame = {}                       # Hold Choice and choice frame
            # if correct answer is choosen (see self._answer)
            self.iscorrect = None
            x = 0   # row grid
            for y, choice in enumerate(choices):
                # Make and display choices
                h_frame, r_choice = self._generate_choices(hold_choices,
                                                           choice,
                                                           answer,
                                                           x,
                                                           y % 2)
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
                    # Destroy all choice
                    [f.destroy() for f in choice_frame.values()]
                    break
                elif self.iscorrect is False:
                    addScore = False    # incorrect answer
                    for ck, cv in choice_frame.items():
                        if ck != answer:
                            # Disable all wrong answer
                            label = cv.children["!label"]
                            label.unbind("<Enter>")
                            label.unbind("<Button-1>")
                            label.unbind("<ButtonRelease-1>")
                            label.unbind("<Leave>")
                            label.config(bg=self.header_bg[0])
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

    def about_tab(self):
        self.canvas_frame.forget()
        self.about_frame = tk.Frame(
            self.body_frame, bg=self.header_bg[0], bd=10)
        self.about_frame.pack(fill="both", expand=1, side="top")
        dev_frame = tk.Frame(self.about_frame, bg=self.body_bg[0])
        dev_git = tk.Frame(dev_frame, bg=self.header_bg[0])
        self._label_button(dev_git,
                           fg=self.header_bg,
                           bg=self.body_bg,
                           text="Github",
                           font=(self.main_font, 20, "bold"),
                           image=self.git_img_file,
                           compound="left",
                           side="top",
                           fill="both",
                           expand=1)
        dev_git.pack(fill="both", side="top", expand=1)
        dev_frame.pack(fill="x", side="top")

    def add_quiz_book(self):
        self.add_quiz_frame = tk.Frame(self.body_frame,
                                       bg=self.header_bg[0])
        self.add_quiz_frame.pack(fill="both",
                                 expand=1)
        border_open_file = tk.Frame(self.add_quiz_frame,
                                    bg=self.body_bg[0],
                                    bd=1)
        open_file_frame = tk.Frame(border_open_file,
                                   bg=self.header_bg[0])
        border_open_file.pack(fill="both",
                              pady=5,
                              padx=5)
        open_file_frame.pack(fill="x")
        self.master.update_idletasks()
        self._label_button(open_file_frame,
                           fg=self.body_bg,
                           bg=self.header_bg,
                           text="Open File",
                           font=(self.main_font, 20, "bold"),
                           height=2,
                           width=4,
                           side="left",
                           fill="x",
                           expand=1,
                           func=self._add_quiz_path)
        self._shadow_effect(open_file_frame,
                            bg=self.body_bg[0],
                            height=2,
                            side="left",
                            pady=3,
                            fill="y")
        self._label_button(open_file_frame,
                           fg=self.body_bg,
                           bg=self.header_bg,
                           text="New Quiz Book",
                           font=(self.main_font, 20, "bold"),
                           height=2,
                           width=4,
                           side="left",
                           fill="both",
                           expand=1,
                           func=self._go_new_quiz_book)

        self._shadow_effect(self.add_quiz_frame,
                            bg=self.body_bg[0],
                            height=2,
                            side="top",
                            pady=3)

    def _new_quiz_book(self):
        self.new_quiz_frame = tk.Frame(self.body_frame,
                                       bg=self.header_bg[0],
                                       bd=10)
        quiz_book_frame = tk.Frame(self.new_quiz_frame,
                                   bg=self.header_bg[0])
        quiz_book_info = tk.Frame(quiz_book_frame,
                                  bg=self.header_bg[0])
        title_label = tk.Label(quiz_book_info,
                               bg=self.header_bg[0],
                               text="Title:\t",
                               fg=self.body_bg[0],
                               font=(self.main_font, 12))
        random_label = tk.Label(quiz_book_info,
                                bg=self.header_bg[0],
                                text="Disable Random: ",
                                fg=self.body_bg[0],
                                font=(self.main_font, 12))
        title_var = tk.StringVar()
        self.is_rand = True
        title_entry = tk.Entry(quiz_book_info,
                               textvariable=title_var,
                               bg=self.header_bg[0],
                               relief="flat",
                               fg=self.body_bg[0],
                               font=(self.main_font, 12),
                               highlightbackground=self.body_bg[0],
                               highlightcolor=self.body_bg[1],
                               highlightthickness=1,
                               insertbackground=self.body_bg[0],
                               selectbackground=self.body_bg[0],
                               selectforeground=self.header_bg[0])
        rand_box_outline = tk.Frame(quiz_book_info,
                                    bg=self.body_bg[0],
                                    bd=1)
        rand_box_body = tk.Frame(rand_box_outline,
                                 bg=self.header_bg[0])
        rand_box_tick = tk.Frame(rand_box_body,
                                 bg=self.body_bg[0],
                                 height=10,
                                 width=10)
        rand_box_tick.bind(
            "<Button-1>",
            lambda e: self._press_content(
                e, lambda: self._is_rand_trig(rand_box_tick)))
        quiz_book_info.columnconfigure(1, weight=1)
        quiz_book_info.rowconfigure(1, minsize=10)
        title_label.grid(row=0,
                         column=0)
        random_label.grid(row=2,
                          column=0,
                          sticky="e")
        title_entry.grid(row=0,
                         column=1,
                         sticky="ew")
        rand_box_outline.grid(row=2,
                              column=1,
                              sticky="w")
        rand_box_body.pack(side="top",
                           fill="both",
                           expand=1)
        rand_box_tick.pack(side="top",
                           fill="both",
                           expand=1,
                           pady=5,
                           padx=5)
        quiz_book_info.pack(side="top",
                            fill="both")
        quiz_book_frame.pack(side="top",
                             fill="both")
        self._shadow_effect(quiz_book_frame,
                            bg=self.body_bg[0],
                            side="top",
                            pady=10)
        self._label_button(self.new_quiz_frame,
                           fg=self.header_bg,
                           bg=self.body_bg,
                           text="Save Quiz Book",
                           font=(self.main_font, 20, "bold"),
                           height=1,
                           width=4,
                           side="bottom",
                           fill="both")
        self.new_quiz_frame.pack(side="top",
                                 fill="both",
                                 expand=1)

    def _is_rand_trig(self, widget):
        if self.is_rand:
            widget.config(bg=self.header_bg[0])
            self.is_rand = False
        else:
            widget.config(bg=self.body_bg[0])
            self.is_rand = True

    def _add_quiz_path(self):
        paths = filedialog.askopenfilenames()
        if len(paths) <= 0:
            return
        file_names = [Path(f).stem for f in paths]
        for file_name, path in zip(file_names, paths):
            if QuizBook.isValid(path):
                QuizBook(file_name, path)
            else:
                messagebox.showwarning("Warning",
                                       "Invalid Quiz Book")
                return
        self.update_quiz_book_list(self.display_frame)
        messagebox.showinfo("Sucessfully added",
                            f'Added: {", ".join(file_names)}')

    def _generate_choices(self, parent, choice, answer, x, y):
        # Make and display choices
        hold_choice = tk.Frame(parent, bg=self.body_bg[0])  # hold choices

        self._shadow_effect(hold_choice,
                            bg=self.header_bg[0],
                            side="right",
                            fill="y")

        if y == 0:
            self._shadow_effect(hold_choice,
                                bg=self.header_bg[0],
                                side="left",
                                fill="y")

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

        self._shadow_effect(hold_choice,
                            bg=self.header_bg[0],
                            expand=1)

        parent.rowconfigure(x, weight=1)        # Make row expandable
        parent.columnconfigure(y, weight=1)     # Make column expandable
        hold_choice.grid(row=x, column=y,
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
        header_content_indicator = self._shadow_effect(header_content_frame,
                                                       bg=self.body_bg[0],
                                                       height=2,
                                                       expand=1)

        return header_content_indicator

    def _label_button(self, parent, **kwarg):
        label_button = tk.Label(parent,
                                fg=kwarg.get("fg", ("#000000"))[0],
                                bg=kwarg.get("bg", ("#ffffff"))[0],
                                text=kwarg.get("text", None),
                                font=kwarg.get("font", None),
                                height=kwarg.get("height", None),
                                width=kwarg.get("width", None),
                                bd=kwarg.get("bd", None),
                                image=kwarg.get("image", None),
                                compound=kwarg.get("compound", None))
        label_button.pack(side=kwarg.get("side", None),
                          fill=kwarg.get("fill", None),
                          expand=kwarg.get("expand", 0))
        label_button = self._button_properties(label_button,
                                               kwarg.get("bg", ("#2e2e2e",
                                                                "#6a6a6a",
                                                                "#161616")),
                                               kwarg.get("func", None))
        return label_button

    def _button_properties(self, label, color, command):
        # Button properties

        # when mouse is over widget
        label.bind("<Enter>",
                   lambda e: self._change_color(e, color[2]))
        # when widget is clicked
        label.bind("<Button-1>",
                   lambda e: self._press_content(e, command, bg=color[1]))
        # when mouse button is released
        label.bind("<ButtonRelease-1>",
                   lambda e: self._change_color(e, color[2]))
        # when mouse is not on widget
        label.bind("<Leave>",
                   lambda e: self._change_color(e, color[0]))
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

    def _go_new_quiz_book(self):
        self._disable_all_frames()
        self._on_header(1)
        self._new_quiz_book()

    def _go_about(self):
        self._disable_all_frames()
        self._on_header(2)
        self.about_tab()

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
        self.canvas_frame.forget()
        if "quiz_book_border" in self.__dict__:
            self.quiz_book_border.destroy()
        if "question_frame" in self.__dict__:
            self.question_frame.destroy()
        if "add_quiz_frame" in self.__dict__:
            self.add_quiz_frame.destroy()
        if "about_frame" in self.__dict__:
            self.about_frame.destroy()
        if "new_quiz_frame" in self.__dict__:
            self.new_quiz_frame.destroy()
        self.master.update_idletasks()

    def resize(self, event):
        # resize Quiz Book List to fit the screen
        self.body_canvas.itemconfig(self.item, width=event.width)

    def _change_color(self, event=None, color="#6d6d6d"):
        # Change color of a widget
        event.widget.config(bg=color)

    def _press_content(self, event=None, func=None, bg=None):
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
