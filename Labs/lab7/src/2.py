import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def minkowski_curve(start, end, depth, points):
    x1, y1 = start

    x2, y2 = end

    if depth == 0:
        points.append((x1, y1))

        return

    dx = (x2 - x1) / 4

    dy = (y2 - y1) / 4

    points_list = [
        (x1, y1),
        (x1 + dx, y1 + dy),
        (x1 + dx - dy, y1 + dy + dx),
        (x1 + 2 * dx - dy, y1 + 2 * dy + dx),
        (x1 + 2 * dx, y1 + 2 * dy),
        (x1 + 3 * dx, y1 + 3 * dy),
        (x1 + 3 * dx + dy, y1 + 3 * dy - dx),
        (x1 + 4 * dx + dy, y1 + 4 * dy - dx),
        (x2, y2),
    ]

    for index in range(len(points_list) - 1):
        minkowski_curve(
            points_list[index],
            points_list[index + 1],
            depth - 1,
            points,
        )


def minkowski_island(depth):
    points = []

    minkowski_curve(
        (0, 0),
        (1, 0),
        depth,
        points,
    )

    minkowski_curve(
        (1, 0),
        (1, 1),
        depth,
        points,
    )

    minkowski_curve(
        (1, 1),
        (0, 1),
        depth,
        points,
    )

    minkowski_curve(
        (0, 1),
        (0, 0),
        depth,
        points,
    )

    points.append((0, 0))

    return points


class App:
    def __init__(self, window):
        self.root = window

        self.root.title("Minkowski Island")

        self.depth = 1

        self.build_ui()

        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.plot_frame,
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

        self.draw_fractal()

    def build_ui(self):
        control = ttk.Frame(self.root)

        control.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10,
        )

        ttk.Label(
            control,
            text="Depth",
        ).pack()

        self.depth_entry = ttk.Entry(control)

        self.depth_entry.insert(0, "1")

        self.depth_entry.pack(pady=5)

        ttk.Button(
            control,
            text="Draw",
            command=self.update_depth,
        ).pack(pady=10)

        self.plot_frame = ttk.Frame(self.root)

        self.plot_frame.pack(
            side="right",
            fill="both",
            expand=True,
        )

    def update_depth(self):
        try:
            self.depth = int(self.depth_entry.get())

        except ValueError:
            self.depth = 1

        self.draw_fractal()

    def draw_fractal(self):
        self.ax.clear()

        points = minkowski_island(self.depth)

        x_values = [point[0] for point in points]

        y_values = [point[1] for point in points]

        self.ax.plot(
            x_values,
            y_values,
            color="blue",
            linewidth=1,
        )

        self.ax.set_aspect("equal")

        self.ax.set_title(f"Minkowski Island depth {self.depth}")

        self.ax.axis("off")

        self.canvas.draw()

    def on_close(self):
        plt.close(self.fig)

        self.root.destroy()


main_window = tk.Tk()

app = App(main_window)

main_window.mainloop()
