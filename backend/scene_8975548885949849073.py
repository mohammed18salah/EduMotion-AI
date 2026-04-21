from manim import *

class MainScene(Scene):
    def construct(self):
        title = Text("قانون نيوتن الثاني", font_size=40).to_edge(UP)
        equation = MathTex("F = m a", font_size=80).shift(UP * 0.5)
        description = Text("القوة = الكتلة × التسارع", font_size=24).next_to(equation, DOWN)
        
        box = Square(side_length=1, color=BLUE, fill_opacity=0.5).shift(LEFT * 3 + DOWN * 2)
        force_arrow = Arrow(start=LEFT * 4.5 + DOWN * 2, end=LEFT * 3.1 + DOWN * 2, color=RED, buff=0)
        force_text = MathTex("F", color=RED).next_to(force_arrow, UP, buff=0.1)
        
        self.play(
            Write(title), 
            Write(equation), 
            FadeIn(description), 
            run_time=2
        )
        
        self.play(
            Create(box),
            GrowArrow(force_arrow),
            Write(force_text),
            run_time=1.5
        )
        
        physics_group = VGroup(box, force_arrow, force_text)
        
        self.play(
            physics_group.animate.shift(RIGHT * 6),
            rate_func=rate_functions.ease_in_quad,
            run_time=3.5
        )
        
        self.wait(1)