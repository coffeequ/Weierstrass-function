from manim import *
import numpy as np


class DrawFunctionExample(MovingCameraScene):
    def construct(self):
        x0 = 0.52
        base_x_window = 6.0
        max_zoom = 32.0
        max_terms = 260
        focus_y_terms = 160

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=6,
            tips=False,
        )
        labels = axes.get_axis_labels(x_label="x", y_label="W(x)")

        a = 0.5
        b = 7
        term_numbers = np.arange(max_terms)
        amplitudes = a ** term_numbers
        frequencies = (b ** term_numbers) * np.pi

        def weierstrass(x, n_terms):
            x_values = np.atleast_1d(x)
            values = (
                amplitudes[:n_terms, None]
                * np.cos(frequencies[:n_terms, None] * x_values)
            ).sum(axis=0)

            if np.isscalar(x):
                return float(values[0])
            return values

        zoom = ValueTracker(1.0)

        def current_zoom():
            return zoom.get_value()

        def current_x_window():
            return base_x_window / current_zoom()

        def current_terms():
            z = current_zoom()
            return int(np.clip(35 + 42 * np.log2(z + 1), 35, max_terms))

        def current_samples():
            z = current_zoom()
            return int(np.clip(900 * np.sqrt(z), 900, 6500))

        def center_point():
            return axes.c2p(x0, weierstrass(x0, focus_y_terms))

        def camera_scale():
            return self.camera.frame.get_width() / config.frame_width

        def make_fractal_graph():
            window = current_x_window()
            x_min = x0 - window / 2
            x_max = x0 + window / 2
            xs = np.linspace(x_min, x_max, current_samples())
            ys = weierstrass(xs, current_terms())

            graph = VMobject()
            graph.set_points_as_corners(
                [axes.c2p(x, y) for x, y in zip(xs, ys)]
            )
            graph.set_stroke(BLUE_C, width=2.4)
            return graph

        def make_zoom_info():
            scale = camera_scale()
            info = VGroup(
                Text("scale", font_size=24),
                DecimalNumber(current_zoom(), num_decimal_places=1, font_size=24),
                Text("x", font_size=24),
                Text("terms", font_size=24),
                Integer(current_terms(), font_size=24),
            )
            info.arrange(RIGHT, buff=0.1)
            info.scale(scale)
            info.move_to(
                self.camera.frame.get_corner(UR)
                + LEFT * (info.width / 2 + 0.22 * scale)
                + DOWN * (info.height / 2 + 0.22 * scale)
            )
            return info

        def make_focus_ring():
            scale = camera_scale()
            ring = Circle(radius=0.17 * scale, color=YELLOW, stroke_width=3)
            ring.move_to(center_point())
            return ring

        def make_focus_window():
            scale = camera_scale()
            window = Rectangle(
                width=2.2 * scale,
                height=1.2 * scale,
                color=YELLOW,
                stroke_width=2,
            )
            window.move_to(center_point())
            return window

        graph = always_redraw(make_fractal_graph)
        dot = always_redraw(
            lambda: Dot(center_point(), color=YELLOW, radius=0.04 * camera_scale())
        )
        focus_ring = always_redraw(make_focus_ring)
        focus_window = make_focus_window()
        zoom_info = always_redraw(make_zoom_info)

        formula = MathTex(r"W(x)=\sum_{n=0}^{\infty} a^n\cos(b^n\pi x)")
        title = Text("Weierstrass function")

        self.play(Write(title))
        self.play(ReplacementTransform(title, formula))
        self.wait(1)
        self.play(FadeOut(formula))

        self.camera.frame.scale(1.08)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(dot), Create(focus_ring), Create(focus_window), run_time=1)
        self.play(FadeIn(zoom_info), run_time=0.6)
        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.42),
            zoom.animate.set_value(4),
            focus_window.animate.set_opacity(0.25),
            run_time=4,
            rate_func=smooth,
        )

        self.play(
            FadeOut(focus_window),
            axes.animate.set_opacity(0.35),
            labels.animate.set_opacity(0.35),
            run_time=1,
        )

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.27),
            zoom.animate.set_value(max_zoom),
            run_time=9,
            rate_func=smooth,
        )

        self.wait(2)
