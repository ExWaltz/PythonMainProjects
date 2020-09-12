import tkinter as tk
from Quiz import PythonQuiz as pq
from tkinter import ttk


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyQuiz")
        self.root.geometry("500x600")
        self._main_Frame()
        self.GetQuizzes()
        self.root.mainloop()

    def _main_Frame(self):
        BigFont = ("Century Gothic bold", 20)
        self.mainFrame = tk.Frame(self.root)
        TextFrame = tk.Frame(self.mainFrame, bg="#ffffff",
                             width=500, height=70, bd=10)
        mainText = tk.Label(TextFrame, text="PyQuiz", font=BigFont)
        self.mainFrame.pack(fill="both")
        TextFrame.pack(fill="x")
        mainText.pack()
        self._hLine(self.mainFrame)
        contentHolder = tk.Frame(self.mainFrame)
        contentHolder.pack(fill="both")

    def _main_Content(self, parent, title=""):
        frameContent = tk.Frame(parent)
        content = tk.Button(frameContent, text=title, height=2)
        frameContent.pack(fill="x", padx=10, pady=5)
        content.pack(fill="x")
        self._main_Content.__dict__["content"] = content
        self._main_Content.__dict__["frame"] = frameContent
        return self._main_Content

    def _hLine(self, parent, bg_="#000000"):
        hrline = tk.Frame(parent, bg=bg_)
        hrline.pack(fill="x")
        return hrline

    def GetQuizzes(self):
        quizzes = pq().AllQuizBook[0]
        print(quizzes)


App()