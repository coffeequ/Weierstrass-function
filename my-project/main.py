from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()
        
        square.set_fill(RED, opacity=1)
        
        circle.set_fill(PINK, opacity=1)  # set the color and transparency
        
        self.play(Create(square), Create(circle))