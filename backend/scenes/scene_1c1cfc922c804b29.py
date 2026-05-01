from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # ---------- Scene 1: Hook ----------
        self.play(FadeOut(Group(*self.mobjects)))
        tri = Polygon(ORIGIN, 4*RIGHT, 4*RIGHT+3*UP, color=TEAL_A)
        sq_a = Square(side_length=4, color=PINK).next_to(tri, DOWN, buff=0)
        sq_b = Square(side_length=3, color=GREEN).next_to(tri, LEFT, buff=0)
        sq_c = Square(side_length=5, color=YELLOW_A).move_to(tri.get_center() + 2.5*UP + 2.5*RIGHT)
        self.play(Create(tri), run_time=0.7)
        self.play(Create(sq_a), run_time=0.6)
        self.play(Create(sq_b), run_time=0.6)
        self.play(Create(sq_c), run_time=0.7)
        self.wait(2.5)
        
        # ---------- Scene 2: Define sides ----------
        self.play(FadeOut(Group(*self.mobjects)))
        tri2 = Polygon(ORIGIN, 4*RIGHT, 4*RIGHT+3*UP, color=TEAL_A)
        sq_a2 = Square(side_length=4, color=PINK).next_to(tri2, DOWN, buff=0)
        sq_b2 = Square(side_length=3, color=GREEN).next_to(tri2, LEFT, buff=0)
        sq_c2 = Square(side_length=5, color=YELLOW_A).move_to(tri2.get_center() + 2.5*UP + 2.5*RIGHT)
        label_a = Text("a", font_size=36, color=WHITE).move_to(sq_a2.get_center())
        label_b = Text("b", font_size=36, color=WHITE).move_to(sq_b2.get_center())
        label_c = Text("c", font_size=36, color=WHITE).move_to(sq_c2.get_center())
        self.play(Create(tri2), run_time=0.6)
        self.play(Create(sq_a2), run_time=0.5)
        self.play(Create(sq_b2), run_time=0.5)
        self.play(Create(sq_c2), run_time=0.6)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), run_time=0.7)
        self.wait(3.5)
        
        # ---------- Scene 3: Area rearrangement ----------
        self.play(FadeOut(Group(*self.mobjects)))
        tri3 = Polygon(ORIGIN, 4*RIGHT, 4*RIGHT+3*UP, color=TEAL_A)
        sq_a3 = Square(side_length=4, color=PINK).move_to(LEFT*5 + DOWN*2)
        sq_b3 = Square(side_length=3, color=GREEN).move_to(LEFT*5 + UP*2)
        sq_c3 = Square(side_length=5, color=YELLOW_A).move_to(RIGHT*2 + UP*1)
        self.play(Create(tri3), run_time=0.6)
        self.play(Create(sq_a3), run_time=0.5)
        self.play(Create(sq_b3), run_time=0.5)
        self.play(Create(sq_c3), run_time=0.6)
        self.wait(1)
        # Move small squares into the large one
        pos_c = sq_c3.get_center()
        self.play(
            sq_a3.animate.move_to(pos_c + LEFT*1.5 + DOWN*1.5),
            sq_b3.animate.move_to(pos_c + RIGHT*1.5 + DOWN*1.5),
            run_time=0.8,
        )
        self.wait(2.5)
        
        # ---------- Scene 4: Real‑world analogy ----------
        self.play(FadeOut(Group(*self.mobjects)))
        wall = Rectangle(width=0.2, height=5, color=WHITE).to_edge(LEFT, buff=1)
        ground = Rectangle(width=8, height=0.2, color=WHITE).to_edge(DOWN, buff=1)
        ladder = Polygon(
            wall.get_bottom() + UP*0.2,
            wall.get_bottom() + UP*0.2 + 6*RIGHT + 4*UP,
            wall.get_bottom() + UP*0.2 + 6*RIGHT + 3.9*UP,
            wall.get_bottom() + UP*0.1,
            color=TEAL_A,
        )
        label_ladder = Text("ladder length c", font_size=30, color=WHITE).next_to(ladder, UP)
        self.play(Create(wall), Create(ground), run_time=0.7)
        self.play(Create(ladder), run_time=0.7)
        self.play(FadeIn(label_ladder), run_time=0.6)
        self.wait(3)
        
        # ---------- Scene 5: Summary ----------
        self.play(FadeOut(Group(*self.mobjects)))
        summary = Text(
            "In a right triangle, a² + b² equals c² – the sum of the squares on the legs matches the square on the hypotenuse.",
            font_size=32,
            color=WHITE,
        )
        self.play(FadeIn(summary), run_time=0.8)
        self.wait(4)