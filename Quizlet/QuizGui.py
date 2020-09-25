import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from Quiz import QuizBook, QuizQuestion


class App():
    def __init__(self, master):
        self.master = master
        self.overlay()

    def overlay(self):
        overlayFrame = tk.Frame(self.master)
        overlayFrame.pack(expand=1, fill="both")
        header = tk.Frame(overlayFrame, bg="blue", height=50)
        content = tk.Frame(overlayFrame, bg="white")
        footer = tk.Frame(overlayFrame, width=100, height=50)
        header.pack(side="top", fill="x")
        content.pack(side="top", fill="both", expand=1)
        footer.pack(side="bottom", fill="x")
        self.master.update_idletasks()
        self.headerWidgets(header)
        self.QuizBooks(content)
        self.footerWidgets(footer)

    def headerWidgets(self, headerFrame):
        headerTitle = tk.Label(headerFrame, text="Python Quiz",
                               height=1, font=("Century Gothic", 20))
        headerTitle.pack(side="top", expand=1, pady=10)
        self.master.update_idletasks()

    def footerWidgets(self, footerFrame):
        quizBookBd = tk.Frame(footerFrame, bg="#000000", bd=1)
        quizBookButton = tk.Button(quizBookBd, text="Quiz Book",
                                   height=2, relief="flat")
        quizBookBd.pack(side="left", expand=1, fill="both")
        quizBookButton.pack(fill="both", expand=1)
        self.master.update_idletasks()

        newQuizBookBd = tk.Frame(footerFrame, bg="#000000", bd=1)
        newQuizBookButton = tk.Button(newQuizBookBd, text="New Quiz Book",
                                      height=2, relief="flat")
        newQuizBookBd.pack(side="left", expand=1, fill="both")
        newQuizBookButton.pack(fill="both", expand=1)
        self.master.update_idletasks()

        settingsBd = tk.Frame(footerFrame, bg="#000000", bd=1)
        settingsButton = tk.Button(settingsBd, text="Settings",
                                   height=2, relief="flat")
        settingsBd.pack(side="left", expand=1, fill="both")
        settingsButton.pack(fill="both", expand=1)
        self.master.update_idletasks()

    def QuizBooks(self, contentFrame):
        names = self._updateContents()
        for name in names:
            quizNum = len(QuizBook(name))
            self.content(contentFrame, name, quizNum)

    def _updateContents(self):
        contents = QuizBook.getRecent()
        filename = [Path(f).stem for f in contents]
        return filename

    def content(self, parent, title, num):
        contents = tk.Frame(parent)
        contentTitle = tk.Button(contents, text=str(title),
                                 fg="#eeeeee", bg="#333333",
                                 activeforeground="#eeeeee",
                                 activebackground="#333333",
                                 height=2, relief="flat")
        contents.pack(side="top", fill="x", padx=10, pady=15)
        contentTitle.pack(side="left", fill="both", expand=1)
        contentTitle.pack_propagate()


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.update_idletasks()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
