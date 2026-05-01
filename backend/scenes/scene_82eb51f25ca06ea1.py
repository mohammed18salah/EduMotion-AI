from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # -------------------------------------------------
        # 1. HOOK_TRIANGLE (4 sec)
        # -------------------------------------------------
        tri = Polygon(
            [0, 0, 0],      # O
            [4, 0, 0],      # A (a = 4)
            [0, 3, 0],      # B (b = 3)
            color=TEAL_A,
            fill_opacity=0.2,
        )
        self.play(Create(tri), run_time=0.7)
        self.wait(3.3)                     # total 4 sec for scene
        self.play(FadeOut(Group(*self.mobjects)))

        # -------------------------------------------------
        # 2. LABEL_SIDES (5 sec)
        # -------------------------------------------------
        tri = Polygon([0,0,0],[4,0,0],[0,3,0],color=TEAL_A,fill_opacity=0.2)
        self.play(Create(tri), run_time=0.6)

        label_a = Text("a", color=WHITE).next_to(midpoint(tri.get_vertices()[0], tri.get_vertices()[1]), DOWN)
        label_b = Text("b", color=WHITE).next_to(midpoint(tri.get_vertices()[0], tri.get_vertices()[2]), LEFT)
        label_c = Text("c", color=WHITE).move_to(tri.get_center() + (tri.get_vertices()[1] - tri.get_vertices()[0]) / 2 + (tri.get_vertices()[2] - tri.get_vertices()[0]) / 2).rotate(-PI/2)
        self.play(Write(label_a), Write(label_b), Write(label_c), run_time=0.6)
        self.wait(4.4)                     # total 5 sec for scene
        self.play(FadeOut(Group(*self.mobjects)))

        # -------------------------------------------------
        # 3. DRAW_SQUARES (7 sec)
        # -------------------------------------------------
        tri = Polygon([0,0,0],[4,0,0],[0,3,0],color=TEAL_A,fill_opacity=0.2)
        self.play(Create(tri), run_time=0.6)

        # square on side a (length 4)
        sq_a = Square(side_length=4, color=PINK, fill_opacity=0.5)
        sq_a.next_to(tri, DOWN, buff=0)

        # square on side b (length 3)
        sq_b = Square(side_length=3, color=PINK, fill_opacity=0.5)
        sq_b.next_to(tri, LEFT, buff=0)

        # square on hypotenuse c (length 5)
        sq_c = Square(side_length=5, color=GREEN, fill_opacity=0.5)
        sq_c.next_to(tri, RIGHT, buff=0)

        self.play(
            Create(sq_a), Create(sq_b), Create(sq_c),
            run_time=0.8
        )
        self.wait(6.2)                     # total 7 sec for scene
        self.play(FadeOut(Group(*self.mobjects)))

        # -------------------------------------------------
        # 4. REARRANGE_AREA (9 sec)
        # -------------------------------------------------
        # Re‑draw triangle and squares for clarity
        tri = Polygon([0,0,0],[4,0,0],[0,3,0],color=TEAL_A,fill_opacity=0.2)
        sq_a = Square(side_length=4, color=PINK, fill_opacity=0.5).next_to(tri, DOWN, buff=0)
        sq_b = Square(side_length=3, color=PINK, fill_opacity=0.5).next_to(tri, LEFT, buff=0)
        sq_c = Square(side_length=5, color=GREEN, fill_opacity=0.5).next_to(tri, RIGHT, buff=0)

        self.play(
            Create(tri), Create(sq_a), Create(sq_b), Create(sq_c),
            run_time=0.8
        )

        # copy the two pink squares and move them into the green square
        copy_a = sq_a.copy()
        copy_b = sq_b.copy()
        self.play(
            TransformFromCopy(sq_a, copy_a),
            TransformFromCopy(sq_b, copy_b),
            run_time=0.7
        )
        self.play(
            copy_a.animate.move_to(sq_c.get_center() + LEFT*1.2),
            copy_b.animate.move_to(sq_c.get_center() + RIGHT*1.2),
            run_time=0.7
        )
        # fade everything except the green square to emphasize the result
        self.play(FadeOut(tri), FadeOut(sq_a), FadeOut(sq_b), FadeOut(copy_a), FadeOut(copy_b), run_time=0.6)
        self.wait(8.4)                     # total 9 sec for scene
        self.play(FadeOut(Group(*self.mobjects)))

        # -------------------------------------------------
        # 5. SUMMARY (5 sec)
        # -------------------------------------------------
        formula = Text("a² + b² = c²", color=GREEN, font_size=72)
        self.play(Write(formula), run_time=0.6)
        self.wait(4.4)                     # total 5 sec for scene
        self.play(FadeOut(formula))