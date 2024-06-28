from licensing.models import *
from licensing.methods import Key, Helpers

RSAPubKey = "<RSAKeyValue><Modulus>wlwFOn0JhMoJvbDkbmTdG7vvgNbfbWo8ePt0+nSyo41eMsjXVKr7LlzUZWPqothBhB8YBYgP16rkAKwgeYUrhm7T9XjTIIB0nSv7eq29R1EWF2AfeZ0OBWeesAox8hG5/gsx+Uxa7lPAl6CHyTvJMm6EYA0qGtZiWWts6XkcQ1Ar8RfXJKkc+OinNLhsSZaHTewWJCbv/eJTd1HgD7KTOda6lmU2pF++BBICISZ2GNEmzkmU1zfpOfcIFOefgTFBUJIVh3z57jQZxeqy7ndqnzaqB3mkLvwTNom30jcysrnMWBsQkmrVuCotUF9/E6SyVvjmSO6XkWnSV+pIJX/5hQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"# ENTER RSAKEY
auth = "WyI4Njg0OTgyNSIsIkxYVVBxbmYxUFBidUZ1RkI4UG1pWXlBWHVod0dRM3A4MEw2bkhmejEiXQ==" ## AUTHKEY WITH ACTIVATE !
def Authkey():
    key = str(input(" Enter license key = "))
    result = Key.activate(token=auth,\
        rsa_pub_key=RSAPubKey,\
        product_id='26174', \
        key=key,\
        machine_code=Helpers.GetMachineCode())

    if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
    # an error occurred or the key is invalid or it cannot be activated
    # (eg. the limit of activated devices was achieved)
        print("The license does not work: {0}".format(result[1]))
        exit()
    else:
    # everything went fine if we are here!e
        print("The license is valid!")
        pass
Authkey()

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import requests
from PIL import Image, ImageTk
import webbrowser

def relative_to_assets(path: str) -> str:
    # Your implementation of relative_to_assets
    return path

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main window setup
window = Tk()
window.geometry("500x400")
window.configure(bg="#212E3C")

# Load and set the window icon
icon_image = PhotoImage(file=relative_to_assets("logo2.png"))
window.iconphoto(False, icon_image)

canvas = Canvas(
    window,
    bg="#212E3C",
    height=400,
    width=500,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    29.0,
    90.0,
    anchor="nw",
    text="Enter cookie",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    29.0,
    196.0,
    anchor="nw",
    text="Output",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_rectangle(
    0.0,
    0.0,
    500.0,
    63.0,
    fill="#042331",
    outline=""
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    253.0,
    145.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#254463",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=49.0,
    y=126.0,
    width=408.0,
    height=37.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    253.0,
    251.0,
    image=entry_image_2
)

entry_2 = Entry(
    bd=0,
    bg="#254463",
    fg="#FFFFFF",
    highlightthickness=0
)

entry_2.place(
    x=49.0,
    y=232.0,
    width=408.0,
    height=37.0
)

# Function to fetch verification link
def fetch_verification_link():
    cookie = entry_1.get().strip()
    if not cookie:
        messagebox.showwarning("Warning", "Please enter a valid cookie.")
        return

    verification_link = get_verification_link(cookie)
    if verification_link:
        entry_2.delete(0, 'end')
        entry_2.insert(0, verification_link)
    else:
        entry_2.delete(0, 'end')
        entry_2.insert(0, "Failed to fetch verification link.")

def get_verification_link(cookie):
    url = 'https://apis.roblox.com/age-verification-service/v1/persona-id-verification/start-verification'
    csrf_token = get_csrf_token(cookie)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'x-csrf-token': csrf_token,
        'cookie': f".ROBLOSECURITY={cookie}"
    }

    body = {
        "generateLink": True
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json().get('verificationLink')
        else:
            messagebox.showerror("Error", f"Failed to fetch verification link.\nStatus Code: {response.status_code}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        return None

def get_csrf_token(cookie):
    url = "https://auth.roblox.com/v2/logout"
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    try:
        response = requests.post(url, headers=headers)
        return response.headers.get("x-csrf-token")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch CSRF token:\n{str(e)}")
        return None

# Button and hover effects
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    background="#042331",
    activebackground="#042331",
    command=lambda: webbrowser.open("https://discord.com/invite/maliturstudio"),
    relief="flat"
)
button_1.place(
    x=259.0,
    y=14.0,
    width=100.0,
    height=34.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )

def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    background="#212E3C",
    activebackground="#212E3C",
    command=fetch_verification_link,  # Updated command for button 2
    relief="flat"
)
button_2.place(
    x=178.0,
    y=314.0,
    width=145.0,
    height=39.0
)

button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )

def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    background="#042331",
    activebackground="#042331",
    command=lambda: webbrowser.open("https://maliturstudio.x10.mx/"),
    relief="flat"
)
button_3.place(
    x=377.0,
    y=15.0,
    width=100.0,
    height=34.0
)

button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )

def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )

button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

original_image = Image.open(relative_to_assets("logo.png"))

# Scale the image
scaled_image = original_image.resize((200, 50))  # Resize to the desired dimensions

# Convert the PIL image to a format Tkinter can use
logo_image = ImageTk.PhotoImage(scaled_image)

# Display the image on the canvas
canvas.create_image(
    10, 6,
    image=logo_image,
    anchor="nw"
)

window.resizable(False, False)
window.mainloop()

