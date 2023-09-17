from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
#key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

window = Tk()
window.title("Secret Note")
window.minsize(400, 600)
window.configure(pady=30)

image = PhotoImage(file="logo.png")
resized = image.subsample(12)
label = Label(window, image=resized, pady=30)
label.pack(pady=30)

#title
title_label = Label(text="Set a name for your secret note")
title_label.pack()
title_entry = Entry()
title_entry.pack()

#note
note_label = Label(text="Enter your secret note here")
note_label.pack()
note_text = Text(width=50, height=10)
note_text.pack()

#parola
password_label = Label(text="Set a password for your note")
password_label.pack()
password_entry = Entry()
password_entry.pack()

password1 = None
password2 = None


def encrypt_and_save():
    title = title_entry.get()
    note = note_text.get("1.0", END)
    global password1
    password1 = password_entry.get()

    if len(title.strip()) == 0:
        messagebox.showerror(message="You didn't give your note a name")
    elif len(note.strip()) == 0:
        messagebox.showerror(message="Please write a note")
    elif len(password1) == 0:
        messagebox.showerror(message="You didn't enter a password")
    else:
        encrypted_note = cipher_suite.encrypt(note.encode())
        file_name = title + "_note.txt"
        with open(file_name, "wb") as file:
            file.write(encrypted_note)
        title_entry.delete(0, END)
        note_text.delete("1.0", END)
        password_entry.delete(0, END)
        messagebox.showinfo(message=f"Note saved as {file_name}")

save_button = Button(text="Save / Encrypt", command=encrypt_and_save)
save_button.pack(pady=10)

#şifre
def decrypt_and_display():
    title = title_entry.get()
    note = note_text.get("1.0", END)
    global password2
    password2 = password_entry.get()
    if len(title.strip()) == 0:
        messagebox.showerror(message="Please enter the name of the secret note")
    elif len(password2) == 0:
        messagebox.showerror(message="Please enter the password to decrypt the note")
    elif password2 == password1:
        file_name = title + "_note.txt"
        try:
            with open(file_name, 'rb') as filekey:
                    master_pass = password_entry.get()
                    encrypted_note = filekey.read()
                    decrypted_note = cipher_suite.decrypt(encrypted_note)
            with open(file_name, 'wb') as encrypted_file:
                    decrypted_note = cipher_suite.decrypt(encrypted_note)
                    encrypted_file.write(decrypted_note)
                    messagebox.showerror(message="Your note decrypted successfully")
        except FileNotFoundError:
            messagebox.showerror(message=f"Secret note with the name {title} not found")
        except Exception as e:
            messagebox.showerror(message=f"Error: {str(e)}")
    else: messagebox.showerror(message="Wrong password")

decrypt_button = Button(text="Decrypt", command=decrypt_and_display)
decrypt_button.pack()

window.mainloop()
