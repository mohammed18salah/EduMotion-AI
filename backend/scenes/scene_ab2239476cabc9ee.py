from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        # Configuration
        self.camera.background_color = BLACK
        
        # --- SCENE 1: HOOK ---
        title = Text("MITREX TECHNOLOGY", color=TEAL_A).scale(1.2)
        question = Text("Invisible Solar Power?", color=WHITE).scale(0.8).next_to(title, DOWN)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(question, shift=UP), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(title), FadeOut(question), run_time=0.5)

        # --- SCENE 2: SETUP ---
        city_base = Line(LEFT*4, RIGHT*4, color=GRAY)
        building = Rectangle(height=3, width=1.5, color=WHITE).shift(UP*1.5)
        context_text = Text("Standard Buildings", color=WHITE).scale(0.6).to_edge(UP)
        
        self.play(Create(city_base), Create(building), run_time=0.8)
        self.play(Write(context_text), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(context_text), run_time=0.5)

        # --- SCENE 3: PROBLEM ---
        bulky_panel = Rectangle(height=0.8, width=1.2, color=RED_B).move_to(building.get_top()).shift(UP*0.5)
        cross_line1 = Line(bulky_panel.get_corner(UL), bulky_panel.get_corner(DR), color=RED_B)
        cross_line2 = Line(bulky_panel.get_corner(UR), bulky_panel.get_corner(DL), color=RED_B)
        problem_text = Text("Bulky & Ugly", color=RED_B).scale(0.7).next_to(bulky_panel, RIGHT)
        
        self.play(Create(bulky_panel), run_time=0.8)
        self.play(Create(cross_line1), Create(cross_line2), Write(problem_text), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(bulky_panel), FadeOut(cross_line1), FadeOut(cross_line2), FadeOut(problem_text), run_time=0.5)

        # --- SCENE 4: EXPLANATION ---
        layer1 = Rectangle(height=2, width=3, color=WHITE).shift(LEFT*1)
        layer2 = Rectangle(height=2, width=0.2, color=PINK).next_to(layer1, RIGHT, buff=0.1)
        explanation_label = Text("Solar Cladding", color=PINK).scale(0.6).to_edge(UP)
        
        self.play(Create(layer1), run_time=0.8)
        self.play(Create(layer2), Write(explanation_label), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(explanation_label), run_time=0.5)

        # --- SCENE 5: SOLUTION ---
        ray1 = Arrow(LEFT*4, LEFT*1.2, color=YELLOW, buff=0)
        ray2 = ray1.copy().shift(DOWN*0.5)
        cell_glow = Rectangle(height=2.2, width=0.4, color=TEAL_A).move_to(layer2).set_fill(TEAL_A, opacity=0.5)
        solution_text = Text("Light Passes Through", color=WHITE).scale(0.6).to_edge(DOWN)
        
        self.play(GrowArrow(ray1), GrowArrow(ray2), run_time=0.8)
        self.play(FadeIn(cell_glow), Write(solution_text), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(ray1), FadeOut(ray2), FadeOut(cell_glow), FadeOut(layer1), FadeOut(layer2), FadeOut(solution_text), run_time=0.5)

        # --- SCENE 6: IMPACT ---
        green_building = Rectangle(height=4, width=2, color=GREEN).set_fill(GREEN, opacity=0.2)
        impact_text = Text("Energy Walls", color=GREEN).scale(0.8).next_to(green_building, UP)
        energy_dots = VGroup(*[Dot(color=YELLOW).move_to(green_building.get_center() + np.random.uniform(-0.5, 0.5, 3)) for _ in range(5)])
        
        self.play(Create(green_building), Write(impact_text), run_time=0.8)
        self.play(FadeIn(energy_dots), run_time=0.8)
        self.wait(2.6)
        self.play(FadeOut(green_building), FadeOut(impact_text), FadeOut(energy_dots), run_time=0.5)

        # --- SCENE 7: SUMMARY ---
        b1 = Text("1. Aesthetic Design", color=WHITE).scale(0.6).shift(UP*1)
        b2 = Text("2. High Efficiency", color=WHITE).scale(0.6)
        b3 = Text("3. Fully Sustainable", color=WHITE).scale(0.6).shift(DOWN*1)
        
        self.play(Write(b1), run_time=0.5)
        self.play(Write(b2), run_time=0.5)
        self.play(Write(b3), run_time=0.5)
        self.wait(2.6)