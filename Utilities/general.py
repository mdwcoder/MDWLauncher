from tkinter import messagebox

def ErrorMsg(title, text) -> None:
    messagebox.showerror(title, text)
    
def AdvMsg(title, text) -> None:
    messagebox.showwarning(title, text)
    
def QstMsg(title, text):
    if messagebox.askquestion(title, text) == "yes":
        return True
    else:
        return False
    