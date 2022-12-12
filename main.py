from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

LANGUAGE_FONT = ["Arial", 40, "italic"]
FOREIGN_FONT = ["Arial", 60, "bold"]
FOREIGN_LANGUAGE = "French"
NATIVE_LANGUAGE = "English"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}

# ----------------- right ------------------
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    current_word = current_card[FOREIGN_LANGUAGE]
    card.itemconfig(card_title, text=FOREIGN_LANGUAGE, fill="black")
    card.itemconfig(card_word, text=current_word, fill="black")
    card.itemconfig(card_image, image=front_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    card.itemconfig(card_image, image=back_image)
    card.itemconfig(card_title, text=NATIVE_LANGUAGE, fill="white")
    card.itemconfig(card_word, text=current_card[NATIVE_LANGUAGE], fill="white")

def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)


# -----------------------UI----------------------------

window = Tk()
window.title(" flashy card app for language learning ")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

card = Canvas(height=526, width=800)
card_image = card.create_image(400, 263, image=front_image)
card.config(highlightthickness=0, bg=BACKGROUND_COLOR)
card_title = card.create_text(400, 150, font=LANGUAGE_FONT, fill="black")
card_word = card.create_text(400, 263, font=FOREIGN_FONT, fill="black")
card.grid(row=0, column=0, columnspan=2)

# Button
wrong_x = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_x, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=0)

right_check = PhotoImage(file="images/right.png")
right_button = Button(image=right_check, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
