from Timer import Timer
import tkinter as tk
import winsound
import threading
import sys


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timer")
        self.root.geometry("500x300")
        self.mainFont = ("Century Gothic", 32)
        self.sideFont = ("Century Gothic", 15)
        self.SetTimer()
        self.root.protocol("WM_DELETE_WINDOW", self._onquit)
        self.root.mainloop()

    def _onquit(self):
        self.root.destroy()
        self._stopAlarm()
        while True:
            sys.exit()
            pass

    def _timeSetter(self, tkParent, tkInt):
        tText = tk.Entry(tkParent, textvariable=tkInt, width=3, font=self.sideFont, relief="flat", justify='right')
        tText.pack(side="left")
        return tText

    def _offTimer(self):
        self.TimerState = False

    def _stopAlarm(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.AlarmState = False
        self.TimerState = True

    def _playAlarm(self):
        winsound.PlaySound("Alarm", winsound.SND_LOOP + winsound.SND_ASYNC)

    def _startTimer(self, tkInt):
        try:
            thour, tmim, tsec = [e.get() for e in tkInt]
            tsh, tsmin, tssec = tkInt
            [tnum.config(state="disabled", font=self.mainFont) for tnum in self.timerNum]
            self.buttonText.set("Stop Timer")
            self.timerButton.config(command=self._offTimer, fg="red", activeforeground="red")
            for th, tm, ts in Timer(thour, tmim, tsec):
                if self.TimerState:
                    tsh.set(th)
                    tsmin.set(tm)
                    tssec.set(ts)
                    self.AlarmState = True
                else:
                    tsh.set(0)
                    tsmin.set(0)
                    tssec.set(0)
                    self.TimerState = True
                    self.AlarmState = False
                    break
                self.root.update()
            if self.AlarmState:
                self.playSound = threading.Thread(target=self._playAlarm)
                self.stopSound = threading.Thread(target=self._stopAlarm)
                self.playSound.start()
                while self.AlarmState:
                    self.timerButton.config(command=lambda: self.stopSound.start())
                    self.root.update()
            self.timerButton.config(command=lambda: self._startTimer(tkInt), fg="black", activeforeground="black")
            [tnum.config(state="normal", font=self.sideFont) for tnum in self.timerNum]
            self.buttonText.set("Start Timer")
            self.root.update()
        except Exception:
            return

    def SetTimer(self):
        mainFrame = tk.Frame(self.root)
        mainFrame.pack(side="top", expand=1)
        timerFrame = tk.Frame(mainFrame, bd=5, height=100)
        hour = tk.IntVar()
        minute = tk.IntVar()
        second = tk.IntVar()
        self.buttonText = tk.StringVar()
        self.buttonText.set("Start Timer")
        self.TimerState = True
        self.AlarmState = False
        tFormat = [hour, minute, second]
        tLabel = ["h", "m", "s"]
        self.timerButton = tk.Button(mainFrame, textvariable=self.buttonText, bd=1, relief="solid", font=self.sideFont, command=lambda: self._startTimer(tFormat))
        timerFrame.pack(side="top", expand=1)
        self.timerButton.pack(side="top", fill="x", expand=0)
        self.timerNum = []
        self.root.update()
        for tf, tl in zip(tFormat, tLabel):
            tIn = self._timeSetter(timerFrame, tf)
            tk.Label(timerFrame, text=tl, font=self.sideFont).pack(side="left", anchor="s")
            self.timerNum.append(tIn)
            self.root.update_idletasks()
        self.root.update()


App()
