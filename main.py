# import libraries
import tkinter
import game
import game_ai


# main window class
class MainWindow:
    # init function
    def __init__(self):
        # initialize tkinter and window
        self.root = tkinter.Tk()
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # ai play button
        self.play_ai_button = tkinter.Button(
            self.root,
            text="Play With AI",
            command=self.start_ai_game,
        )
        self.play_ai_button.place(width=600, height=40, x=100, y=20)

        # local multiplayer button
        self.play_local_button = tkinter.Button(
            self.root,
            text="Play Local Multiplayer",
            command=self.start_game,
        )
        self.play_local_button.place(width=600, height=40, x=100, y=80)

        # time control checkbox
        self.time_control_state = tkinter.BooleanVar()
        self.time_control_box = tkinter.Checkbutton(
            self.root,
            text="Time Control",
            variable=self.time_control_state,
            offvalue=False,
            onvalue=True,
        )

        # minutes and seconds label
        self.minutes_label = tkinter.Label(self.root, text="Minutes+")
        self.seconds_label = tkinter.Label(self.root, text="Seconds")

        self.time_control_box.place(x=100, y=160)
        self.minutes_label.place(x=100, y=220)
        self.seconds_label.place(x=400, y=220)

        # Validation function to allow valid input
        vcmd_minutes = (self.root.register(self.validate_input_minutes), "%P")
        vcmd_seconds = (self.root.register(self.validate_input_seconds), "%P")

        # minutes and seconds input boxes
        self.minutes = tkinter.StringVar()
        self.seconds = tkinter.StringVar()
        self.minutes_box = tkinter.Entry(
            self.root,
            validate="key",
            validatecommand=vcmd_minutes,
            textvariable=self.minutes,
        )
        self.seconds_box = tkinter.Entry(
            self.root,
            validate="key",
            validatecommand=vcmd_seconds,
            textvariable=self.seconds,
        )

        self.minutes_box.place(x=100, y=260)
        self.seconds_box.place(x=400, y=260)

        # start the loop
        self.root.mainloop()

    # start the ai game function
    def start_ai_game(self):
        # close window and run
        self.root.destroy()
        game_ai.main()

    # start normal game
    def start_game(self):
        if self.time_control_state.get():
            if self.minutes.get() != "" and self.seconds.get() != "":
                # if time control and valid time control selected
                # close window
                self.root.destroy()
                # start game
                game.main(
                    time_control=(
                        int(self.minutes.get()) * 60,
                        int(self.seconds.get()),
                    )
                )
        # no time control
        else:
            # close window and run
            self.root.destroy()
            game.main()

    def validate_input_seconds(self, value):
        # Validate if the input is a positive integer or 0 or empty
        if value.isdigit():
            if int(value) >= 0:
                return True
        else:
            if value == "":
                return True
        return False

    def validate_input_minutes(self, value):
        # Validate if the input is a positive integer or empty
        if value.isdigit():
            if int(value) > 0:
                return True
        else:
            if value == "":
                return True
        return False


MainWindow()
