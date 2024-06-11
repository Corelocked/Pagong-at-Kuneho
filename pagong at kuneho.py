import tkinter as tk
import random
from PIL import Image, ImageTk
import os

# Get the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Initialize main window
root = tk.Tk()
root.title("Ang Pagong at Ang Kuneho")
root.resizable(False, False)
canvas_width = 640
canvas_height = 360
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Initialize turtle and bunny positions and speed
turtle_x, turtle_y = 20, 150
bunny_x, bunny_y = 20, 250
turtle_speed = 1

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

# Load winner images
turtle_won_image_path = os.path.join(current_directory, "turtlewon.png")
turtle_won_img = Image.open(turtle_won_image_path)
turtle_won_img_resized = turtle_won_img.resize((400, 200))  # Adjust size as needed
turtle_won_image = ImageTk.PhotoImage(turtle_won_img_resized)

bunny_won_image_path = os.path.join(current_directory, "bunnywon.png")
bunny_won_img = Image.open(bunny_won_image_path)
bunny_won_img_resized = bunny_won_img.resize((400, 200))  # Adjust size as needed
bunny_won_image = ImageTk.PhotoImage(bunny_won_img_resized)

# Load restart button image
restart_image_path = os.path.join(current_directory, "restart.png")
restart_img = Image.open(restart_image_path)
restart_img_resized = restart_img.resize((100, 40))  # Adjust size as needed
restart_image = ImageTk.PhotoImage(restart_img_resized)

# Finish line
finish_line_width = 20
finish_line_interval = 20
finish_line_thickness = 20

start_y = 6 * finish_line_interval
end_y = canvas_height - (3 * finish_line_interval)

for i in range(start_y, end_y, finish_line_interval):
    color = 'white' if (i // finish_line_interval) % 2 == 0 else 'black'
    canvas.create_line(500, i, 500, i + finish_line_width, fill=color, width=finish_line_thickness)

# Create winner image container
winner_image_id = canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER)

canvas.tag_raise(turtle)
canvas.tag_raise(bunny)
canvas.tag_raise(winner_image_id)

# Move turtle
def move_turtle():
    global turtle_x
    canvas.move(turtle, turtle_speed, 0)
    turtle_x += turtle_speed
    if turtle_x >= 500:
        display_winner('turtle')
        end_game()
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
    canvas.itemconfig(winner_image_id, image='')  # Hide winner image
    move_turtle()
    restart_button.place_forget()

# Create restart button
restart_button = tk.Button(root, image=restart_image, command=restart_game, borderwidth=0, highlightthickness=0, bd=0)
restart_button.place_forget()

# Game state
game_over = False

# Move bunny
def move_bunny(event=None):
    global bunny_x, bunny_y
    if not game_over and event:
        direction = random.choice(["a", "d", "d"])
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
    if bunny_x >= 500:
        display_winner('bunny')
        end_game()
    elif turtle_x >= 500:
        display_winner('turtle')
        end_game()
    else:
        root.after(50, move_bunny)

# Display winner image
def display_winner(winner):
    if winner == 'turtle':
        canvas.itemconfig(winner_image_id, image=turtle_won_image)
    elif winner == 'bunny':
        canvas.itemconfig(winner_image_id, image=bunny_won_image)

# End game
def end_game():
    global game_over
    game_over = True
    restart_button.place(x=canvas_width // 2 - restart_button.winfo_reqwidth() // 2, y=canvas_height // 2 + 130)  # Show the restart button centered under the winner image

# Start the race
move_turtle()

canvas.bind('<Button-1>', move_bunny)

root.mainloop()
