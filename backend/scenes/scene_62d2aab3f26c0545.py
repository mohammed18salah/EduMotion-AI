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
        hook_text = Text("Bubble Sort: like bubbles rising in water", color=WHITE, font_size=36)
        bubble = Circle(radius=0.5, color=TEAL_A).set_fill(TEAL_A, opacity=0.6)
        arrow_up = Arrow(start=bubble.get_bottom(), end=bubble.get_top() + UP, color=PINK, buff=0)
        hook_group = VGroup(hook_text, bubble, arrow_up).arrange(DOWN, buff=0.5)
        self.play(FadeIn(hook_group), run_time=0.7)
        self.wait(2.0)

        # ---------- Scene 2: Unsorted array ----------
        self.play(FadeOut(Group(*self.mobjects)))
        vals = [5, 2, 4, 1, 3]
        squares = []
        for v in vals:
            sq = Square(side_length=1, color=TEAL_A).set_fill(TEAL_A, opacity=0.5)
            num = Text(str(v), color=WHITE, font_size=36)
            grp = VGroup(sq, num)
            squares.append(grp)
        array = VGroup(*squares).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1)
        self.play(FadeIn(array), run_time=0.7)
        self.wait(1.5)

        # ---------- Scene 3: First pass ----------
        self.play(FadeOut(Group(*self.mobjects)))
        # recreate array for animation
        squares = []
        for v in vals:
            sq = Square(side_length=1, color=TEAL_A).set_fill(TEAL_A, opacity=0.5)
            num = Text(str(v), color=WHITE, font_size=36)
            grp = VGroup(sq, num)
            squares.append(grp)
        array = VGroup(*squares).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1)
        self.play(FadeIn(array), run_time=0.7)

        # compare 5 & 2 -> swap
        a, b = squares[0], squares[1]
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        # compare 5 & 4 -> swap
        a, b = squares[0], squares[2]  # after previous swap, 5 is now at index 1
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        # compare 5 & 1 -> swap
        a, b = squares[0], squares[3]
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        # compare 5 & 3 -> swap
        a, b = squares[0], squares[4]
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(GREEN), b.animate.set_color(TEAL_A), run_time=0.3)

        self.wait(1.2)

        # ---------- Scene 4: After first pass ----------
        self.play(FadeOut(Group(*self.mobjects)))
        # recreate array showing result of first pass
        vals_pass1 = [2, 4, 1, 3, 5]
        squares = []
        for v in vals_pass1:
            sq = Square(side_length=1, color=TEAL_A).set_fill(TEAL_A, opacity=0.5)
            num = Text(str(v), color=WHITE, font_size=36)
            grp = VGroup(sq, num)
            squares.append(grp)
        array = VGroup(*squares).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1)
        highlight = squares[-1].copy().set_color(GREEN).set_stroke(width=4)
        self.play(FadeIn(array), run_time=0.7)
        self.play(Create(highlight), run_time=0.5)
        self.wait(2.0)

        # ---------- Scene 5: Second pass ----------
        self.play(FadeOut(Group(*self.mobjects)))
        # recreate unsorted part for second pass
        vals_pass2 = [2, 4, 1, 3, 5]
        squares = []
        for v in vals_pass2:
            sq = Square(side_length=1, color=TEAL_A).set_fill(TEAL_A, opacity=0.5)
            num = Text(str(v), color=WHITE, font_size=36)
            grp = VGroup(sq, num)
            squares.append(grp)
        array = VGroup(*squares).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1)
        self.play(FadeIn(array), run_time=0.7)

        # compare 2 & 4 -> no swap
        a, b = squares[0], squares[1]
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.4)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        # compare 4 & 1 -> swap
        a, b = squares[1], squares[2]
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        # compare 4 & 3 -> swap
        a, b = squares[2], squares[3]
        pos_a, pos_b = a.get_center(), b.get_center()
        self.play(a.animate.set_color(YELLOW_A), b.animate.set_color(YELLOW_A), run_time=0.5)
        self.wait(0.3)
        self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a), run_time=0.7)
        self.play(a.animate.set_color(TEAL_A), b.animate.set_color(TEAL_A), run_time=0.3)

        self.wait(1.5)

        # ---------- Scene 6: Sorted array summary ----------
        self.play(FadeOut(Group(*self.mobjects)))
        sorted_vals = [1, 2, 3, 4, 5]
        squares = []
        for v in sorted_vals:
            sq = Square(side_length=1, color=GREEN).set_fill(GREEN, opacity=0.5)
            num = Text(str(v), color=WHITE, font_size=36)
            grp = VGroup(sq, num)
            squares.append(grp)
        final_array = VGroup(*squares).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1)
        self.play(FadeIn(final_array), run_time=0.8)
        self.wait(3.0)