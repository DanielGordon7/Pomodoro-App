from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
mark = ""
timer = None
text_list = ["Work", "Timer", "Short Break", "Long Break"]


def write_goal(event):
    if title_label.cget("text") != "Short Break" and title_label.cget("text") != "Long Break":
        title_label.config(text=goal_entry.get().title(), font=(FONT_NAME, 20, "bold"))
        goal_entry.delete(0, END)


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN, font=(FONT_NAME, 40, "bold"))
    check_marks.config(text="")
    global reps, mark
    mark = ""
    reps = 0


def start_timer():
    global reps
    reps += 1
    work = WORK_MIN * 60
    short_rest = SHORT_BREAK_MIN * 60
    long_rest = LONG_BREAK_MIN * 60
    if reps == 8:
        title_label.config(text="Long Break", fg=RED, font=(FONT_NAME, 30, "bold"))
        count_down(long_rest)
    elif reps % 2 == 0:
        title_label.config(text="Short Break", fg=PINK, font=(FONT_NAME, 30, "bold"))
        count_down(short_rest)
    else:
        if title_label.cget("text") in text_list:
            title_label.config(text="Work", fg=GREEN, font=(FONT_NAME, 40, "bold"))
        count_down(work)


def count_down(count):
    min = math.floor(count / 60)
    sec = int(count % 60)
    if sec < 10:
        sec = "0"+str(sec)
    canvas.itemconfig(timer_text, text=f"{min}:{sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:  # this runs when the count reached zero
        global mark
        if reps == 8:
            reset_timer()
        else:
            if reps % 2 != 0:
                mark += "✔"
                check_marks.config(text=mark, fg=GREEN)
                goal_entry.delete(0, END)
            start_timer()


# GUI code below:

window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50, bg=YELLOW)

# tomato
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1, row=1)

# buttons
start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

# label
goal_label = Label(text="Work Session's Goal:")
goal_label.grid(column=1, row=4)

title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
title_label.grid(column=0, row=0, columnspan=3)

# checkmark (label)
check_marks = Label(fg=GREEN, bg=YELLOW, font=(20))
check_marks.grid(column=1, row=3)

# Entry
goal_entry = Entry()
goal_entry.focus()
goal_entry.grid(column=1, row=5)
goal_entry.bind('<Return>', write_goal)


window.mainloop()