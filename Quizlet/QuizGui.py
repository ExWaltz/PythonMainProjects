import json
import tkinter as tk
from pathlib import Path
from Quiz import QuizBook, QuizQuestion


class App():
    def __init__(self, master):
        self.master = master
        self.main_font = "Bahnschrift"
        self.symbol = "Wingdings 3"
        self.header_bg = "#3e3e3e"
        self.body_bg = "#f3f3f3"
        self.content_bg = "#5d5d5d"
        self.Overlay()

    def Overlay(self):
        header = tk.Frame(self.master, bg=self.header_bg, height=50)
        header.pack(side="top", fill="x")
        body = tk.Frame(self.master, bg=self.body_bg)
        body.pack(side="top", fill="both", expand=1)
        self.master.update_idletasks()
        self.header_content(header)
        self.body_content(body)

    def header_content(self, parent_frame):
        header_frame = tk.Frame(parent_frame, bg=self.header_bg)
        header_frame.pack(side="top", fill="both")

        header_title = tk.Label(header_frame, text="Python Quiz", fg=self.body_bg, bg=self.header_bg, font=(self.main_font, 20))
        header_title.pack(side="top", pady=10)

        header_buttons_frame = tk.Frame(header_frame, bg=self.header_bg)
        header_buttons_frame.pack(side="top", fill="both")

        header_button_names = {"Contents": None, "Add": None, "Settings": None}
        self.header_indicator = []
        for key, val in header_button_names.items():
            indicator = self._generate_header_buttons(header_buttons_frame, key, val)
            indicator.config(bg=self.header_bg)
            self.header_indicator.append(indicator)

        self.header_indicator[0].config(bg=self.body_bg)

    def body_content(self, parent_frame):
        self.body_frame = tk.Frame(parent_frame, bg=self.body_bg)
        self.body_frame.pack(side="top", fill="both", expand=1)
        self.body_canvas = tk.Canvas(self.body_frame, bd=0, relief="flat", highlightthickness=0)
        body_scroll_bar = tk.Scrollbar(self.body_frame, orient="vertical", command=self.body_canvas.yview)
        display_frame = tk.Frame(self.body_canvas, bg="blue")
        self.body_canvas.config(yscrollcommand=body_scroll_bar.set)

        body_scroll_bar.pack(side="right", fill="y")
        self.item = self.body_canvas.create_window(0, 0, window=display_frame, anchor="nw")
        self.body_canvas.bind("<Configure>", self._update_scroll)
        self.master.update_idletasks()
        for _ in range(100):
            self.generate_content(display_frame)
        self.body_canvas.pack(side="top", fill="both", expand=1)
        self.body_canvas.bind("<Configure>", self.resize)

    def _generate_header_buttons(self, parent, title, command=None):
        header_content_frame = tk.Frame(parent, bg=self.header_bg)
        header_content_frame.pack(side="left", fill="x", expand=1)

        header_content_button = tk.Label(header_content_frame, text=title, fg=self.body_bg, bg=self.header_bg, font=(self.main_font, 17))
        header_content_button.pack(side="top", fill="x", expand=1)
        header_content_button.bind("<Enter>", lambda e: self._change_color(e, "#4e4e4e"))
        header_content_button.bind("<Button-1>", lambda e: self._press_content(e, command))
        header_content_button.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.header_bg))
        header_content_button.bind("<Leave>", lambda e: self._change_color(e, self.header_bg))

        header_content_indicator = tk.Frame(header_content_frame, height=2, bg=self.body_bg)
        header_content_indicator.pack(side="bottom", fill="x", expand=1)

        return header_content_indicator

    def generate_content(self, parent_frame):
        content_frame = tk.Frame(parent_frame, bg=self.content_bg)
        content_frame.pack(side="top", fill="x")

        content_shadow = tk.Frame(content_frame, bg="#4d4d4d", height=1)
        content_shadow.pack(side="bottom", fill="x")

        content_label = tk.Label(content_frame, fg=self.body_bg, text="Hello", bg=self.content_bg, height=2, width=68)
        content_label.pack(side="top", fill="x", expand=1)
        content_label.bind("<Enter>", lambda e: self._change_color(e, "#6d6d6d"))
        content_label.bind("<Button-1>", lambda e: self._press_content(e))  # Add OpenQuizFunc
        content_label.bind("<ButtonRelease-1>", lambda e: self._change_color(e, self.content_bg))
        content_label.bind("<Leave>", lambda e: self._change_color(e, self.content_bg))
        self.master.update_idletasks()

    def resize(self, event):
        self.body_canvas.itemconfig(self.item, height=event.height, width=event.width)

    def _update_scroll(self, event=None):
        self.body_canvas.config(scrollregion=self.body_canvas.bbox("all"), width=200, height=200)

    def _change_color(self, event=None, color="#6d6d6d"):
        event.widget.config(bg=color)

    def _press_content(self, event=None, func=None):
        event.widget.config(bg="#4d4d4d")
        print("YEs")


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.update_idletasks()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
