from manim import *
import numpy as np

class DrawFunctionExample(MovingCameraScene):
    def construct(self):
        # 1. Create Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
        )

        # 2. Weierstrass function
        def weierstrass(x, a=0.5, b=7, n_terms=100):
            return sum(
                a**n * np.cos((b**n) * np.pi * x)
                for n in range(n_terms)
            )

        # 3. Plot the function
        func = axes.plot(
            lambda x: weierstrass(x),
            color=BLUE,
            use_smoothing=False  # важно для "рваного" графика
        )

        # 4. Labels
        labels = axes.get_axis_labels(x_label="x", y_label="W(x)")

        self.play(self.camera.frame.animate.scale(4.0))

        # 5. Animations
        self.play(Create(axes))
        self.play(Write(labels))
        self.play(Create(func), run_time=3)
        self.wait(2)