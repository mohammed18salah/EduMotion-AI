from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Scene 1: INTRO_TRIANGLE ---
        title = Text("نظرية فيثاغورس", font="Arial", font_size=54, color=TEAL_A)
        subtitle = Text("للمثلثات القائمة", font="Arial", font_size=36, color=WHITE).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=1.5)
        self.wait(1.0)

        # Create vertices for a right-angled triangle
        p1 = LEFT * 3 + DOWN * 2
        p2 = RIGHT * 3 + DOWN * 2
        p3 = LEFT * 3 + UP * 2.5
        
        triangle = Polygon(p1, p2, p3, color=PINK, fill_opacity=0.3)
        
        self.play(FadeOut(VGroup(title, subtitle)), run_time=0.8)
        self.play(Create(triangle), run_time=1.2)
        self.wait(1.0) # Scene 1 ends (1.5+0.8+1.2+1.0 = 4.5 sec)
        
        self.play(FadeOut(triangle), run_time=0.8)

        # --- Scene 2: RIGHT_ANGLE_HIGHLIGHT ---
        # Recreate triangle for a clean animation
        triangle = Polygon(p1, p2, p3, color=PINK, fill_opacity=0.3)
        self.add(triangle)

        right_angle_mark = Square(side_length=0.4, color=YELLOW_A, fill_opacity=0).move_to(p1, UR).shift(0.05 * (DOWN + RIGHT))
        self.play(Create(right_angle_mark), run_time=0.8)
        right_angle_text = Text("الزاوية القائمة (90°)", font="Arial", font_size=30, color=YELLOW_A).next_to(right_angle_mark, UP + RIGHT, buff=0.3)
        self.play(Write(right_angle_text), run_time=0.8)
        self.wait(3.0) # Scene 2 ends (0.8+0.8+3.0 = 4.6 sec)

        self.play(FadeOut(VGroup(right_angle_mark, right_angle_text)), run_time=0.8)

        # --- Scene 3: LABEL_SIDES ---
        # Legs
        side_a = Line(p1, p3, color=TEAL_A)
        label_a = Text("الضلع (أ)", font="Arial", font_size=30, color=TEAL_A).next_to(side_a, LEFT, buff=0.2)
        
        side_b = Line(p1, p2, color=TEAL_A)
        label_b = Text("الضلع (ب)", font="Arial", font_size=30, color=TEAL_A).next_to(side_b, DOWN, buff=0.2)
        
        self.play(Create(VGroup(side_a, side_b)), run_time=0.8)
        self.play(Write(VGroup(label_a, label_b)), run_time=0.8)
        self.wait(1.0)

        # Hypotenuse
        hypotenuse_line = Line(p2, p3, color=GREEN)
        label_c = Text("الوتر (ج)", font="Arial", font_size=30, color=GREEN).next_to(hypotenuse_line, RIGHT + UP, buff=0.2)
        self.play(Create(hypotenuse_line), run_time=0.8)
        self.play(Write(label_c), run_time=0.8)
        self.wait(1.8) # Scene 3 ends (0.8+0.8+1.0+0.8+0.8+1.8 = 6.0 sec)

        self.play(FadeOut(VGroup(triangle, side_a, side_b, hypotenuse_line, label_a, label_b, label_c)), run_time=0.8)

        # --- Scene 4: PYTHAGOREAN_THEOREM ---
        theorem_text = Text("نظرية فيثاغورس", font="Arial", font_size=48, color=TEAL_A)
        self.play(Write(theorem_text), run_time=1.0)
        self.wait(0.5)

        formula = Text("أ² + ب² = ج²", font="Arial", font_size=60, color=WHITE).next_to(theorem_text, DOWN, buff=1.0)
        self.play(Write(formula), run_time=1.5)
        
        square_a = Square(side_length=1.5, color=TEAL_A, fill_opacity=0.3).shift(LEFT * 3 + UP * 1)
        square_b = Square(side_length=2.0, color=TEAL_A, fill_opacity=0.3).shift(LEFT * 0 + DOWN * 1)
        square_c = Square(side_length=2.5, color=GREEN, fill_opacity=0.3).shift(RIGHT * 3 + UP * 0)

        self.play(FadeOut(theorem_text), formula.animate.move_to(UP*2.5), run_time=0.8)
        
        self.play(Create(square_a), run_time=0.6)
        self.play(Create(square_b), run_time=0.6)
        self.play(Create(square_c), run_time=0.6)

        plus_sign = Text("+", font="Arial", font_size=60, color=WHITE).next_to(square_a, RIGHT, buff=0.5)
        equals_sign = Text("=", font="Arial", font_size=60, color=WHITE).next_to(square_b, RIGHT, buff=0.5)

        self.play(Write(plus_sign), run_time=0.5)
        self.play(Write(equals_sign), run_time=0.5)

        self.wait(2.0) # Scene 4 ends (1.0+0.5+1.5+0.8+0.6+0.6+0.6+0.5+0.5+2.0 = 8.6 sec)
        
        self.play(FadeOut(VGroup(formula, square_a, square_b, square_c, plus_sign, equals_sign)), run_time=0.8)

        # --- Scene 5: NUMERICAL_EXAMPLE ---
        # Recreate triangle, sides, and angle mark for clarity
        p1 = LEFT * 3 + DOWN * 2
        p2 = RIGHT * 1 + DOWN * 2
        p3 = LEFT * 3 + UP * 1.5

        example_triangle = Polygon(p1, p2, p3, color=PINK, fill_opacity=0.3)
        self.add(example_triangle)
        
        right_angle_mark = Square(side_length=0.4, color=YELLOW_A, fill_opacity=0).move_to(p1, UR).shift(0.05 * (DOWN + RIGHT))
        self.add(right_angle_mark)

        side_a_line = Line(p1, p3, color=TEAL_A)
        val_a = Text("3", font="Arial", font_size=36, color=TEAL_A).next_to(side_a_line, LEFT, buff=0.2)
        
        side_b_line = Line(p1, p2, color=TEAL_A)
        val_b = Text("4", font="Arial", font_size=36, color=TEAL_A).next_to(side_b_line, DOWN, buff=0.2)
        
        hypotenuse_line = Line(p2, p3, color=GREEN)
        val_c = Text("؟", font="Arial", font_size=36, color=GREEN).next_to(hypotenuse_line, RIGHT + UP, buff=0.2)

        self.play(Create(VGroup(side_a_line, side_b_line, hypotenuse_line)), run_time=0.8)
        self.play(Write(VGroup(val_a, val_b)), run_time=0.8)
        self.play(Write(val_c), run_time=0.8)
        self.wait(1.0)
        
        result_text = Text("3² + 4² = ؟²", font="Arial", font_size=40, color=WHITE).shift(UP * 2.5)
        self.play(Write(result_text), run_time=0.8)
        
        calculated_c = Text("5", font="Arial", font_size=36, color=GREEN).next_to(hypotenuse_line, RIGHT + UP, buff=0.2)
        self.play(Transform(val_c, calculated_c), run_time=0.8)
        self.wait(1.0) # Scene 5 ends (0.8+0.8+0.8+1.0+0.8+0.8+1.0 = 6.0 sec)

        self.play(FadeOut(VGroup(example_triangle, right_angle_mark, side_a_line, side_b_line, hypotenuse_line, val_a, val_b, val_c, result_text)), run_time=0.8)

        # --- Scene 6: SUMMARY ---
        summary_title = Text("تذكر دائماً!", font="Arial", font_size=48, color=TEAL_A).to_edge(UP)
        summary_point1 = Text("فقط للمثلثات القائمة", font="Arial", font_size=36, color=WHITE).shift(UP * 0.5)
        summary_point2 = Text("الوتر (ج) هو أطول ضلع ومقابل للزاوية القائمة", font="Arial", font_size=36, color=GREEN).next_to(summary_point1, DOWN, buff=0.5)
        summary_point3 = Text("أ² + ب² = ج²", font="Arial", font_size=48, color=WHITE).next_to(summary_point2, DOWN, buff=0.5)

        self.play(Write(summary_title), run_time=0.8)
        self.play(FadeIn(summary_point1, shift=UP), run_time=0.6)
        self.play(FadeIn(summary_point2, shift=UP), run_time=0.6)
        self.play(FadeIn(summary_point3, shift=UP), run_time=0.6)
        self.wait(1.0) # Scene 6 ends (0.8+0.6+0.6+0.6+1.0 = 3.6 sec)

        self.wait(0.5) # Final buffer