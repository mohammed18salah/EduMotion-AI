from manim import *

config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 8.0
config.frame_height = 14.22
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Visual System Colors ---
        PRIMARY_COLOR = TEAL_A
        ACCENT_COLOR = PINK
        SUCCESS_COLOR = GREEN
        TEXT_COLOR = WHITE
        PROBLEM_COLOR = RED_B

        # Helper function to create a number box VGroup
        def create_number_box(number, position, color=PRIMARY_COLOR, text_color=TEXT_COLOR):
            rect = Rectangle(width=1.2, height=1.2, stroke_color=color, fill_opacity=0.1).move_to(position)
            num_text = Text(str(number), font_size=40, color=text_color).move_to(position)
            return VGroup(rect, num_text)

        # --- Scene 1: Hook ---
        title = Text("BUBBLE SORT", font_size=72, color=PRIMARY_COLOR, weight=BOLD)
        question = Text("How does it organize data?", font_size=36, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=0.7)
        self.play(Write(question), run_time=0.7)
        self.wait(2.6) # Scene 1 ends

        self.remove(title, question) # Instant removal

        # --- Scene 2: Setup ---
        # Represent an unsorted array of 5 numbers
        numbers_list = [5, 1, 4, 2, 8]
        number_boxes = VGroup()
        for i, num in enumerate(numbers_list):
            box = create_number_box(num, ORIGIN)
            number_boxes.add(box)
        
        # Arrange them horizontally, centered in the narrow aspect ratio
        number_boxes.arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        
        info_text_2 = Text("We have unsorted numbers:", font_size=32, color=TEXT_COLOR).next_to(number_boxes, UP, buff=0.8)

        self.play(Write(info_text_2), run_time=0.6)
        self.play(Create(number_boxes), run_time=0.6)
        self.wait(2.6) # Scene 2 ends

        self.remove(info_text_2) # Instant removal, keep number_boxes

        # --- Scene 3: Problem ---
        problem_text = Text("How do we put them in order?", font_size=32, color=TEXT_COLOR).next_to(number_boxes, UP, buff=0.8)
        
        # Highlight first two elements for comparison
        box1_rect = number_boxes[0][0] # Rectangle of the first number box (5)
        box2_rect = number_boxes[1][0] # Rectangle of the second number box (1)
        
        self.play(Write(problem_text), run_time=0.6)
        self.play(
            box1_rect.animate.set_stroke_color(PROBLEM_COLOR),
            box2_rect.animate.set_stroke_color(PROBLEM_COLOR),
            run_time=0.6
        )
        self.wait(2.6) # Scene 3 ends

        self.remove(problem_text) # Instant removal
        # Reset colors instantly for next scene
        self.add(box1_rect.set_stroke_color(PRIMARY_COLOR), box2_rect.set_stroke_color(PRIMARY_COLOR))


        # --- Scene 4: Explanation (Compare and Swap) ---
        explain_text = Text("Compare adjacent items.", font_size=32, color=TEXT_COLOR).next_to(number_boxes, UP, buff=0.8)
        
        self.play(Write(explain_text), run_time=0.6)
        self.play(
            number_boxes[0][0].animate.set_stroke_color(ACCENT_COLOR), # Highlight current 5
            number_boxes[1][0].animate.set_stroke_color(ACCENT_COLOR), # Highlight current 1
            run_time=0.6
        )
        
        # Animate swap of 5 and 1
        box_5 = number_boxes[0] # VGroup for 5
        box_1 = number_boxes[1] # VGroup for 1
        
        pos_5 = box_5.get_center()
        pos_1 = box_1.get_center()
        
        self.play(
            box_5.animate.move_to(pos_1).set_color(PRIMARY_COLOR), # Move 5 to 1's position
            box_1.animate.move_to(pos_5).set_color(PRIMARY_COLOR), # Move 1 to 5's position
            run_time=0.8
        )
        # Update the VGroup's logical order after the visual swap
        number_boxes.submobjects[0], number_boxes.submobjects[1] = number_boxes.submobjects[1], number_boxes.submobjects[0]
        
        self.wait(2.6) # Scene 4 ends

        self.remove(explain_text) # Instant removal


        # --- Scene 5: Solution (One Pass Animation) ---
        solution_text = Text("Repeat the process.", font_size=32, color=TEXT_COLOR).next_to(number_boxes, UP, buff=0.8)
        
        self.play(Write(solution_text), run_time=0.6)
        
        # Current logical state: [1, 5, 4, 2, 8]
        # Animate comparison of (5,4)
        self.play(
            number_boxes[1][0].animate.set_stroke_color(ACCENT_COLOR), # Highlight current 5
            number_boxes[2][0].animate.set_stroke_color(ACCENT_COLOR), # Highlight current 4
            run_time=0.6
        )
        # Swap 5 and 4
        box_5_current = number_boxes[1] # VGroup for 5
        box_4_current = number_boxes[2] # VGroup for 4
        
        pos_5_current = box_5_current.get_center()
        pos_4_current = box_4_current.get_center()
        
        self.play(
            box_5_current.animate.move_to(pos_4_current).set_color(PRIMARY_COLOR),
            box_4_current.animate.move_to(pos_5_current).set_color(PRIMARY_COLOR),
            run_time=0.8
        )
        number_boxes.submobjects[1], number_boxes.submobjects[2] = number_boxes.submobjects[2], number_boxes.submobjects[1]
        
        self.wait(2.6) # Scene 5 ends

        self.remove(solution_text) # Instant removal


        # --- Scene 6: Impact (Sorted Array) ---
        impact_text = Text("Eventually, all items", font_size=32, color=TEXT_COLOR).next_to(number_boxes, UP, buff=0.8)
        impact_text_2 = Text("are in perfect order!", font_size=32, color=TEXT_COLOR).next_to(impact_text, DOWN, buff=0.2)

        # Create sorted boxes for transition
        sorted_numbers = [1, 2, 4, 5, 8]
        sorted_boxes = VGroup()
        for i, num in enumerate(sorted_numbers):
            # Position based on the final arrangement of number_boxes
            box = create_number_box(num, number_boxes[i].get_center(), color=SUCCESS_COLOR) 
            sorted_boxes.add(box)

        self.play(
            FadeOut(number_boxes, shift=DOWN), # Fade out the old unsorted/partially sorted one
            Create(sorted_boxes), run_time=0.8 # Create sorted in place
        )
        self.play(Write(impact_text), run_time=0.6)
        self.play(Write(impact_text_2), run_time=0.6)
        self.wait(2.6) # Scene 6 ends

        self.remove(sorted_boxes, impact_text, impact_text_2) # Instant removal


        # --- Scene 7: Summary ---
        summary_title = Text("Bubble Sort Summary:", font_size=48, color=PRIMARY_COLOR, weight=BOLD).to_edge(UP)
        
        bullet1 = Text("• Compares adjacent elements.", font_size=36, color=TEXT_COLOR).next_to(summary_title, DOWN, buff=0.6).align_to(summary_title, LEFT)
        bullet2 = Text("• Swaps if they are out of order.", font_size=36, color=TEXT_COLOR).next_to(bullet1, DOWN, buff=0.4).align_to(bullet1, LEFT)
        bullet3 = Text("• Repeats until the list is sorted.", font_size=36, color=TEXT_COLOR).next_to(bullet2, DOWN, buff=0.4).align_to(bullet1, LEFT)

        self.play(Write(summary_title), run_time=0.5)
        self.play(Write(bullet1), run_time=0.5)
        self.play(Write(bullet2), run_time=0.5)
        self.play(Write(bullet3), run_time=0.5)
        self.wait(2.6) # Scene 7 ends and video concludes.