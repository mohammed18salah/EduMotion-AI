from manim import *

class MainScene(Scene):
    def construct(self):
        # Set background to a darker color for contrast
        self.camera.background_color = DARK_GRAY

        # Title
        title = Text("Newton's Second Law", color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Formula F = m * a
        formula_text = Text("F = m * a", color=YELLOW)
        formula_text.next_to(title, DOWN, buff=0.8)
        self.play(Write(formula_text))
        self.wait(1)

        # Define common objects
        object_mass = Square(side_length=1.5, color=BLUE_D, fill_opacity=0.8)
        object_mass_label = Text("Mass (m)", color=BLUE_A, font_size=30).next_to(object_mass, DOWN)
        
        # Position for our demonstration
        demo_center = ORIGIN + DOWN * 1.5

        # --- Illustrate F (Force) ---
        force_arrow_small = Arrow(start=LEFT * 3, end=LEFT * 0.5, color=RED_D, buff=0.1)
        force_label = Text("Force (F)", color=RED_A, font_size=30).next_to(force_arrow_small, LEFT)

        self.play(
            FadeOut(formula_text),
            title.animate.to_edge(UP * 0.5)
        )

        # Initial setup for Force, Mass, Acceleration
        initial_group = VGroup(object_mass, object_mass_label).move_to(demo_center + RIGHT * 1.5)
        
        self.play(FadeIn(initial_group))
        self.wait(0.5)

        self.play(GrowArrow(force_arrow_small), Write(force_label))
        self.wait(0.5)

        acceleration_label = Text("Acceleration (a)", color=GREEN_A, font_size=30).next_to(object_mass, UP)
        
        self.play(
            initial_group.animate.shift(RIGHT * 3),
            Write(acceleration_label),
            run_time=1.5, rate_func=linear
        )
        self.wait(1)

        # Remove elements for the next part
        self.play(
            FadeOut(initial_group),
            FadeOut(force_arrow_small),
            FadeOut(force_label),
            FadeOut(acceleration_label)
        )
        self.wait(0.5)

        # --- Varying Force, Constant Mass ---
        force_title = Text("More Force (F)", color=RED).to_edge(UP).shift(DOWN*0.5)
        acceleration_effect_title = Text("More Acceleration (a)", color=GREEN).next_to(force_title, DOWN)
        
        self.play(Transform(title, force_title), Write(acceleration_effect_title))
        self.wait(0.5)

        # Constant Mass (medium size)
        mass_medium = Square(side_length=1.5, color=BLUE_D, fill_opacity=0.8).move_to(demo_center + RIGHT)
        self.play(FadeIn(mass_medium))
        self.wait(0.5)

        # Small Force, Slow Acceleration
        arrow_weak = Arrow(start=LEFT * 3.5, end=mass_medium.get_left(), color=RED_A)
        self.play(GrowArrow(arrow_weak))
        self.play(mass_medium.animate.shift(RIGHT * 3), run_time=1, rate_func=linear)
        self.play(FadeOut(mass_medium), FadeOut(arrow_weak))
        self.wait(0.5)

        # Strong Force, Fast Acceleration
        mass_medium = Square(side_length=1.5, color=BLUE_D, fill_opacity=0.8).move_to(demo_center + RIGHT) # Reset object
        arrow_strong = Arrow(start=LEFT * 3.5, end=mass_medium.get_left(), color=RED_E, stroke_width=8)
        self.play(FadeIn(mass_medium), GrowArrow(arrow_strong))
        self.play(mass_medium.animate.shift(RIGHT * 3), run_time=0.5, rate_func=linear) # Faster
        self.play(FadeOut(mass_medium), FadeOut(arrow_strong))
        self.wait(0.5)

        self.play(FadeOut(acceleration_effect_title), Transform(title, Text("Newton's Second Law", color=WHITE).to_edge(UP * 0.5)))
        self.wait(0.5)

        # --- Varying Mass, Constant Force ---
        mass_title = Text("More Mass (m)", color=BLUE).to_edge(UP).shift(DOWN*0.5)
        acceleration_decrease_title = Text("Less Acceleration (a)", color=GREEN).next_to(mass_title, DOWN)
        
        self.play(Transform(title, mass_title), Write(acceleration_decrease_title))
        self.wait(0.5)

        # Constant Force (medium arrow)
        arrow_constant = Arrow(start=LEFT * 3.5, end=LEFT * 0.5, color=RED_D)

        # Small Mass, Fast Acceleration
        mass_small = Square(side_length=1, color=BLUE_A, fill_opacity=0.8).move_to(demo_center + RIGHT * 1.5)
        arrow_constant_small = arrow_constant.copy().set_x(mass_small.get_left()[0]) # Adjust arrow position dynamically
        self.play(GrowArrow(arrow_constant_small), FadeIn(mass_small))
        self.play(mass_small.animate.shift(RIGHT * 3), run_time=0.7, rate_func=linear) # Fast
        self.play(FadeOut(mass_small), FadeOut(arrow_constant_small))
        self.wait(0.5)

        # Large Mass, Slow Acceleration
        mass_large = Square(side_length=2, color=BLUE_E, fill_opacity=0.8).move_to(demo_center + RIGHT * 1.5)
        arrow_constant_large = arrow_constant.copy().set_x(mass_large.get_left()[0]) # Adjust arrow position dynamically
        self.play(GrowArrow(arrow_constant_large), FadeIn(mass_large))
        self.play(mass_large.animate.shift(RIGHT * 3), run_time=1.5, rate_func=linear) # Slow
        self.play(FadeOut(mass_large), FadeOut(arrow_constant_large))
        self.wait(0.5)

        self.play(FadeOut(acceleration_decrease_title))
        self.wait(0.5)

        # --- Final Summary ---
        final_formula = Text("F = m * a", color=YELLOW)
        final_formula.next_to(title, DOWN, buff=1)
        
        self.play(Transform(title, Text("Newton's Second Law", color=WHITE).to_edge(UP)), Write(final_formula))

        summary_text1 = Text("More Force = More Acceleration", color=WHITE, font_size=30).next_to(final_formula, DOWN, buff=0.5)
        summary_text2 = Text("More Mass = Less Acceleration", color=WHITE, font_size=30).next_to(summary_text1, DOWN, buff=0.2)

        self.play(Write(summary_text1))
        self.play(Write(summary_text2))
        self.wait(2)

        self.play(FadeOut(VGroup(title, final_formula, summary_text1, summary_text2)))
        self.wait(0.5)