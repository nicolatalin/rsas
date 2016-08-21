import tkinter as tk

from src.lib.scanner import Scanner
from src.lib.const import CONST
from .outputbox import OutputBox


class GUI:

    @staticmethod
    def start():
        # main window
        winroot = tk.Tk()
        winroot.title(CONST.PROG_LONGNAME)

        # menu bar
        menubar = tk.Menu(winroot)
        menubar.add_command(label='Apps', command=lambda: out.clr().ins(Scanner().printapps().str()))
        menubar.add_command(label='Arts', command=lambda: out.clr().ins(Scanner().printartifacts().str()))
        menubar.add_command(label='Scan', command=lambda: out.clr().ins(Scanner().scan(1).str()))
        menubar.add_command(label='ScanV', command=lambda: out.clr().ins(Scanner().scan(3).str()))
        menubar.add_command(label='ScanVV', command=lambda: out.clr().ins(Scanner().scan(4).str()))
        menubar.add_command(label='About', command=lambda: out.clr().ins(CONST.PROG_ABOUT))
        menubar.add_command(label='Quit', command=lambda: winroot.destroy())
        winroot.config(menu=menubar)

        # main frame and output
        fr = tk.Frame(winroot, height=300, width=500)
        fr.pack(side=tk.TOP, fill="both", expand=True)
        fr.grid_propagate(False)                # adapt on win resize
        fr.grid_rowconfigure(0, weight=1)       # adapt on win resize
        fr.grid_columnconfigure(0, weight=1)    # adapt on win resize
        out = OutputBox(fr)

        # start main window
        winroot.mainloop()
