import tkinter
from tkinter import messagebox
from password_generator import generate_password
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    password_input.delete(0, tkinter.END)
    password_input.insert(0, generate_password())
    pyperclip.copy(password_input.get())
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    new_data = {website: {"email": email, "password": password}}

    if website == "" or password == "":
        messagebox.showerror(title="Empty fields", message="Fields can not be empty.")
    else:
        try:
            file = open("data.json", mode="r")
        except FileNotFoundError:
            file = open("data.json", mode="w")
            json.dump(new_data, file, indent=4)
        else:
            try:
                data = json.load(file)
                data.update(new_data)
                file.close()

                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)

            except json.decoder.JSONDecodeError:
                file = open("data.json", mode="w")
                json.dump(new_data, file, indent=4)
                file.close()
        finally:
            file.close()


        website_input.delete(0, tkinter.END)
        password_input.delete(0, tkinter.END)

def search():
    search_term = website_input.get()
    print(search_term)

    if search_term == "":
        return 
    
    try:
        with open("data.json", mode="r") as file:
            json_data = json.load(file)

            if search_term in json_data.keys():
                found_item = json_data[search_term]
                email = found_item["email"]
                password = found_item["password"]

                email_input.delete(0, tkinter.END)
                email_input.insert(0, email)
                password_input.delete(0, tkinter.END)
                password_input.insert(0, password)
            else:
                messagebox.showerror(title="Not found", message=f"Website {search_term} not found.")

    except FileNotFoundError:
        messagebox.showerror(title="No Passwords", message="There are no passwords saved yet.")
        
# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Pyssword Manager")
window.config(padx=50, pady=50)

canvas = tkinter.Canvas(height=200, width=200)
logo_image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 93, image=logo_image)
canvas.grid(column=1, row=0)

label_1 = tkinter.Label(text="Website:", width=15)
label_2 = tkinter.Label(text="Email/Username:", width=15)
label_3 = tkinter.Label(text="Password:", width=15)

website_input = tkinter.Entry(width=37)
email_input = tkinter.Entry(width=56)
password_input = tkinter.Entry(width=37)

button_search = tkinter.Button(text="Search", padx=10 ,pady=0, width=15, command=search)
button_gen = tkinter.Button(text="Generate Password", padx=10, pady=0, width=15, command=generate)
button_add = tkinter.Button(text="Add", padx=0, pady=0, width=56, command=save)

label_1.grid(column=0, row=1)
label_2.grid(column=0, row=2)
label_3.grid(column=0, row=3)

website_input.grid(column=1, row=1)
email_input.grid(column=1, row=2, columnspan=2)
password_input.grid(column=1, row=3)

button_search.grid(column=2, row=1)
button_gen.grid(column=2, row=3)
button_add.grid(column=1, row=4, columnspan=2)

website_input.focus()
email_input.insert(0, "paulowells@gmail.com")

window.mainloop()