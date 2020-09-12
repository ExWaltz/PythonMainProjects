from Timer import Timer
import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timer")
        self.root.geometry("500x300")
        self.mainFont = ("Century Gothic", 12)
        self.SetTimer()
        self.root.mainloop()

    def _timeSetter(self, tkParent, tkInt):
        tText = tk.Entry(tkParent, textvariable=tkInt, width=5, font=self.mainFont, justify='right')
        tText.pack(side="left")
        return tText

    def _startTimer(self, tkInt):
        thour, tmim, tsec = [e.get() for e in tkInt]
        for tm in Timer(thour, tmim, tsec):
            print(tm)
            self.root.update()

    def SetTimer(self):
        mainFrame = tk.Frame(self.root)
        mainFrame.pack(side="top", expand=1)
        timerFrame = tk.Frame(mainFrame, bd=5, height=100)
        hour = tk.IntVar()
        minute = tk.IntVar()
        second = tk.IntVar()
        tFormat = [hour, minute, second]
        tLabel = ["h", "m", "s"]
        timerButton = tk.Button(mainFrame, text="Start Timer", font=self.mainFont, command=lambda: self._startTimer(tFormat))
        timerFrame.pack(side="top", expand=1)
        timerButton.pack(side="top", fill="x")
        for tf, tl in zip(tFormat, tLabel):
            self._timeSetter(timerFrame, tf)
            tk.Label(timerFrame, text=tl, font=self.mainFont).pack(side="left")


App()
