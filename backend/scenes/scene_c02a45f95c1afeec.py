from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # SCENE 1: HOOK
        title = Text("Newton's Second Law", font_size=40, color=TEAL_A)
        title.to_edge(UP)
        box = Rectangle(width=2, height=2, color=PINK, fill_opacity=0.3)
        box.move_to(ORIGIN)
        arrow = Arrow(box.get_right(), box.get_right() + RIGHT * 2, color=GREEN, buff=0.1)
        
        self.play(FadeIn(title), Create(box), Create(arrow))
        self.wait(2.0)
        self.play(FadeOut(Group(title, box, arrow)))

        # SCENE 2: MASS EFFECT
        heavy_box = Rectangle(width=3, height=3, color=RED_B, fill_opacity=0.4)
        heavy_box.move_to(LEFT * 2)
        light_box = Rectangle(width=1.5, height=1.5, color=GREEN, fill_opacity=0.4)
        light_box.move_to(RIGHT * 2)
        label_heavy = Text("Heavy", font_size=24, color=WHITE).next_to(heavy_box, DOWN)
        label_light = Text("Light", font_size=24, color=WHITE).next_to(light_box, DOWN)
        force_arrow = Arrow(ORIGIN, RIGHT * 2, color=TEAL_A, buff=0)
        force_arrow.move_to(ORIGIN)
        
        self.play(Create(heavy_box), Create(label_heavy), Create(light_box), Create(label_light))
        self.play(force_arrow.animate.move_to(ORIGIN).scale(1.5))
        self.wait(2.5)
        self.play(FadeOut(Group(heavy_box, label_heavy, light_box, label_light, force_arrow)))

        # SCENE 3: FORCE EFFECT
        obj = Square(side_length=2, color=TEAL_A, fill_opacity=0.3)
        obj.move_to(ORIGIN)
        soft_arrow = Arrow(ORIGIN, RIGHT * 1.5, color=YELLOW_A, buff=0)
        hard_arrow = Arrow(ORIGIN, RIGHT * 3.5, color=GREEN, buff=0)
        
        self.play(Create(obj), Create(soft_arrow))
        self.wait(1.5)
        self.play(FadeOut(soft_arrow), Create(hard_arrow))
        self.wait(2.0)
        self.play(FadeOut(Group(obj, hard_arrow)))

        # SCENE 4: THE FORMULA
        f_text = Text("F", font_size=60, color=PINK)
        eq = Text("=", font_size=60, color=WHITE)
        m_text = Text("m", font_size=60, color=TEAL_A)
        times = Text("x", font_size=60, color=WHITE)
        a_text = Text("a", font_size=60, color=GREEN)
        formula = VGroup(f_text, eq, m_text, times, a_text).arrange(RIGHT, buff=0.3)
        formula.move_to(ORIGIN)
        
        self.play(FadeIn(f_text), FadeIn(eq), FadeIn(m_text), FadeIn(times), FadeIn(a_text))
        self.wait(3.0)
        self.play(FadeOut(Group(f_text, eq, m_text, times, a_text)))

        # SCENE 5: REAL WORLD
        car = Rectangle(width=2, height=1, color=TEAL_A, fill_opacity=0.3)
        car.move_to(LEFT * 2)
        truck = Rectangle(width=4, height=2, color=RED_B, fill_opacity=0.3)
        truck.move_to(RIGHT * 2)
        label_car = Text("Small Force", font_size=20, color=WHITE).next_to(car, UP)
        label_truck = Text("Huge Force", font_size=20, color=WHITE).next_to(truck, UP)
        
        self.play(Create(car), Create(label_car), Create(truck), Create(label_truck))
        self.wait(2.5)
        self.play(FadeOut(Group(car, label_car, truck, label_truck)))

        # SCENE 6: SUMMARY
        summary = Text("Force = Mass x Acceleration", font_size=40, color=TEAL_A)
        summary.to_edge(UP)
        check = Text("Got it!", font_size=40, color=GREEN)
        check.move_to(ORIGIN)
        
        self.play(FadeIn(summary), Create(check))
        self.wait(3.0)
        self.play(FadeOut(Group(summary, check)))