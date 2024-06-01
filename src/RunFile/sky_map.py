# Libraries
from src.Modules._5_sky_map.skyMap import SkyMapApp as SkyMap
import tkinter as tk

# The code that runs the sentence
root = tk.Tk()
app = SkyMap(root, num_stars=500)  # number of stars (num_stars)
root.mainloop()