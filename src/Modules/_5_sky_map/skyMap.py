import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random

class SkyMapApp:
    """
    Class creates a sky map in the window (using a library), with the Sun indicated at the center. Additionally,
    stars are drawn at random positions and brightness. The number of generated stars can be specified by the user.
    """
    def __init__(self, master, num_stars=100):
        self.master = master
        self.num_stars = num_stars
        master.title("Sky Map")

        # size a screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2

        # geometry for window
        master.geometry(f"800x600+{x}+{y}")

        # create a new picture
        self.sky_image = Image.new("RGB", (800, 600), "black")
        self.draw = ImageDraw.Draw(self.sky_image)

        # draw initial stars
        self.draw_stars(self.num_stars)

        # sun
        sun_position = (400, 300)
        self.draw.ellipse((sun_position[0]-5, sun_position[1]-5, sun_position[0]+5, sun_position[1]+5), fill="yellow")
        self.add_sun_values()

        # format of picture for Tkinter
        self.photo = ImageTk.PhotoImage(self.sky_image)
        # sky map with Canvas
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Input for number of stars
        self.star_count_label = tk.Label(master, text="Number of Stars:")
        self.star_count_label.place(x=10, y=560)
        self.star_count_entry = tk.Entry(master)
        self.star_count_entry.place(x=120, y=560)
        self.star_count_button = tk.Button(master, text="Generate Stars", command=self.update_stars)
        self.star_count_button.place(x=250, y=556)

    def draw_stars(self, num_stars):
        # Rysujemy określoną ilość gwiazd o losowych pozycjach i jasnościach
        for _ in range(num_stars):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            brightness = random.randint(100, 255)
            self.draw.ellipse((x-1, y-1, x+1, y+1), fill=(brightness, brightness, brightness))

    def add_sun_values(self):
        # baseline values for the sun
        sun_values = {
            "Temperature": "5778 K",
            "Brightness": "3.846 x 10^26 W",
            "Distance": "1 AU"
        }
        y_offset = 20
        for label, value in sun_values.items():
            x = 20
            y = 20 + y_offset
            self.draw.text((x, y), f"{label}: {value}", fill="white")
            y_offset += 20

    def update_stars(self):
        try:
            num_stars = int(self.star_count_entry.get())
            if num_stars < 0:
                raise ValueError("Number of stars must be a positive integer.")
        except ValueError:
            print("Please enter a valid number.")
            return

        # clear the previous image
        self.sky_image = Image.new("RGB", (800, 600), "black")
        self.draw = ImageDraw.Draw(self.sky_image)

        # redraw stars and sun
        self.draw_stars(num_stars)
        sun_position = (400, 300)
        self.draw.ellipse((sun_position[0]-5, sun_position[1]-5, sun_position[0]+5, sun_position[1]+5), fill="yellow")
        self.add_sun_values()

        # update the canvas with the new image
        self.photo = ImageTk.PhotoImage(self.sky_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)