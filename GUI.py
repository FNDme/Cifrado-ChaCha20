from pydoc import plain
from tkinter import Tk, Button, Label, Text, Entry, Canvas,  END, DISABLED, NORMAL
from ChaCha20 import *

# Main window
base = Tk()
base.title('RC4')
base.resizable(False, False)
base.geometry('500x400')
base.configure(background='#232426')
# Canvas
Canva = Canvas(base, width=500, height=65, bg='#2a2b2d', highlightthickness=0)
Canva.place(x=0, y=335)

# GUI version of encrypt and decrypt
def gui_ChaCha20():
    # Get text from entry
    # key
    key_ = key.get()
    key_ = key_.replace(':', '')
    key_ = key_.replace(' ', '')
    key_ = [key_[i:i+8] for i in range(0, len(key_), 8)]
    for i in range(len(key_)):
        aux = []
        for j in range(8, 0, -2):
            aux.append(key_[i][j - 2:j])
        key_[i] = int("".join(aux), 16)
    # counter
    counter_ = counter.get()
    counter_ = counter_.replace(':', '')
    counter_ = counter_.replace(' ', '')
    aux = []
    for i in range(8, 0, -2):
        aux.append(counter_[i - 2:i])
    counter_ = int("".join(aux), 16)
    # nonce
    nonce_ = nonce.get()
    nonce_ = nonce_.replace(':', '')
    nonce_ = nonce_.replace(' ', '')
    nonce_ = [nonce_[i:i+8] for i in range(0, len(nonce_), 8)]
    for i in range(len(nonce_)):
        aux = []
        for j in range(8, 0, -2):
            aux.append(nonce_[i][j - 2:j])
        nonce_[i] = int("".join(aux), 16)
    # plaintext
    plaintext_ = plainText.get("1.0", END).strip()
    plaintext_ = txt_to_bytes(plaintext_)
    # ciphertext
    ciphertext_ = chacha20_encrypt(key_, counter_, nonce_, plaintext_)
    print(ciphertext_)
    ciphertext_ = bytes_to_txt(ciphertext_)
    plainText.delete("1.0", END)
    plainText.insert(END, ciphertext_)
    cipherText.config(state=NORMAL)
    cipherText.delete("1.0", END)
    cipherText.insert(END, ciphertext_)
    cipherText.config(state=DISABLED)
    return

# Clear all blocks
def clear():
    key.delete(0, END)
    key.insert(0, '00:01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10:11:12:13:14:15:16:17:18:19:1a:1b:1c:1d:1e:1f')
    counter.delete(0, END)
    counter.insert(0, '01:00:00:00')
    nonce.delete(0, END)
    nonce.insert(0, '00:00:00:09:00:00:00:4a:00:00:00:00')
    plainText.delete("1.0", END)
    cipherText.config(state=NORMAL)
    cipherText.delete("1.0", END)
    cipherText.config(state=DISABLED)
    return

# Input
    # Entry 80x2
keyLabel = Label(base, text="Key:", bg='#232426', fg='#ffffff')
keyLabel.place(x=10, y=10)
key = Entry(base, width=80, bg='#2a2b2d', fg='#ffffff', highlightthickness=0)
key.place(x=10, y=40)
key.insert(0, '00:01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10:11:12:13:14:15:16:17:18:19:1a:1b:1c:1d:1e:1f')
    # Count
counterLabel = Label(base, text="Counter:", bg='#232426', fg='#ffffff')
counterLabel.place(x=10, y=70)
counter = Entry(base, width=10, bg='#2a2b2d', fg='#ffffff', highlightthickness=0)
counter.place(x=10, y=100)
counter.insert(0, '01:00:00:00')
    # Nonce
nonceLabel = Label(base, text="Nonce:", bg='#232426', fg='#ffffff')
nonceLabel.place(x=100, y=70)
nonce = Entry(base, width=30, bg='#2a2b2d', fg='#ffffff', highlightthickness=0)
nonce.place(x=100, y=100)
nonce.insert(0, '00:00:00:09:00:00:00:4a:00:00:00:00')
    # Plaintext
plainLabel = Label(base, text="Plaintext:", bg='#232426', fg='#ffffff')
plainLabel.place(x=10, y=150)
plainText = Text(base, width=28, height=6, bg='#2a2b2d', fg='#ffffff', highlightthickness=0)
plainText.place(x=10, y=180)
    # Ciphertext
cipherLabel = Label(base, text="Ciphertext:", bg='#232426', fg='#ffffff')
cipherLabel.place(x=260, y=150)
cipherText = Text(base, width=28, height=6, bg='#2a2b2d', fg='#ffffff', highlightthickness=0, state=DISABLED)
cipherText.place(x=260, y=180)

# Buttons
    # Encrypt/Decrypt by text
cipher = Button(base, text='Cipher text', command=lambda: gui_ChaCha20())
cipher.place(x=30, y=355)
cipher.configure(background='#04BF68', foreground='#155939', borderwidth=0, activebackground='#232426', pady=5, padx=10)
    # Clear
Clear = Button(base, text='Clear', command=lambda: clear())
Clear.place(x=410, y=355)
Clear.configure(background='#04BF68', foreground='#155939', borderwidth=0, activebackground='#232426', pady=5, padx=10)


base.mainloop()