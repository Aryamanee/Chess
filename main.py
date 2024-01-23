import tkinter
import game
import game_ai


class MainWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.play_ai_button = tkinter.Button(
            self.root,
            text="Play With AI",
            command=self.start_ai_game,
        )
        self.play_ai_button.place(width=600, height=40, x=100, y=20)
        self.play_ai_button = tkinter.Button(
            self.root,
            text="Play Local Multiplayer",
            command=self.start_game,
        )
        self.play_ai_button.place(width=600, height=40, x=100, y=80)
        self.time_control_state = tkinter.BooleanVar()
        self.time_control_box = tkinter.Checkbutton(
            self.root,
            text="Time Control",
            variable=self.time_control_state,
            offvalue=False,
            onvalue=True,
        )
        self.minutes_label = tkinter.Label(self.root, text="Minutes+")
        self.seconds_label = tkinter.Label(self.root, text="Seconds")
        self.time_control_box.place(x=100, y=160)
        self.minutes_label.place(x=100, y=220)
        self.seconds_label.place(x=400, y=220)
        self.minutes_box = tkinter.Entry(self.root)
        self.seconds_box = tkinter.Entry(self.root)
        self.minutes_box.place(x=100, y=260)
        self.seconds_box.place(x=400, y=260)
        self.root.mainloop()

    def start_ai_game(self):
        self.root.destroy()
        game_ai.main()

    def start_game(self):
        self.root.destroy()
        if self.time_control_state == tkinter.TRUE:
            game.main(
                time_control=(
                    int(self.minutes_box.get()) * 60,
                    int(self.seconds_box.get()),
                )
            )
        else:
            game.main()


MainWindow()
