import tkinter as tk


class OutputBox:

    def __init__(self, parent):
        self.__parent = parent
        self.__txt = self.__init_txt()

    def __init_txt(self):
        # start text box
        txt = tk.Text(self.__parent, borderwidth=3, relief="sunken", font=("consolas", 12), undo=True, wrap='word', state=tk.DISABLED)
        txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # start scrollbar and associate with text box
        sb = tk.Scrollbar(self.__parent, command=txt.yview)
        sb.grid(row=0, column=1, sticky='nsew')
        txt['yscrollcommand'] = sb.set

        return txt

    # insert text at the end of the text currently in the box
    # while keeping user input disabled
    def ins(self, str):
        self.__txt.config(state=tk.NORMAL)
        self.__txt.insert(tk.END, str)
        self.__txt.config(state=tk.DISABLED)

    # clear contents of the text box
    def clr(self):
        self.__txt = self.__init_txt()
        return self
