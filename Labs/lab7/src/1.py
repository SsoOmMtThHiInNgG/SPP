import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def side(self, point):
        return self.a * point.x + self.b * point.y + self.c


class App:
    def __init__(self, window):
        self.root = window

        self.root.title("Point and Line")

        self.points = []

        self.line = Line(1, -1, 0)

        self.paused = False

        self.after_id = None

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

        self.update_plot()

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
            text="Points count",
        ).pack()

        self.n_entry = ttk.Entry(control)

        self.n_entry.insert(0, "30")

        self.n_entry.pack(pady=5)

        ttk.Button(
            control,
            text="Generate points",
            command=self.generate_points,
        ).pack(pady=5)

        ttk.Label(
            control,
            text="Line: Ax + By + C = 0",
        ).pack(pady=10)

        self.a_entry = ttk.Entry(control)

        self.b_entry = ttk.Entry(control)

        self.c_entry = ttk.Entry(control)

        entries = [
            ("A", self.a_entry, "1"),
            ("B", self.b_entry, "-1"),
            ("C", self.c_entry, "0"),
        ]

        for label, entry, value in entries:
            ttk.Label(
                control,
                text=label,
            ).pack()

            entry.insert(0, value)

            entry.pack(pady=2)

        ttk.Button(
            control,
            text="Update line",
            command=self.update_line,
        ).pack(pady=10)

        ttk.Button(
            control,
            text="Pause",
            command=self.toggle_pause,
        ).pack(pady=5)

        ttk.Button(
            control,
            text="Screenshot",
            command=self.save_screenshot,
        ).pack(pady=5)

        self.plot_frame = ttk.Frame(self.root)

        self.plot_frame.pack(
            side="right",
            fill="both",
            expand=True,
        )

    def generate_points(self):
        try:
            count = int(self.n_entry.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid number",
            )

            return

        self.points = []

        for _ in range(count):
            point = Point(
                random.uniform(-10, 10),
                random.uniform(-10, 10),
            )

            self.points.append(point)

    def update_line(self):
        try:
            a = float(self.a_entry.get())

            b = float(self.b_entry.get())

            c = float(self.c_entry.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid coefficients",
            )

            return

        self.line = Line(a, b, c)

    def toggle_pause(self):
        self.paused = not self.paused

    def save_screenshot(self):
        self.fig.savefig("screenshot.png")

        messagebox.showinfo(
            "Saved",
            "Screenshot saved",
        )

    def draw_line(self):
        a = self.line.a

        b = self.line.b

        c = self.line.c

        x_values = [-10, 10]

        if b != 0:
            y_values = []

            for x in x_values:
                y = (-a * x - c) / b

                y_values.append(y)

        else:
            x_values = [-c / a] * 2

            y_values = [-10, 10]

        self.ax.plot(
            x_values,
            y_values,
            "k-",
        )

    def draw_points(self):
        left = []

        right = []

        on_line = []

        for point in self.points:
            side = self.line.side(point)

            if side > 0:
                right.append(point)

            elif side < 0:
                left.append(point)

            else:
                on_line.append(point)

        self.ax.scatter(
            [p.x for p in left],
            [p.y for p in left],
            color="red",
            label="Left",
        )

        self.ax.scatter(
            [p.x for p in right],
            [p.y for p in right],
            color="blue",
            label="Right",
        )

        self.ax.scatter(
            [p.x for p in on_line],
            [p.y for p in on_line],
            color="green",
            label="On line",
        )

    def update_plot(self):
        if not self.root.winfo_exists():
            return

        if not self.paused:
            self.ax.clear()

            self.ax.grid(True)

            self.ax.set_title("Point-Line")

            self.draw_line()

            self.draw_points()

            self.ax.legend()

            self.canvas.draw()

        self.after_id = self.root.after(
            200,
            self.update_plot,
        )

    def on_close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        self.root.destroy()


main_window = tk.Tk()

app = App(main_window)

main_window.mainloop()
