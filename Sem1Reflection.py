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
    ANIM_TIME = 2.5

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Colors
    WHITE = (245, 245, 245)
    GRAY = (220, 220, 220)
    AXIS_COLOR = (80, 80, 80)
    BLUE = (0, 102, 204)    # Original Vector
    RED = (204, 0, 0)      # Transformed Vector
    I_HAT_COLOR = (0, 153, 0) # Green for i
    J_HAT_COLOR = (255, 128, 0) # Orange for j

    def to_screen(v):
        return (CENTER + np.array([v[0], -v[1]]) * SCALE).astype(int)

    def draw_vector(v, color, width=4, alpha=255):
        start_pos = to_screen(np.array([0, 0]))
        end_pos = to_screen(v)
        if np.array_equal(start_pos, end_pos): return
        
        # Create a temporary surface for alpha if needed
        if alpha < 255:
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            color_with_alpha = (*color, alpha)
            pygame.draw.line(temp_surface, color_with_alpha, start_pos, end_pos, width)
        else:
            pygame.draw.line(screen, color, start_pos, end_pos, width)
        
        # Draw arrow head
        direction = v
        norm = np.linalg.norm(direction)
        if norm > 0:
            unit = direction / norm
            perp = np.array([-unit[1], unit[0]])
            
            tip = end_pos
            side1 = to_screen(v - unit * 0.2 + perp * 0.1)
            side2 = to_screen(v - unit * 0.2 - perp * 0.1)
            
            if alpha < 255:
                pygame.draw.polygon(temp_surface, color_with_alpha, [tip, side1, side2])
                screen.blit(temp_surface, (0, 0))
            else:
                pygame.draw.polygon(screen, color, [tip, side1, side2])

    identity = np.eye(2)
    i_hat = np.array([1, 0])
    j_hat = np.array([0, 1])

    t = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        t = min(t + dt / ANIM_TIME, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Interpolated Matrix
        current_matrix = (1 - t) * identity + t * matrix
        
        screen.fill(WHITE)

        # Draw Animated Grid
        grid_alpha = 100 # Subtler grid
        temp_grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(-10, 11):
            p1 = current_matrix @ np.array([i, -10])
            p2 = current_matrix @ np.array([i, 10])
            pygame.draw.line(temp_grid_surface, (*GRAY, grid_alpha), to_screen(p1), to_screen(p2), 1)
            
            p3 = current_matrix @ np.array([-10, i])
            p4 = current_matrix @ np.array([10, i])
            pygame.draw.line(temp_grid_surface, (*GRAY, grid_alpha), to_screen(p3), to_screen(p4), 1)
        screen.blit(temp_grid_surface, (0, 0))

        # Draw Main Axes (transformed)
        pygame.draw.line(screen, AXIS_COLOR, to_screen(current_matrix @ np.array([-10, 0])), to_screen(current_matrix @ np.array([10, 0])), 2)
        pygame.draw.line(screen, AXIS_COLOR, to_screen(current_matrix @ np.array([0, -10])), to_screen(current_matrix @ np.array([0, 10])), 2)

        # Draw Basis Vectors
        draw_vector(current_matrix @ i_hat, I_HAT_COLOR, width=3, alpha=50)
        draw_vector(current_matrix @ j_hat, J_HAT_COLOR, width=3, alpha=50)

        # Draw Original Vector
        draw_vector(vector, BLUE, width=2, alpha=30) 

        # Draw Current Transforming Vector
        current_vector = current_matrix @ vector
        draw_vector(current_vector, RED, width=5, alpha=255)

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
        # Loop through and fill Matrix and Vector entries
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

