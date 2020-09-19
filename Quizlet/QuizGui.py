import tkinter as tk
from tkinter import ttk
import time
import random
from Quiz import PythonQuiz as qb


class App():
    """ Number 1 of my: Let's make 9 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects
        Note to self:
            * Don't put everything in one class
            * AAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAA
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
        self._mainFrame()
        self.root.mainloop()

    def _mainFrame(self):
        self.mainFrame = tk.Frame(self.root)
        TextFrame = tk.Frame(self.mainFrame, bg="#ffffff", width=500, height=70, bd=10)
        self.mainText = tk.Label(TextFrame, text="PyQuiz", font=self.titleFont)
        self.goBack = tk.Button(TextFrame, text="Back", font=self.smallFont)
        self.mainFrame.pack(fill="both", expand=1)
        TextFrame.pack(fill="x")
        self.mainText.pack()
        self._hLine(self.mainFrame)
        self.contentHolder = tk.Frame(self.mainFrame)
        self.contentHolder.pack(fill="both", pady=10)
        newQuiz = tk.Button(self.contentHolder, text="New Quiz", height=2, relief="solid", font=self.mainFont, command=self._newQuiz)
        newQuiz.pack(fill="x")
        self._hLine(self.contentHolder).pack_configure(pady=10)
        self.root.update_idletasks()
        self.quizInfo = self.GetQuizzes()
        for eachQuiz, eachVal in self.quizInfo.items():
            self._mainContent(self.contentHolder, eachQuiz, eachVal)
            self.root.update_idletasks()

    def _mainContent(self, parent, title="", quizInfo=None):
        frameContent = tk.Frame(parent)
        content = tk.Button(frameContent, text=title, height=2, relief="solid", font=self.mainFont, command=lambda: self._openQuiz(title, quizInfo))
        frameContent.pack(fill="x", padx=10, pady=5)
        content.pack(fill="x")
        self._mainContent.__dict__["content"] = content
        self._mainContent.__dict__["frame"] = frameContent
        return self._mainContent

    def _startQuiz(self, title, quizInfo, bTime, rng):
        self.questionFrame.forget()
        self.goBack.destroy()
        self.holdquiz = tk.Frame(self.mainFrame)
        quizFrame = tk.Frame(self.holdquiz)
        choiceFrame = tk.Frame(self.holdquiz)
        self.holdquiz.pack(expand=1)
        quizFrame.pack(side="top")
        choiceFrame.pack(side="bottom", expand=0)
        self.root.update()
        if rng:
            random.shuffle(quizInfo)
        self.correct = False
        self.tries = 0
        for eq in quizInfo:
            question = tk.Label(quizFrame, text=eq[0], font=self.titleFont)
            question.pack(side="top", anchor="n", pady=50)
            cList = []
            col = 0
            for row, choice in enumerate(eq[1]):
                chButton = self._button(choiceFrame, choice, eq[2], col, row)
                cList.append(chButton)
                if row % 2 == 1:
                    col += 1
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
            highScore.pack()
        results = tk.Label(self.holdquiz, text=resText, font=self.mainFont, justify="left")
        retryQuiz = tk.Button(self.holdquiz, text="Retry", width=40, height=3, font=self.smallFont, command=lambda: self._retry(title, quizInfo, bTime, rng))
        returnMain = tk.Button(self.holdquiz, text="Go Back To Main Menu", width=40, height=3, font=self.smallFont, command=self._returnMain)
        results.pack(pady=50)
        retryQuiz.pack()
        returnMain.pack()

    def _openQuiz(self, title, quizInfo):
        self.contentHolder.forget()
        self.mainText.config(text=title)
        self.goBack.config(command=self._returnMain)
        self.goBack.place(relx=0, rely=0.20)
        self.questionFrame = tk.Frame(self.mainFrame)
        self.questionFrame.pack(expand=1)
        quizBookFrame = tk.Frame(self.questionFrame, bg="blue", width=2000, bd=100)
        self.root.update_idletasks()
        print(quizInfo)
        if len(quizInfo[0]) != 0:
            nquizText = f"{len(quizInfo[0])} quiz"
            nquizInfo = f"Random: \t{quizInfo[1][1]}\n"
            if quizInfo[1][2]:
                nquizInfo += f"Best Time:\t{quizInfo[1][3]}"
            numQuiz = tk.Label(quizBookFrame, text=nquizText, font=self.largeFont, wraplength=300)
            infoQuiz = tk.Label(quizBookFrame, text=nquizInfo, font=self.mainFont, wraplength=300, justify="left")
            startButton = tk.Button(self.questionFrame, text="Start Quiz", height=3, font=self.smallFont, command=lambda: self._startQuiz(title, quizInfo[0], quizInfo[1][3], quizInfo[1][1]))
            newQuiz = tk.Button(self.questionFrame, text="New Quiz", font=self.smallFont, command=lambda: self._newQuiz(quizInfo[1][0], quizInfo[0], quizInfo[1][1], quizInfo[1][2]))
            editQuiz = tk.Button(self.questionFrame, text="Edit Quiz", font=self.smallFont)
            editQuiz.pack(side="top", anchor="e", pady=10)
            newQuiz.place(relx=0.815, rely=0.022, anchor="ne")
            numQuiz.pack()
            infoQuiz.pack()
            startButton.pack(side="bottom", fill="x", pady=10)
        else:
            numQuiz = tk.Label(quizBookFrame, text="No Quizzes Found", font=self.titleFont, wraplength=300)
            newQuiz = tk.Button(self.questionFrame, text="New Quiz", height=3, font=self.smallFont, command=self._newQuiz)
            newQuiz.pack(side="bottom", fill="x", pady=30)
            numQuiz.pack(expand=1)
        quizBookFrame.pack(side="top")
        self.root.update()

    def _newQuiz(self, header="New Quiz", questionInfo=[""], mode=True, qrandom=False, recordTime=True):
        try:
            self._delWidget(self.questionFrame)
        except Exception:
            pass
        self._delWidget(self.contentHolder)
        self.goBack.config(command=self._returnMain)
        self.goBack.place(relx=0, rely=0.20)
        self.mainText.config(text=header)
        self.newQuizFrame = tk.Frame(self.mainFrame, bd=10)
        self.newQuizFrame.pack(fill="both")

        titleFrame = tk.Frame(self.newQuizFrame)
        titleFrame.pack(side="top", anchor="w", pady=10)
        titleText = tk.Label(titleFrame, text="Title:\t", font=self.mainFont)
        title = tk.Entry(titleFrame, font=self.mainFont)
        titleText.pack(side="left", anchor="nw")
        title.pack(side="top", fill="x")

        OptFrame = tk.Frame(self.newQuizFrame)
        OptFrame.pack(side="top", anchor="n", pady=10)
        randVar = tk.BooleanVar()
        recTVar = tk.BooleanVar()
        randVar.set(qrandom)
        recTVar.set(recordTime)
        randomOpt = tk.Radiobutton(OptFrame, text="Random", variable=randVar, value=True)
        recTimeOpt = tk.Radiobutton(OptFrame, text="Record Time", variable=recTVar, value=True)
        resetOpt = tk.Button(OptFrame, text="Reset Options", relief="solid", command=lambda: self._resetOpt(randVar, recTVar))
        randomOpt.pack(side="left", anchor="nw")
        recTimeOpt.pack(side="left", anchor="nw")
        resetOpt.pack(side="top", anchor="nw")

        questionFrame = tk.Frame(self.newQuizFrame)
        questionFrame.pack(side="top", anchor="nw", pady=10)
        questionTitle = tk.Label(questionFrame, text="Question:\t", font=self.mainFont)
        question = tk.Entry(questionFrame, font=self.mainFont)
        questionTitle.pack(side="left", anchor="nw")
        question.pack(side="left", anchor="nw")

        qTypeFrame = tk.Frame(self.newQuizFrame)
        qTypeFrame.pack(side="top", anchor="n")
        qTypeMode = tk.BooleanVar()
        qTypeMode.set(mode)
        trueOrFalseType = tk.Radiobutton(qTypeFrame, text="True or False", font=self.smallFont, variable=qTypeMode, value=True)
        choicesType = tk.Radiobutton(qTypeFrame, text="Multiple Choice", font=self.smallFont, variable=qTypeMode, value=False)
        trueOrFalseType.pack(side="left")
        choicesType.pack(side="left")
        self.root.update_idletasks()

        choiceList = []

        def choiceMode():
            cFrame = tk.Frame(self.newQuizFrame)
            cFrame.pack(side="top", anchor="nw")
            mulFrame = tk.Frame(cFrame)
            mulFrame.pack(side="top", anchor="nw")
            choiceTitle = tk.Label(mulFrame, text="Choices:\t", font=self.mainFont)
            choiceTitle.pack(side="left", anchor="nw")
            addChoice = tk.Button(mulFrame, text="Add Choices")
            addChoice.config(command=lambda: self._choices(mulFrame, addChoice, choiceList))
            for e in questionInfo:
                cOpt = self._choices(mulFrame, addChoice, choiceList)
                cOpt.insert(1, str(e[1]))
            addChoice.pack(side="top", fill="x", pady=10)

            def UpdateAnswers(combobox):
                answerText = []
                for e in choiceList:
                    answerText.append(e.get())
                combobox["values"] = answerText

            answerFrame = tk.Frame(cFrame)
            answerFrame.pack(side="top", anchor="nw")
            answerTitle = tk.Label(answerFrame, text="Answers:\t", font=self.mainFont)
            answerTitle.pack(side="left", anchor="nw")
            answerCombobox = ttk.Combobox(answerFrame)
            answerCombobox.configure(postcommand=lambda: UpdateAnswers(answerCombobox))
            answerCombobox.pack(side="left")
            UpdateAnswers(answerCombobox)
            return cFrame

        tofVar = tk.BooleanVar()

        def trueOrFalseMode():
            tofFrame = tk.Frame(self.newQuizFrame)
            tofTitle = tk.Label(tofFrame, text="Answer:\t", font=self.mainFont)
            tofTitle.pack(side="left", anchor="nw")
            trueButton = tk.Radiobutton(tofFrame, text="True", indicatoron=0, font=self.mainFont, width=10, variable=tofVar, value=True)
            falseButton = tk.Radiobutton(tofFrame, text="false", indicatoron=0, font=self.mainFont, width=10, variable=tofVar, value=False)
            tofFrame.pack(side="top", anchor="nw")
            trueButton.pack(side="left")
            falseButton.pack(side="left")
            return tofFrame

        def choiceTrigger(*args):
            if qTypeMode.get():
                mList[1].forget()
                mList[0].pack(side="top", anchor="nw")
            else:
                mList[0].forget()
                mList[1].pack(side="top", anchor="nw")
            self.root.update_idletasks()

        mList = [trueOrFalseMode(), choiceMode()]
        qTypeMode.trace("w", choiceTrigger)
        choiceTrigger("s")

    def _choices(self, parent, button, cList=[]):
        def delWid(cVal, widget):
            cList.remove(cVal)
            self._delWidget(widget)
        chFrame = tk.Frame(parent)
        chFrame.pack()
        choice = tk.Entry(chFrame, font=self.mainFont)
        delChoice = tk.Button(chFrame, width=2, height=1, text="x", fg="red", command=lambda: delWid(choice, chFrame))
        choice.pack(side="left")
        delChoice.pack(side="left")
        button.forget()
        button.pack(side="top", fill="x", pady=10)
        cList.append(choice)
        return choice

    def _delWidget(self, *widget):
        for e in widget:
            e.destroy()

    def _resetOpt(self, *var):
        for e in var:
            e.set(False)

    def _hLine(self, parent, bg_="#000000"):
        hrline = tk.Frame(parent, bg=bg_)
        hrline.pack(fill="x")
        return hrline

    def _button(self, parent, name, answer, row, col):
        row = row % 2
        col = col % 2
        ch = tk.Button(parent, text=str(name), font=self.smallFont, command=lambda: self._answer(name, answer), width=20, height=3)
        ch.grid(row=row, column=col)
        return ch

    def _answer(self, choice, answer):
        if choice == answer:
            self.correct = True
            return
        self.tries += 1
        self.correct = False

    def _returnMain(self):
        self._delWidget(self.mainFrame)
        self._mainFrame()

    def _retry(self, title, quizInfo, bTime, rng):
        self._delWidget(self.holdquiz)
        self._startQuiz(title, quizInfo, bTime, rng)

    def GetQuizzes(self):
        quizzes = qb().AllQuizBook
        quizInfo = {}
        for each in quizzes:
            quizInfo[each.name] = [each.allquiz, each.info]
        return quizInfo


App()
