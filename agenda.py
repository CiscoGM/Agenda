import tkinter as tk
from tkinter import ttk, messagebox
import csv  

win = tk.Tk()
win.geometry('600x400')
win.title('Contacts Agenda')

agenda = []

""" save data in local """
FILE_NAME = "agenda.csv"

""" functions  """

def show_temp_message(title, message, duration=2000):
   
    temp_window = tk.Toplevel()
    temp_window.title(title)
    temp_window.geometry("300x100")  
    temp_window.resizable(False, False)
    temp_window.attributes("-topmost", True)  

    
    label = tk.Label(temp_window, text=message, font=("Arial", 12), wraplength=280, justify="center")
    label.pack(expand=True, padx=10, pady=10)

    
    temp_window.after(duration, temp_window.destroy)
 
def load_data():
  
    global agenda
    try:
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            agenda = [[int(row[0]), row[1], row[2]] for row in reader]
    except FileNotFoundError:
       
        agenda = []

def save_data():
    """Guarda los datos en un archivo CSV."""
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(agenda)

def add():
    name = input_name.get()
    phone = input_phone.get()
    if not (name and phone):
        messagebox.showwarning("Empty Fields", "You need to fill out all fields")
        return

    for cont in agenda:
        if name in cont and phone in cont:
            messagebox.showwarning("Existing name and phone", "Name or phone already exists")
            return

    id_a = len(agenda) + 1
    agenda.append([id_a, name, phone])
    save_data()  
    update()

def update():
    for elem in tree_agenda.get_children():
        tree_agenda.delete(elem)
    for contact in agenda:
        tree_agenda.insert('', 'end', values=(contact[0], contact[1], contact[2]))

def remove_Selected():
    selected = tree_agenda.selection()
    if selected:
        contact = tree_agenda.item(selected, "values")
        contact_list = [int(contact[0]), contact[1], contact[2]]
        if contact_list in agenda:
            agenda.remove(contact_list)
            tree_agenda.delete(selected)
            save_data()  
            show_temp_message("Contact Deleted", "The contact has been removed from the list", duration=1500)
        else:
            messagebox.showerror("Error", "Selected contact not found in agenda")
    else:
        messagebox.showwarning("No Selection", "Please select a contact to remove")

def update_Selected():
    selected = tree_agenda.selection()
    if selected:
        name = input_name.get()
        phone = input_phone.get()

        if not (name and phone):
            messagebox.showwarning("Empty Fields", "You need to fill out all fields")
            return

        contact = list(tree_agenda.item(selected, "values"))
        contact[0] = int(contact[0])

        if contact in agenda:
            idx = agenda.index(contact)
            agenda[idx] = [contact[0], name, phone]
            save_data()   
            update()
        else:
            messagebox.showerror("Error", "Selected contact not found in agenda")
    else:
        messagebox.showwarning("No Selection", "Please select a contact to update")


load_data()
""" declaration of elements  """
input_name = tk.Entry(win)
input_phone = tk.Entry(win)

lbl_name = tk.Label(win, text='Name:')
lbl_phone = tk.Label(win, text='Phone:')

btn_add = tk.Button(win, text='Add', command=add)
btn_remove = tk.Button(win, text='Remove', command=remove_Selected)
btn_update = tk.Button(win, text='Update', command=update_Selected)


""" treeview """

tree_agenda = ttk.Treeview(win, columns=('id', 'name', 'phone'), show='headings')
tree_agenda.heading("id", text="ID")
tree_agenda.heading("name", text="Name")
tree_agenda.heading("phone", text="Phone")
tree_agenda.insert("", "end", values=())


""" display the elements  """
lbl_name.grid(row=0, column=0, pady=6)
input_name.grid(row=0, column=1, pady=6)
lbl_phone.grid(row=1, column=0, pady=6)
input_phone.grid(row=1, column=1, pady=6)
btn_add.grid(row=0, column=2, pady=6)
btn_update.grid(row=1, column=2, pady=6)
btn_remove.grid(row=2, column=2, pady=6)
tree_agenda.grid(row=3, column=0, columnspan=4)

update()

win.mainloop()
