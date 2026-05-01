from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"

import math


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # -------------------------------------------------
        # 1. HOOK
        # -------------------------------------------------
        hook = Text(
            "What if you could measure a triangle's longest side just by its other two sides?",
            font_size=36,
            color=TEAL_A,
        )
        hook.move_to(ORIGIN)
        self.play(FadeIn(hook, run_time=0.8))
        self.wait(4)          # scene duration
        self.play(FadeOut(hook, run_time=0.5))
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # -------------------------------------------------
        # 2. RIGHT TRIANGLE
        # -------------------------------------------------
        # vertices for a 3‑4‑5 right triangle
        A = LEFT * 2          # (-2, 0)
        B = RIGHT * 2         # ( 2, 0)
        C = UP * 2.5          # ( 0, 2.5)
        tri = Polygon(A, B, C, color=TEAL_A)
        self.play(Create(tri, run_time=0.8))

        # side labels
        a_lbl = Text("a", color=TEAL_A).next_to(Line(A, B), DOWN)
        b_lbl = Text("b", color=TEAL_A).next_to(Line(A, C), LEFT)
        c_lbl = Text("c", color=TEAL_A).next_to(Line(B, C), RIGHT)
        self.play(
            FadeIn(a_lbl, run_time=0.5),
            FadeIn(b_lbl, run_time=0.5),
            FadeIn(c_lbl, run_time=0.5),
        )
        self.wait(6)          # scene duration
        self.play(FadeOut(Group(tri, a_lbl, b_lbl, c_lbl), run_time=0.5))
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # -------------------------------------------------
        # 3. SQUARES ON SIDES
        # -------------------------------------------------
        # build the triangle again at the origin
        tri = Polygon(ORIGIN, RIGHT * 4, UP * 3, color=TEAL_A)
        self.play(Create(tri, run_time=0.8))

        # squares on the legs
        sq_a = Square(side_length=4, color=PINK, fill_opacity=0.2).next_to(tri, DOWN, buff=0)
        sq_b = Square(side_length=3, color=PINK, fill_opacity=0.2).next_to(tri, LEFT, buff=0)
        self.play(FadeIn(sq_a, run_time=0.5), FadeIn(sq_b, run_time=0.5))

        # square on the hypotenuse (length 5)
        hyp_len = 5
        mid = (RIGHT * 4 + UP * 3) / 2
        angle = math.atan2(3, 4)          # angle of the hypotenuse
        sq_c = Square(side_length=hyp_len, color=PINK, fill_opacity=0.2)
        sq_c.rotate(angle, about_point=mid)
        self.play(FadeIn(sq_c, run_time=0.5))

        # area labels
        a2 = Text("a²", color=WHITE).move_to(sq_a.get_center())
        b2 = Text("b²", color=WHITE).move_to(sq_b.get_center())
        c2 = Text("c²", color=WHITE).move_to(sq_c.get_center())
        self.play(FadeIn(a2, run_time=0.5), FadeIn(b2, run_time=0.5), FadeIn(c2, run_time=0.5))

        self.wait(8)          # scene duration
        self.play(FadeOut(Group(tri, sq_a, sq_b, sq_c, a2, b2, c2), run_time=0.5))
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # -------------------------------------------------
        # 4. REARRANGEMENT PROOF
        # -------------------------------------------------
        # four copies of the original triangle
        base_tri = Polygon(ORIGIN, RIGHT * 4, UP * 3, color=TEAL_A)
        copies = VGroup(*[base_tri.copy().rotate(k * PI / 2, about_point=ORIGIN) for k in range(4)])
        # place them to form a 5×5 square outline
        positions = [
            ORIGIN,
            RIGHT * 4,
            UP * 3,
            RIGHT * 4 + UP * 3,
        ]
        for cp, pos in zip(copies, positions):
            cp.move_to(pos)
        self.play(FadeIn(copies, run_time=0.8))

        # fade the four triangles and reveal the c² square
        self.play(FadeOut(copies, run_time=0.5))
        self.play(FadeIn(sq_c, run_time=0.5))

        self.wait(8)          # scene duration
        self.play(FadeOut(Group(sq_c), run_time=0.5))
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # -------------------------------------------------
        # 5. SUMMARY
        # -------------------------------------------------
        summary = Text(
            "a² + b² = c² — the Pythagorean theorem",
            font_size=48,
            color=GREEN,
        )
        self.play(FadeIn(summary, run_time=0.8))
        self.wait(4)          # scene duration
        self.play(FadeOut(summary, run_time=0.5))