from manim import *

config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 8.0
config.frame_height = 14.22
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        title = Text("Newtons Second Law", font_size=40)
        formula = Text("F = m * a", font_size=60, color=YELLOW)
        
        box = Square(side_length=2, color=BLUE)
        box.set_fill(BLUE_E, opacity=0.5)
        
        force_arrow = Arrow(start=LEFT*3, end=LEFT*1, color=RED)
        
        self.play(Write(title), run_time=0.5)
        self.play(FadeOut(title), run_time=0.5)
        
        self.play(Create(box), run_time=0.5)
        self.play(GrowArrow(force_arrow), run_time=0.5)
        
        group = VGroup(box, force_arrow)
        self.play(group.animate.shift(RIGHT*4), run_time=1.0)
        
        label = Text("Force causes acceleration", font_size=30, color=GREEN)
        label.to_edge(UP)
        self.play(Write(label), run_time=0.5)
        
        self.play(Write(formula), run_time=0.5)
        self.play(FadeOut(formula), run_time=0.5)
        
        small_box = Square(side_length=1, color=ORANGE)
        small_box.set_fill(ORANGE, opacity=0.5)
        self.play(ReplacementTransform(box, small_box), run_time=0.5)
        
        fast_arrow = Arrow(start=LEFT*3, end=LEFT*0.5, color=RED)
        self.play(ReplacementTransform(force_arrow, fast_arrow), run_time=0.5)
        self.play(small_box.animate.shift(RIGHT*6), run_time=0.5)
        
        final_text = Text("Less mass = More acceleration", font_size=30, color=GOLD)
        self.play(Write(final_text), run_time=0.5)
        self.wait(1)