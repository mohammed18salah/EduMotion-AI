from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_width = 14.22
config.frame_height = 8.0
config.background_color = "#111111"


class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # SCENE 1: INTRO_PLANE_CIRCLE
        # -----------------------------------------------------------
        plane = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE, "stroke_width": 2},
            background_line_style={"stroke_opacity": 0.4, "stroke_color": WHITE},
            x_length=6,
            y_length=6
        ).add_coordinates(font_size=24, x_values=[-1, 0, 1], y_values=[-1, 0, 1])
        
        x_label = Text("x", color=WHITE).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("y", color=WHITE).next_to(plane.y_axis.get_end(), UP, buff=0.1)
        origin_label = Text("0", color=WHITE).next_to(plane.get_origin(), DL, buff=0.1)

        circle = Circle(radius=plane.get_x_unit_size(), color=TEAL_A, stroke_width=4).move_to(ORIGIN)

        self.play(Create(plane), Create(x_label), Create(y_label), Create(origin_label), run_time=1.5)
        self.play(Create(circle), run_time=1.0)
        self.wait(3)

        self.play(FadeOut(Group(plane, x_label, y_label, origin_label, circle)))
        self.wait(0.5)

        # SCENE 2: ANGLE_POINT
        # -----------------------------------------------------------
        plane = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE, "stroke_width": 2},
            background_line_style={"stroke_opacity": 0.4, "stroke_color": WHITE},
            x_length=6,
            y_length=6
        )
        circle = Circle(radius=plane.get_x_unit_size(), color=TEAL_A, stroke_width=4).move_to(ORIGIN)
        self.add(plane, circle)

        angle_text = Text("زاوية θ", font_size=36, color=PINK).shift(UP*1.5 + RIGHT*0.5)
        
        initial_angle = PI/4 # 45 degrees
        point_on_circle = Dot(circle.point_at_angle(initial_angle), color=PINK, radius=0.15)
        
        radius_line = Line(ORIGIN, point_on_circle.get_center(), color=PINK, stroke_width=4)
        
        arc = Arc(
            radius=0.3 * plane.get_x_unit_size(),
            start_angle=0,
            angle=initial_angle,
            arc_center=ORIGIN,
            color=PINK,
            stroke_width=3
        )
        
        self.play(Create(radius_line), run_time=1.0)
        self.play(Create(arc), Write(angle_text), run_time=1.5)
        self.play(Create(point_on_circle), run_time=0.8)
        self.wait(3)

        self.play(FadeOut(Group(plane, circle, point_on_circle, radius_line, arc, angle_text)))
        self.wait(0.5)

        # SCENE 3: COSINE_X_COORD
        # -----------------------------------------------------------
        plane = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE, "stroke_width": 2},
            background_line_style={"stroke_opacity": 0.4, "stroke_color": WHITE},
            x_length=6,
            y_length=6
        )
        circle = Circle(radius=plane.get_x_unit_size(), color=TEAL_A, stroke_width=4).move_to(ORIGIN)
        self.add(plane, circle)

        point_on_circle = Dot(circle.point_at_angle(initial_angle), color=PINK, radius=0.15)
        radius_line = Line(ORIGIN, point_on_circle.get_center(), color=PINK, stroke_width=4)
        arc = Arc(radius=0.3 * plane.get_x_unit_size(), start_angle=0, angle=initial_angle, arc_center=ORIGIN, color=PINK, stroke_width=3)
        self.add(point_on_circle, radius_line, arc)

        x_coord_actual_manim = point_on_circle.get_center()[0]

        projection_line_x = DashedLine(point_on_circle.get_center(), [x_coord_actual_manim, 0, 0], color=GREEN, stroke_width=3)
        x_value_line = Line(ORIGIN, [x_coord_actual_manim, 0, 0], color=GREEN, stroke_width=5)
        cos_label = Text("cos(θ) = x", font_size=36, color=GREEN).next_to(x_value_line, DOWN, buff=0.3)
        
        self.play(Create(projection_line_x), run_time=1.0)
        self.play(Create(x_value_line), run_time=1.0)
        self.play(Write(cos_label), run_time=1.0)
        self.wait(4)

        self.play(FadeOut(Group(projection_line_x, x_value_line, cos_label)))
        self.wait(0.5)

        # SCENE 4: SINE_Y_COORD
        # -----------------------------------------------------------
        # Plane, circle, point_on_circle, radius_line, arc are already present
        
        y_coord_actual_manim = point_on_circle.get_center()[1]

        projection_line_y = DashedLine(point_on_circle.get_center(), [0, y_coord_actual_manim, 0], color=YELLOW_A, stroke_width=3)
        y_value_line = Line(ORIGIN, [0, y_coord_actual_manim, 0], color=YELLOW_A, stroke_width=5)
        sin_label = Text("sin(θ) = y", font_size=36, color=YELLOW_A).next_to(y_value_line, LEFT, buff=0.3)

        self.play(Create(projection_line_y), run_time=1.0)
        self.play(Create(y_value_line), run_time=1.0)
        self.play(Write(sin_label), run_time=1.0)
        self.wait(4)

        self.play(FadeOut(Group(projection_line_y, y_value_line, sin_label)))
        self.wait(0.5)

        # SCENE 5: SUMMARY_DYNAMIC
        # -----------------------------------------------------------
        # Plane, circle, point_on_circle, radius_line, arc are already present
        cos_label_static = Text("cos(θ) = x", font_size=30, color=GREEN).shift(DOWN*2 + LEFT*1.5)
        sin_label_static = Text("sin(θ) = y", font_size=30, color=YELLOW_A).shift(DOWN*2 + RIGHT*1.5)
        self.add(cos_label_static, sin_label_static)

        dynamic_projection_x = DashedLine(point_on_circle.get_center(), [point_on_circle.get_center()[0], 0, 0], color=GREEN, stroke_width=3)
        dynamic_projection_y = DashedLine(point_on_circle.get_center(), [0, point_on_circle.get_center()[1], 0], color=YELLOW_A, stroke_width=3)
        
        dynamic_x_line = Line(ORIGIN, [point_on_circle.get_center()[0], 0, 0], color=GREEN, stroke_width=5)
        dynamic_y_line = Line(ORIGIN, [0, point_on_circle.get_center()[1], 0], color=YELLOW_A, stroke_width=5)

        self.add(dynamic_projection_x, dynamic_projection_y, dynamic_x_line, dynamic_y_line)

        def update_lines_and_arc(mobj):
            x_coord_current = point_on_circle.get_center()[0]
            y_coord_current = point_on_circle.get_center()[1]
            dynamic_projection_x.become(DashedLine(point_on_circle.get_center(), [x_coord_current, 0, 0], color=GREEN, stroke_width=3))
            dynamic_projection_y.become(DashedLine(point_on_circle.get_center(), [0, y_coord_current, 0], color=YELLOW_A, stroke_width=3))
            dynamic_x_line.become(Line(ORIGIN, [x_coord_current, 0, 0], color=GREEN, stroke_width=5))
            dynamic_y_line.become(Line(ORIGIN, [0, y_coord_current, 0], color=YELLOW_A, stroke_width=5))
            radius_line.put_start_and_end_on(ORIGIN, point_on_circle.get_center())

            current_angle = np.arctan2(y_coord_current, x_coord_current)
            if current_angle < 0:
                current_angle += 2 * PI
            arc.become(Arc(radius=0.3 * plane.get_x_unit_size(), start_angle=0, angle=current_angle, arc_center=ORIGIN, color=PINK, stroke_width=3))

        self.add_updater(update_lines_and_arc)

        self.play(
            MoveAlongPath(point_on_circle, circle.get_arc(initial_angle, initial_angle + PI*1.5)),
            run_time=3.0,
            rate_func=linear
        )
        
        self.remove_updater(update_lines_and_arc)
        
        self.wait(4)

        self.play(FadeOut(Group(*self.mobjects)))