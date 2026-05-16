from manim import *
import numpy as np

config.frame_rate = 30


class DrawFunctionExample(MovingCameraScene):
    def construct(self):
        x0 = 0.52
        base_x_window = 6.0
        max_x_stretch = 7.0
        second_x_stretch = 11.0
        max_terms = 90
        graph_samples = 3200
        smoothing_kernel = np.array(
            [1, 2, 4, 7, 11, 15, 18, 15, 11, 7, 4, 2, 1],
            dtype=float,
        )
        smoothing_kernel /= smoothing_kernel.sum()
        focus_y_terms = max_terms

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=6,
            tips=False,
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        a = 0.5
        b = 13
        condition_bound = 1 + 3 * np.pi / 2
        holder_exponent = -np.log(a) / np.log(b)
        term_numbers = np.arange(max_terms)
        amplitudes = a ** term_numbers
        frequencies = (float(b) ** term_numbers) * np.pi

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

        def current_terms():
            return max_terms

        def current_samples():
            return graph_samples

        def current_y_gain():
            return current_zoom() ** holder_exponent

        def current_x_stretch():
            return x_stretch.get_value()

        def focus_blend():
            return extra_smooth(extra_smooth((current_zoom() - 1) / 3))

        def focus_y():
            return weierstrass(x0, focus_y_terms)

        def extra_smooth(t):
            t = np.clip(t, 0, 1)
            return t * t * t * (t * (t * 6 - 15) + 10)

        def center_point():
            return axes.c2p(x0, focus_y())

        def camera_scale():
            return self.camera.frame.get_width() / config.frame_width

        def smooth_values(values):
            padding = len(smoothing_kernel) // 2
            padded = np.pad(values, padding, mode="edge")
            return np.convolve(padded, smoothing_kernel, mode="valid")

        def make_fractal_graph():
            blend = focus_blend()
            x_min = -base_x_window / 2
            x_max = base_x_window / 2
            xs = np.linspace(x_min, x_max, current_samples())
            n_terms = current_terms()

            active_x_stretch = np.exp(blend * np.log(current_x_stretch()))
            active_y_gain = np.exp(blend * np.log(current_y_gain()))
            source_xs = x0 + (xs - x0) / active_x_stretch
            source_y_anchor = weierstrass(x0, n_terms)
            ys = weierstrass(source_xs, n_terms)

            display_xs = xs
            display_ys = focus_y() + (ys - source_y_anchor) * active_y_gain
            display_ys = smooth_values(display_ys)

            graph = VMobject()
            graph.set_points_smoothly(
                [axes.c2p(x, y) for x, y in zip(display_xs, display_ys)]
            )
            graph.set_stroke(BLUE_C, width=2.1)
            return graph

        def make_focus_ring():
            scale = camera_scale()
            ring = Circle(radius=0.17 * scale, color=YELLOW, stroke_width=3)
            ring.move_to(center_point())
            return ring

        def make_focus_window():
            scale = camera_scale()
            window = Circle(
                radius=0.85 * scale,
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
        parameters = MathTex(
            rf"a={a:g},\quad b={b},\quad ab={a * b:g}>1+\frac{{3\pi}}{{2}}\approx{condition_bound:.2f}",
            font_size=34,
        )
        title = Text(
            "\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u0412\u0435\u0439\u0435\u0440\u0448\u0442\u0440\u0430\u0441\u0441\u0430",
            font="Times New Roman",
        )
        properties_title = Text(
            "Основные свойства",
            font="Times New Roman",
            font_size=46,
        )
        property_texts = [
            "Непрерывна в каждой точке числовой прямой,\n"
            "но график похож на бесконечный зубчатый зигзаг.",
            "Не имеет конечной производной ни в одной точке.",
            "Имеет фрактальную структуру: при увеличении масштаба\n"
            "мелкие детали повторяют характер всего графика.",
            "Задается рядом при 0 < a < 1, нечетном натуральном b\n"
            "и условии ab > 1 + 3π/2.",
        ]
        properties = VGroup(
            *[
                Text(f"- {text}", font="Times New Roman", font_size=32)
                for text in property_texts
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        properties.scale_to_fit_width(config.frame_width * 1.6)

        self.camera.frame.scale(3)

        self.play(Write(title))
        self.play(ReplacementTransform(title, formula))
        self.wait(1)
        self.play(formula.animate.scale(0.72).to_edge(UP))
        parameters.next_to(formula, DOWN, buff=0.3)
        properties_title.next_to(parameters, DOWN, buff=0.35)
        properties.next_to(properties_title, DOWN, buff=0.35)
        VGroup(parameters, properties_title, properties).move_to(
            [
                formula.get_center()[0],
                VGroup(parameters, properties_title, properties).get_center()[1],
                0,
            ]
        )
        self.play(FadeIn(parameters, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(properties_title, shift=DOWN * 0.2), run_time=0.8)
        for property_line in properties:
            self.play(FadeIn(property_line, shift=RIGHT * 0.25), run_time=0.8)
            self.wait(2.6)
        self.wait(1)
        self.play(FadeOut(VGroup(formula, parameters, properties_title, properties)))

        self.camera.frame.scale(1.08)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(dot), Create(focus_window), run_time=1)
        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.62),
            zoom.animate.set_value(2.2),
            x_stretch.animate.set_value(max_x_stretch),
            focus_window.animate.set_opacity(0.25),
            run_time=6,
            rate_func=extra_smooth,
        )

        freeze_graph()
        self.wait(1.5)
        resume_graph()

        self.play(
            self.camera.frame.animate.move_to(center_point()).scale(0.68),
            zoom.animate.set_value(4),
            x_stretch.animate.set_value(second_x_stretch),
            run_time=5.5,
            rate_func=extra_smooth,
        )

        freeze_graph()
        self.wait(1.5)
        resume_graph()

        self.play(
            FadeOut(focus_window),
            FadeOut(dot),
            axes.animate.set_opacity(0.35),
            labels.animate.set_opacity(0.35),
            run_time=1,
        )

        freeze_graph()
        self.wait(2)
