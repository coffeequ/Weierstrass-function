from manim import *
import numpy as np


class DrawFunctionExample(MovingCameraScene):
    def construct(self):
        x0 = 0.0
        base_x_window = 6.0
        max_x_stretch = 10.0
        max_terms = 260
        focus_y_terms = 160

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=6,
            tips=False,
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        a = 0.5
        b = 7
        holder_exponent = -np.log(a) / np.log(b)
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
        x_stretch = ValueTracker(1.0)

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

        def current_y_gain():
            return current_zoom() ** holder_exponent

        def current_x_stretch():
            return x_stretch.get_value()

        def focus_y():
            return weierstrass(x0, focus_y_terms)

        def center_point():
            return axes.c2p(x0, focus_y())

        def camera_scale():
            return self.camera.frame.get_width() / config.frame_width

        def make_fractal_graph():
            window = current_x_window()
            x_min = x0 - window / 2
            x_max = x0 + window / 2
            xs = np.linspace(x_min, x_max, current_samples())
            n_terms = current_terms()
            y_anchor = weierstrass(x0, n_terms)
            ys = weierstrass(xs, n_terms)
            display_xs = x0 + (xs - x0) * current_x_stretch()
            display_ys = focus_y() + (ys - y_anchor) * current_y_gain()

            graph = VMobject()
            graph.set_points_smoothly(
                [axes.c2p(x, y) for x, y in zip(display_xs, display_ys)]
            )
            graph.set_stroke(BLUE_C, width=2.4)
            return graph

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

        def freeze_graph():
            graph.clear_updaters()
            graph.become(make_fractal_graph())

        def resume_graph():
            graph.add_updater(lambda mob: mob.become(make_fractal_graph()))

        graph = always_redraw(make_fractal_graph)
        dot = always_redraw(
            lambda: Dot(center_point(), color=YELLOW, radius=0.04 * camera_scale())
        )
        focus_ring = always_redraw(make_focus_ring)
        focus_window = make_focus_window()

        formula = MathTex(r"W(x)=\sum_{n=0}^{\infty} a^n\cos(b^n\pi x)")
        title = Text(
            "\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u0412\u0435\u0439\u0435\u0440\u0448\u0442\u0440\u0430\u0441\u0441\u0430",
            font="Times New Roman",
        )

        self.camera.frame.scale(4)

        self.play(Write(title))
        self.play(ReplacementTransform(title, formula))
        self.wait(1)
        self.play(FadeOut(formula))

        self.camera.frame.scale(1.08)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(dot), Create(focus_ring), Create(focus_window), run_time=1)
        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.62),
            zoom.animate.set_value(2.2),
            x_stretch.animate.set_value(max_x_stretch),
            focus_window.animate.set_opacity(0.25),
            run_time=2.2,
            rate_func=rush_into,
        )

        freeze_graph()
        self.wait(1.5)
        resume_graph()

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.68),
            zoom.animate.set_value(4),
            run_time=1.8,
            rate_func=smooth,
        )

        freeze_graph()
        self.wait(1.5)
        resume_graph()

        self.play(
            FadeOut(focus_window),
            FadeOut(dot),
            FadeOut(focus_ring),
            axes.animate.set_opacity(0.35),
            labels.animate.set_opacity(0.35),
            run_time=1,
        )

        freeze_graph()
        self.wait(2)
