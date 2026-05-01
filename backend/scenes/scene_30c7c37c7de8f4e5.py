from manim import *

config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 8.0
config.frame_height = 14.22
config.background_color = "#111111"


# SETTING ASPECT RATIO TO 9:16
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

class MainScene(Scene):
    def construct(self):
        # REQUIRED BACKGROUND COLOR
        self.camera.background_color = BLACK

        # --- SCENE 1: HOOK ---
        title = Text("PYTHAGORAS", color=TEAL_A, font_size=48).shift(UP * 2)
        hook = Text("Missing a side?", color=WHITE, font_size=36).next_to(title, DOWN)
        s1_group = VGroup(title, hook)
        
        self.play(Write(title, run_time=0.8))
        self.play(FadeIn(hook, shift=UP, run_time=0.7))
        self.wait(2.6)
        self.play(FadeOut(s1_group, run_time=0.5))

        # --- SCENE 2: SETUP ---
        wall = Line(LEFT * 1.5 + DOWN * 3, LEFT * 1.5 + UP * 2, color=WHITE)
        ground = Line(LEFT * 1.5 + DOWN * 3, RIGHT * 1.5 + DOWN * 3, color=WHITE)
        ladder = Line(LEFT * 1.5 + UP * 2, RIGHT * 1.5 + DOWN * 3, color=PINK)
        
        setup_group = VGroup(wall, ground, ladder)
        
        self.play(Create(wall, run_time=0.8), Create(ground, run_time=0.8))
        self.play(Create(ladder, run_time=0.8))
        self.wait(2.6)

        # --- SCENE 3: PROBLEM ---
        label_4 = Text("4m", color=WHITE, font_size=32).next_to(wall, LEFT)
        label_3 = Text("3m", color=WHITE, font_size=32).next_to(ground, DOWN)
        label_q = Text("?", color=RED_B, font_size=48).move_to(ladder.get_center() + UP * 0.5 + RIGHT * 0.5)
        
        prob_group = VGroup(label_4, label_3, label_q)
        
        self.play(Write(label_4, run_time=0.6), Write(label_3, run_time=0.6))
        self.play(Indicate(label_q, color=RED_B, run_time=0.8))
        self.wait(2.6)
        self.play(FadeOut(setup_group), FadeOut(prob_group), run_time=0.5)

        # --- SCENE 4: EXPLANATION ---
        formula = Text("a^2 + b^2 = c^2", color=TEAL_A, font_size=44)
        theory_text = Text("The Secret Formula", color=WHITE, font_size=30).next_to(formula, UP * 2)
        
        self.play(Write(theory_text, run_time=0.8))
        self.play(FadeIn(formula, scale=1.5, run_time=0.8))
        self.wait(2.6)
        self.play(FadeOut(theory_text), run_time=0.5)

        # --- SCENE 5: SOLUTION ---
        step1 = Text("3^2 + 4^2 = 25", color=WHITE, font_size=36).move_to(UP)
        step2 = Text("sqrt(25) = 5", color=GREEN, font_size=48).next_to(step1, DOWN * 2)
        
        self.play(Transform(formula, step1, run_time=0.8))
        self.play(Write(step2, run_time=0.8))
        self.wait(2.6)
        self.play(FadeOut(formula), FadeOut(step1), FadeOut(step2), run_time=0.5)

        # --- SCENE 6: IMPACT ---
        impact_text = Text("ARCHITECTURE", color=TEAL_A, font_size=40).shift(UP * 2)
        house_base = Square(side_length=2, color=WHITE).shift(DOWN)
        roof = Polygon([-1.2, 0, 0], [1.2, 0, 0], [0, 1.2, 0], color=PINK).next_to(house_base, UP, buff=0)
        
        impact_group = VGroup(impact_text, house_base, roof)
        
        self.play(Write(impact_text, run_time=0.7))
        self.play(Create(house_base, run_time=0.5), Create(roof, run_time=0.5))
        self.wait(2.6)
        self.play(FadeOut(impact_group, run_time=0.5))

        # --- SCENE 7: SUMMARY ---
        sum_title = Text("SUMMARY", color=TEAL_A, font_size=40).shift(UP * 3)
        b1 = Text("1. Right Triangles", color=WHITE, font_size=32)
        b2 = Text("2. Square Both Sides", color=WHITE, font_size=32)
        b3 = Text("3. Find Square Root", color=GREEN, font_size=32)
        
        bullets = VGroup(b1, b2, b3).arrange(DOWN, buff=0.8, aligned_edge=LEFT).shift(DOWN * 0.5)
        
        self.play(Write(sum_title, run_time=0.8))
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT) for b in bullets], lag_ratio=0.4, run_time=1.0))
        self.wait(2.6)