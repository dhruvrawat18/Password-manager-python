from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json

YOUR_PREFERRED_EMAIL = "random@email.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any of the fields empty")
    else:
        try:
            with open("Manager.json", "r") as file:
                # Reading the old data into a dict
                data = json.load(file)

        except FileNotFoundError:
            with open("Manager.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating the old data by adding into the dict
            data.update(new_data)

            with open("Manager.json", "w") as file:
                # Writing/saving the updated data to the file
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORDS ------------------------------- #
def search_password():
    website_search = website_entry.get()
    try:
        with open("Manager.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data file found")

    else:
        if website_search in data:
            messagebox.showinfo(title="Login Details", message=f"Email: {data[website_search]['email']}\n "
                                                           f"Password: {data[website_search]['password']}")
        else:
            messagebox.showinfo(title="Error", message="No details for this website exists!")

    finally:
        website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Safe Pass")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="EW", pady=10)
website_entry.focus()

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=10)
email_entry.insert(0, YOUR_PREFERRED_EMAIL)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW", pady=10)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="we")

search_button = Button(text="Search", command=search_password)
search_button.grid(row=1, column=2, sticky="we")

add_button = Button(text="Add", width=36, command=add_data)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")


window.mainloop()
