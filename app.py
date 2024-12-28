import numpy as np
import colorsys
import random
import pygame
import sys
import dearpygui.dearpygui as dpg
from fluid import FluidSimulation


class App:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = (1200, 800)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Advanced Fluid Cellular Automaton")

        self.sim = FluidSimulation(120, 80)
        self.cell_size = 10

        self.viz_modes = ["Vectors", "Pressure", "Temperature", "Vorticity", "Color"]
        self.current_viz_mode = "Vectors"
        self.show_grid = False
        self.vector_scale = 1.0
        self.color_mode = "Rainbow"
        self.current_color = (1.0, 1.0, 1.0)
        self.brush_size = 1
        self.temperature_brush = 0.5

        dpg.create_context()
        self.create_gui()
        dpg.create_viewport(title="Controls", width=400, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        self.drawing = False
        self.running = True

    def create_gui(self):
        with dpg.window(label="Controls", width=400, height=600):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Play/Pause", callback=self.toggle_simulation)
                dpg.add_button(label="Clear", callback=self.clear_simulation)
                dpg.add_button(label="Random", callback=self.add_random_vectors)

            dpg.add_separator()

            dpg.add_text("Visualization")
            dpg.add_combo(
                items=self.viz_modes,
                default_value=self.current_viz_mode,
                callback=lambda s, a: setattr(self, "current_viz_mode", a),
            )
            dpg.add_checkbox(
                label="Show Grid",
                default_value=self.show_grid,
                callback=lambda s, a: setattr(self, "show_grid", a),
            )
            dpg.add_slider_float(
                label="Vector Scale",
                default_value=1.0,
                min_value=0.1,
                max_value=5.0,
                callback=lambda s, a: setattr(self, "vector_scale", a),
            )

            dpg.add_separator()
            dpg.add_text("Simulation Parameters")
            dpg.add_slider_float(
                label="Diffusion Rate",
                default_value=0.1,
                min_value=0.0,
                max_value=1.0,
                callback=lambda s, a: setattr(self.sim, "diffusion_rate", a),
            )
            dpg.add_slider_float(
                label="Viscosity",
                default_value=0.1,
                min_value=0.0,
                max_value=1.0,
                callback=lambda s, a: setattr(self.sim, "viscosity", a),
            )
            dpg.add_slider_float(
                label="Vorticity Strength",
                default_value=0.5,
                min_value=0.0,
                max_value=2.0,
                callback=lambda s, a: setattr(self.sim, "vorticity_strength", a),
            )

            dpg.add_separator()
            dpg.add_text("Brush Settings")
            dpg.add_slider_int(
                label="Brush Size",
                default_value=1,
                min_value=1,
                max_value=10,
                callback=lambda s, a: setattr(self, "brush_size", a),
            )
            dpg.add_slider_float(
                label="Temperature",
                default_value=0.5,
                min_value=0.0,
                max_value=1.0,
                callback=lambda s, a: setattr(self, "temperature_brush", a),
            )
            dpg.add_color_edit(
                label="Brush Color",
                default_value=(255, 255, 255),
                callback=self.update_brush_color,
            )

    def update_brush_color(self, sender, app_data):
        r, g, b = app_data[:3]
        self.current_color = (r / 255, g / 255, b / 255)

    def add_random_vectors(self):
        for _ in range(100):
            x = random.randint(0, self.sim.width - 1)
            y = random.randint(0, self.sim.height - 1)
            angle = random.uniform(0, 2 * np.pi)
            vx = np.cos(angle)
            vy = np.sin(angle)
            color = tuple(random.random() for _ in range(3))
            temp = random.random()
            self.sim.add_vector(x, y, vx, vy, color, temp)

    def draw_grid(self):
        self.screen.fill((0, 0, 0))

        if self.show_grid:
            for x in range(0, self.WINDOW_SIZE[0], self.cell_size):
                pygame.draw.line(
                    self.screen, (20, 20, 20), (x, 0), (x, self.WINDOW_SIZE[1])
                )
            for y in range(0, self.WINDOW_SIZE[1], self.cell_size):
                pygame.draw.line(
                    self.screen, (20, 20, 20), (0, y), (self.WINDOW_SIZE[0], y)
                )

        for y in range(self.sim.height):
            for x in range(self.sim.width):
                cell = self.sim.grid[y][x]

                if self.current_viz_mode == "Vectors" and (
                    cell.velocity_x != 0 or cell.velocity_y != 0
                ):
                    self.draw_vector(x, y, cell)
                elif self.current_viz_mode == "Pressure":
                    self.draw_pressure(x, y, cell)
                elif self.current_viz_mode == "Temperature":
                    self.draw_temperature(x, y, cell)
                elif self.current_viz_mode == "Vorticity":
                    self.draw_vorticity(x, y, cell)
                elif self.current_viz_mode == "Color":
                    self.draw_color(x, y, cell)

    def draw_vector(self, x, y, cell):
        start_x = x * self.cell_size + self.cell_size // 2
        start_y = y * self.cell_size + self.cell_size // 2
        end_x = start_x + cell.velocity_x * self.cell_size * self.vector_scale
        end_y = start_y + cell.velocity_y * self.cell_size * self.vector_scale

        magnitude = np.sqrt(cell.velocity_x**2 + cell.velocity_y**2)
        hue = (magnitude * 360) % 360 / 360.0
        rgb = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0))

        pygame.draw.line(self.screen, rgb, (start_x, start_y), (end_x, end_y), 2)

    def draw_pressure(self, x, y, cell):
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        intensity = int(cell.pressure * 255)
        pygame.draw.rect(self.screen, (0, intensity, intensity), rect)

    def draw_temperature(self, x, y, cell):
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        temp = cell.temperature
        pygame.draw.rect(self.screen, (int(temp * 255), 0, int((1 - temp) * 255)), rect)

    def draw_vorticity(self, x, y, cell):
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        v = (cell.vorticity + 1) / 2
        pygame.draw.rect(self.screen, (int(v * 255), 0, int((1 - v) * 255)), rect)

    def draw_color(self, x, y, cell):
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        color = tuple(int(c * 255) for c in cell.color)
        pygame.draw.rect(self.screen, color, rect)

    def handle_mouse_input(self, pos, buttons):
        if buttons[0]:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if not self.drawing:
                self.drawing = True
                self.last_pos = (x, y)
            else:
                dx = x - self.last_pos[0]
                dy = y - self.last_pos[1]
                length = np.sqrt(dx * dx + dy * dy)
                if length > 0:
                    dx, dy = dx / length, dy / length
                    for by in range(-self.brush_size + 1, self.brush_size):
                        for bx in range(-self.brush_size + 1, self.brush_size):
                            self.sim.add_vector(
                                x + bx,
                                y + by,
                                dx,
                                dy,
                                self.current_color,
                                self.temperature_brush,
                            )
                self.last_pos = (x, y)
        else:
            self.drawing = False

    def toggle_simulation(self):
        self.sim.is_running = not self.sim.is_running

    def clear_simulation(self):
        self.sim.clear()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.drawing = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            self.handle_mouse_input(mouse_pos, mouse_buttons)

            self.sim.update()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

            dpg.render_dearpygui_frame()

        dpg.destroy_context()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()
