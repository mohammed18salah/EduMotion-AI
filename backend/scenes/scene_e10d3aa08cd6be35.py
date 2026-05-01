from manim import *

config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 8.0
config.frame_height = 14.22
config.background_color = "#111111"


# Set configuration for 9:16 aspect ratio
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16
config.frame_width = 9

class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Scene 1: Hook ---
        title = Text("Bubble Sort", color=TEAL_A, font_size=72).shift(UP * 2)
        question = Text("How to sort data?", color=WHITE, font_size=48).next_to(title, DOWN)
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(2.6)

        # --- Scene 2: Setup ---
        self.play(FadeOut(title), FadeOut(question), run_time=0.5)
        box1 = Square(side_length=1.5, color=TEAL_A).shift(LEFT * 1.6 + UP * 1)
        box2 = Square(side_length=1.5, color=TEAL_A).shift(RIGHT * 1.6 + UP * 1)
        num1 = Text("8", color=WHITE).move_to(box1.get_center())
        num2 = Text("3", color=WHITE).move_to(box2.get_center())
        group = VGroup(box1, box2, num1, num2)
        
        setup_text = Text("Unordered List", color=WHITE, font_size=40).shift(DOWN * 2)
        self.play(Create(group), Write(setup_text), run_time=0.8)
        self.wait(2.6)

        # --- Scene 3: Problem ---
        self.play(setup_text.animate.set_color(RED_B), run_time=0.5)
        problem_text = Text("Not in order!", color=RED_B, font_size=40).shift(DOWN * 3)
        rect_highlight = Rectangle(height=2, width=5, color=PINK).move_to(group.get_center())
        self.play(Create(rect_highlight), Write(problem_text), run_time=0.8)
        self.wait(2.6)

        # --- Scene 4: Explanation ---
        self.play(FadeOut(rect_highlight), FadeOut(problem_text), FadeOut(setup_text), run_time=0.5)
        expl_text = Text("Compare Neighbors", color=TEAL_A, font_size=40).shift(DOWN * 2)
        arrow1 = Arrow(start=UP*4, end=UP*2, color=PINK).next_to(box1, UP)
        arrow2 = Arrow(start=UP*4, end=UP*2, color=PINK).next_to(box2, UP)
        self.play(Write(expl_text), FadeIn(arrow1), FadeIn(arrow2), run_time=0.8)
        self.wait(2.6)

        # --- Scene 5: Solution ---
        self.play(FadeOut(arrow1), FadeOut(arrow2), run_time=0.5)
        swap_text = Text("Swap if needed", color=YELLOW, font_size=40).shift(DOWN * 3)
        self.play(Write(swap_text), run_time=0.5)
        self.play(
            box1.animate.move_to(box2.get_center()),
            num1.animate.move_to(box2.get_center()),
            box2.animate.move_to(box1.get_center()),
            num2.animate.move_to(box1.get_center()),
            run_time=0.8
        )
        self.wait(2.6)

        # --- Scene 6: Impact ---
        self.play(FadeOut(swap_text), FadeOut(expl_text), run_time=0.5)
        success_text = Text("Largest Bubbles Up", color=GREEN, font_size=40).shift(DOWN * 2)
        box1.set_color(GREEN)
        box2.set_color(GREEN)
        self.play(Write(success_text), run_time=0.8)
        self.wait(2.6)

        # --- Scene 7: Summary ---
        self.play(FadeOut(group), FadeOut(success_text), run_time=0.5)
        sum_title = Text("Recap", color=TEAL_A, font_size=50).shift(UP * 4)
        p1 = Text("1. Compare neighbors", font_size=36).shift(UP * 2)
        p2 = Text("2. Swap positions", font_size=36).next_to(p1, DOWN * 1.5)
        p3 = Text("3. Repeat until sorted", font_size=36).next_to(p2, DOWN * 1.5)
        
        self.play(Write(sum_title), run_time=0.5)
        self.play(FadeIn(p1), run_time=0.5)
        self.play(FadeIn(p2), run_time=0.5)
        self.play(FadeIn(p3), run_time=0.5)
        self.wait(2.6)