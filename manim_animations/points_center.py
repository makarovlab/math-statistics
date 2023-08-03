from manimlib import *
import numpy as np

class PointsCenter(Scene):
    def construct(self): 
        axes = Axes(
            x_range=(-5, 10),
            y_range=(-5, 10, 1),
            height=6,
            width=10,
        )

        axes.add_coordinate_labels(
            font_size=10,
            num_decimal_places=1,
        )
        self.add(axes)

        initial_centroid = (6, 1)

        coords = [
            (3, 4),
            (2, 5),
            (6, 7),
            (5, 8),
            (4, 1),
            (9, 3),
            (2, 8),
            (10, 1),
        ]

        for coord in coords:
            x, y = coord

            dot = Dot(color=BLUE)
            dot.move_to(axes.c2p(x, y))
            self.add(dot)

        centroid = Dot(color=RED)
        centroid.move_to(axes.c2p(initial_centroid[0], initial_centroid[1]))
        self.add(centroid)

        x_center = sum([coord[0] for coord in coords]) / len(coords)
        y_center = sum([coord[1] for coord in coords]) / len(coords)
        
        self.wait()
        self.play(centroid.animate.move_to(axes.c2p(x_center, y_center)))
