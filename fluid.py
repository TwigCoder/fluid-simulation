import dearpygui.dearpygui as dpg
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FluidCell:
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    pressure: float = 0.0
    temperature: float = 0.0
    vorticity: float = 0.0
    color: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    def copy(self):
        return FluidCell(
            self.velocity_x,
            self.velocity_y,
            self.pressure,
            self.temperature,
            self.vorticity,
            self.color,
        )


class FluidSimulation:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[FluidCell() for _ in range(width)] for _ in range(height)]
        self.buffer = [[FluidCell() for _ in range(width)] for _ in range(height)]
        self.is_running = False

        self.diffusion_rate = 0.1
        self.viscosity = 0.1
        self.temperature_diffusion = 0.05
        self.vorticity_strength = 0.5
        self.color_diffusion = 0.1
        self.decay_rate = 0.995

    def update(self):
        if not self.is_running:
            return

        for y in range(self.height):
            for x in range(self.width):
                self.update_cell(x, y)

        self.grid, self.buffer = self.buffer, self.grid

    def update_cell(self, x: int, y: int):
        neighbors = self.get_neighbors(x, y)
        current = self.grid[y][x]
        buffer_cell = self.buffer[y][x]

        avg_vel_x = sum(n.velocity_x for n in neighbors) / len(neighbors)
        avg_vel_y = sum(n.velocity_y for n in neighbors) / len(neighbors)
        avg_pressure = sum(n.pressure for n in neighbors) / len(neighbors)
        avg_temp = sum(n.temperature for n in neighbors) / len(neighbors)

        vorticity = self.calculate_vorticity(x, y)

        pressure_gradient_x = (
            self.grid[y][(x + 1) % self.width].pressure
            - self.grid[y][(x - 1) % self.width].pressure
        )
        pressure_gradient_y = (
            self.grid[(y + 1) % self.height][x].pressure
            - self.grid[(y - 1) % self.height][x].pressure
        )

        spiral_factor = 0.2
        buffer_cell.velocity_x = (
            avg_vel_x * (1 - self.viscosity) + current.velocity_x * self.viscosity
        ) * self.decay_rate + pressure_gradient_y * spiral_factor
        buffer_cell.velocity_y = (
            avg_vel_y * (1 - self.viscosity) + current.velocity_y * self.viscosity
        ) * self.decay_rate - pressure_gradient_x * spiral_factor

        temp_factor = 0.15
        buffer_cell.velocity_y -= (current.temperature - 0.5) * temp_factor
        buffer_cell.velocity_x += (current.temperature - 0.5) * vorticity * 0.1

        vorticity_scale = self.vorticity_strength * (1 + current.temperature)
        buffer_cell.velocity_x += vorticity * vorticity_scale
        buffer_cell.velocity_y += vorticity * vorticity_scale

        buffer_cell.pressure = (
            avg_pressure * self.decay_rate + np.sin(current.pressure * np.pi) * 0.1
        )

        buffer_cell.temperature = (
            avg_temp * (1 - self.temperature_diffusion)
            + current.temperature * self.temperature_diffusion
        ) * self.decay_rate

        flow_strength = np.sqrt(buffer_cell.velocity_x**2 + buffer_cell.velocity_y**2)
        color_flow_factor = 0.1 * flow_strength

        r = sum(n.color[0] for n in neighbors) / len(neighbors)
        g = sum(n.color[1] for n in neighbors) / len(neighbors)
        b = sum(n.color[2] for n in neighbors) / len(neighbors)

        buffer_cell.color = (
            (r * (1 - self.color_diffusion) + current.color[0] * self.color_diffusion)
            * (1 + color_flow_factor),
            (g * (1 - self.color_diffusion) + current.color[1] * self.color_diffusion)
            * (1 + color_flow_factor),
            (b * (1 - self.color_diffusion) + current.color[2] * self.color_diffusion)
            * (1 + color_flow_factor),
        )

        max_color = max(buffer_cell.color)
        if max_color > 1.0:
            buffer_cell.color = tuple(c / max_color for c in buffer_cell.color)

    def calculate_vorticity(self, x: int, y: int) -> float:
        right = self.grid[y][(x + 1) % self.width].velocity_y
        left = self.grid[y][(x - 1) % self.width].velocity_y
        top = self.grid[(y - 1) % self.height][x].velocity_x
        bottom = self.grid[(y + 1) % self.height][x].velocity_x

        return (right - left - bottom + top) * 0.25

    def get_neighbors(self, x: int, y: int) -> List[FluidCell]:
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                neighbors.append(self.grid[ny][nx])
        return neighbors

    def add_vector(
        self,
        x: int,
        y: int,
        vx: float,
        vy: float,
        color: Tuple[float, float, float],
        temp: float,
    ):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x].velocity_x = vx
            self.grid[y][x].velocity_y = vy
            self.grid[y][x].pressure = 1.0
            self.grid[y][x].temperature = temp
            self.grid[y][x].color = color

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = FluidCell()
                self.buffer[y][x] = FluidCell()
