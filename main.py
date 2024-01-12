import customtkinter
import game

class main_window():
  def __init__(self):
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")

    self.root = customtkinter.CTk()
    self.root.geometry("800x600")
    self.root.resizable(False, False)

    self.ai_or_pvp = customtkinter.CTkComboBox(self.root, 700, 28, values=["PVP", "AI"], state="readonly")
    self.ai_or_pvp.grid(padx = 50, pady = 10, column = 0, row = 0)
    self.ai_or_pvp.set("PVP")
    self.time_control = customtkinter.CTkComboBox(self.root, 700, 28, values=["Time Control Off", "Time Control On"], state="readonly")
    self.time_control.set("Time Control Off")
    self.time_control.grid(padx = 50, pady = 10, column = 0, row = 1)
    self.time_control_text = customtkinter.CTkLabel(self.root, 700, text = "Time Control: 1 + 0")
    self.time_control_text.grid(padx =50, pady = 10, column = 0, row = 2)
    self.minutes = customtkinter.CTkSlider(self.root, 300, 28, from_= 1, to=60, command=self.update_time)
    self.minutes.grid(padx = 50, pady = 10, column = 0, row = 3, sticky = customtkinter.W)
    self.minutes.set(1)
    self.increment = customtkinter.CTkSlider(self.root, 300, 28, from_= 0, to=120, command=self.update_time)
    self.increment.grid(padx = 50, pady = 10, column=0, row = 3, sticky = customtkinter.E)
    self.increment.set(0)
    self.start_game_button = customtkinter.CTkButton(self.root, 700, 100, text="PLAY!", command=self.start_game)
    self.start_game_button.grid(padx = 50, pady= 10, column = 0, row = 4)

    self.root.mainloop()

  def start_game(self):
    if self.ai_or_pvp.get() == "PVP":
      if self.time_control.get() == "Time Control Off":
        self.root.destroy()
        game.main()
      else:
        self.root.destroy()
        game.main(time_control=(round(self.minutes.get())*60, round(self.increment.get())))
    elif self.ai_or_pvp.get() == "AI":
      pass

  def update_time(self, value):
    self.time_control_text.configure(text = "Time Control: " + str(round(self.minutes.get())) + " + " + str(round(self.increment.get())))

window = main_window()