from manim import *

class WeierstrassFun(ThreeDScene):
    def construct(self):
        axes = Axes().animate
        self.add(axes)

        self.play()
        