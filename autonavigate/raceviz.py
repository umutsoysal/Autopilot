from collections import defaultdict
from typing import DefaultDict, List, Dict, Tuple
from utils import pol2cart, swap_tuple2
from windfields import WindAtPoint
import matplotlib.pyplot as plt
from matplotlib import animation, cm
from sympy import Point2D
import math
import numpy as np


class RaceViz:
    wind_data_list: List[Dict[Point2D, WindAtPoint]]
    boat_coords_list: DefaultDict[str, List[Point2D]]
    fixed_coordinate_order: List[Point2D]
    field_bounds: Dict[str, float]
    boat_color_set = cm.get_cmap("Dark2")

    def __init__(self) -> None:
        self.wind_data_list = []
        self.boat_coords_list = defaultdict(list)

    def render_race_animation(self):
        raise NotImplementedError

    def save_race_animation(self, output_path):
        raise NotImplementedError

    def register_wind_data(self, incoming_wind_data: Dict[Point2D, WindAtPoint]):
        if not self.wind_data_list:
            # TODO: should this be in the subclass and not here?
            self.fixed_coordinate_order = sorted(
                incoming_wind_data.keys(), key=lambda p: (p.x, p.y)
            )
        self.wind_data_list.append(incoming_wind_data)

    def register_field_bounds(self, field_bounds):
        self.field_bounds = field_bounds

    def register_boat_coords(self, boat_coord_data: Dict[str, Point2D]):
        for boat_name, boat_coords in boat_coord_data.items():
            self.boat_coords_list[boat_name].append(boat_coords)


class MPLRaceViz(RaceViz):
    def render_race_animation(self):
        fig, ax = plt.subplots()
        X, Y = zip(*[(coord.x, coord.y) for coord in self.fixed_coordinate_order])
        U, V = self._UV_for_frame(frame=0)
        Q = ax.quiver(X, Y, U, V, color="red")
        coords, colors = self._scatter_N_for_frame(frame=0)
        S = ax.scatter(coords[:, 0], coords[:, 1], c=colors)

        # ax.set_xlim(self.field_bounds["x-left"], self.field_bounds["x-right"])
        # ax.set_ylim(self.field_bounds["y-bot"], self.field_bounds["y-top"])

        def update_quiver(frame, Q, S):
            U, V = self._UV_for_frame(frame)
            Q.set_UVC(U, V)
            coords, colors = self._scatter_N_for_frame(frame=frame)
            S.set_offsets(coords)
            # S.set_array(colors)
            return (Q,)

        self.anim = animation.FuncAnimation(
            fig,
            update_quiver,
            fargs=(Q, S),
            frames=len(self.wind_data_list),
            blit=False,
        )

        fig.tight_layout()

    def _UV_for_frame(self, frame: int):
        return zip(
            *[
                swap_tuple2(
                    pol2cart(
                        self.wind_data_list[frame][coord].tws,
                        2 * math.pi - self.wind_data_list[frame][coord].twa,
                    )
                )
                for coord in self.fixed_coordinate_order
            ]
        )

    def _scatter_N_for_frame(self, frame: int):
        N = len(self.boat_coords_list.keys())
        X = np.empty((N, 2), dtype=float)
        colors = []
        for idx_N, boat_name in enumerate(sorted(list(self.boat_coords_list.keys()))):
            X[idx_N, 0], X[idx_N, 1] = (
                self.boat_coords_list[boat_name][frame].x,
                self.boat_coords_list[boat_name][frame].y,
            )
            colors.append(self.boat_color_set(idx_N))
        return X, colors

    def save_race_animation(self, output_path):
        Writer = animation.writers["ffmpeg"]
        writer = Writer(fps=15, metadata=dict(artist="Me"), bitrate=1800)
        self.anim.save(output_path, writer=writer)


if __name__ == "__main__":
    fig, ax = plt.subplots()
    X, Y = [[0, 10], [10, 0]], [[0, 10], [0, 10]]
    U, V = [[1, -1], [1, -1]], [[1, 1], [-1, -1]]
    ax.quiver(X, Y, U, V)
    fig.show()
    plt.waitforbuttonpress()
