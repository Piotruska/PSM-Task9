import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, Scale, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GameOfLife:
    def __init__(self, master, size=100, interval=100):
        self.master = master
        self.size = size
        self.interval = interval
        self.grid = np.zeros((size, size), dtype=int)
        self.running = False
        self.job = None
        self.structure = None
        self.rotation = 0
        self.birth_rules = [3]  # Default birth rule: B3
        self.survival_rules = [2, 3]  # Default survival rules: S23

        self.master.title("Game of Life - Advanced Structure Placement and Custom Rules")
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.ax.axis('on')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(2)
            spine.set_color('black')

        self.im = self.ax.imshow(self.grid, cmap='gray_r', vmin=0, vmax=1, interpolation='nearest')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

        menu = Menu(master)
        master.config(menu=menu)
        structure_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Structures", menu=structure_menu)
        structure_menu.add_command(label="Gosper Glider Gun", command=lambda: self.set_structure('Gosper Glider Gun'))
        structure_menu.add_command(label="Spaceship", command=lambda: self.set_structure('Spaceship'))
        structure_menu.add_command(label="Pulsar", command=lambda: self.set_structure('Pulsar'))
        structure_menu.add_command(label="Point", command=lambda: self.set_structure('Point'))
        options_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Set Rules", command=self.set_rules_dialog)

        control_panel = tk.Frame(master)
        control_panel.pack(side=tk.TOP, fill=tk.X)
        tk.Button(control_panel, text="Start", command=self.start_simulation).pack(side=tk.LEFT)
        tk.Button(control_panel, text="Stop", command=self.stop_simulation).pack(side=tk.LEFT)
        tk.Button(control_panel, text="Clear", command=self.clear_grid).pack(side=tk.LEFT)
        self.mode_label = Label(control_panel, text="Mode: Place Points")
        self.mode_label.pack(side=tk.LEFT)
        self.rotation_scale = Scale(control_panel, from_=0, to=360, resolution=90, orient='horizontal', label="Rotation", command=self.update_rotation)
        self.rotation_scale.pack(side=tk.LEFT)

        self.place_mode = "points"  # Start with placing points
        self.structures = {
            'Gosper Glider Gun': self.get_gosper_glider_gun(),
            'Spaceship': self.get_spaceship(),
            'Pulsar': self.get_pulsar(),
            'Point': np.array([[1]])
        }

    def set_structure(self, name):
        self.structure = self.structures.get(name, np.array([[1]]))
        self.place_mode = "gun" if name != "Point" else "points"
        self.mode_label.config(text=f"Mode: Place {name}")

    def set_rules_dialog(self):
        rule_string = simpledialog.askstring("Set Rules", "Enter rules in Bxxx/Sxxx format (e.g., 'B3/S23'):")
        if rule_string:
            try:
                self.parse_rules(rule_string)
                messagebox.showinfo("Rules Updated", f"New rules set successfully:\nBirth: {self.birth_rules}\nSurvival: {self.survival_rules}")
            except ValueError:
                messagebox.showerror("Error", "Invalid rule format! Please use Bxxx/Sxxx format.")

    def parse_rules(self, rule_string):
        birth_part, survival_part = rule_string.upper().split('/')
        self.birth_rules = [int(n) for n in birth_part.strip()[1:]]
        self.survival_rules = [int(n) for n in survival_part.strip()[1:]]

    def update_rotation(self, value):
        self.rotation = int(value)

    def on_canvas_click(self, event):
        if event.inaxes is not self.ax:
            return
        x, y = int(event.ydata), int(event.xdata)
        if self.place_mode == "gun" and self.structure is not None:
            self.place_structure(x, y)
        elif self.place_mode == "points":
            if 0 <= x < self.size and 0 <= y < self.size:
                self.grid[x, y] = 1 - self.grid[x, y]
        self.update_plot()

    def place_structure(self, x, y):
        structure = np.rot90(self.structure, self.rotation // 90)
        rows, cols = structure.shape
        if x + rows <= self.size and y + cols <= self.size:
            self.grid[x:x + rows, y:y + cols] = structure

    def get_gosper_glider_gun(self):
        return np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
             0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0]
        ])

    def get_spaceship(self):
        # Define the spaceship pattern...
        return np.array([
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
        ])

    def get_pulsar(self):
        # Define the pulsar pattern...
        return np.array([
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0]
        ])

    def clear_grid(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.update_plot()

    def update_plot(self):
        self.im.set_data(self.grid)
        self.canvas.draw()

    def run_step(self):
        if not self.running:
            return
        new_grid = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                total = sum(self.grid[(i + a) % self.size, (j + b) % self.size] for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b)
                if self.grid[i, j] == 1 and total in self.survival_rules:
                    new_grid[i, j] = 1
                elif self.grid[i, j] == 0 and total in self.birth_rules:
                    new_grid[i, j] = 1
        self.grid[:] = new_grid
        self.update_plot()
        self.job = self.master.after(self.interval, self.run_step)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_step()

    def stop_simulation(self):
        self.running = False
        if self.job:
            self.master.after_cancel(self.job)
            self.job = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLife(root)
    root.mainloop()
