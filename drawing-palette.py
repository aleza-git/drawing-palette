import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox


class DrawingPalette:

    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Palette")
        self.root.geometry("950x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4eee7")

        self.current_color = "#2d2a26"
        self.brush_size = 8
        self.last_x = None
        self.last_y = None

        self.create_ui()

    # ==================== UI ====================

    def create_ui(self):

        # Top bar
        top = tk.Frame(
            self.root,
            bg="#2d2a26",
            height=75
        )
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="🎨  Drawing Palette",
            font=("Georgia", 22, "bold"),
            bg="#2d2a26",
            fg="#fffaf3"
        ).pack(
            side="left",
            padx=25
        )

        tk.Label(
            top,
            text="a little space to create",
            font=("Georgia", 10, "italic"),
            bg="#2d2a26",
            fg="#d8cec2"
        ).pack(
            side="right",
            padx=25
        )

        # Toolbar
        toolbar = tk.Frame(
            self.root,
            bg="#e7ddd2",
            height=70
        )
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        # Colors
        tk.Label(
            toolbar,
            text="COLORS",
            font=("Arial", 8, "bold"),
            bg="#e7ddd2",
            fg="#62594f"
        ).pack(
            side="left",
            padx=(20, 8)
        )

        colors = [
            "#2d2a26",
            "#d94f4f",
            "#e8894f",
            "#e6b84f",
            "#70a85b",
            "#4f91c6",
            "#8064a2",
            "#d875a5",
            "#ffffff"
        ]

        for color in colors:

            tk.Button(
                toolbar,
                bg=color,
                activebackground=color,
                width=2,
                height=1,
                relief="flat",
                bd=0,
                command=lambda c=color: self.set_color(c)
            ).pack(
                side="left",
                padx=3
            )

        # Custom color
        tk.Button(
            toolbar,
            text="＋",
            font=("Arial", 12, "bold"),
            bg="#fffaf3",
            fg="#2d2a26",
            relief="flat",
            command=self.choose_color
        ).pack(
            side="left",
            padx=(5, 15)
        )

        # Brush size
        tk.Label(
            toolbar,
            text="BRUSH",
            font=("Arial", 8, "bold"),
            bg="#e7ddd2",
            fg="#62594f"
        ).pack(side="left")

        self.size_scale = tk.Scale(
            toolbar,
            from_=2,
            to=30,
            orient="horizontal",
            bg="#e7ddd2",
            fg="#2d2a26",
            highlightthickness=0,
            troughcolor="#cfc2b5",
            length=100,
            command=self.change_size
        )
        self.size_scale.set(8)
        self.size_scale.pack(
            side="left",
            padx=5
        )

        # Eraser
        tk.Button(
            toolbar,
            text="⌫ Eraser",
            font=("Arial", 9, "bold"),
            bg="#fffaf3",
            fg="#2d2a26",
            relief="flat",
            command=self.eraser
        ).pack(
            side="left",
            padx=10,
            ipadx=8,
            ipady=5
        )

        # Canvas
        canvas_frame = tk.Frame(
            self.root,
            bg="#cfc2b5",
            padx=5,
            pady=5
        )
        canvas_frame.pack(
            padx=25,
            pady=20
        )

        self.canvas = tk.Canvas(
            canvas_frame,
            width=890,
            height=410,
            bg="#fffdf9",
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>",
            self.start_draw
        )
        self.canvas.bind(
            "<B1-Motion>",
            self.draw
        )
        self.canvas.bind(
            "<ButtonRelease-1>",
            self.stop_draw
        )

        # Bottom buttons
        bottom = tk.Frame(
            self.root,
            bg="#f4eee7"
        )
        bottom.pack(
            fill="x",
            padx=25
        )

        tk.Button(
            bottom,
            text="↻  Clear Canvas",
            font=("Arial", 10, "bold"),
            bg="#e7ddd2",
            fg="#2d2a26",
            relief="flat",
            command=self.clear_canvas
        ).pack(
            side="left",
            ipadx=15,
            ipady=8
        )

        tk.Button(
            bottom,
            text="💾  Save Drawing",
            font=("Arial", 10, "bold"),
            bg="#2d2a26",
            fg="#fffaf3",
            relief="flat",
            command=self.save_drawing
        ).pack(
            side="right",
            ipadx=15,
            ipady=8
        )

    # ==================== DRAWING ====================

    def start_draw(self, event):

        self.last_x = event.x
        self.last_y = event.y

        # Draw a dot if the user simply clicks
        self.canvas.create_oval(
            event.x - self.brush_size / 2,
            event.y - self.brush_size / 2,
            event.x + self.brush_size / 2,
            event.y + self.brush_size / 2,
            fill=self.current_color,
            outline=self.current_color
        )

    def draw(self, event):

        if self.last_x is not None and self.last_y is not None:

            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                fill=self.current_color,
                width=self.brush_size,
                capstyle=tk.ROUND,
                smooth=True
            )

        self.last_x = event.x
        self.last_y = event.y

    def stop_draw(self, event):

        self.last_x = None
        self.last_y = None

    # ==================== COLORS ====================

    def set_color(self, color):

        self.current_color = color

    def choose_color(self):

        color = colorchooser.askcolor(
            title="Choose a color"
        )

        if color[1]:
            self.current_color = color[1]

    def eraser(self):

        self.current_color = "#fffdf9"

    # ==================== BRUSH ====================

    def change_size(self, value):

        self.brush_size = int(value)

    # ==================== CANVAS ====================

    def clear_canvas(self):

        answer = messagebox.askyesno(
            "Clear Canvas",
            "Are you sure you want to clear your drawing?"
        )

        if answer:
            self.canvas.delete("all")

    # ==================== SAVE ====================

    def save_drawing(self):

        messagebox.showinfo(
            "Save Drawing",
            "For this beginner version, your drawing can be saved using a screenshot of the canvas."
        )


# ==================== RUN ====================

root = tk.Tk()

app = DrawingPalette(root)

root.mainloop()