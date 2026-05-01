from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#1E1E2E"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Visual System Colors
        PRIMARY_NEON = TEAL_A
        ACCENT = PINK
        SUCCESS = GREEN
        WARNING = YELLOW_A
        PROBLEM = RED_B
        NEUTRAL = WHITE

        # Helper function to create a number block
        def create_number_block(number, color=NEUTRAL, rect_color=PRIMARY_NEON):
            rect = Square(side_length=1.0, color=rect_color, fill_opacity=0.2).set_stroke(width=2)
            num_text = Text(str(number), color=color, font_size=48)
            return VGroup(rect, num_text)

        # Helper function to get the number from a block
        def get_number_from_block(block):
            return int(block[1].text)

        # Initial unsorted array
        initial_numbers = [5, 1, 4, 2, 8]
        blocks = VGroup()
        for i, num in enumerate(initial_numbers):
            block = create_number_block(num).shift(i * 1.2 * RIGHT)
            blocks.add(block)
        blocks.center().shift(UP * 0.5)

        # --- SCENE 1: INTRO & UNSORTED LIST (Total ~4 sec) ---
        title = Text("Bubble Sort Algorithm", color=ACCENT, font_size=56).to_edge(UP)
        self.play(Write(title))
        self.wait(0.8)

        intro_text = Text("Let's sort this list:", color=NEUTRAL, font_size=36).next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(0.8)

        self.play(Create(blocks, run_time=1.0))
        self.wait(1.4) # Scene duration ends here: 0.8+0.8+1.0(runtime)+1.4 = 4.0s

        # Clear intro text to make room for explanation
        self.play(FadeOut(intro_text))
        
        # --- SCENE 2: FIRST PASS: COMPARE & SWAP (Total ~12 sec) ---
        explanation_text = Text("Compare adjacent, swap if wrong order.", color=NEUTRAL, font_size=36).next_to(title, DOWN, buff=0.5)
        self.play(Transform(title, Text("First Pass", color=ACCENT, font_size=56).to_edge(UP)), FadeIn(explanation_text))
        self.wait(1.0)

        current_blocks = blocks.copy()
        n = len(initial_numbers)
        
        # Function to swap two blocks visually and logically
        def swap_blocks(vg, i, j):
            block1, block2 = vg[i], vg[j]
            self.play(
                block1.animate.shift(block2.get_center() - block1.get_center()),
                block2.animate.shift(block1.get_center() - block2.get_center()),
                run_time=0.7
            )
            vg.submobjects[i], vg.submobjects[j] = vg.submobjects[j], vg.submobjects[i]

        pass_label = Text("Pass 1", color=PRIMARY_NEON, font_size=32).to_edge(LEFT).shift(UP*1.5)
        self.play(FadeIn(pass_label))
        self.wait(0.5)

        # Perform the first pass (4 comparisons)
        for i in range(n - 1): # n-1 comparisons
            block1 = current_blocks[i]
            block2 = current_blocks[i+1]
            num1 = get_number_from_block(block1)
            num2 = get_number_from_block(block2)

            self.play(
                block1.animate.set_stroke(color=WARNING, width=4),
                block2.animate.set_stroke(color=WARNING, width=4),
                run_time=0.6
            )
            self.wait(0.6) # Wait for highlight

            if num1 > num2:
                self.play(
                    block1[1].animate.set_color(PROBLEM),
                    block2[1].animate.set_color(PROBLEM),
                    run_time=0.6
                )
                self.wait(0.4) # Wait for problem indication
                swap_blocks(current_blocks, i, i+1) # run_time 0.7
                self.wait(0.4) # Wait after swap
                self.play(
                    block1[1].animate.set_color(NEUTRAL),
                    block2[1].animate.set_color(NEUTRAL),
                    block1.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    block2.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    run_time=0.6
                )
                self.wait(0.4) # Wait after reset
            else:
                self.play(
                    block1.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    block2.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    run_time=0.6
                )
                self.wait(0.6) # Wait for no swap reset
        
        # The last element is now sorted (number 8)
        self.play(
            current_blocks[n-1][0].animate.set_stroke(color=SUCCESS, width=4),
            current_blocks[n-1][1].animate.set_color(SUCCESS),
            run_time=0.8
        )
        self.wait(1.5) # Scene duration ends here: ~12s total
        
        self.play(FadeOut(explanation_text, pass_label))

        # --- SCENE 3: SUBSEQUENT PASSES: REFINEMENT (Total ~8 sec) ---
        self.play(Transform(title, Text("Subsequent Passes", color=ACCENT, font_size=56).to_edge(UP)))
        self.wait(0.8)
        
        pass_label_2 = Text("Pass 2", color=PRIMARY_NEON, font_size=32).to_edge(LEFT).shift(UP*1.5)
        self.play(FadeIn(pass_label_2))
        self.wait(0.5)

        # Perform a quicker second pass (3 comparisons)
        for i in range(n - 2): # n-2 comparisons
            block1 = current_blocks[i]
            block2 = current_blocks[i+1]
            num1 = get_number_from_block(block1)
            num2 = get_number_from_block(block2)

            self.play(
                block1.animate.set_stroke(color=WARNING, width=4),
                block2.animate.set_stroke(color=WARNING, width=4),
                run_time=0.6
            )
            self.wait(0.5) # Wait for highlight

            if num1 > num2: # This will happen for (4,2)
                self.play(
                    block1[1].animate.set_color(PROBLEM),
                    block2[1].animate.set_color(PROBLEM),
                    run_time=0.6
                )
                self.wait(0.5) # Wait for problem
                swap_blocks(current_blocks, i, i+1) # run_time 0.7
                self.wait(0.5) # Wait after swap
                self.play(
                    block1[1].animate.set_color(NEUTRAL),
                    block2[1].animate.set_color(NEUTRAL),
                    block1.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    block2.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    run_time=0.6
                )
                self.wait(0.5) # Wait after reset
            else: # This will happen for (1,4) and (4,5) (after 4-2 swap, it's 4-5)
                self.play(
                    block1.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    block2.animate.set_stroke(color=PRIMARY_NEON, width=2),
                    run_time=0.6
                )
                self.wait(0.5) # Wait for no swap reset
        
        # Mark the new sorted element (number 5)
        self.play(
            current_blocks[n-2][0].animate.set_stroke(color=SUCCESS, width=4),
            current_blocks[n-2][1].animate.set_color(SUCCESS),
            run_time=0.8
        )
        self.wait(1.0) # Scene duration ends here: ~8s total
        
        self.play(FadeOut(pass_label_2))

        # --- SCENE 4: CONCLUSION: SORTED LIST (Total ~6 sec) ---
        # Finish sorting the remaining elements to show the final state quickly
        for i in range(n - 2): # Elements 0, 1, 2
            self.play(
                current_blocks[i][0].animate.set_stroke(color=SUCCESS, width=4),
                current_blocks[i][1].animate.set_color(SUCCESS),
                run_time=0.4 # Quick visual highlight
            )
            self.wait(0.2) # Small pause
        
        self.wait(0.5)

        self.play(Transform(title, Text("Bubble Sort Complete!", color=ACCENT, font_size=56).to_edge(UP)))
        self.wait(1.0)
        
        summary_text = Text("Repeatedly compare and swap until sorted.", color=NEUTRAL, font_size=36).next_to(title, DOWN, buff=0.5)
        self.play(Write(summary_text))
        self.wait(2.5) # Scene duration ends here: ~6s total

        self.play(FadeOut(Group(*self.mobjects)))