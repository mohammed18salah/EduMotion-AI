from manim import *

class MainScene(Scene):
    def construct(self):
        header = Text("Bubble Sort", color=GOLD).to_edge(UP, buff=0.5)
        self.add(header)
        
        vals = [5, 2, 4, 1]
        cols = [TEAL, PINK, BLUE, ORANGE]
        m = []
        
        for i in range(4):
            r = Rectangle(width=1.3, height=1.3, stroke_width=8, stroke_color=cols[i])
            txt = Text(str(vals[i]))
            m.append(VGroup(r, txt))
        
        objs = VGroup(*m).arrange(RIGHT, buff=0.6)
        self.play(FadeIn(objs), run_time=0.5)

        for i in range(3):
            for j in range(3 - i):
                # Indicate comparison by shifting up
                self.play(
                    m[j].animate.shift(UP * 0.3), 
                    m[j+1].animate.shift(UP * 0.3), 
                    run_time=0.2
                )
                
                if vals[j] > vals[j+1]:
                    # Swap logic
                    vals[j], vals[j+1] = vals[j+1], vals[j]
                    p1 = m[j].get_center().copy()
                    p2 = m[j+1].get_center().copy()
                    
                    self.play(
                        m[j].animate.move_to(p2),
                        m[j+1].animate.move_to(p1),
                        run_time=0.4
                    )
                    # Swap indices in the list to track positions
                    m[j], m[j+1] = m[j+1], m[j]
                else:
                    self.wait(0.1)
                
                # Shift back down
                self.play(
                    m[j].animate.shift(DOWN * 0.3), 
                    m[j+1].animate.shift(DOWN * 0.3), 
                    run_time=0.2
                )
        
        # Success state
        final_group = VGroup(*m)
        self.play(final_group.animate.set_color(GREEN), run_time=0.5)
        self.wait(1)