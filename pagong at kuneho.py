import tkinter as tk
import random
from PIL import Image, ImageTk
import os

# Get the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Initialize main window
root = tk.Tk()
root.title("Ang Pagong at Ang Kuneho")
root.resizable(False, False)  # Prevent resizing in both directions
canvas_width = 640
canvas_height = 360
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Initialize turtle and bunny positions and speeds
turtle_x, turtle_y = 20, 150
bunny_x, bunny_y = 20, 250
turtle_speed = 10

# Load background
background_image_path = os.path.join(current_directory, "background.png")
background_img = Image.open(background_image_path)
background_img_resized = background_img.resize((canvas_width, canvas_height))
background_image = ImageTk.PhotoImage(background_img_resized)
canvas.create_image(0, 0, image=background_image, anchor=tk.NW)

# Load turtle image
turtle_image_path = os.path.join(current_directory, "Turtle.png")
turtle_img = Image.open(turtle_image_path)
turtle_img_resized = turtle_img.resize((int(turtle_img.width * 3), int(turtle_img.height * 3)))
turtle_image = ImageTk.PhotoImage(turtle_img_resized)
turtle = canvas.create_image(turtle_x, turtle_y, image=turtle_image)

# Load bunny image
bunny_image_path = os.path.join(current_directory, "Bunny.png")
bunny_img = Image.open(bunny_image_path)
bunny_img_resized = bunny_img.resize((int(bunny_img.width * 2.5), int(bunny_img.height * 2.5)))
bunny_image = ImageTk.PhotoImage(bunny_img_resized)
bunny = canvas.create_image(bunny_x, bunny_y, image=bunny_image)

# finish line
finish_line_width = 20  
finish_line_interval = 20
finish_line_thickness = 20 

start_y = 6 * finish_line_interval
end_y = canvas_height - (3 * finish_line_interval)

for i in range(start_y, end_y, finish_line_interval):
    color = 'white' if (i // finish_line_interval) % 2 == 0 else 'black'
    canvas.create_line(500, i, 500, i + finish_line_width, fill=color, width=finish_line_thickness)


winner_text = canvas.create_text(canvas_width // 2, canvas_height // 2, text='', font=('Arial', 40), anchor=tk.CENTER)


canvas.tag_raise(turtle)
canvas.tag_raise(bunny)


# Move turtle
def move_turtle():
    global turtle_x
    canvas.move(turtle, turtle_speed, 0)
    turtle_x += turtle_speed
    if turtle_x >= 500:
        canvas.itemconfig(winner_text, text='Turtle won!')
    else:
        root.after(50, move_turtle)

# Restart game
def restart_game():
    global turtle_x, turtle_y, bunny_x, bunny_y, game_over
    turtle_x, turtle_y = 20, 150
    bunny_x, bunny_y = 20, 250
    game_over = False
    canvas.coords(turtle, turtle_x, turtle_y)
    canvas.coords(bunny, bunny_x, bunny_y)
    canvas.itemconfig(winner_text, text='')
    restart_button.pack_forget() 

# Create restart button (initially hidden)
restart_button = tk.Button(root, text="Restart Game", command=restart_game)
restart_button.pack_forget()


# Game state
game_over = False

# Move bunny
def move_bunny(event=None):
    global bunny_x, bunny_y
    if not game_over and event:
        direction = random.choice(["w", "a", "s", "d", "d"])
        if direction == "w" and bunny_y > 0:
            bunny_y -= 10
        elif direction == "a" and bunny_x > 0:
            bunny_x -= 10
        elif direction == "s" and bunny_y < canvas_height - bunny_img_resized.height:
            bunny_y += 10
        elif direction == "d" and bunny_x < canvas_width - bunny_img_resized.width:
            bunny_x += 10
        canvas.coords(bunny, bunny_x, bunny_y)
        check_win()

# Check win
def check_win():
    global game_over
    if bunny_x >= 500:
        canvas.itemconfig(winner_text, text='Bunny won!')
        game_over = True
        restart_button.place(x=canvas_width//2.25 - restart_button.winfo_width()//2, y=canvas_height//2 + 130)  # Show the restart button centered under the winner text
    elif turtle_x >= 500:
        canvas.itemconfig(winner_text, text='Turtle won!')
        game_over = True
        restart_button.place(x=canvas_width//2.25 - restart_button.winfo_width()//2, y=canvas_height//2 + 130)  # Show the restart button centered under the winner text
    else:
        root.after(50, move_bunny)

   


# Start the race
move_turtle()

canvas.bind('<Button-1>', move_bunny)

root.mainloop()
