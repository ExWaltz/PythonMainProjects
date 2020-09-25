import FileExplorer as fe
import tkinter as tk
from PIL import Image, ImageTk


class App:
    def __init__(self, master):
        self.master = master
        self.mainFont = "Gill Sans Nova"
        self.folder = Image.open("Icons/folder.png").resize((20, 20), Image.ANTIALIAS)
        self.file = Image.open("Icons/file.jpg").resize((20, 20), Image.ANTIALIAS)
        self.folder = ImageTk.PhotoImage(self.folder)
        self.file = ImageTk.PhotoImage(self.file)
        self.frames()

    def frames(self):
        header = tk.Frame(self.master, bg="#202020", height=100)
        content = tk.Frame(self.master, bg="#2d2d2d")
        header.pack(fill="x", side="top")
        content.pack(fill="both", expand=1)
        self.contentHead(content)
        self.files(content)

    def contentHead(self, parent):
        contentFrame = tk.Frame(parent, bg="#2d2d2d")
        contentFrame.pack(fill="x", side="top")
        contentName = tk.Label(contentFrame, text="Title", font=(self.mainFont, 12), justify="left", anchor="w")
        contentName.pack(side="left", fill="x", expand=1)

    def _generateFile(self, parent):
        gfileFrame = tk.Frame(parent)
        gfileButton = tk.Button(gfileFrame, text="Hello", bd=0, relief="flat", font=(self.mainFont, 12), image=self.file, compound="left", highlightthickness=0)
        gfileFrame.pack(fill="x", side="top", expand=1)
        gfileButton.pack(side="left", fill="x", expand=1)

    def _updateScroll(self, event):
        self.filesCanvas.configure(scrollregion=self.filesCanvas.bbox("all"), width=200, height=200)

    def files(self, parent):
        filesFrame = tk.Frame(parent, bg="#ffffff")
        filesFrame.pack(side="top", fill="both", expand=1)
        self.filesCanvas = tk.Canvas(filesFrame, bg="#000000", bd=0, relief="flat", highlightthickness=0)
        holdFrames = tk.Frame(self.filesCanvas)
        filesScroll = tk.Scrollbar(filesFrame, orient="vertical", command=self.filesCanvas.yview)
        self.filesCanvas.config(yscrollcommand=filesScroll.set)

        filesScroll.pack(side="right", fill="y")
        self.filesCanvas.create_window((0, 0), window=holdFrames, anchor="nw")
        holdFrames.bind("<Configure>", self._updateScroll)
        self._generateFile(holdFrames)
        self._updateScroll(None)
        self.filesCanvas.pack(side="top", fill="both", expand=1)


def main():
    root = tk.Tk()
    root.geometry("500x500")
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
