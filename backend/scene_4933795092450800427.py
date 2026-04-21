from manim import *

class MainScene(Scene):
    def construct(self):
        numbers = [4, 2, 5, 1]
        colors = [RED_A, GREEN_A, BLUE_A, GOLD_A]
        elements = VGroup()
        
        for i in range(len(numbers)):
            box = Square(side_length=1.2, stroke_width=8, color=colors[i])
            val = Text(str(numbers[i]), font_size=40, color=WHITE)
            element = VGroup(box, val)
            elements.add(element)
            
        elements.arrange(RIGHT, buff=0.5).center()
        title = Text("Bubble Sort", font_size=44, color=WHITE).to_edge(UP, buff=0.5)
        
        self.add(title, elements)
        self.wait(0.3)
        
        n = len(numbers)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight current pair
                self.play(
                    elements[j][0].animate.set_stroke(WHITE, width=12),
                    elements[j+1][0].animate.set_stroke(WHITE, width=12),
                    run_time=0.2
                )
                
                if numbers[j] > numbers[j+1]:
                    # Visual swap
                    p1, p2 = elements[j].get_center().copy(), elements[j+1].get_center().copy()
                    self.play(
                        elements[j].animate.move_to(p2),
                        elements[j+1].animate.move_to(p1),
                        run_time=0.4
                    )
                    # Data swap
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                    elements[j], elements[j+1] = elements[j+1], elements[j]
                
                # Restore stroke
                self.play(
                    elements[j][0].animate.set_stroke(width=8),
                    elements[j+1][0].animate.set_stroke(width=8),
                    run_time=0.1
                )
        
        # Success animation
        success_rect = Rectangle(width=7, height=2, color=GREEN, stroke_width=4).move_to(elements)
        self.play(Create(success_rect), elements.animate.set_color(GREEN), run_time=0.5)
        self.wait(0.5)