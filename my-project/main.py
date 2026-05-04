from manim import *
import numpy as np

class DrawFunctionExample(MovingCameraScene):
    def construct(self):
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
        )

        def weierstrass(x, a=0.5, b=7, n_terms=80):
            return sum(
                a**n * np.cos((b**n) * np.pi * x)
                for n in range(n_terms)
            )

        func = axes.plot(
            lambda x: weierstrass(x),
            color=BLUE,
            use_smoothing=False
        )

        labels = axes.get_axis_labels(x_label="x", y_label="W(x)")
        formula = MathTex(r"W(x)=\sum a^n \cos(b^n \pi x)")
        text = Text("Weierstrass function")

        self.play(self.camera.frame.animate.scale(4))

        self.play(Write(text))
        self.play(ReplacementTransform(text, formula))
        self.wait(2)
        self.play(FadeOut(formula))

        self.play(Create(axes))
        self.play(Write(labels))
        self.play(Create(func), run_time=1.5)
        self.wait()

        # --- ВЫБОР ТОЧКИ ДЛЯ ЗУМА ---
        x0 = 0.5
        y0 = weierstrass(x0)
        zoom_point = axes.c2p(x0, y0)

        square = Square(side_length=0.8, color=RED)
        
        square.move_to(zoom_point)

        self.play(FadeIn(square))

        # --- ПРИБЛИЖЕНИЕ ---
        self.play(
            self.camera.frame.animate
            .move_to(zoom_point)
            .scale(0.4),
            run_time=3
        )

        self.wait()

        # --- УВЕЛИЧИВАЕМ ДЕТАЛИЗАЦИЮ ---
        zoom_func = axes.plot(
            lambda x: weierstrass(x, n_terms=120),
            color=YELLOW,
            use_smoothing=False
        )

        self.play(Transform(func, zoom_func), run_time=2)
        self.wait(2)

        # --- ВТОРОЙ ЗУМ (чтобы стало очевидно) ---
        x1 = 0.52
        y1 = weierstrass(x1, n_terms=120)
        zoom_point2 = axes.c2p(x1, y1)

        self.play(
            self.camera.frame.animate
            .move_to(zoom_point2)
            .scale(0.4),
            run_time=3
        )

        zoom_func2 = axes.plot(
            lambda x: weierstrass(x, n_terms=160),
            color=GREEN,
            use_smoothing=False
        )

        self.play(Transform(func, zoom_func2), run_time=2)

        self.wait(2)