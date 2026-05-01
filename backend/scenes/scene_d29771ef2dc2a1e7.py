from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ---------- Scene 1: Hook ----------
        title = Text("خوارزمية الفقاعات", font_size=48, color=TEAL_A)
        title.to_edge(UP)
        bubble = Circle(radius=0.3, fill_opacity=0.8, fill_color=WHITE, stroke_width=0)
        bubble.move_to(DOWN * 2)
        water_line = Line(LEFT * 6, RIGHT * 6, color=TEAL_A).shift(DOWN * 1.5)

        self.play(FadeIn(title, shift=UP), run_time=0.7)
        self.play(FadeIn(water_line), run_time=0.5)
        self.play(FadeIn(bubble, shift=UP), run_time=0.6)
        self.play(bubble.animate.shift(UP * 3), run_time=0.8)
        self.wait(5)          # scene duration
        self.play(FadeOut(Group(*self.mobjects)))
        
        # ---------- Scene 2: Show Array ----------
        numbers = [5, 1, 4, 2, 8]
        squares = []
        start_x = -2.5
        spacing = 1.5
        for i, n in enumerate(numbers):
            sq = Square(side_length=1, color=WHITE, fill_opacity=0.2, fill_color=BLACK)
            txt = Text(str(n), font_size=36, color=WHITE)
            grp = VGroup(sq, txt).move_to(np.array([start_x + i * spacing, 0, 0]))
            squares.append(grp)

        array_group = VGroup(*squares)
        self.play(FadeIn(array_group, shift=UP), run_time=0.8)
        self.wait(6)          # scene duration
        self.play(FadeOut(Group(*self.mobjects)))
        
        # ---------- Scene 3: Compare & Swap ----------
        # Recreate array for this scene
        squares = []
        for i, n in enumerate(numbers):
            sq = Square(side_length=1, color=WHITE, fill_opacity=0.2, fill_color=BLACK)
            txt = Text(str(n), font_size=36, color=WHITE)
            grp = VGroup(sq, txt).move_to(np.array([start_x + i * spacing, 0, 0]))
            squares.append(grp)
        array_group = VGroup(*squares)
        self.play(FadeIn(array_group, shift=UP), run_time=0.6)

        # highlight first pair
        highlight = Rectangle(width=2.2, height=1.2, color=YELLOW_A, stroke_width=4)
        highlight.move_to(array_group[0].get_center() + RIGHT * spacing/2)
        self.play(FadeIn(highlight, scale=0.5), run_time=0.5)

        # compare 5 and 1 -> swap
        if numbers[0] > numbers[1]:
            # swap positions
            left = squares[0]
            right = squares[1]
            self.play(
                left.animate.shift(RIGHT * spacing),
                right.animate.shift(LEFT * spacing),
                run_time=0.7,
            )
            # swap references in list
            squares[0], squares[1] = squares[1], squares[0]

        self.play(FadeOut(highlight), run_time=0.4)
        self.wait(7)          # scene duration
        self.play(FadeOut(Group(*self.mobjects)))
        
        # ---------- Scene 4: Full Pass ----------
        # Re‑create original unsorted array
        numbers = [5, 1, 4, 2, 8]
        squares = []
        for i, n in enumerate(numbers):
            sq = Square(side_length=1, color=WHITE, fill_opacity=0.2, fill_color=BLACK)
            txt = Text(str(n), font_size=36, color=WHITE)
            grp = VGroup(sq, txt).move_to(np.array([start_x + i * spacing, 0, 0]))
            squares.append(grp)
        array_group = VGroup(*squares)
        self.play(FadeIn(array_group, shift=UP), run_time=0.6)

        # Perform one full pass (bubble up the biggest element)
        for i in range(len(squares) - 1):
            left = squares[i]
            right = squares[i + 1]
            # highlight the pair
            hl = Rectangle(width=2.2, height=1.2, color=YELLOW_A, stroke_width=4)
            hl.move_to((left.get_center() + right.get_center()) / 2)
            self.play(FadeIn(hl, scale=0.5), run_time=0.4)

            # compare and possibly swap
            if int(left[1].text) > int(right[1].text):
                self.play(
                    left.animate.shift(RIGHT * spacing),
                    right.animate.shift(LEFT * spacing),
                    run_time=0.7,
                )
                squares[i], squares[i + 1] = squares[i + 1], squares[i]
            self.play(FadeOut(hl), run_time=0.3)

        # highlight the element now at the end (the biggest)
        biggest = squares[-1]
        box = Rectangle(width=1.2, height=1.2, color=GREEN, stroke_width=6)
        box.move_to(biggest.get_center())
        self.play(FadeIn(box, run_time=0.5))
        self.wait(7)          # scene duration
        self.play(FadeOut(Group(*self.mobjects)))
        
        # ---------- Scene 5: Summary ----------
        # Final sorted array
        sorted_numbers = [1, 2, 4, 5, 8]
        squares = []
        for i, n in enumerate(sorted_numbers):
            sq = Square(side_length=1, color=WHITE, fill_opacity=0.2, fill_color=BLACK)
            txt = Text(str(n), font_size=36, color=WHITE)
            grp = VGroup(sq, txt).move_to(np.array([start_x + i * spacing, 0, 0]))
            squares.append(grp)
        array_group = VGroup(*squares)
        self.play(FadeIn(array_group, shift=UP), run_time=0.6)

        done = Text("الترتيب انتهى!", font_size=48, color=TEAL_A).to_edge(UP)
        self.play(FadeIn(done, shift=DOWN), run_time=0.7)
        self.wait(5)          # scene duration
        self.play(FadeOut(Group(*self.mobjects)))