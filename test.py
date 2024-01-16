import tkinter
import tkinter.ttk
import game

root = tkinter.Tk()
def play():
    root.destroy()
    game.main()
button = tkinter.ttk.Button(root, text="Play", command=play)
button.pack()
root.mainloop()

