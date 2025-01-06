import pyperclip
import random
import string
from tkinter import *
from tkinter import messagebox
import json

# ---------------------------- FINDING PASSWORD ------------------------------- #
def find_password():
    website = website_insert.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found!")
    except json.JSONDecodeError:
        messagebox.showinfo(title="Error", message="Error decoding the JSON file!")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generating(length=12):
    password_insert.delete(0, END)
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    password_insert.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_insert.get()
    email = username_insert.get()
    password = password_insert.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Make sure you haven't left any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"The entered details: \nEmail: {email} \nPassword: {password} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    #Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    #Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                password_insert.delete(0, END)
                website_insert.delete(0, END)
                username_insert.delete(0, END)
        else:
            password_insert.delete(0, END)
            website_insert.delete(0, END)
            username_insert.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file= "logo.png")
canvas.create_image(100, 100, image= logo_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:", font="Arial")
label_website.grid(column=0, row=1)
website_insert = Entry(width=21)
website_insert.focus()
website_insert.grid(column=1, row=1)

label_username = Label(text="Email/Username:", font="Arial")
label_username.grid(column=0, row=2)
username_insert = Entry(width=35)
username_insert.grid(column=1, row=2, columnspan=2)

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)
password_insert = Entry(width=21)
password_insert.grid(column=1, row=3)

button_generate = Button(text="Generate Password", width=10, command=password_generating)
button_generate.grid(column=2, row=3)

button_add = Button(text="Add", width=33, command=save)
button_add.grid(column=1, row=4, columnspan=2)

button_search = Button(text="Search", width=10, command=find_password)
button_search.grid(column=2, row=1)


window.mainloop()

