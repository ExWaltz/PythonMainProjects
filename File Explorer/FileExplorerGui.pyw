import FileExplorer as fe
import tkinter as tk
from subprocess import check_output
from PIL import Image, ImageTk

# Todo:
#   Add More Icon(Img, Video, music, zip)


class App:
    def __init__(self, master):
        self.master = master

        # Fonts
        self.mainFont = "Bahnschrift"
        self.symbol = "Wingdings 3"
        # Images
        self.folder = Image.open("Icons/folder.png").resize((20, 20), Image.ANTIALIAS)
        self.file = Image.open("Icons/file.jpg").resize((20, 20), Image.ANTIALIAS)
        self.folder = ImageTk.PhotoImage(self.folder)
        self.file = ImageTk.PhotoImage(self.file)
        # Set Root Directory
        self.sPath = fe.getCwd()
        self.pathList = []  # Path history
        self.pathList.append(self.sPath)
        self.pathCounter = 0    # Path iterator
        self.master.update_idletasks()  # Update to lower loading speed
        self.frames()   # Initiate tkinter gui

    def frames(self):
        header = tk.Frame(self.master, bg="#202020")
        content = tk.Frame(self.master, bg="#2d2d2d")
        header.pack(fill="x", side="top")
        content.pack(fill="both", expand=1)
        self.master.update_idletasks()  # Update to lower loading speed

        self.headerContent(header)
        self.master.update_idletasks()  # Update to lower loading speed

        self.contentHead(content)
        self.master.update_idletasks()  # Update to lower loading speed

        self.files(content)
        self.master.update_idletasks()  # Update to lower loading speed

    def headerContent(self, parent):
        headerFrame = tk.Frame(parent, bg="#ffffff")
        headerFrame.pack(side="bottom", fill="x", expand=1)
        self.backButton = tk.Button(headerFrame, text="f", font=(self.symbol, 12), relief="flat", bd=0, highlightthickness=0, command=self.goBack)
        self.backButton.pack(side="left", padx=5)
        self.forwardButton = tk.Button(headerFrame, text="g", font=(self.symbol, 12), relief="flat", bd=0, highlightthickness=0, command=self.goForward)
        self.forwardButton.pack(side="left", padx=5)
        upButton = tk.Button(headerFrame, text="h", font=(self.symbol, 12), relief="flat", bd=0, highlightthickness=0, command=lambda: self.goUp(self.sPath))
        upButton.pack(side="left", padx=5)
        self.pathText = tk.Text(headerFrame, font=(self.mainFont, 12), height=1)
        self.pathText.insert(0.0, self.sPath)
        self.pathText.pack(side="left", fill="x", expand=1, padx=0)

    def contentHead(self, parent):
        contentFrame = tk.Frame(parent, bg="#2d2d2d")
        contentFrame.pack(fill="x", side="top")
        contentName = tk.Label(contentFrame, text="Title", font=(self.mainFont, 12), justify="left", anchor="w")
        contentName.pack(side="left", fill="x", expand=1)

    def _generateFile(self, path="null", isfile=False):
        dirImg = self.file
        name = fe.getName(path)
        gfileFrame = tk.Frame(self.dirFrame)
        gfileButton = tk.Button(gfileFrame, text=name, bd=0, relief="flat", anchor="w", font=(self.mainFont, 12), compound="left", highlightthickness=0, command=lambda: self._openFile(path))
        if not isfile:
            dirImg = self.folder
            gfileButton.config(command=lambda: self._wrapOpenDir(path))
        gfileButton.config(image=dirImg)
        gfileFrame.pack(fill="x", side="top", expand=1)
        gfileButton.pack(side="left", fill="x", expand=1)

    def _openFile(self, path):
        command = f'"{path}"'
        print(command)
        check_output(command, shell=True).decode()

    def _wrapOpenDir(self, path):
        self.OpenDir(path)
        self.pathList.append(self.sPath)

    def nextPList(self):
        """Get Next List item"""
        if self.pathCounter < len(self.pathList) - 1:
            self.pathCounter += 1
        rplist = self.pathList[self.pathCounter]
        return rplist

    def prevPList(self):
        """Get Previous List item"""
        if self.pathCounter > 0:
            self.pathCounter -= 1
        rplist = self.pathList[self.pathCounter]
        return rplist

    def updateButton(self):
        """Set Forward and Back button"""
        if self.pathCounter > 0:
            self.backButton.config(state="normal")
        if self.pathCounter < len(self.pathList) - 1:
            self.forwardButton.config(state="normal")
        if self.pathCounter <= 0:
            self.backButton.config(state="disabled")
        if self.pathCounter >= len(self.pathList) - 1:
            self.forwardButton.config(state="disabled")
        self.master.update_idletasks()

    def goForward(self):
        """Go to next list item in self.pathlist"""
        forpath = self.nextPList()
        self.OpenDir(forpath)

    def goBack(self):
        """Go to previous list item in self.pathlist"""
        backpath = self.prevPList()
        self.OpenDir(backpath)

    def goUp(self, path):
        """Go to root folder of current working directory"""
        self.pathCounter += 1
        rootPath = str(path).split("/")
        rootPath = "/".join(rootPath[:-1])
        if rootPath.find("/") == -1:
            rootPath += "/"
        self.OpenDir(rootPath)
        self.pathList.append(self.sPath)

    def OpenDir(self, path):
        """Show path directory items"""
        self.sPath = path
        self.updateButton()
        self.pathText.delete(0.0, "end")
        self.pathText.insert(0.0, path)
        self.dirFrame.destroy()
        self.dirFrame = tk.Frame(self.holdFrames)
        self.dirFrame.pack(side="top", fill="both", expand=1)
        fileList = fe.fileList(fe.getDir(self.sPath))
        folderList = fe.dirList(fe.getDir(self.sPath))
        fileList.sort()
        folderList.sort()
        filedirs = folderList + fileList
        for fd in filedirs:
            isFile = False
            if fe.isFile(fd):
                isFile = True
            self._generateFile(fd, isFile)

    def _updateScroll(self, event=None):
        self.filesCanvas.configure(scrollregion=self.filesCanvas.bbox("all"), width=200, height=200)

    def files(self, parent):
        self.updateButton()
        filesFrame = tk.Frame(parent, bg="#ffffff")
        filesFrame.pack(side="top", fill="both", expand=1)
        self.master.update_idletasks()

        # initiate scrollable frame
        self.filesCanvas = tk.Canvas(filesFrame, bg="#000000", bd=0, relief="flat", highlightthickness=0)
        self.holdFrames = tk.Frame(self.filesCanvas)
        filesScroll = tk.Scrollbar(filesFrame, orient="vertical", command=self.filesCanvas.yview)
        self.filesCanvas.config(yscrollcommand=filesScroll.set)

        # initiate scrollbar
        filesScroll.pack(side="right", fill="y")
        self.filesCanvas.create_window((0, 0), window=self.holdFrames, anchor="nw")
        self.holdFrames.bind("<Configure>", self._updateScroll)

        # initaite diretory frame
        self.dirFrame = tk.Frame(self.holdFrames)
        self.dirFrame.pack(side="top", fill="both", expand=1)

        # get folder and files
        fileList = fe.fileList(fe.getDir(self.sPath))
        folderList = fe.dirList(fe.getDir(self.sPath))
        fileList.sort()
        folderList.sort()
        filedirs = folderList + fileList    # show folders first then files
        self.prevDir = filedirs
        for fd in filedirs:
            isFile = False
            if fe.isFile(fd):
                isFile = True
            self._generateFile(fd, isFile)
        self._updateScroll()
        self.filesCanvas.pack(side="top", fill="both", expand=1)


def main():
    root = tk.Tk()
    root.geometry("700x500")
    root.update_idletasks()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
