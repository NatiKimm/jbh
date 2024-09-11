import tkinter as tk
from PIL import Image, ImageTk
import random
import math
from matplotlib import pyplot
from time import time
import os
from symmetrical_atractor import search_attractors_with_symmetry
from layers import search_attractors_layered
from colour_gradient import search_attractors_with_color_gradient

# Create the main window
root = tk.Tk()
root.geometry("850x700")
root.configure(bg='black')
root.title("Chaos Theory")

selected_colour = 'white'  # Default color
selected_size = 0.5  # Default size
image_label = None  # Global variable to hold the image label widget

# Ensure directories exist
if not os.path.exists("pictures"):
    os.makedirs("pictures")


# Reference: https://www.youtube.com/watch?v=AzdpM-vfUCQ , https://www.youtube.com/watch?v=sGdFR9cpE6A
# Function to generate attractor images and save them
def search_attractors(n, colour, size):
    found = 0
    while found < n:

        # random starting point
        x = random.uniform(-0.5, 0.5)
        y = random.uniform(-0.5, 0.5)

        # random alernative point nearby
        xe = x + random.uniform(-0.5, 0.5) / 1000
        ye = y + random.uniform(-0.5, 0.5) / 1000

        # distance between the two points
        dx = xe - x
        dy = ye - y
        d0 = math.sqrt(dx * dx + dy * dy)

        # random parameter vector
        a = [random.uniform(-2, 2) for _ in range(12)]

        # lists to store the entire path
        x_list = [x]
        y_list = [y]

        # initialize convergence boolean and lyapunov exponent
        converge = False
        lyapunov = 0

        # iteratively pass (x,y) into the quadratic map
        for i in range(10000):

            # compute next point (using the quadratic map)
            xnew = a[0] + a[1] * x + a[2] * x * x + a[3] * y + a[4] * y * y + a[5] * x * y
            ynew = a[6] + a[7] * x + a[8] * x * x + a[9] * y + a[10] * y * y + a[11] * x * y

            # check if we converge to infinity
            if xnew > 1e10 or ynew > 1e10 or xnew < -1e10 or ynew < -1e10:
                converge = True
                break

            # check if we converge to a single point
            if abs(x - xnew) < 1e-10 and abs(y - ynew) < 1e-10:
                converge = True
                break

            # check for chaotic behavior
            if i > 1000:

                # compute next alternative point
                xenew = a[0] + a[1] * xe + a[2] * xe * xe + a[3] * ye + a[4] * ye * ye + a[5] * xe * ye
                yenew = a[6] + a[7] * xe + a[8] * xe * xe + a[9] * ye + a[10] * ye * ye + a[11] * xe * ye

                # compute the distance between the new points
                dx = xenew - xnew
                dy = yenew - ynew
                d = math.sqrt(dx * dx + dy * dy)

                # lyapunov exponent
                lyapunov += math.log(abs(d / d0))

                # rescale the alternative point
                xe = xnew + d0 * dx / d
                ye = ynew + d0 * dy / d

            # update (x,y)
            x = xnew
            y = ynew

            # store (x,y) in our path lists
            x_list.append(x)
            y_list.append(y)

        # if chaotic behaviour has been found
        if not converge and lyapunov >= 10:

            # update counter and have a little print message
            found += 1
            print(f"Found another strange attractor with Lyapunov exponent = {lyapunov}!")

            # Name of the image
            name = f"pictures/attractor_{time()}.png"

            # Plot design
            pyplot.style.use("dark_background")
            pyplot.axis("off")

            #create the plot
            pyplot.scatter(x_list[100:], y_list[100:], s=float(size), c=colour, linewidth=0)

            # Save the figure
            pyplot.savefig(name, dpi=500)
            pyplot.close()

            # Display the image
            display_image_in_window(name)


# Reference: https://github.com/shaq31415926/python_tech_basics/blob/main/tech_basics_two/06Lecture/streamA_age_gui.py
# Display the background image on the first page
def first_page_foto():
    img = Image.open("pictures/background.png")
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    pic = ImageTk.PhotoImage(img)
    Lab = tk.Label(root, image=pic)
    Lab.place(x=10, y=80)
    Lab.image = pic

