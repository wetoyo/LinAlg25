"""
Description:
This program demonstrates how matrices act as linear transformations on vectors in two-dimensional space. 
The user inputs a vector and a 2×2 matrix, and the program visually displays both the original vector and the transformed vector. 
This connects the algebraic process of matrix–vector multiplication with its geometric interpretation.
To run:
install numpy, pygame, and tkinter
"""
import tkinter as tk
import numpy as np
import pygame
import sys

def launch_visualizer(matrix, vector):
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    CENTER = np.array([WIDTH // 2, HEIGHT // 2])
    SCALE = 80
    FPS = 60
    ANIM_TIME = 2.0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Colors
    WHITE = (245, 245, 245)
    GRAY = (220, 220, 220)
    BLACK = (0, 0, 0)
    BLUE = (0, 102, 204)
    RED = (204, 0, 0)

    def to_screen(v):
        return CENTER + np.array([v[0], -v[1]]) * SCALE

    def draw_grid():
        for i in range(-10, 11):
            pygame.draw.line(screen, GRAY, to_screen(np.array([i, -10])), to_screen(np.array([i, 10])), 1)
            pygame.draw.line(screen, GRAY, to_screen(np.array([-10, i])), to_screen(np.array([10, i])), 1)

        pygame.draw.line(screen, BLACK, to_screen(np.array([-10, 0])), to_screen(np.array([10, 0])), 3)
        pygame.draw.line(screen, BLACK, to_screen(np.array([0, -10])), to_screen(np.array([0, 10])), 3)

    def draw_vector(v, color):
        pygame.draw.line(screen, color, to_screen(np.zeros_like(v)), to_screen(v), 4)
        # Draw arrow head
        v_screen = to_screen(v)
        origin_screen = to_screen(np.zeros_like(v))
        if not np.array_equal(v_screen, origin_screen):
            direction = (v_screen - origin_screen)
            norm = np.linalg.norm(direction)
            if norm > 0:
                unit = direction / norm
                # Finds dir perp the vector to make the triangle
                perp = np.array([-unit[1], unit[0]])
                side1 = v_screen - unit * 15 + perp * 7
                side2 = v_screen - unit * 15 - perp * 7
                pygame.draw.polygon(screen, color, [v_screen, side1, side2])

    transformed = matrix @ vector

    t = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        t = min(t + dt / ANIM_TIME, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Lerp between original and transformed
        current = (1 - t) * vector + t * transformed

        screen.fill(WHITE)
        draw_grid()
        draw_vector(vector, BLUE)
        draw_vector(current, RED)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("2x2 Linear Transformation Visualizer")
        self.root.configure(padx=20, pady=20)
        
        # Container for Matrix and Vector
        self.main_container = tk.Frame(root)
        self.main_container.pack(pady=10)

        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.pack()

        # Matrix Section
        matrix_frame = tk.LabelFrame(self.main_container, text="2x2 Transformation Matrix", padx=10, pady=10)
        matrix_frame.grid(row=0, column=0, padx=10)
        
        self.matrix_entries = []
        for r in range(2):
            row_entries = []
            for c in range(2):
                e = tk.Entry(matrix_frame, width=6, justify="center", font=("Helvetica", 10))
                e.grid(row=r, column=c, padx=5, pady=5)
                e.insert(0, "1" if r == c else "0")
                row_entries.append(e)
            self.matrix_entries.append(row_entries)

        # Vector Section
        vector_frame = tk.LabelFrame(self.main_container, text="2x1 Vector", padx=10, pady=10)
        vector_frame.grid(row=0, column=1, padx=10, sticky="n")
        
        self.vector_entries = []
        for r in range(2):
            e = tk.Entry(vector_frame, width=6, justify="center", font=("Helvetica", 10))
            e.grid(row=r, column=0, padx=5, pady=5)
            e.insert(0, "1")
            self.vector_entries.append(e)

        # Action Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Visualize Transformation", 
                  command=self.submit, 
                  bg="#28a745", fg="white", 
                  font=("Helvetica", 11, "bold"), 
                  padx=20, pady=10).pack()

    def submit(self):
        # Loop through and fill matrix and vector entries
        try:
            matrix_data = []
            for r in range(2):
                row_data = []
                for c in range(2):
                    val = float(self.matrix_entries[r][c].get())
                    row_data.append(val)
                matrix_data.append(row_data)
            
            vector_data = []
            for r in range(2):
                val = float(self.vector_entries[r].get())
                vector_data.append(val)

            matrix = np.array(matrix_data)
            vector = np.array(vector_data)

            self.root.destroy()
            launch_visualizer(matrix, vector)

        except ValueError:
            self.error_label.config(text="Invalid input. Please ensure all entries are numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

