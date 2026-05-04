from manim import *


class CreateCircle(Scene):
    def construct(self):

        def weierstrass(x, a=0.5, b=7, n_terms=80):
            return sum(
                a**n * np.cos((b**n) * np.pi * x)
                for n in range(n_terms)
            )

        # --- ИСХОДНЫЕ ОСИ ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
        )

        func = axes.plot(lambda x: weierstrass(x), color=BLUE, use_smoothing=False)

        self.play(Create(axes), Create(func))
        self.wait()

        # --- ОБЛАСТЬ ДЛЯ ЗУМА ---
        x0 = 0.5
        zoom_width = 0.5

        square = Square(side_length=0.8, color=RED)
        square.move_to(axes.c2p(x0, weierstrass(x0)))
        self.play(FadeIn(square))

        # --- ПРИБЛИЖЕНИЕ К КВАДРАТУ ---
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(square),
            run_time=2
        )

        self.wait()

        # --- ЗАТЕМНЕНИЕ ---
        fade_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0
        )
        fade_rect.move_to(self.camera.frame.get_center())

        self.play(fade_rect.animate.set_opacity(1), run_time=1)

        # --- НОВЫЕ ОСИ (ЗУМ ВНУТРЬ) ---
        new_axes = Axes(
            x_range=[x0 - zoom_width, x0 + zoom_width, 0.1],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=5,
        )

        new_func = new_axes.plot(
            lambda x: weierstrass(x, n_terms=120),
            color=YELLOW,
            use_smoothing=False
        )

        # Удаляем старое
        self.remove(axes, func, square)

        # Сбрасываем камеру
        self.camera.frame.move_to(ORIGIN).scale(1)

        # Добавляем новое
        self.add(new_axes, new_func)

        # --- УБИРАЕМ ЗАТЕМНЕНИЕ ---
        self.play(fade_rect.animate.set_opacity(0), run_time=1)

        self.wait(2)
