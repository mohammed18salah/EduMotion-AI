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
        hook = Text("ما هي خوارزمية الفقاعة؟", font="Arial", font_size=48, color=TEAL_A)
        self.play(Write(hook, run_time=0.7))
        self.wait(3)
        self.play(FadeOut(hook, run_time=0.5))

        # ---------- Scene 2: Initial List ----------
        numbers = [5, 1, 4, 2, 8]
        elems = VGroup(*[Text(str(n), font="Arial", font_size=36, color=TEAL_A) for n in numbers])
        elems.arrange(RIGHT, buff=0.8)
        self.play(FadeIn(elems, run_time=0.8))
        self.wait(5)
        self.play(FadeOut(elems, run_time=0.5))

        # ---------- Scene 3: First Pass ----------
        # recreate list
        elems = VGroup(*[Text(str(n), font="Arial", font_size=36, color=TEAL_A) for n in numbers])
        elems.arrange(RIGHT, buff=0.8)
        self.play(FadeIn(elems, run_time=0.8))

        # comparison 5 vs 1
        arr1 = DoubleArrow(elems[0].get_bottom(), elems[1].get_bottom(), color=YELLOW_A)
        self.play(Create(arr1, run_time=0.5))
        self.wait(0.5)
        self.play(
            elems[0].animate.move_to(elems[1].get_center()),
            elems[1].animate.move_to(elems[0].get_center()),
            run_time=0.7,
        )
        self.play(FadeOut(arr1, run_time=0.3))

        # comparison (now 5) vs 4
        arr2 = DoubleArrow(elems[0].get_bottom(), elems[2].get_bottom(), color=YELLOW_A)
        self.play(Create(arr2, run_time=0.5))
        self.wait(0.5)
        self.play(
            elems[0].animate.move_to(elems[2].get_center()),
            elems[2].animate.move_to(elems[0].get_center()),
            run_time=0.7,
        )
        self.play(FadeOut(arr2, run_time=0.3))

        # comparison (now 5) vs 2
        arr3 = DoubleArrow(elems[0].get_bottom(), elems[3].get_bottom(), color=YELLOW_A)
        self.play(Create(arr3, run_time=0.5))
        self.wait(0.5)
        self.play(
            elems[0].animate.move_to(elems[3].get_center()),
            elems[3].animate.move_to(elems[0].get_center()),
            run_time=0.7,
        )
        self.play(FadeOut(arr3, run_time=0.3))

        # final arrangement after first pass
        self.play(elems.animate.arrange(RIGHT, buff=0.8), run_time=0.6)
        self.wait(6)
        self.play(FadeOut(elems, run_time=0.5))

        # ---------- Scene 4: Second Pass ----------
        # list after first pass: 1 4 2 5 8
        numbers2 = [1, 4, 2, 5, 8]
        elems = VGroup(*[Text(str(n), font="Arial", font_size=36, color=TEAL_A) for n in numbers2])
        elems.arrange(RIGHT, buff=0.8)
        self.play(FadeIn(elems, run_time=0.8))

        # comparison 1 vs 4 (no swap) – just show arrow briefly
        arr4 = DoubleArrow(elems[0].get_bottom(), elems[1].get_bottom(), color=YELLOW_A)
        self.play(Create(arr4, run_time=0.4))
        self.wait(0.4)
        self.play(FadeOut(arr4, run_time=0.3))

        # comparison 4 vs 2 -> swap
        arr5 = DoubleArrow(elems[1].get_bottom(), elems[2].get_bottom(), color=YELLOW_A)
        self.play(Create(arr5, run_time=0.5))
        self.wait(0.5)
        self.play(
            elems[1].animate.move_to(elems[2].get_center()),
            elems[2].animate.move_to(elems[1].get_center()),
            run_time=0.7,
        )
        self.play(FadeOut(arr5, run_time=0.3))

        # remaining comparisons (no swaps)
        arr6 = DoubleArrow(elems[2].get_bottom(), elems[3].get_bottom(), color=YELLOW_A)
        self.play(Create(arr6, run_time=0.4))
        self.wait(0.4)
        self.play(FadeOut(arr6, run_time=0.3))

        arr7 = DoubleArrow(elems[3].get_bottom(), elems[4].get_bottom(), color=YELLOW_A)
        self.play(Create(arr7, run_time=0.4))
        self.wait(0.4)
        self.play(FadeOut(arr7, run_time=0.3))

        # rearrange after second pass
        self.play(elems.animate.arrange(RIGHT, buff=0.8), run_time=0.6)
        self.wait(6)
        self.play(FadeOut(elems, run_time=0.5))

        # ---------- Scene 5: Summary ----------
        final_nums = [1, 2, 4, 5, 8]
        final_elems = VGroup(*[Text(str(n), font="Arial", font_size=36, color=GREEN) for n in final_nums])
        final_elems.arrange(RIGHT, buff=0.8)
        self.play(FadeIn(final_elems, run_time=0.8))
        summary = Text("القائمة مرتبة بالكامل!", font="Arial", font_size=42, color=PINK)
        summary.next_to(final_elems, DOWN, buff=0.6)
        self.play(Write(summary, run_time=0.7))
        self.wait(4)