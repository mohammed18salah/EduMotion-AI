from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Animation run_time for each play() call: 0.65 seconds
        # Total animation time: 9 plays * 0.65s = 5.85s
        # Total wait time: 7 scenes * 1.3s = 9.1s
        # Total video duration: 5.85s + 9.1s = 14.95s (approx. 15s)
        ANIM_RUN_TIME = 0.65
        WAIT_TIME = 1.3

        # Scene 1: Hook - Bold title + question
        title = Text("UNDERSTANDING MITREX", font_size=60, weight=BOLD).set_color(TEAL_A)
        question = Text("How does it work?", font_size=36).next_to(title, DOWN, buff=0.5).set_color(WHITE)
        
        self.play(
            Write(title),
            FadeIn(question, shift=UP),
            run_time=ANIM_RUN_TIME # Play 1
        )
        self.wait(WAIT_TIME)

        # Scene 2: Setup - Real-world context
        input_square = Square(side_length=1).set_color(TEAL_A).shift(LEFT * 3)
        process_arrow = Arrow(input_square.get_right(), RIGHT * 0.5, buff=0.1).set_color(WHITE)
        output_circle = Circle(radius=0.5).set_color(TEAL_A).shift(RIGHT * 3)
        setup_group = VGroup(input_square, process_arrow, output_circle)

        self.play(
            FadeOut(title, question), # Transition from S1
            Create(input_square),
            Create(process_arrow),
            Create(output_circle),
            run_time=ANIM_RUN_TIME # Play 2
        )
        self.wait(WAIT_TIME)

        # Scene 3: Problem - Show the challenge visually
        # Using a fixed seed for random-like positions for consistency, as `random` import is forbidden.
        # These are just predefined coordinates.
        noise_positions = [
            (-3.5, 1.5), (-2.8, -0.5), (-4.2, 0.8), (-3.0, 2.0), (-2.5, -1.8), (-3.8, 0)
        ]
        data_positions = [
            (-3.0, 0.0), (-2.0, 1.0), (-3.5, -1.0), (-2.2, -0.2)
        ]
        
        noise_squares = VGroup(*[
            Square(side_length=0.4).set_color(RED_B).move_to(pos[0] * RIGHT + pos[1] * UP)
            for pos in noise_positions
        ])
        data_squares = VGroup(*[
            Square(side_length=0.4).set_color(TEAL_A).move_to(pos[0] * RIGHT + pos[1] * UP)
            for pos in data_positions
        ])
        
        inlet_box = Rectangle(width=0.5, height=3).set_color(LIGHT_GRAY).shift(RIGHT * 4)
        problem_elements = VGroup(noise_squares, data_squares)

        self.play(
            FadeOut(setup_group), # Transition from S2
            LaggedStart(
                *[Create(sq) for sq in noise_squares],
                *[Create(sq) for sq in data_squares],
                lag_ratio=0.1
            ),
            Create(inlet_box),
            run_time=ANIM_RUN_TIME # Play 3
        )
        # Animate elements moving towards the inlet_box
        self.play(
            *[m.animate.shift(RIGHT * 7.5) for m in problem_elements],
            run_time=ANIM_RUN_TIME # Play 4
        )
        self.wait(WAIT_TIME)

        # Scene 4: Explanation - Core concept animated in detail
        mitrex_core = Rectangle(width=4, height=2).set_color(TEAL_A).shift(LEFT * 0.5)
        input_arrow_core = Arrow(LEFT * 4, mitrex_core.get_left() + LEFT * 0.1, buff=0.1).set_color(TEAL_A)
        output_arrow_core = Arrow(mitrex_core.get_right() + RIGHT * 0.1, RIGHT * 4, buff=0.1).set_color(TEAL_A)
        
        # Define initial positions for dots (simulating random)
        dot_start_positions = [
            LEFT*3.5 + 0.5*UP, LEFT*3.5 - 0.2*UP, LEFT*3.5 + 1.0*UP, # TEAL_A dots
            LEFT*3.5 - 0.8*UP, LEFT*3.5 + 0.0*UP                    # RED_B dots
        ]
        input_dots = VGroup(*[
            Dot(point=pos, radius=0.1, color=color) for pos, color in zip(dot_start_positions, [TEAL_A]*3 + [RED_B]*2)
        ])
        
        dot_animations = []
        for dot in input_dots:
            if dot.get_color() == TEAL_A:
                dot_animations.append(dot.animate.shift(RIGHT * 7.5)) # Pass through and exit
            else:
                # Move to a rejection point, shrink, and fade
                dot_animations.append(dot.animate.shift(RIGHT * 4).shift(UP * 0.5).set_color(RED_B).scale(0.5).fade(0.8))

        self.play(
            FadeOut(problem_elements, inlet_box), # Transition from S3
            Create(mitrex_core),
            Create(input_arrow_core),
            Create(output_arrow_core),
            FadeIn(input_dots),
            LaggedStart(*dot_animations, lag_ratio=0.1), # All dots move and filter
            run_time=ANIM_RUN_TIME # Play 5
        )
        self.wait(WAIT_TIME)

        # Scene 5: Solution - Step-by-step animated answer
        mitrex_processor = Rectangle(width=4, height=2).set_color(TEAL_A).shift(LEFT * 0.5)
        raw_input_start = Square(side_length=0.7).set_color(TEAL_A).shift(LEFT * 4)
        noise_element_start = Circle(radius=0.3).set_color(RED_B).shift(LEFT * 4 + UP * 0.5)
        
        # Target for raw_input to transform into, then move out
        processed_output_in_core = Circle(radius=0.5).set_color(GREEN).move_to(mitrex_processor.get_center())
        processed_output_final_position = processed_output_in_core.copy().shift(RIGHT * 3)

        self.play(
            FadeOut(mitrex_core, input_arrow_core, output_arrow_core, input_dots), # Transition from S4
            Create(mitrex_processor),
            FadeIn(raw_input_start),
            FadeIn(noise_element_start),
            raw_input_start.animate.move_to(mitrex_processor.get_center()), # Move input into processor
            noise_element_start.animate.move_to(mitrex_processor.get_left() + LEFT * 0.5).fade(0.8), # Noise rejected visually
            Transform(raw_input_start, processed_output_in_core), # Raw transforms to processed
            processed_output_in_core.animate.move_to(processed_output_final_position), # Move processed out
            run_time=ANIM_RUN_TIME # Play 6
        )
        self.wait(WAIT_TIME)
        
        # Scene 6: Impact - Why it matters
        # Fixed positions for chaos and order elements
        chaos_element_positions = [
            (-3.5, 1.5), (-2.8, -0.5), (-4.2, 0.8), (-3.0, 2.0), (-2.5, -1.8),
            (-3.8, 0), (-3.1, 0.5), (-2.4, 1.8), (-4.0, -1.5), (-2.9, -0.9)
        ]
        chaos_elements = VGroup(*[
            Square(side_length=0.3, color=color).move_to(pos[0] * RIGHT + pos[1] * UP)
            for pos, color in zip(chaos_element_positions, [RED_B, TEAL_A, RED_B, TEAL_A, RED_B, TEAL_A, RED_B, TEAL_A, RED_B, TEAL_A])
        ])
        
        order_elements = VGroup(*[
            Circle(radius=0.2, color=GREEN).shift(RIGHT*1.5 + j*UP*0.8 - UP*1.2) for j in range(3)
        ]).arrange(DOWN, buff=0.3)
        checkmark = Polygon(
            [-0.5, 0, 0], [0, -0.5, 0], [0.5, 0.5, 0]
        ).scale(0.8).rotate(PI/4).set_color(GREEN).next_to(order_elements, RIGHT, buff=0.8)

        self.play(
            FadeOut(mitrex_processor, raw_input_start, noise_element_start, processed_output_in_core), # Transition from S5
            FadeIn(chaos_elements),
            run_time=ANIM_RUN_TIME # Play 7
        )
        self.play(
            ReplacementTransform(chaos_elements, order_elements),
            Create(checkmark),
            run_time=ANIM_RUN_TIME # Play 8
        )
        self.wait(WAIT_TIME)

        # Scene 7: Summary - 3 bullet points animated
        bullet_points = VGroup(
            VGroup(Dot(color=PINK), Text("1. Filter Noise", font_size=32).set_color(WHITE).next_to(Dot(), RIGHT, buff=0.3)),
            VGroup(Dot(color=PINK), Text("2. Optimize Flow", font_size=32).set_color(WHITE).next_to(Dot(), RIGHT, buff=0.3)),
            VGroup(Dot(color=PINK), Text("3. Enhance Output", font_size=32).set_color(WHITE).next_to(Dot(), RIGHT, buff=0.3))
        ).arrange(DOWN, buff=0.5).center() # Arrange and center for presentation

        self.play(
            FadeOut(order_elements, checkmark), # Transition from S6
            FadeIn(bullet_points[0], shift=UP),
            FadeIn(bullet_points[1], shift=UP),
            FadeIn(bullet_points[2], shift=UP),
            run_time=ANIM_RUN_TIME # Play 9
        )
        self.wait(WAIT_TIME)