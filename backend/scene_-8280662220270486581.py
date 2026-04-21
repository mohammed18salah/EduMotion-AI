from manim import *

class MainScene(Scene):
    def construct(self):
        # Title of the animation
        title = Text("Bubble Sort", color=BLUE).scale(0.8)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))

        # Initial data for sorting
        values = [6, 2, 8, 3]
        elements = []
        
        # Create bars representing the values
        for val in values:
            rect = Rectangle(width=0.6, height=val * 0.4, fill_opacity=0.8, fill_color=TEAL)
            label = Text(str(val)).scale(0.6).next_to(rect, DOWN)
            elements.append(VGroup(rect, label))

        # Arrange bars horizontally
        bars_group = VGroup(*elements).arrange(RIGHT, buff=0.4).center()
        self.play(Create(bars_group))
        self.wait(0.5)

        n = len(values)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight bars being compared
                self.play(
                    elements[j][0].animate.set_color(YELLOW),
                    elements[j+1][0].animate.set_color(YELLOW),
                    run_time=0.3
                )

                if values[j] > values[j+1]:
                    # Swap logic in the value list
                    values[j], values[j+1] = values[j+1], values[j]
                    
                    # Visual swap animation
                    pos_left = elements[j].get_center().copy()
                    pos_right = elements[j+1].get_center().copy()
                    
                    self.play(
                        elements[j].animate.move_to(pos_right),
                        elements[j+1].animate.move_to(pos_left),
                        run_time=0.4
                    )
                    
                    # Update order in the elements list
                    elements[j], elements[j+1] = elements[j+1], elements[j]
                
                # Revert colors after comparison/swap
                self.play(
                    elements[j][0].animate.set_color(TEAL),
                    elements[j+1][0].animate.set_color(TEAL),
                    run_time=0.2
                )
            
            # Mark the sorted element at the end of the pass as green
            self.play(elements[n-i-1][0].animate.set_color(GREEN), run_time=0.3)

        # Final sorted state notification
        success_msg = Text("Array Sorted!", color=GREEN).scale(0.7).next_to(bars_group, UP, buff=0.8)
        self.play(Write(success_msg))
        self.wait(2)