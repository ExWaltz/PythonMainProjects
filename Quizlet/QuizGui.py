import tkinter as tk
from tkinter import ttk
from Quiz import QuizBook, QuizQuestion


class App():
    def __init__(self, master):
        self.master = master
        self.menuBar()
        self.overlay()

    def overlay(self):
        overlayFrame = tk.Frame(self.master)
        overlayFrame.pack(expand=1, fill="both")
        header = tk.Frame(overlayFrame, bg="blue", height=50)
        content = tk.Frame(overlayFrame, bg="white")
        footer = tk.Frame(overlayFrame, bg="black", width=100, height=50)
        header.pack(side="top", fill="x")
        content.pack(side="top", fill="both", expand=1)
        footer.pack(side="bottom", fill="x")
        self.headerWidgets(header)
        self.QuizBooks(content)
        self.footerWidgets(footer)

    def menuBar(self):
        menuBar = tk.Menu(self.master)
        filemenu = tk.Menu(menuBar, tearoff=0)
        filemenu.add_command(label="New Quiz Book")
        filemenu.add_command(label="Open Quiz Book")
        menuBar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menuBar)

    def headerWidgets(self, headerFrame):
        headerTitle = tk.Label(headerFrame, text="Python Quiz", height=1, font=("Century Gothic", 20))
        headerTitle.pack(side="top", expand=1, pady=10)

    def footerWidgets(self, footerFrame):
        quizBookButton = tk.Button(footerFrame, text="Quiz Book", height=2, relief="solid")
        newQuizBookButton = tk.Button(footerFrame, text="New Quiz Book", height=2, relief="solid")
        settingsButton = tk.Button(footerFrame, text="Settings", height=2, relief="solid")
        quizBookButton.pack(side="left", fill="both", expand=1)
        newQuizBookButton.pack(side="left", fill="both", expand=1)
        settingsButton.pack(side="left", fill="both", expand=1)

    def QuizBooks(self, contentFrame):

    def content(self, parent, title):
        contents = tk.Frame(contentFrame)
        contents.pack(side="top", expand=1, fill="both", padx=10, pady=15)


def main():
    root = tk.Tk()
    root.geometry("500x500")
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
