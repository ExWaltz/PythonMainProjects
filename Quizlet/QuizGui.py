import tkinter as tk
import time
import random
from Quiz import PythonQuiz as qb


class App():
    """ Number 1 of my: Let's make 9 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects
    """

    def __init__(self):
        self.titleFont = ("Century Gothic bold", 32)
        self.largeFont = ("Century Gothic", 22)
        self.mainFont = ("Century Gothic", 16)
        self.smallFont = ("Century Gothic", 12)
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
        self.quizInfo = self.GetQuizzes()
        for eachQuiz, eachVal in self.quizInfo.items():
            self._main_Content(self.contentHolder, eachQuiz, eachVal)
            self.root.update_idletasks()

    def _main_Content(self, parent, title="", quizInfo=None):
        frameContent = tk.Frame(parent)
        content = tk.Button(frameContent, text=title, height=2, relief="solid", font=self.mainFont, command=lambda: self._openQuiz(title, quizInfo))
        frameContent.pack(fill="x", padx=10, pady=5)
        content.pack(fill="x")
        self._main_Content.__dict__["content"] = content
        self._main_Content.__dict__["frame"] = frameContent
        return self._main_Content

    def _startQuiz(self, title, quizInfo, bTime, rng):
        self.questionFrame.forget()
        self.holdquiz = tk.Frame(self.mainFrame)
        quizFrame = tk.Frame(self.holdquiz)
        choiceFrame = tk.Frame(self.holdquiz)
        self.holdquiz.pack(expand=1)
        quizFrame.pack(side="top")
        choiceFrame.pack(side="top")
        self.root.update()
        if rng:
            random.shuffle(quizInfo)
        self.correct = False
        self.tries = 0
        for eq in quizInfo:
            question = tk.Label(quizFrame, text=eq[0], font=self.titleFont)
            question.pack(side="top", anchor="n", pady=50)
            cList = []
            for choice in eq[1]:
                chButton = self._button(choiceFrame, choice, eq[2])
                cList.append(chButton)
            initTime = time.time()
            self.root.update()
            while not self.correct:
                self.root.update_idletasks()
                self.root.update()
            question.destroy()
            endTime = time.time()
            finalTime = float("%.2f" % (endTime - initTime))
            eq[3] = finalTime
            for e in cList:
                e.destroy()
            self.correct = False
            self.root.update()
            qb().quizTime(title, eq[0], eq[3])
        quizFrame.forget()
        choiceFrame.forget()
        tryTime = qb().AvgTime(title)
        resText = f"Total Mistakes: \t{self.tries}\nTime: \t\t{tryTime}\nBest Time: \t{bTime}"
        if tryTime < bTime:
            highScore = tk.Label(self.holdquiz, text="New High Score", font=self.titleFont)
            highScore.pack(pady=100)
        results = tk.Label(self.holdquiz, text=resText, font=self.mainFont, justify="left")
        retryQuiz = tk.Button(self.holdquiz, text="Retry", width=40, height=3, font=self.smallFont, command=lambda: self._retry(title, quizInfo, bTime))
        returnMain = tk.Button(self.holdquiz, text="Go Back To Main Menu", width=40, height=3, font=self.smallFont, command=self._returnMain)
        results.pack(pady=10)
        retryQuiz.pack()
        returnMain.pack()

    def _button(self, parent, name, answer):
        ch = tk.Button(parent, text=str(name), font=self.smallFont, command=lambda: self._answer(name, answer), width=40, height=3)
        ch.pack()
        return ch

    def _answer(self, choice, answer):
        if choice == answer:
            self.correct = True
            return
        self.tries += 1
        self.correct = False

    def _returnMain(self):
        self.mainFrame.destroy()
        self._main_Frame()

    def _retry(self, title, quizInfo, bTime):
        self.holdquiz.destroy()
        self._startQuiz(title, quizInfo, bTime)

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
            nquizInfo = f"Random: \t{quizInfo[1][1]}\n"
            if quizInfo[1][2]:
                nquizInfo += f"Best Time:\t{quizInfo[1][3]}"
            numQuiz = tk.Label(quizBookFrame, text=nquizText, font=self.largeFont, wraplength=300)
            infoQuiz = tk.Label(quizBookFrame, text=nquizInfo, font=self.mainFont, wraplength=300, justify="left")
            startButton = tk.Button(self.questionFrame, text="Start Quiz", height=3, font=self.smallFont, command=lambda: self._startQuiz(title, quizInfo[0], quizInfo[1][3], quizInfo[1][1]))
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
