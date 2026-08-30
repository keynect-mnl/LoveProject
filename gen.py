import tkinter as tk
from tkinter import ttk, messagebox
import json
import base64
import secrets
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data.json"


def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("data.json must contain an object.")

        return data

    except json.JSONDecodeError:
        messagebox.showerror(
            "Error",
            "data.json contains invalid JSON."
        )
        return None


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )
        f.write("\n")


def generate_id(data):
    while True:
        new_id = secrets.token_hex(3).upper()

        if new_id not in data:
            return new_id


def encode_entry(sender, receiver, date, message):

    entry = {
        "sender": sender,
        "receiver": receiver,
        "date": date,
        "message": message
    }

    # Compact JSON
    json_string = json.dumps(
        entry,
        separators=(",", ":"),
        ensure_ascii=False
    )

    # Base64 encode
    encoded = base64.b64encode(
        json_string.encode("utf-8")
    ).decode("ascii")

    return encoded


def generate():

    sender = sender_var.get().strip()
    receiver = receiver_var.get().strip()
    date = date_var.get().strip()
    message = message_box.get("1.0", tk.END).strip()

    if not sender:
        messagebox.showwarning(
            "Missing Sender",
            "Please enter the sender."
        )
        return

    if not receiver:
        messagebox.showwarning(
            "Missing Receiver",
            "Please enter the receiver."
        )
        return

    if not date:
        messagebox.showwarning(
            "Missing Date",
            "Please enter the date."
        )
        return

    if not message:
        messagebox.showwarning(
            "Missing Message",
            "Please enter a message."
        )
        return

    data = load_data()

    if data is None:
        return

    # Generate unique 6-character hexadecimal ID
    love_id = generate_id(data)

    # Encode the entry
    encoded = encode_entry(
        sender,
        receiver,
        date,
        message
    )

    # Append to data.json
    data[love_id] = encoded

    try:
        save_data(data)

    except Exception as e:

        messagebox.showerror(
            "Save Error",
            str(e)
        )

        return

    # Generate URL
    url = (
        "https://keynect-mnl.github.io/"
        "LoveProject/?id="
        + love_id
    )

    # Display results
    id_var.set(love_id)
    encoded_var.set(encoded)
    url_var.set(url)

    status_var.set(
        f"Successfully added {love_id}"
    )

    messagebox.showinfo(
        "Success",
        f"Love letter added!\n\n"
        f"ID: {love_id}\n\n"
        f"Saved to:\n{DATA_FILE}"
    )


def copy_id():

    value = id_var.get()

    if value:
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()

        status_var.set("ID copied.")


def copy_url():

    value = url_var.get()

    if value:
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()

        status_var.set("URL copied.")


def clear_form():

    sender_var.set("")
    receiver_var.set("")
    date_var.set("")

    message_box.delete(
        "1.0",
        tk.END
    )

    id_var.set("")
    encoded_var.set("")
    url_var.set("")

    status_var.set("Ready.")


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title(
    "Love Project Generator"
)

root.geometry(
    "700x620"
)

root.resizable(
    True,
    True
)


# Main container
main = ttk.Frame(
    root,
    padding=25
)

main.pack(
    fill="both",
    expand=True
)


# Title
ttk.Label(
    main,
    text="Love Project Generator",
    font=("Segoe UI", 20, "bold")
).pack(
    anchor="w"
)

ttk.Label(
    main,
    text="Create a Base64-obfuscated love letter entry",
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    pady=(0, 25)
)


# ============================================================
# FORM
# ============================================================

form = ttk.Frame(main)

form.pack(
    fill="x"
)

form.columnconfigure(
    1,
    weight=1
)


sender_var = tk.StringVar()
receiver_var = tk.StringVar()
date_var = tk.StringVar()


# Sender
ttk.Label(
    form,
    text="Sender"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=7
)

ttk.Entry(
    form,
    textvariable=sender_var
).grid(
    row=0,
    column=1,
    sticky="ew",
    padx=(15, 0),
    pady=7
)


# Receiver
ttk.Label(
    form,
    text="Receiver"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=7
)

ttk.Entry(
    form,
    textvariable=receiver_var
).grid(
    row=1,
    column=1,
    sticky="ew",
    padx=(15, 0),
    pady=7
)


# Date
ttk.Label(
    form,
    text="Date"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=7
)

ttk.Entry(
    form,
    textvariable=date_var
).grid(
    row=2,
    column=1,
    sticky="ew",
    padx=(15, 0),
    pady=7
)

ttk.Label(
    form,
    text="YYYY-MM-DD",
    font=("Segoe UI", 8)
).grid(
    row=2,
    column=2,
    padx=8
)


# Message
ttk.Label(
    form,
    text="Message"
).grid(
    row=3,
    column=0,
    sticky="nw",
    pady=7
)

message_box = tk.Text(
    form,
    height=6,
    wrap="word",
    font=("Segoe UI", 10)
)

message_box.grid(
    row=3,
    column=1,
    columnspan=2,
    sticky="ew",
    padx=(15, 0),
    pady=7
)


# ============================================================
# BUTTONS
# ============================================================

buttons = ttk.Frame(
    main
)

buttons.pack(
    fill="x",
    pady=20
)


ttk.Button(
    buttons,
    text="Generate & Append",
    command=generate
).pack(
    side="left"
)


ttk.Button(
    buttons,
    text="Clear",
    command=clear_form
).pack(
    side="left",
    padx=10
)


# ============================================================
# OUTPUT
# ============================================================

ttk.Separator(
    main
).pack(
    fill="x",
    pady=(0, 20)
)


ttk.Label(
    main,
    text="Generated Entry",
    font=("Segoe UI", 13, "bold")
).pack(
    anchor="w",
    pady=(0, 10)
)


output = ttk.Frame(
    main
)

output.pack(
    fill="x"
)

output.columnconfigure(
    1,
    weight=1
)


id_var = tk.StringVar()
encoded_var = tk.StringVar()
url_var = tk.StringVar()


# ID
ttk.Label(
    output,
    text="ID"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=5
)

ttk.Entry(
    output,
    textvariable=id_var,
    state="readonly"
).grid(
    row=0,
    column=1,
    sticky="ew",
    padx=10
)

ttk.Button(
    output,
    text="Copy",
    command=copy_id
).grid(
    row=0,
    column=2
)


# URL
ttk.Label(
    output,
    text="URL"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=5
)

ttk.Entry(
    output,
    textvariable=url_var,
    state="readonly"
).grid(
    row=1,
    column=1,
    sticky="ew",
    padx=10
)

ttk.Button(
    output,
    text="Copy",
    command=copy_url
).grid(
    row=1,
    column=2
)


# Base64
ttk.Label(
    output,
    text="Base64"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=5
)

ttk.Entry(
    output,
    textvariable=encoded_var,
    state="readonly"
).grid(
    row=2,
    column=1,
    sticky="ew",
    padx=10
)


# Status
status_var = tk.StringVar(
    value="Ready."
)

ttk.Label(
    main,
    textvariable=status_var
).pack(
    anchor="w",
    pady=(20, 0)
)


# Start application
root.mainloop()
