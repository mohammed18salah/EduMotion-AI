from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#2F4F4F"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        self.play(FadeOut(Group(*self.mobjects)))   # clear start

        # -------------------------------------------------
        # Scene 1 – Hook
        title = Text("Bubble Sort", font_size=48, color=WHITE).to_edge(UP)
        bubble = Circle(radius=0.5, color=TEAL_A, fill_opacity=0.5)
        bubble.move_to(3 * UP + 2 * LEFT)

        self.play(Create(title), run_time=0.7)
        self.play(Create(bubble), run_time=0.7)
        self.play(bubble.animate.shift(3 * DOWN), run_time=0.8)
        self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # -------------------------------------------------
        # Scene 2 – Adjacent comparison
        nums = [5, 2, 4, 1, 3]
        squares = VGroup(*[
            Square(side_length=0.8, color=TEAL_A).add(Text(str(n), font_size=24, color=WHITE))
            for n in nums
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        arrow = Arrow(
            start=squares[0].get_right(),
            end=squares[1].get_left(),
            buff=0.1,
            color=PINK,
        )

        self.play(Create(squares), run_time=0.7)
        self.wait(0.5)
        self.play(Create(arrow), run_time=0.6)
        self.wait(0.8)

        # swap if out of order (5 > 2)
        pos0 = squares[0].get_center()
        pos1 = squares[1].get_center()
        self.play(
            squares[0].animate.move_to(pos1),
            squares[1].animate.move_to(pos0),
            run_time=0.7,
        )
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # -------------------------------------------------
        # Scene 3 – First pass (bubble the largest)
        nums = [5, 2, 4, 1, 3]
        arr = VGroup(*[
            Square(side_length=0.8, color=TEAL_A).add(Text(str(n), font_size=24, color=WHITE))
            for n in nums
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        self.play(Create(arr), run_time=0.7)
        self.wait(0.5)

        # swap 5 & 2
        pos_a = arr[0].get_center()
        pos_b = arr[1].get_center()
        self.play(
            arr[0].animate.move_to(pos_b),
            arr[1].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(0.4)

        # swap 5 & 4
        pos_a = arr[1].get_center()
        pos_b = arr[2].get_center()
        self.play(
            arr[1].animate.move_to(pos_b),
            arr[2].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(0.4)

        # swap 5 & 1
        pos_a = arr[2].get_center()
        pos_b = arr[3].get_center()
        self.play(
            arr[2].animate.move_to(pos_b),
            arr[3].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(0.4)

        # swap 5 & 3 (final position)
        pos_a = arr[3].get_center()
        pos_b = arr[4].get_center()
        self.play(
            arr[3].animate.move_to(pos_b),
            arr[4].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # -------------------------------------------------
        # Scene 4 – Second pass (ignore last element)
        nums = [2, 4, 1, 3, 5]
        arr2 = VGroup(*[
            Square(side_length=0.8, color=TEAL_A).add(Text(str(n), font_size=24, color=WHITE))
            for n in nums
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        self.play(Create(arr2), run_time=0.7)
        self.wait(0.5)

        # compare 2 & 4 – no swap
        self.wait(0.5)

        # swap 4 & 1
        pos_a = arr2[1].get_center()
        pos_b = arr2[2].get_center()
        self.play(
            arr2[1].animate.move_to(pos_b),
            arr2[2].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(0.4)

        # swap 4 & 3
        pos_a = arr2[2].get_center()
        pos_b = arr2[3].get_center()
        self.play(
            arr2[2].animate.move_to(pos_b),
            arr2[3].animate.move_to(pos_a),
            run_time=0.7,
        )
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # -------------------------------------------------
        # Scene 5 – No‑swap pass (algorithm finishes)
        nums = [2, 1, 3, 4, 5]
        arr3 = VGroup(*[
            Square(side_length=0.8, color=TEAL_A).add(Text(str(n), font_size=24, color=WHITE))
            for n in nums
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        self.play(Create(arr3), run_time=0.7)
        self.wait(0.5)

        notice = Text(
            "No swaps needed – sorting complete",
            font_size=36,
            color=GREEN,
        ).next_to(arr3, UP, buff=0.6)

        self.play(Write(notice), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # -------------------------------------------------
        # Scene 6 – Summary
        sorted_nums = [1, 2, 3, 4, 5]
        sorted_arr = VGroup(*[
            Square(side_length=0.8, color=GREEN).add(Text(str(n), font_size=24, color=WHITE))
            for n in sorted_nums
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        summary = Text(
            "Bubble sort repeatedly sweeps, moving the largest item each pass. O(n²) time.",
            font_size=28,
            color=WHITE,
        ).to_edge(UP)

        self.play(Create(sorted_arr), run_time=0.8)
        self.play(Write(summary), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)