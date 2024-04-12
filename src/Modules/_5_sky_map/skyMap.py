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
        master.title("Sky Map")

        # size a screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2

        # geoemtry for window
        master.geometry(f"800x600+{x}+{y}")

        # create a new picture
        self.sky_image = Image.new("RGB", (800, 600), "black")
        self.draw = ImageDraw.Draw(self.sky_image)

        # stars
        self.draw_stars(num_stars)

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