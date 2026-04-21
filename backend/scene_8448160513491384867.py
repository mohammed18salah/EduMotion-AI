from manim import *

class MainScene(Scene):
    def construct(self):
        # Title and Formula
        title = Text("قانون نيوتن الثاني", font_size=36).to_edge(UP)
        formula = Text("F = m * a", font_size=44).next_to(title, DOWN)
        
        self.play(Write(title), Write(formula), run_time=1.5)
        
        # Physical objects
        ground = Line(LEFT * 4 + DOWN * 1.5, RIGHT * 4 + DOWN * 1.5)
        mass_box = Square(side_length=1.2, color=BLUE).shift(LEFT * 2.5 + DOWN * 0.9)
        mass_label = Text("m", font_size=28).move_to(mass_box)
        mass_group = VGroup(mass_box, mass_label)
        
        force_arrow = Arrow(start=LEFT * 4.5 + DOWN * 0.9, end=LEFT * 3.1 + DOWN * 0.9, color=RED)
        force_label = Text("F", color=RED, font_size=28).next_to(force_arrow, UP)
        
        self.play(Create(ground), Create(mass_group), Create(force_arrow), Write(force_label), run_time=1.5)
        
        # Acceleration Visual
        accel_arrow = Arrow(start=LEFT * 1.8 + DOWN * 0.4, end=RIGHT * 0.5 + DOWN * 0.4, color=YELLOW)
        accel_label = Text("التسارع a", color=YELLOW, font_size=28).next_to(accel_arrow, UP)
        
        # Movement Animation (Acceleration)
        self.play(
            mass_group.animate.shift(RIGHT * 4.5),
            force_arrow.animate.shift(RIGHT * 4.5),
            force_label.animate.shift(RIGHT * 4.5),
            Create(accel_arrow),
            Write(accel_label),
            run_time=3,
            rate_func=rate_functions.ease_in_quad
        )
        
        self.wait(1)