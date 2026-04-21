from manim import *

class MainScene(Scene):
    def construct(self):
        numbers = [5, 2, 8, 1]
        colors = [BLUE, PINK, CYAN, PURPLE]
        
        boxes = VGroup()
        labels = VGroup()
        
        for i, val in enumerate(numbers):
            sq = Square(side_length=1.2, color=colors[i], stroke_width=6)
            sq.shift(LEFT * 2.25 + RIGHT * i * 1.5)
            boxes.add(sq)
            
            txt = Text(str(val), font_size=36)
            txt.move_to(sq.get_center())
            labels.add(txt)
            
        title = Text("Bubble Sort", font_size=40).to_edge(UP, buff=0.5)
        self.add(title, boxes, labels)
        
        pointer = Triangle(fill_opacity=1, color=YELLOW).scale(0.2).rotate(PI)
        pointer.next_to(boxes[0], DOWN, buff=0.2)
        self.add(pointer)
        
        n = len(numbers)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Move pointer to current pair
                self.play(pointer.animate.next_to(boxes[j], DOWN, buff=0.2), run_time=0.3)
                
                # Highlight pair
                self.play(
                    boxes[j].animate.set_color(YELLOW),
                    boxes[j+1].animate.set_color(YELLOW),
                    run_time=0.2
                )
                
                if numbers[j] > numbers[j+1]:
                    # Swap logic
                    pos1 = boxes[j].get_center()
                    pos2 = boxes[j+1].get_center()
                    
                    self.play(
                        boxes[j].animate.move_to(pos2),
                        boxes[j+1].animate.move_to(pos1),
                        labels[j].animate.move_to(pos2),
                        labels[j+1].animate.move_to(pos1),
                        run_time=0.4
                    )
                    
                    # Update variables
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                    boxes[j], boxes[j+1] = boxes[j+1], boxes[j]
                    labels[j], labels[j+1] = labels[j+1], labels[j]
                
                # Restore color
                self.play(
                    boxes[j].animate.set_color(colors[j % 4]),
                    boxes[j+1].animate.set_color(colors[(j+1) % 4]),
                    run_time=0.2
                )
                
        # Final highlight
        success_text = Text("Sorted!", color=GREEN).to_edge(DOWN)
        self.play(Write(success_text), run_time=0.5)
        self.wait(1)