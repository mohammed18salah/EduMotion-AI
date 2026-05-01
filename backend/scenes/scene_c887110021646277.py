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
        # Create two circles
        circle1 = Circle(radius=0.3, color=TEAL_A).shift(UP*2 + LEFT*2)
        circle2 = Circle(radius=0.3, color=PINK).shift(UP*2 + RIGHT*2)
        # Appear
        self.play(FadeIn(circle1, run_time=0.6), FadeIn(circle2, run_time=0.6))
        # Drop together
        self.play(
            circle1.animate.shift(DOWN*4),
            circle2.animate.shift(DOWN*4),
            run_time=0.8,
        )
        # End of scene 1 (5 sec total)
        self.wait(5 - 0.6 - 0.6 - 0.8)   # 3.0 sec

        # ---------- Scene 2: Define Free Fall ----------
        # Clear previous
        self.play(FadeOut(Group(*self.mobjects), run_time=0.5))
        # Definition text
        def_text = Text(
            "Free fall: motion under gravity alone", 
            color=WHITE
        ).to_edge(UP)
        arrow_down = Arrow(
            start=def_text.get_bottom() + DOWN*0.2,
            end=def_text.get_bottom() + DOWN*1,
            color=YELLOW_A
        )
        self.play(FadeIn(def_text, run_time=0.6), FadeIn(arrow_down, run_time=0.6))
        self.wait(5 - 0.6 - 0.6)   # 3.8 sec

        # ---------- Scene 3: Constant Acceleration ----------
        self.play(FadeOut(Group(*self.mobjects), run_time=0.5))
        # Show g value
        g_text = Text("g = 9.8 m/s²", color=GREEN).to_edge(UP)
        self.play(FadeIn(g_text, run_time=0.6))

        # Dot that will move faster each step
        dot = Dot(radius=0.12, color=TEAL_A).shift(LEFT*3 + DOWN*1)
        self.play(FadeIn(dot, run_time=0.6))

        # Create three arrows of increasing length to represent speed
        arrows = []
        for i, length in enumerate([1, 1.8, 2.7]):   # each step longer
            arr = Arrow(
                start=dot.get_center() + RIGHT*0,
                end=dot.get_center() + RIGHT*length,
                color=PINK,
                buff=0
            )
            arrows.append(arr)
            self.play(FadeIn(arr, run_time=0.7))
            # move dot to end of arrow for next step
            self.play(dot.animate.shift(RIGHT*length), run_time=0.7)

        self.wait(6 - (0.6+0.6+0.7*3+0.7*3))   # 6 - 4.8 = 1.2 sec

        # ---------- Scene 4: Mass Independence ----------
        self.play(FadeOut(Group(*self.mobjects), run_time=0.5))
        # Heavy and light circles with labels
        heavy = Circle(radius=0.3, color=TEAL_A).shift(UP*2 + LEFT*2)
        light = Circle(radius=0.3, color=PINK).shift(UP*2 + RIGHT*2)
        label_heavy = Text("10 kg", color=WHITE, font_size=24).next_to(heavy, DOWN)
        label_light = Text("2 kg", color=WHITE, font_size=24).next_to(light, DOWN)
        group = VGroup(heavy, light, label_heavy, label_light)
        self.play(FadeIn(group, run_time=0.6))
        # Drop together
        self.play(
            heavy.animate.shift(DOWN*4),
            light.animate.shift(DOWN*4),
            run_time=0.8,
        )
        self.wait(7 - 0.5 - 0.6 - 0.8)   # 5.1 sec

        # ---------- Scene 5: Summary ----------
        self.play(FadeOut(Group(*self.mobjects), run_time=0.5))
        summary = Text(
            "All objects fall with the same acceleration g, independent of their mass.",
            color=WHITE,
        ).scale(0.8).to_edge(UP)
        # Highlight key phrases
        same_acc = Text("same acceleration", color=GREEN).next_to(summary, DOWN, buff=0.3)
        independent = Text("independent of their mass", color=YELLOW_A).next_to(same_acc, DOWN, buff=0.2)
        self.play(FadeIn(summary, run_time=0.6), FadeIn(same_acc, run_time=0.6), FadeIn(independent, run_time=0.6))
        self.wait(7 - 0.5 - 0.6*3)   # 5.7 sec