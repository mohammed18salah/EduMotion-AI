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
        cart_light = Rectangle(width=1, height=0.5, color=TEAL_A).shift(LEFT * 2)
        cart_heavy = Rectangle(width=1.5, height=0.5, color=TEAL_A).shift(RIGHT * 2)
        hand = Triangle().scale(0.5).set_fill(PINK, opacity=1).rotate(PI / 2)
        hand.next_to(cart_light, LEFT)
        force_arrow = Arrow(start=hand.get_right(), end=cart_light.get_left(), color=PINK)
        question = Text("ماذا سيحدث؟", font_size=36, color=WHITE).to_edge(UP)

        self.play(FadeIn(cart_light), run_time=0.6)
        self.play(FadeIn(cart_heavy), run_time=0.6)
        self.play(FadeIn(hand), FadeIn(force_arrow), run_time=0.6)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # ---------- Scene 2: Definition ----------
        txt_force = Text("القوة", color=TEAL_A, font_size=48)
        txt_eq = Text("=", color=WHITE, font_size=48)
        txt_mass = Text("الكتلة", color=PINK, font_size=48)
        txt_mul = Text("×", color=WHITE, font_size=48)
        txt_acc = Text("التسارع", color=GREEN, font_size=48)

        equation = VGroup(txt_force, txt_eq, txt_mass, txt_mul, txt_acc).arrange(RIGHT, buff=0.2)
        definition = Text("القوة تجعل الجسم يغير سرعته", font_size=30, color=WHITE).next_to(equation, DOWN)

        self.play(FadeIn(txt_force), run_time=0.6)
        self.play(FadeIn(txt_eq), run_time=0.6)
        self.play(FadeIn(txt_mass), run_time=0.6)
        self.play(FadeIn(txt_mul), run_time=0.6)
        self.play(FadeIn(txt_acc), run_time=0.6)
        self.play(FadeIn(definition), run_time=0.6)
        self.wait(6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # ---------- Scene 3: Same Force, Different Mass ----------
        mass_small = Circle(radius=0.3, color=TEAL_A).shift(LEFT * 2)
        mass_big = Circle(radius=0.5, color=TEAL_A).shift(RIGHT * 2)

        force_small = Arrow(
            start=mass_small.get_bottom() + DOWN * 0.2,
            end=mass_small.get_bottom() + DOWN * 0.2 + RIGHT * 2,
            color=PINK,
        )
        force_big = Arrow(
            start=mass_big.get_bottom() + DOWN * 0.2,
            end=mass_big.get_bottom() + DOWN * 0.2 + RIGHT * 2,
            color=PINK,
        )

        acc_small = Arrow(
            start=mass_small.get_center(),
            end=mass_small.get_center() + RIGHT * 2,
            color=GREEN,
        )
        acc_big = Arrow(
            start=mass_big.get_center(),
            end=mass_big.get_center() + RIGHT * 1,
            color=GREEN,
        )

        label_force = Text("قوة ثابتة", font_size=24, color=PINK).next_to(force_small, DOWN)
        label_acc = Text("تسارع مختلف", font_size=24, color=GREEN).next_to(acc_small, UP)

        self.play(FadeIn(mass_small), FadeIn(mass_big), run_time=0.6)
        self.play(FadeIn(force_small), FadeIn(force_big), run_time=0.6)
        self.play(FadeIn(label_force), run_time=0.6)
        self.wait(1)
        self.play(FadeIn(acc_small), FadeIn(acc_big), run_time=0.6)
        self.play(FadeIn(label_acc), run_time=0.6)
        self.wait(8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # ---------- Scene 4: Same Mass, Different Force ----------
        mass = Circle(radius=0.4, color=TEAL_A)

        force_low = Arrow(
            start=mass.get_bottom() + DOWN * 0.2,
            end=mass.get_bottom() + DOWN * 0.2 + RIGHT * 1.5,
            color=PINK,
        )
        force_high = Arrow(
            start=mass.get_bottom() + DOWN * 0.2,
            end=mass.get_bottom() + DOWN * 0.2 + RIGHT * 3,
            color=PINK,
        )
        acc_low = Arrow(
            start=mass.get_center(),
            end=mass.get_center() + RIGHT * 1,
            color=GREEN,
        )
        acc_high = Arrow(
            start=mass.get_center(),
            end=mass.get_center() + RIGHT * 2,
            color=GREEN,
        )

        label_low = Text("قوة صغيرة", font_size=24, color=PINK).next_to(force_low, DOWN)
        label_high = Text("قوة كبيرة", font_size=24, color=PINK).next_to(force_high, DOWN)

        self.play(FadeIn(mass), run_time=0.6)
        self.play(FadeIn(force_low), FadeIn(acc_low), run_time=0.6)
        self.play(FadeIn(label_low), run_time=0.6)
        self.wait(1)

        # Transform to larger force and larger acceleration
        self.play(
            Transform(force_low, force_high),
            Transform(acc_low, acc_high),
            Transform(label_low, label_high),
            run_time=0.7,
        )
        self.wait(7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # ---------- Scene 5: Summary ----------
        summary_eq = VGroup(txt_force.copy(), txt_eq.copy(), txt_mass.copy(),
                            txt_mul.copy(), txt_acc.copy()).arrange(RIGHT, buff=0.2)
        summary_eq.to_edge(UP)

        insight = Text(
            "قوة أكبر → تسارع أكبر، كتلة أكبر → تسارع أصغر",
            font_size=36,
            color=WHITE,
        )
        insight.next_to(summary_eq, DOWN, buff=0.8)

        check = Text("✔", font_size=72, color=GREEN).next_to(insight, RIGHT, buff=0.5)

        self.play(FadeIn(summary_eq), run_time=0.6)
        self.play(FadeIn(insight), run_time=0.6)
        self.play(FadeIn(check), run_time=0.6)
        self.wait(4)