from manim import *

class MainScene(Scene):
    def construct(self):
        title = Text("Bubble Sort Algorithm", color=BLUE).scale(0.8)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        nums = [8, 3, 6, 1, 9, 2]
        colors = [RED, GREEN, YELLOW, ORANGE, PINK, BLUE]
        squares = VGroup()
        for i, val in enumerate(nums):
            sq = Square(fill_opacity=1, color=colors[i], side_length=0.8)
            txt = Text(str(val), color=WHITE).scale(0.5)
            group = VGroup(sq, txt)
            group.move_to(LEFT * 4 + i * 1.6 * RIGHT)
            squares.add(group)

        self.play(Create(squares))

        status = Text("Comparing...", color=WHITE).to_edge(DOWN)
        self.add(status)

        # Bubble sort logic for index 0 and 1 (8 and 3)
        self.play(squares[0].animate.set_color(YELLOW), squares[1].animate.set_color(YELLOW))
        self.wait(0.5)
        
        status.become(Text("Swapping!", color=RED).to_edge(DOWN))
        arr1 = Arrow(start=squares[0].get_bottom(), end=squares[1].get_bottom(), color=RED)
        arr2 = Arrow(start=squares[1].get_top(), end=squares[0].get_top(), color=RED)
        self.play(Create(arr1), Create(arr2))
        
        self.play(squares[0].animate.move_to(squares[1].get_center()),
                  squares[1].animate.move_to(squares[0].get_center()))
        squares[0], squares[1] = squares[1], squares[0]
        
        self.play(FadeOut(arr1), FadeOut(arr2))
        
        for sq in squares:
            sq.set_color(GREEN)
        
        self.play(FadeOut(status))
        final_text = Text("Sorted!", color=GOLD).scale(1.5)
        self.play(Write(final_text))
        self.wait(1)