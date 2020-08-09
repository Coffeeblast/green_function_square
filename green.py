import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def green(x, y, x0, y0, n):
    """
    Calculates approximation of green function of Laplacian on a square <0, 1> x <0, 1>
    :param x: x coordinate of the point, where calculation is taken
    :param y: y coordinate of the point, where calculation is taken
    :param x0: x coordinate of the point, where delta function is singular
    :param y0: y coordinate of the point, where delta function is singular
    :param n: integer, at which the Fourier series is cut off
    :return: value of the Green function
    """
    result = 0.0
    for i in range(n):
        alpha = (i + 1) * np.pi
        for j in range(n):
            beta = (j + 1) * np.pi
            lam = -(alpha**2 + beta**2)
            result += (4 / lam) * np.sin(alpha * x0) * np.sin(alpha * x) * np.sin(beta * y0) * np.sin(beta * y)
    return result


class App:
    """Simple GUI app to visualize the Green function"""
    def __init__(self):
        self.n = 2
        self.x0 = 0.25
        self.y0 = 0.5
        x = np.linspace(0, 1, 50)
        y = np.linspace(0, 1, 50)
        self.X, self.Y = np.meshgrid(x, y)
        self.fig = Figure()

        self.create_ui()

        self.ax = Axes3D(self.fig)
        self.plot_graph()

    def create_ui(self):
        root = tk.Tk()
        root.wm_title("Green function")

        # create frames
        fr_graph = tk.Frame(root, padx=5, pady=5)
        fr_graph.pack(side=tk.LEFT)
        fr_ui = tk.Frame(root)
        fr_ui.pack(side=tk.RIGHT)
        fr_display = tk.Frame(fr_ui, padx=5, pady=5, highlightbackground="black", highlightthickness=1)
        fr_display.pack(side=tk.TOP)
        fr_buttons = tk.Frame(fr_ui, padx=5, pady=5)
        fr_buttons.pack(side=tk.BOTTOM)

        # create labels
        self.n_text = tk.StringVar()
        self.n_text.set(f"n = {self.n}")
        lbl_n = tk.Label(fr_display, textvariable=self.n_text)
        lbl_n.pack(side=tk.TOP)

        self.pos_text = tk.StringVar()
        self.pos_text.set(f"(x_0,y_0) = ({self.x0}, {self.y0})")
        lbl_loc = tk.Label(fr_display, textvariable=self.pos_text)
        lbl_loc.pack(side=tk.TOP)

        # create canvas and navigation toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=fr_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, fr_graph)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # buttons for add / subtract N
        button_add = tk.Button(master=fr_buttons, text="n --> n + 1", command=self.add_n)
        button_sub = tk.Button(master=fr_buttons, text="n --> n - 1", command=self.sub_n)
        button_add.pack(side=tk.TOP, expand=1)
        button_sub.pack(side=tk.TOP, expand=1)

        # widgets for changing coordinates of the charge
        fr_coords_x = tk.Frame(master=fr_buttons)
        fr_coords_x.pack(side=tk.TOP)

        lbl_x0 = tk.Label(master=fr_coords_x, text="x0: ")
        self.entry_x0 = tk.Entry(master=fr_coords_x)
        lbl_x0.pack(side=tk.LEFT)
        self.entry_x0.pack(side=tk.RIGHT)

        fr_coords_y = tk.Frame(master=fr_buttons)
        fr_coords_y.pack(side=tk.TOP)

        lbl_y0 = tk.Label(master=fr_coords_y, text="y0: ")
        self.entry_y0 = tk.Entry(master=fr_coords_y)
        lbl_y0.pack(side=tk.LEFT)
        self.entry_y0.pack(side=tk.RIGHT)

        btn_set = tk.Button(master=fr_buttons, text="Set (x0,y0)", command=self.set_pos)
        btn_set.pack(side=tk.BOTTOM, expand=1)

    def plot_graph(self):
        self.ax.cla()
        green_fun = green(self.X, self.Y, self.x0, self.y0, self.n)
        self.ax.plot_surface(self.X, self.Y, green_fun)
        self.ax.plot(np.array([self.x0]), np.array([self.y0]), np.array([0.0]), marker='o', markersize=8, color="red")
        self.ax.plot(np.array([self.x0, self.x0]), np.array([0, 1]), np.array([0, 0]), color="red", linewidth=1,
                     marker="")
        self.ax.plot(np.array([0, 1]), np.array([self.y0, self.y0]), np.array([0, 0]), color="red", linewidth=1,
                     marker="")
        zmin, zmax = self.ax.get_zlim()
        self.ax.plot(np.array([self.x0, self.x0]), np.array([self.y0, self.y0]), np.array([zmin, zmax]), color="red",
                     linewidth=1, marker="")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_title(f"n = {self.n}")
        self.canvas.draw()

        self.n_text.set(f"n = {self.n}")
        self.pos_text.set(f"(x0,y0) = ({self.x0}, {self.y0})")

    def add_n(self):
        if self.n <= 200:
            self.n += 1
            self.plot_graph()

    def sub_n(self):
        if self.n >= 2:
            self.n -= 1
            self.plot_graph()

    def set_pos(self):
        try:
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            self.x0, self.y0 = float(x0), float(y0)
            self.pos_text.set(f"(x0,y0) = ({self.x0}, {self.y0})")
            self.plot_graph()
        except ValueError:
            messagebox.showinfo("Error", "Enter x0, and y0, that are numbers!")


def main():
    myApp = App()
    tk.mainloop()

if __name__ == '__main__':
    main()
