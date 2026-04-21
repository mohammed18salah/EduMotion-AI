from manim import *

config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 8.0
config.frame_height = 14.22
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        # Header section
        title = Text("Newton's 2nd Law", color=GOLD).scale(0.7).shift(UP * 3.5)
        formula = Text("F = m * a", color=YELLOW).scale(1.2).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=0.5)
        self.play(Write(formula), run_time=0.5)
        
        # Scenario 1: Light Mass
        force_label1 = Text("Force", color=RED).scale(0.4)
        arrow1 = Arrow(LEFT * 1.2, LEFT * 0.2, color=RED, buff=0)
        box1 = Square(side_length=0.6, color=BLUE, fill_opacity=0.7)
        mass_label1 = Text("m", color=WHITE).scale(0.5).move_to(box1.get_center())
        
        light_obj = VGroup(box1, mass_label1)
        group1 = VGroup(force_label1, arrow1, light_obj).arrange(RIGHT, buff=0.1).shift(UP * 0.8 + LEFT * 1.2)
        force_label1.shift(UP * 0.5 + RIGHT * 0.8) # Position label above arrow

        # Scenario 2: Heavy Mass
        force_label2 = Text("Force", color=RED).scale(0.4)
        arrow2 = Arrow(LEFT * 1.2, LEFT * 0.2, color=RED, buff=0)
        box2 = Square(side_length=1.2, color=GREEN, fill_opacity=0.7)
        mass_label2 = Text("M", color=WHITE).scale(0.7).move_to(box2.get_center())
        
        heavy_obj = VGroup(box2, mass_label2)
        group2 = VGroup(force_label2, arrow2, heavy_obj).arrange(RIGHT, buff=0.1).shift(DOWN * 1.5 + LEFT * 1.2)
        force_label2.shift(UP * 0.8 + RIGHT * 0.8)

        # Labels for the scenario
        lab1 = Text("Small Mass", color=BLUE).scale(0.4).next_to(group1, UP, buff=0.5)
        lab2 = Text("Large Mass", color=GREEN).scale(0.4).next_to(group2, UP, buff=0.2)

        self.play(
            Create(group1), Create(group2),
            Write(lab1), Write(lab2),
            run_time=0.8
        )
        self.wait(0.2)

        # Animation of acceleration
        # The light mass moves significantly further/faster
        self.play(
            group1.animate.shift(RIGHT * 2.5),
            group2.animate.shift(RIGHT * 0.7),
            run_time=1.5,
            rate_func=smooth
        )

        # Conclusion Text
        summary1 = Text("Same Force Applied", color=WHITE).scale(0.5).shift(DOWN * 3.2)
        summary2 = Text("More Mass = Less Acceleration", color=ORANGE).scale(0.5).next_to(summary1, DOWN, buff=0.2)
        
        self.play(Write(summary1), run_time=0.5)
        self.play(Write(summary2), run_time=0.5)
        
        # Final highlight
        box_rect = Rectangle(width=4.0, height=1.2, color=YELLOW).move_to(summary2.get_center())
        self.play(Create(box_rect), run_time=0.5)
        self.wait(1.0)

        # Quick fade out
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=0.5)

# Config for 9:16 aspect ratio is usually handled by CLI flags
# but the positioning above is optimized for a narrow vertical frame.
[Finished]