# Function to display an image in the Tkinter window
def display_image_in_window(image_path):
    global image_label

    # Load the image
    img = Image.open(image_path)
    img = img.resize((600, 600), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    if image_label is None:

        # Create a new label if it doesn't exist
        image_label = tk.Label(root, image=img_tk, bg='black')
        image_label.place(x=130, y=150)
    else:
        # Update the image in the existing label
        image_label.config(image=img_tk)

    image_label.image = img_tk  # This line is necessary to prevent garbage collection


# Function to show the first page of the application
def first_page():

    #loading the background photo to the first page
    first_page_foto()
    title_text = tk.Label(root, text="Chaos Theory", bg='black', fg='white', font="georgia 25 bold")
    title_text.place(x=350, y=15)

    description_text = tk.Label(root,
                                text= "Chaos Theory:\n\n"
                                      "Chaos theory studies how certain systems can behave unpredictably."
                                      "It deals with how small changes in the initial conditions of a system can lead to drastically different outcomes."
                                      " A famous example is Lorenz's 'butterfly effect', which suggests that something as small as a butterfly flapping its wings could eventually " 
                                     "cause a storm elsewhere. In chaos theory, even tiny changes in a system's starting state can have a significant impact on the outcome,"
                                    " making long-term predictions difficult \n\n"
      
"About this Application:\n\n"
"This application lets you explore the fascinating world of chaos theory by generating various types of chaotic attractor images."
" You can experiment with simple attractors, symmetrical designs, and layered or gradient art. Adjust different parameters, "
"such as color and size, to see how these changes affect the visual representation of chaos.",
bg='black', fg='white', font="georgia 15 bold", wraplength=400)
    description_text.place(x=420, y=100)

    go_to_second = tk.Button(text='EXPLORE', font='georgia 20', fg='black', bg='black', command=second_page)
    go_to_second.place(rely=0.79, relx=0.91, relwidth=0.15, relheight=0.1, anchor='n')

# Function to generate a simple image
def generate_image():
    if selected_size == "various":
        size = random.uniform(0.1, 3)  #if "various" is chosed, its chooses a random number
    else:
        size = selected_size
    search_attractors(1, selected_colour, size)

# Function to generate layered art
def generate_layered_art():
    # calling the search_attractors_layered() from layers.py where the name of a picture is being saved
    name_layered = search_attractors_layered()
    # Showing the image in the tk window
    display_image_in_window(name_layered)

# Function to generate symmetrical art
def generate_symmetrical_art():
    #calling the search function from symmetrical_attractor.py where the name of a picture is being saved
    name_symmetrical = search_attractors_with_symmetry()
    # Showing the image in the tk windows
    display_image_in_window(name_symmetrical)

def gradient_art():
    # calling the earch_attractors_with_color_gradient() from colour_gradient.py. where the name of a picture is being saved
    name_gradient = search_attractors_with_color_gradient()
    display_image_in_window(name_gradient)


# Function to switch to the second page of the application
def second_page():
    clear_widgets(root)

   #labels for choosing colours and sizes
    colour_label = tk.Label(root, text="Colour", bd=3, relief='flat', fg='white', bg='black', font="georgia 15 bold")
    colour_label.place(x=250, y=20)

    size_label = tk.Label(root, text="Size", bd=3, relief='flat', fg='white', bg='black', font="georgia 15 bold")
    size_label.place(x=250, y=60)

    # A little explanation label that the colour and size setting are only for the Simple Art generation
    explain_label = tk.Label(root, text="*Colour and Size settings apply only to Simple Art",
                             bd=3, relief='flat', fg='white', bg='black', wraplength=400,
                             font="georgia 10 bold")
    explain_label.place(x=550, y=25)

    #calling the dropdown menus for colour and size
    option_colour()
    option_size()

    # Simple attractor button
    generate_button = tk.Button(root, text="Simple", font='georgia 15 bold', fg='black', bg='black', command=generate_image)
    generate_button.place(x=450, y=100)

    # Symmetrical art button
    symmetrical_button = tk.Button(root, text="Symmetrical", font='georgia 15 bold', fg='black', bg='black', command=generate_symmetrical_art)
    symmetrical_button.place(x=270, y=100)

    # Layered art button
    layered_button = tk.Button(root, text="Layered", font='georgia 15 bold', fg='black', bg='black', command=generate_layered_art)
    layered_button.place(x=130, y=100)

    # colour gradient art button
    gradient_button = tk.Button(root, text="Gradient", font='georgia 15 bold', fg='black', bg='black',
                               command=gradient_art)
    gradient_button.place(x=600, y=100)

# Function to clear widgets from the root window
def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()

# Reference: https://github.com/NatiKimm/Natalia-Kim-tbii-exam/blob/main/App_Exam_II/app.py
# Colour selection dropdown menu
def option_colour():
    global selected_colour
    colours = ["white", "blue", "green", "red", "yellow", "pink"]
    var_colour = tk.StringVar(root)
    var_colour.set(colours[0])
    dropdown = tk.OptionMenu(root, var_colour, *colours, command=lambda v: set_colour(v))
    dropdown.place(x=350, y=10)
    dropdown.config(width=15, height=3, bg='black', fg="white", font=('georgia', 15,), bd=0, relief="flat")


def set_colour(value):
    global selected_colour
    selected_colour = value
    print("Selected colour:", selected_colour)


# Size selection dropdown menu
def option_size():
    global selected_size
    sizes = ["0.5", "1.0", "2.0", "various"]
    var_size = tk.StringVar(root)
    var_size.set(sizes[0])
    dropdown = tk.OptionMenu(root, var_size, *sizes, command=lambda v: set_size(v))
    dropdown.place(x=350, y=50)
    dropdown.config(width=10, height=3, bg='black', fg="white", font=('georgia', 15,), bd=0, relief="flat")


def set_size(value):
    global selected_size
    selected_size = value
    print("Selected size:", selected_size)

# Launch the first page
first_page()

# Start the Tkinter main loop
root.mainloop()
