import tkinter as tk
import random
from Quiz import PythonQuiz as qb


class App():
    def __init__(self):
        self.titleFont = ("Century Gothic bold", 32)
        self.largeFont = ("Century Gothic", 22)
        self.mainFont = ("Century Gothic", 16)
        self.root = tk.Tk()
        self.root.title("PyQuiz")
        self.root.geometry("500x600")
        self.root.update()
        self._main_Frame()
        self.root.mainloop()

    def _main_Frame(self):
        self.mainFrame = tk.Frame(self.root)
        TextFrame = tk.Frame(self.mainFrame, bg="#ffffff",
                             width=500, height=70, bd=10)
        self.mainText = tk.Label(TextFrame, text="PyQuiz", font=self.titleFont)
        self.mainFrame.pack(fill="both", expand=1)
        TextFrame.pack(fill="x")
        self.mainText.pack()
        self._hLine(self.mainFrame)
        self.contentHolder = tk.Frame(self.mainFrame)
        self.contentHolder.pack(fill="both", pady=10)
        self.root.update_idletasks()
        quizInfo = self.GetQuizzes()
        for eachQuiz, eachVal in quizInfo.items():
            self._main_Content(self.contentHolder, eachQuiz, eachVal)
            self.root.update_idletasks()

    def _main_Content(self, parent, title="", quizInfo=None):
        frameContent = tk.Frame(parent)
        content = tk.Button(frameContent, text=title, height=2, relief="solid", command=lambda: self._openQuiz(title, quizInfo))
        frameContent.pack(fill="x", padx=10, pady=5)
        content.pack(fill="x")
        self._main_Content.__dict__["content"] = content
        self._main_Content.__dict__["frame"] = frameContent
        return self._main_Content

    def _startQuiz(self, quizInfo):
        self.questionFrame.forget()
        self.holdquiz = tk.Frame(self.mainFrame)
        quizFrame = tk.Frame(self.holdquiz)
        choiceFrame = tk.Frame(self.holdquiz)
        self.holdquiz.pack(expand=1)
        quizFrame.pack(side="top")
        choiceFrame.pack(side="top")
        self.root.update()
        self.correct = False
        for eq in quizInfo:
            question = tk.Label(quizFrame, text=eq[0])
            question.pack()
            for choice in eq[1]:
                print(choice)
                # not properly adding choices
                choices = tk.Button(choiceFrame, text=choice, command=lambda: self._answer(choice, eq[2]))
                choices.pack()
            while not self.correct:
                self.root.update_idletasks()
                self.root.update()

    def _answer(self, choice, answer):
        print([choice, answer])
        if choice == answer:
            self.correct = True
            return
        self.correct = False

    def _openQuiz(self, title, quizInfo):
        self.contentHolder.forget()
        self.mainText.config(text=title)
        self.questionFrame = tk.Frame(self.mainFrame)
        self.questionFrame.pack(expand=1)
        quizBookFrame = tk.Frame(self.questionFrame, bg="blue", width=2000, bd=100)
        quizBookFrame.pack(side="top")
        self.root.update_idletasks()
        if len(quizInfo[0]) != 0:
            nquizText = f"{len(quizInfo[0])} quiz"
            nquizInfo = f"Random: {quizInfo[1][1]}\nRecord Time: {quizInfo[1][2]}"
            numQuiz = tk.Label(quizBookFrame, text=nquizText, font=self.largeFont, wraplength=300)
            infoQuiz = tk.Label(quizBookFrame, text=nquizInfo, font=self.mainFont, wraplength=300, justify="left")
            startButton = tk.Button(self.questionFrame, text="Start Quiz", height=3, command=lambda: self._startQuiz(quizInfo[0]))
            numQuiz.pack()
            infoQuiz.pack()
            startButton.pack(fill="x", pady=10)
            self.root.update()
        else:
            numQuiz = tk.Label(quizBookFrame, text="No Quizzes Found", font=self.titleFont, wraplength=300)
            startButton = tk.Button(self.questionFrame, text="New Quizlet", height=3)
            startButton.pack(fill="x", pady=10)
            numQuiz.pack(expand=1)
            self.root.update()

    def _hLine(self, parent, bg_="#000000"):
        hrline = tk.Frame(parent, bg=bg_)
        hrline.pack(fill="x")
        return hrline

    def GetQuizzes(self):
        quizzes = qb().AllQuizBook
        quizInfo = {}
        for each in quizzes:
            quizInfo[each.name] = [each.allquiz, each.info]
        return quizInfo


App()
