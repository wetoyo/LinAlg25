"""
Description:
This program demonstrates how matrices act as linear transformations on vectors in two-dimensional space. 
The user inputs a vector and a 2×2 matrix, and the program visually displays both the original vector and the transformed vector. 
This connects the algebraic process of matrix–vector multiplication with its geometric interpretation.
To run:
install numpy, pygame, and tkinter

Notes:

@ is the matrix multiplication operator, and is used when transforming the vectors/grid lines and when composing the matrices.
"""
import tkinter as tk
import numpy as np
import pygame
import threading
import queue
import time

class Visualizer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = True
        self.daemon = True
        
        # Transformation State
        self.current_total_matrix = np.eye(2)
        self.target_total_matrix = np.eye(2)
        self.start_matrix = np.eye(2)
        
        self.vector = np.array([1, 1])
        
        self.t = 1.0  # Animation progress (0 to 1)
        self.anim_time = 1.5
        
    def run(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 800
        CENTER = np.array([WIDTH // 2, HEIGHT // 2])
        SCALE = 80
        FPS = 60

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Linear Algebra Visualizer")
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
            
            # Pygame shenanigans to handle alpha (making transparent layer and bliting to that, then composing)
            if alpha < 255:
                temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                color_with_alpha = (*color, alpha)
                pygame.draw.line(temp_surface, color_with_alpha, start_pos, end_pos, width)
            else:
                pygame.draw.line(screen, color, start_pos, end_pos, width)
            
            # Draw arrow head
            # Uses the orthogonality of the unit vector and the perpendicular vector to draw the arrow head.
            # By moving out to the left and right of the vector, we can get the 3 points that define the arrow head
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

        i_hat = np.array([1, 0])
        j_hat = np.array([0, 1])

        while self.running:
            dt = clock.tick(FPS) / 1000
            
            # Check for new transformations
            try:
                # Read messages from tkinter
                while not self.queue.empty():
                    msg_type, data = self.queue.get_nowait()
                    if msg_type == 'TRANSFORM':
                        new_m, new_v = data
                        self.vector = new_v
                        self.start_matrix = self.target_total_matrix.copy()
                        self.target_total_matrix = new_m @ self.target_total_matrix
                        self.t = 0.0
                    elif msg_type == 'RESET':
                        self.target_total_matrix = np.eye(2)
                        self.start_matrix = np.eye(2)
                        self.current_total_matrix = np.eye(2)
                        self.vector = data
                        self.t = 1.0
            except queue.Empty:
                pass

            if self.t < 1.0:
                self.t = min(self.t + dt / self.anim_time, 1.0)
            
            # Interpolated Matrix
            # Linear interpolation between start and target matrices, with (1-t) of the start and t of the target
            self.current_total_matrix = (1 - self.t) * self.start_matrix + self.t * self.target_total_matrix
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            screen.fill(WHITE)

            # Draw Animated Grid
            grid_alpha = 100
            temp_grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(-10, 11):
                # Construct a grid line as a vector from (-10, i) to (10, i). Multiply it by the current total matrix to transform it

                # Horizontal

                p1 = self.current_total_matrix @ np.array([i, -10])
                p2 = self.current_total_matrix @ np.array([i, 10])
                pygame.draw.line(temp_grid_surface, (*GRAY, grid_alpha), to_screen(p1), to_screen(p2), 1)
                
                # Vertical
                p3 = self.current_total_matrix @ np.array([-10, i])
                p4 = self.current_total_matrix @ np.array([10, i])
                pygame.draw.line(temp_grid_surface, (*GRAY, grid_alpha), to_screen(p3), to_screen(p4), 1)
            screen.blit(temp_grid_surface, (0, 0))

            
            # Draw Main Axes. Same logic as grid lines, just twice as thick and different color.
            pygame.draw.line(screen, AXIS_COLOR, to_screen(self.current_total_matrix @ np.array([-10, 0])), to_screen(self.current_total_matrix @ np.array([10, 0])), 2)
            pygame.draw.line(screen, AXIS_COLOR, to_screen(self.current_total_matrix @ np.array([0, -10])), to_screen(self.current_total_matrix @ np.array([0, 10])), 2)


            # Compose the basis vectors with the current total matrix to get the transformed basis vectors
            draw_vector(self.current_total_matrix @ i_hat, I_HAT_COLOR, width=3, alpha=100)
            draw_vector(self.current_total_matrix @ j_hat, J_HAT_COLOR, width=3, alpha=100)

            # Draw Original Vector
            draw_vector(self.vector, BLUE, width=2, alpha=60) 

            # Draw Current Transforming Vector
            current_vector = self.current_total_matrix @ self.vector
            draw_vector(current_vector, RED, width=5, alpha=255)

            pygame.display.flip()

        pygame.quit()

    def apply_transform(self, matrix, vector):
        self.queue.put(('TRANSFORM', (matrix, vector)))

    def reset(self, vector):
        self.queue.put(('RESET', vector))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("2x2 Linear Transformation Visualizer")
        self.root.configure(padx=20, pady=20)
        
        self.visualizer = None
        
        # Container for Matrix and Vector
        self.main_container = tk.Frame(root)
        self.main_container.pack(pady=10)

        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.pack()

        # Net Matrix Display Section
        self.net_frame = tk.LabelFrame(self.main_container, text="Net Transformation Matrix", padx=10, pady=10)
        self.net_frame.grid(row=0, column=2, padx=10, sticky="n")
        
        self.net_matrix_labels = []
        for r in range(2):
            row_labels = []
            for c in range(2):
                l = tk.Label(self.net_frame, text="1.0" if r == c else "0.0", width=8, 
                             font=("Helvetica", 10, "bold"), fg="#0066cc")
                l.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(l)
            self.net_matrix_labels.append(row_labels)

        # Matrix Section
        matrix_frame = tk.LabelFrame(self.main_container, text="Input Matrix (New Step)", padx=10, pady=10)
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
        
        self.apply_btn = tk.Button(button_frame, text="Apply Transformation", 
                  command=self.submit, 
                  bg="#28a745", fg="white", 
                  font=("Helvetica", 11, "bold"), 
                  padx=20, pady=10)
        self.apply_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(button_frame, text="Reset", 
                  command=self.reset_visualizer, 
                  bg="#dc3545", fg="white", 
                  font=("Helvetica", 11, "bold"), 
                  padx=20, pady=10)
        self.net_matrix = np.eye(2)
        self.update_net_display()

    def update_net_display(self):
        for r in range(2):
            for c in range(2):
                val = self.net_matrix[r, c]
                self.net_matrix_labels[r][c].config(text=f"{val:.2f}")

    def get_inputs(self):
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

        return np.array(matrix_data), np.array(vector_data)

    def submit(self):
        try:
            matrix, vector = self.get_inputs()
            self.error_label.config(text="")
            
            if self.visualizer is None or not self.visualizer.is_alive():
                self.visualizer = Visualizer()
                self.visualizer.start()
                # Wait a bit for window to init
                time.sleep(0.1)
            
            self.visualizer.apply_transform(matrix, vector)
            
            # Update local net matrix for display
            self.net_matrix = matrix @ self.net_matrix
            self.update_net_display()

        except ValueError:
            self.error_label.config(text="Invalid input. Please ensure all entries are numbers.")

    def reset_visualizer(self):
        try:
            _, vector = self.get_inputs()
            if self.visualizer and self.visualizer.is_alive():
                self.visualizer.reset(vector)
            
            # Reset local net matrix for display
            self.net_matrix = np.eye(2)
            self.update_net_display()
        except ValueError:
            self.error_label.config(text="Invalid input for vector.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
