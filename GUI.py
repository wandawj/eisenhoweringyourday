import tkinter as tk
from eisenhowerSchedule import eisenhower

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.eisenhower = tk.Button(self)
        self.eisenhower["text"] = "Create Schedule\n(click me)"
        self.eisenhower["command"] = self.make_image
        self.eisenhower.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def make_image(self):
        eisenhower("tasks.csv", "schedule.csv")

    global img
    def save_picture(self):
        img = ImageTk.PhotoImage(Image.open("eisenhowerblock.png"))

root = tk.Tk()
app = Application(master=root)
app.mainloop()