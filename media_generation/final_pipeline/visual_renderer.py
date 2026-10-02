from manim import *
import os
import re
import json


# ─────────────────────────────────────────────
# LOAD SCENE DATA FROM ENV
# ─────────────────────────────────────────────

def load_scene():
    raw = os.environ.get("EDU_SCENE_JSON", "")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    return {
        "title": os.environ.get("EDU_TITLE", "Educational Lesson"),
        "narration": os.environ.get("EDU_DESCRIPTION", ""),
        "visual_type": "text_explanation",
        "keywords": [],
        "objects": [],
        "labels": [],
        "equations": [],
        "animation": "fade_in_text",
        "language": "en",
    }


PALETTE = {
    "bg":     "#F8FAFC",
    "dark":   "#0F172A",
    "blue":   "#2563EB",
    "orange": "#F97316",
    "green":  "#16A34A",
    "red":    "#DC2626",
    "purple": "#7C3AED",
    "yellow": "#EAB308",
    "teal":   "#0D9488",
    "slate":  "#64748B",
    "white":  "#FFFFFF",
}

COLORS = [
    PALETTE["blue"], PALETTE["orange"], PALETTE["green"],
    PALETTE["purple"], PALETTE["red"], PALETTE["teal"],
]


def wrap(text, width=42):
    """Hard-wrap text to fit Manim canvas."""
    words = text.split()
    lines, line = [], []
    for w in words:
        if sum(len(x) for x in line) + len(line) + len(w) > width:
            lines.append(" ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        lines.append(" ".join(line))
    return "\n".join(lines)


def safe_text(t, size=28, color=None, bold=False):
    color = color or PALETTE["dark"]
    weight = BOLD if bold else NORMAL
    t = t[:120]
    return Text(t, font_size=size, color=color, weight=weight,
                line_spacing=1.3)


# ─────────────────────────────────────────────
# MAIN SCENE CLASS
# ─────────────────────────────────────────────

class EducationalScene(Scene):

    def construct(self):
        scene_data = load_scene()
        self.camera.background_color = PALETTE["bg"]

        vtype = scene_data.get("visual_type", "text_explanation")

        dispatch = {
            "title_card":         self.render_title_card,
            "text_explanation":   self.render_text_explanation,
            "bullet_explanation": self.render_bullet_explanation,
            "process_flow":       self.render_process_flow,
            "cycle":              self.render_cycle,
            "timeline":           self.render_timeline,
            "comparison":         self.render_comparison,
            "diagram":            self.render_diagram,
            "equation":           self.render_equation,
            "mathematical_steps": self.render_mathematical_steps,
            "physics_motion":     self.render_physics_motion,
            "graph":              self.render_graph,
            "concept_map":        self.render_concept_map,
            "nature_scene":       self.render_nature_scene,
            "real_world_example": self.render_real_world_example,
            "summary":            self.render_summary,
        }

        renderer = dispatch.get(vtype, self.render_text_explanation)
        renderer(scene_data)
        self.wait(0.5)

    # ─────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────

    def draw_header(self, title):
        bar = Rectangle(
            width=14.2, height=0.9,
            fill_color=PALETTE["blue"],
            fill_opacity=1, stroke_width=0
        ).to_edge(UP, buff=0)
        t = Text(title[:55], font_size=28, color=PALETTE["white"],
                 weight=BOLD)
        t.move_to(bar.get_center())
        self.play(FadeIn(bar), Write(t), run_time=0.7)
        return VGroup(bar, t)

    def draw_narration_box(self, narration, y=-2.8):
        txt = wrap(narration, 60)
        t = Text(txt, font_size=20, color=PALETTE["slate"],
                 line_spacing=1.2)
        t.scale_to_fit_width(12.5)
        box = RoundedRectangle(
            width=13, height=max(1.0, t.height + 0.5),
            corner_radius=0.2,
            fill_color="#EFF6FF", fill_opacity=1,
            stroke_color=PALETTE["blue"], stroke_width=1.5
        )
        box.move_to([0, y, 0])
        t.move_to(box.get_center())
        self.play(FadeIn(box), FadeIn(t), run_time=0.6)
        return VGroup(box, t)

    # ─────────────────────────────────────────
    # TITLE CARD
    # ─────────────────────────────────────────

    def render_title_card(self, d):
        title = d.get("title", "Educational Lesson")
        narration = d.get("narration", "")
        keywords = d.get("keywords", [])

        bg = Rectangle(
            width=14.2, height=8.1,
            fill_color=PALETTE["blue"], fill_opacity=1, stroke_width=0
        )
        self.add(bg)

        t = Text(wrap(title, 30), font_size=48, color=PALETTE["white"],
                 weight=BOLD, line_spacing=1.2)
        t.scale_to_fit_width(11)
        t.move_to(UP * 1.2)
        self.play(Write(t), run_time=1.2)

        if narration:
            sub = Text(wrap(narration[:80], 50), font_size=24,
                       color="#BFDBFE", line_spacing=1.3)
            sub.scale_to_fit_width(10)
            sub.next_to(t, DOWN, buff=0.6)
            self.play(FadeIn(sub, shift=UP * 0.3), run_time=0.8)

        if keywords:
            kw_group = VGroup()
            for i, kw in enumerate(keywords[:5]):
                pill_bg = RoundedRectangle(
                    width=len(kw) * 0.18 + 0.6, height=0.45,
                    corner_radius=0.2,
                    fill_color=PALETTE["orange"], fill_opacity=0.9,
                    stroke_width=0
                )
                pill_t = Text(kw, font_size=18, color=PALETTE["white"])
                pill_t.move_to(pill_bg.get_center())
                kw_group.add(VGroup(pill_bg, pill_t))
            kw_group.arrange(RIGHT, buff=0.3)
            kw_group.move_to(DOWN * 2.5)
            self.play(FadeIn(kw_group, shift=UP * 0.2), run_time=0.7)

        self.wait(2)

    # ─────────────────────────────────────────
    # TEXT EXPLANATION
    # ─────────────────────────────────────────

    def render_text_explanation(self, d):
        header = self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        keywords = d.get("keywords", [])

        txt = wrap(narration, 52)
        t = Text(txt, font_size=26, color=PALETTE["dark"], line_spacing=1.4)
        t.scale_to_fit_width(11.5)
        t.move_to(UP * 0.3)
        box = RoundedRectangle(
            width=12.5, height=max(2.5, t.height + 0.8),
            corner_radius=0.3,
            fill_color=PALETTE["white"], fill_opacity=1,
            stroke_color="#CBD5E1", stroke_width=2
        )
        box.move_to(t.get_center())
        self.play(FadeIn(box), Write(t), run_time=1.0)

        if keywords:
            dots = VGroup()
            for i, kw in enumerate(keywords[:4]):
                c = Circle(radius=0.35, fill_color=COLORS[i % len(COLORS)],
                           fill_opacity=0.85, stroke_width=0)
                kt = Text(kw[:12], font_size=16, color=PALETTE["white"])
                kt.scale_to_fit_width(0.62)
                kt.move_to(c.get_center())
                dots.add(VGroup(c, kt))
            dots.arrange(RIGHT, buff=0.5)
            dots.move_to(DOWN * 2.8)
            self.play(FadeIn(dots, shift=UP * 0.2), run_time=0.6)

        self.wait(2.5)

    # ─────────────────────────────────────────
    # BULLET EXPLANATION
    # ─────────────────────────────────────────

    def render_bullet_explanation(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        sentences = [s.strip() for s in re.split(r"[।,;]+", narration)
                     if len(s.strip()) > 8][:5]
        if not sentences:
            sentences = [narration[:100]]

        bullets = VGroup()
        for i, s in enumerate(sentences):
            dot = Circle(radius=0.12, fill_color=COLORS[i % len(COLORS)],
                         fill_opacity=1, stroke_width=0)
            txt = Text(s[:70], font_size=22, color=PALETTE["dark"])
            txt.scale_to_fit_width(10.5)
            dot.next_to(txt, LEFT, buff=0.25)
            row = VGroup(dot, txt)
            bullets.add(row)

        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        bullets.move_to(ORIGIN + UP * 0.3)
        bullets.scale_to_fit_height(5.5)

        for i, row in enumerate(bullets):
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.45)
        self.wait(2)

    # ─────────────────────────────────────────
    # PROCESS FLOW
    # ─────────────────────────────────────────

    def render_process_flow(self, d):
        self.draw_header(d.get("title", ""))
        labels = d.get("labels") or d.get("keywords", [])
        narration = d.get("narration", "")

        # Derive steps from labels or split narration
        if not labels:
            parts = [s.strip() for s in re.split(r"[।,;]+", narration)
                     if len(s.strip()) > 5][:5]
            labels = parts if parts else ["Start", "Process", "Result"]

        labels = labels[:5]
        n = len(labels)
        spacing = min(2.6, 11.0 / n)

        nodes = VGroup()
        for i, lbl in enumerate(labels):
            rect = RoundedRectangle(
                width=2.0, height=0.9, corner_radius=0.2,
                fill_color=COLORS[i % len(COLORS)], fill_opacity=0.9,
                stroke_width=0
            )
            lt = Text(lbl[:18], font_size=20, color=PALETTE["white"],
                      weight=BOLD)
            lt.scale_to_fit_width(1.8)
            lt.move_to(rect.get_center())
            node = VGroup(rect, lt)
            node.move_to(RIGHT * (i - (n - 1) / 2) * spacing)
            nodes.add(node)

        nodes.move_to(ORIGIN)

        arrows = VGroup()
        for i in range(n - 1):
            a = Arrow(
                nodes[i].get_right(), nodes[i + 1].get_left(),
                buff=0.1, color=PALETTE["slate"], stroke_width=3
            )
            arrows.add(a)

        for node in nodes:
            self.play(FadeIn(node, shift=UP * 0.3), run_time=0.4)
        for arrow in arrows:
            self.play(GrowArrow(arrow), run_time=0.35)

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # CYCLE
    # ─────────────────────────────────────────

    def render_cycle(self, d):
        self.draw_header(d.get("title", ""))
        labels = d.get("labels") or d.get("keywords", [])
        narration = d.get("narration", "")

        if not labels:
            parts = [s.strip() for s in re.split(r"[।,;]+", narration)
                     if len(s.strip()) > 5][:4]
            labels = parts if parts else ["Stage 1", "Stage 2",
                                          "Stage 3", "Stage 4"]
        labels = labels[:6]
        n = len(labels)
        radius = 2.0

        nodes = VGroup()
        positions = []
        for i in range(n):
            angle = PI / 2 - i * (2 * PI / n)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            positions.append(pos)
            circ = Circle(radius=0.55,
                          fill_color=COLORS[i % len(COLORS)],
                          fill_opacity=0.9, stroke_width=0)
            lt = Text(labels[i][:14], font_size=18, color=PALETTE["white"],
                      weight=BOLD)
            lt.scale_to_fit_width(0.95)
            lt.move_to(circ.get_center())
            node = VGroup(circ, lt)
            node.move_to(pos)
            nodes.add(node)

        arrows = VGroup()
        for i in range(n):
            src = positions[i]
            dst = positions[(i + 1) % n]
            mid = (src + dst) / 2
            direction = dst - src
            norm = np.array([-direction[1], direction[0], 0])
            norm = norm / (np.linalg.norm(norm) + 1e-9)
            ctrl = mid + norm * 0.4
            a = CurvedArrow(src, dst, angle=TAU / 8,
                            color=PALETTE["slate"], stroke_width=2.5)
            arrows.add(a)

        for node in nodes:
            self.play(FadeIn(node, scale=0.8), run_time=0.35)
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.3)

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # TIMELINE
    # ─────────────────────────────────────────

    def render_timeline(self, d):
        self.draw_header(d.get("title", ""))
        labels = d.get("labels") or d.get("keywords", [])
        narration = d.get("narration", "")

        if not labels:
            parts = [s.strip() for s in re.split(r"[।,;]+", narration)
                     if len(s.strip()) > 5][:5]
            labels = parts if parts else ["Event 1", "Event 2", "Event 3"]
        labels = labels[:5]
        n = len(labels)

        line = Line(LEFT * 5.5, RIGHT * 5.5,
                    color=PALETTE["blue"], stroke_width=3)
        line.move_to(ORIGIN)
        self.play(Create(line), run_time=0.6)

        spacing = 11.0 / (n + 1)
        for i, lbl in enumerate(labels):
            x = -5.5 + spacing * (i + 1)
            dot = Circle(radius=0.22,
                         fill_color=COLORS[i % len(COLORS)],
                         fill_opacity=1, stroke_width=0)
            dot.move_to([x, 0, 0])

            above = (i % 2 == 0)
            y_off = 1.1 if above else -1.1
            txt = Text(lbl[:20], font_size=19, color=PALETTE["dark"])
            txt.scale_to_fit_width(min(1.9, len(lbl) * 0.13))
            txt.move_to([x, y_off, 0])

            connector = Line([x, 0, 0], [x, y_off * 0.75, 0],
                             color=PALETTE["slate"], stroke_width=1.5)

            self.play(
                FadeIn(dot), Create(connector), FadeIn(txt),
                run_time=0.4
            )

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # COMPARISON
    # ─────────────────────────────────────────

    def render_comparison(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        labels = d.get("labels", [])

        # Split narration into two halves for left/right
        parts = [s.strip() for s in re.split(r"[।,;]+", narration)
                 if len(s.strip()) > 5]
        left_text = parts[0] if len(parts) > 0 else narration[:60]
        right_text = parts[1] if len(parts) > 1 else narration[60:120]

        left_lbl = labels[0] if len(labels) > 0 else "A"
        right_lbl = labels[1] if len(labels) > 1 else "B"

        divider = Line(UP * 2.8, DOWN * 2.8,
                       color=PALETTE["slate"], stroke_width=2)
        self.play(Create(divider), run_time=0.4)

        for side, text, lbl, color, x in [
            ("left",  left_text,  left_lbl,  PALETTE["blue"],   -3.2),
            ("right", right_text, right_lbl, PALETTE["orange"],  3.2),
        ]:
            header_box = RoundedRectangle(
                width=5.5, height=0.75, corner_radius=0.2,
                fill_color=color, fill_opacity=1, stroke_width=0
            )
            header_box.move_to([x, 2.2, 0])
            ht = Text(lbl[:20], font_size=24, color=PALETTE["white"],
                      weight=BOLD)
            ht.move_to(header_box.get_center())

            body = RoundedRectangle(
                width=5.5, height=3.2, corner_radius=0.2,
                fill_color=PALETTE["white"], fill_opacity=1,
                stroke_color=color, stroke_width=2
            )
            body.move_to([x, -0.4, 0])
            bt = Text(wrap(text, 28), font_size=21,
                      color=PALETTE["dark"], line_spacing=1.3)
            bt.scale_to_fit_width(5.0)
            bt.move_to(body.get_center())

            self.play(
                FadeIn(header_box), Write(ht),
                FadeIn(body), FadeIn(bt),
                run_time=0.6
            )

        self.wait(2.5)

    # ─────────────────────────────────────────
    # DIAGRAM
    # ─────────────────────────────────────────

    def render_diagram(self, d):
        self.draw_header(d.get("title", ""))
        labels = d.get("labels") or d.get("keywords", [])
        narration = d.get("narration", "")

        if not labels:
            labels = ["Part A", "Part B", "Part C"]
        labels = labels[:6]
        n = len(labels)

        # Central node
        center = Circle(radius=0.7,
                        fill_color=PALETTE["blue"], fill_opacity=0.9,
                        stroke_width=0)
        ct = Text(d.get("title", "")[:12], font_size=20,
                  color=PALETTE["white"], weight=BOLD)
        ct.scale_to_fit_width(1.2)
        ct.move_to(center.get_center())
        central = VGroup(center, ct)
        central.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(central, scale=0.7), run_time=0.5)

        # Satellite nodes
        for i, lbl in enumerate(labels):
            angle = i * (2 * PI / n)
            pos = central.get_center() + 2.5 * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            sat = Circle(radius=0.5,
                         fill_color=COLORS[i % len(COLORS)],
                         fill_opacity=0.85, stroke_width=0)
            sat.move_to(pos)
            st = Text(lbl[:14], font_size=17, color=PALETTE["white"])
            st.scale_to_fit_width(0.88)
            st.move_to(sat.get_center())

            line = Line(central.get_center(), pos,
                        color=PALETTE["slate"], stroke_width=1.8)

            self.play(
                Create(line),
                FadeIn(VGroup(sat, st), scale=0.8),
                run_time=0.4
            )

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # EQUATION
    # ─────────────────────────────────────────

    def render_equation(self, d):
        self.draw_header(d.get("title", ""))
        equations = d.get("equations", [])
        narration = d.get("narration", "")
        keywords = d.get("keywords", [])

        if not equations:
            # Try to pull equation-like text from narration
            found = re.findall(
                r"[A-Za-z\d\s\+\-\*\/\^=²³]{3,40}=[^\n,।]{1,30}",
                narration
            )
            equations = [f.strip() for f in found[:3]]

        if not equations:
            equations = [narration[:60]]

        y_start = 1.5
        for i, eq in enumerate(equations[:3]):
            box = RoundedRectangle(
                width=10, height=1.1, corner_radius=0.25,
                fill_color="#EFF6FF", fill_opacity=1,
                stroke_color=PALETTE["blue"], stroke_width=2
            )
            box.move_to([0, y_start - i * 1.5, 0])
            et = Text(eq[:60], font_size=30, color=PALETTE["blue"],
                      weight=BOLD)
            et.scale_to_fit_width(9.2)
            et.move_to(box.get_center())
            self.play(FadeIn(box), Write(et), run_time=0.7)

        if keywords:
            kw_row = VGroup()
            for i, kw in enumerate(keywords[:4]):
                pill = RoundedRectangle(
                    width=len(kw) * 0.17 + 0.5, height=0.42,
                    corner_radius=0.18,
                    fill_color=COLORS[i % len(COLORS)], fill_opacity=0.85,
                    stroke_width=0
                )
                pt = Text(kw[:14], font_size=17, color=PALETTE["white"])
                pt.move_to(pill.get_center())
                kw_row.add(VGroup(pill, pt))
            kw_row.arrange(RIGHT, buff=0.3)
            kw_row.move_to(DOWN * 2.8)
            self.play(FadeIn(kw_row), run_time=0.5)

        self.draw_narration_box(narration[:100], y=-3.2)
        self.wait(2)

    # ─────────────────────────────────────────
    # MATHEMATICAL STEPS
    # ─────────────────────────────────────────

    def render_mathematical_steps(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        steps = [s.strip() for s in re.split(r"[।,;]+", narration)
                 if len(s.strip()) > 5][:5]
        if not steps:
            steps = [narration[:80]]

        for i, step in enumerate(steps):
            num_circ = Circle(radius=0.28,
                              fill_color=PALETTE["orange"],
                              fill_opacity=1, stroke_width=0)
            num_t = Text(str(i + 1), font_size=20,
                         color=PALETTE["white"], weight=BOLD)
            num_t.move_to(num_circ.get_center())

            step_box = RoundedRectangle(
                width=10.5, height=0.75, corner_radius=0.2,
                fill_color=PALETTE["white"], fill_opacity=1,
                stroke_color="#CBD5E1", stroke_width=1.5
            )
            st = Text(step[:70], font_size=22, color=PALETTE["dark"])
            st.scale_to_fit_width(10.0)
            st.move_to(step_box.get_center())

            row = VGroup(VGroup(num_circ, num_t), step_box)
            row.arrange(RIGHT, buff=0.3)
            row.move_to([0, 2.0 - i * 1.1, 0])

            self.play(
                FadeIn(VGroup(num_circ, num_t)),
                FadeIn(step_box), FadeIn(st),
                run_time=0.45
            )

        self.wait(2)

    # ─────────────────────────────────────────
    # PHYSICS MOTION
    # ─────────────────────────────────────────

    def render_physics_motion(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        labels = d.get("labels", [])

        # Ground
        ground = Line(LEFT * 5.5, RIGHT * 5.5,
                      color=PALETTE["slate"], stroke_width=3)
        ground.move_to(DOWN * 1.5)
        self.play(Create(ground), run_time=0.4)

        # Object block
        block = Rectangle(
            width=1.2, height=0.8,
            fill_color=PALETTE["blue"], fill_opacity=0.9,
            stroke_width=0
        )
        block.move_to(LEFT * 3.5 + DOWN * 1.1)
        block_lbl = Text(labels[0][:8] if labels else "m",
                         font_size=22, color=PALETTE["white"], weight=BOLD)
        block_lbl.move_to(block.get_center())
        obj = VGroup(block, block_lbl)
        self.play(FadeIn(obj), run_time=0.4)

        # Force arrow
        force_arrow = Arrow(
            obj.get_right(), obj.get_right() + RIGHT * 2.2,
            buff=0, color=PALETTE["orange"], stroke_width=5
        )
        force_lbl = Text(labels[1][:8] if len(labels) > 1 else "F",
                         font_size=22, color=PALETTE["orange"], weight=BOLD)
        force_lbl.next_to(force_arrow, UP, buff=0.15)
        self.play(GrowArrow(force_arrow), FadeIn(force_lbl), run_time=0.5)

        # Animate motion
        self.play(
            obj.animate.shift(RIGHT * 4.5),
            force_arrow.animate.shift(RIGHT * 4.5),
            force_lbl.animate.shift(RIGHT * 4.5),
            run_time=1.5, rate_func=linear
        )

        # Velocity arrow
        vel_arrow = Arrow(
            obj.get_top(), obj.get_top() + RIGHT * 1.5,
            buff=0, color=PALETTE["green"], stroke_width=4
        )
        vel_lbl = Text(labels[2][:8] if len(labels) > 2 else "v",
                       font_size=20, color=PALETTE["green"])
        vel_lbl.next_to(vel_arrow, UP, buff=0.1)
        self.play(GrowArrow(vel_arrow), FadeIn(vel_lbl), run_time=0.4)

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # GRAPH
    # ─────────────────────────────────────────

    def render_graph(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        labels = d.get("labels", [])

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"color": PALETTE["dark"], "stroke_width": 2},
            tips=True,
        )
        axes.move_to(ORIGIN + DOWN * 0.3)

        x_lbl = Text(labels[0][:16] if labels else "X",
                     font_size=20, color=PALETTE["dark"])
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.3)
        y_lbl = Text(labels[1][:16] if len(labels) > 1 else "Y",
                     font_size=20, color=PALETTE["dark"])
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.3)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # Draw a smooth rising curve
        curve = axes.plot(
            lambda x: 0.15 * x ** 2,
            x_range=[0, 5.5],
            color=PALETTE["blue"],
            stroke_width=3
        )
        self.play(Create(curve), run_time=1.0)

        # Highlight a point
        dot = Dot(axes.c2p(3, 0.15 * 9), color=PALETTE["orange"], radius=0.12)
        self.play(FadeIn(dot, scale=1.5), run_time=0.4)

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # CONCEPT MAP
    # ─────────────────────────────────────────

    def render_concept_map(self, d):
        self.draw_header(d.get("title", ""))
        keywords = d.get("keywords", [])
        narration = d.get("narration", "")

        if not keywords:
            keywords = [s.strip() for s in re.split(r"[।,;]+", narration)
                        if len(s.strip()) > 4][:5]
        if not keywords:
            keywords = ["Concept"]

        central_kw = keywords[0]
        branches = keywords[1:6]

        center_circ = Circle(radius=0.8,
                             fill_color=PALETTE["blue"], fill_opacity=0.9,
                             stroke_width=0)
        ct = Text(central_kw[:14], font_size=22,
                  color=PALETTE["white"], weight=BOLD)
        ct.scale_to_fit_width(1.4)
        ct.move_to(center_circ.get_center())
        central = VGroup(center_circ, ct)
        central.move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(central, scale=0.7), run_time=0.5)

        n = len(branches)
        for i, kw in enumerate(branches):
            angle = -PI / 2 + i * (PI / max(n - 1, 1)) if n > 1 else 0
            dist = 2.8
            pos = central.get_center() + dist * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            node = RoundedRectangle(
                width=max(1.6, len(kw) * 0.18), height=0.6,
                corner_radius=0.2,
                fill_color=COLORS[(i + 1) % len(COLORS)], fill_opacity=0.85,
                stroke_width=0
            )
            node.move_to(pos)
            nt = Text(kw[:16], font_size=19, color=PALETTE["white"])
            nt.scale_to_fit_width(node.width - 0.2)
            nt.move_to(node.get_center())
            edge = Line(central.get_center(), pos,
                        color=PALETTE["slate"], stroke_width=1.8)
            self.play(
                Create(edge),
                FadeIn(VGroup(node, nt), scale=0.8),
                run_time=0.4
            )

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # NATURE SCENE
    # ─────────────────────────────────────────

    def render_nature_scene(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        keywords = d.get("keywords", [])
        text_lower = narration.lower()

        elements = VGroup()

        # Sun
        if any(w in text_lower for w in
               ["sun", "solar", "सूरज", "सूर्य", "किरण"]):
            sun = Circle(radius=0.7, fill_color=PALETTE["yellow"],
                         fill_opacity=0.95, stroke_width=0)
            sun.move_to(UP * 2.2 + RIGHT * 4)
            rays = VGroup()
            for ang in range(0, 360, 30):
                ray = Line(
                    sun.get_center(),
                    sun.get_center() + 1.2 * np.array(
                        [np.cos(ang * DEGREES), np.sin(ang * DEGREES), 0]
                    ),
                    color=PALETTE["yellow"], stroke_width=2
                )
                rays.add(ray)
            elements.add(VGroup(rays, sun))

        # Tree
        if any(w in text_lower for w in
               ["tree", "plant", "leaf", "पेड़", "पौधा", "पत्ती", "लता", "तरु"]):
            trunk = Rectangle(
                width=0.45, height=1.8,
                fill_color="#92400E", fill_opacity=1, stroke_width=0
            )
            trunk.move_to(LEFT * 2 + DOWN * 0.5)
            for pos, r in [(UP * 1.4, 0.85), (LEFT * 0.7 + UP * 0.9, 0.65),
                           (RIGHT * 0.7 + UP * 0.9, 0.65)]:
                leaf = Circle(radius=r, fill_color=PALETTE["green"],
                              fill_opacity=0.8, stroke_width=0)
                leaf.move_to(trunk.get_top() + pos)
                elements.add(leaf)
            elements.add(trunk)

        # River / water
        if any(w in text_lower for w in
               ["river", "water", "नदी", "जल", "जलधारा", "पानी"]):
            for i in range(3):
                wave = Arc(radius=1.5, angle=PI,
                           color=PALETTE["teal"], stroke_width=2.5)
                wave.move_to(DOWN * 2.0 + LEFT * (1.5 - i * 1.5))
                elements.add(wave)

        # Flower
        if any(w in text_lower for w in
               ["flower", "फूल", "पुष्प"]):
            stem = Line(DOWN * 2.5, DOWN * 1.2,
                        color=PALETTE["green"], stroke_width=3)
            stem.move_to(RIGHT * 1.5 + DOWN * 0.5)
            petals = VGroup()
            for ang in range(0, 360, 60):
                p = Ellipse(width=0.4, height=0.25,
                            fill_color=PALETTE["orange"], fill_opacity=0.85,
                            stroke_width=0)
                p.move_to(
                    RIGHT * 1.5 + DOWN * 0.2 +
                    0.45 * np.array([np.cos(ang * DEGREES),
                                     np.sin(ang * DEGREES), 0])
                )
                petals.add(p)
            center_dot = Circle(radius=0.18, fill_color=PALETTE["yellow"],
                                fill_opacity=1, stroke_width=0)
            center_dot.move_to(RIGHT * 1.5 + DOWN * 0.2)
            elements.add(stem, petals, center_dot)

        if len(elements) == 0:
            # Generic nature fallback: sky gradient + ground
            sky = Rectangle(width=14.2, height=4,
                            fill_color="#BFDBFE", fill_opacity=0.5,
                            stroke_width=0)
            sky.move_to(UP * 1)
            ground_rect = Rectangle(width=14.2, height=1.5,
                                    fill_color="#86EFAC", fill_opacity=0.6,
                                    stroke_width=0)
            ground_rect.move_to(DOWN * 2.5)
            elements.add(sky, ground_rect)

        self.play(FadeIn(elements, shift=UP * 0.2), run_time=1.0)

        # Keyword labels
        if keywords:
            kw_group = VGroup()
            for i, kw in enumerate(keywords[:4]):
                pill_bg = RoundedRectangle(
                    width=len(kw) * 0.17 + 0.5, height=0.42,
                    corner_radius=0.18,
                    fill_color=COLORS[i % len(COLORS)], fill_opacity=0.85,
                    stroke_width=0
                )
                pill_t = Text(kw[:16], font_size=17, color=PALETTE["white"])
                pill_t.move_to(pill_bg.get_center())
                kw_group.add(VGroup(pill_bg, pill_t))
            kw_group.arrange(RIGHT, buff=0.3)
            kw_group.move_to(DOWN * 3.0)
            self.play(FadeIn(kw_group), run_time=0.5)

        self.draw_narration_box(narration[:120])
        self.wait(2)

    # ─────────────────────────────────────────
    # REAL WORLD EXAMPLE
    # ─────────────────────────────────────────

    def render_real_world_example(self, d):
        self.draw_header(d.get("title", ""))
        narration = d.get("narration", "")
        keywords = d.get("keywords", [])

        # Spotlight circle
        spotlight = Circle(radius=1.8,
                           fill_color=PALETTE["yellow"], fill_opacity=0.15,
                           stroke_color=PALETTE["yellow"], stroke_width=2)
        spotlight.move_to(UP * 0.5)
        self.play(Create(spotlight), run_time=0.5)

        icon_t = Text("💡", font_size=60)
        icon_t.move_to(spotlight.get_center())
        self.play(FadeIn(icon_t, scale=0.5), run_time=0.5)

        txt = wrap(narration[:100], 44)
        body = Text(txt, font_size=23, color=PALETTE["dark"], line_spacing=1.3)
        body.scale_to_fit_width(11)
        body.move_to(DOWN * 2.0)
        self.play(FadeIn(body, shift=UP * 0.2), run_time=0.7)

        if keywords:
            kw_row = VGroup()
            for i, kw in enumerate(keywords[:4]):
                pill = RoundedRectangle(
                    width=len(kw) * 0.17 + 0.5, height=0.42,
                    corner_radius=0.18,
                    fill_color=COLORS[i % len(COLORS)], fill_opacity=0.85,
                    stroke_width=0
                )
                pt = Text(kw[:14], font_size=17, color=PALETTE["white"])
                pt.move_to(pill.get_center())
                kw_row.add(VGroup(pill, pt))
            kw_row.arrange(RIGHT, buff=0.3)
            kw_row.move_to(DOWN * 3.2)
            self.play(FadeIn(kw_row), run_time=0.4)

        self.wait(2.5)

    # ─────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────

    def render_summary(self, d):
        self.draw_header(d.get("title", ""))
        keywords = d.get("keywords", [])
        narration = d.get("narration", "")

        points = keywords if keywords else [
            s.strip() for s in re.split(r"[।,;]+", narration)
            if len(s.strip()) > 5
        ][:5]

        if not points:
            points = [narration[:80]]

        summary_box = RoundedRectangle(
            width=12.5, height=5.5, corner_radius=0.35,
            fill_color=PALETTE["white"], fill_opacity=1,
            stroke_color=PALETTE["blue"], stroke_width=2.5
        )
        summary_box.move_to(DOWN * 0.2)
        self.play(FadeIn(summary_box), run_time=0.4)

        rows = VGroup()
        for i, pt in enumerate(points[:5]):
            check = Text("✓", font_size=22, color=PALETTE["green"],
                         weight=BOLD)
            txt = Text(pt[:65], font_size=21, color=PALETTE["dark"])
            txt.scale_to_fit_width(10.5)
            check.next_to(txt, LEFT, buff=0.25)
            row = VGroup(check, txt)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.move_to(summary_box.get_center())
        rows.scale_to_fit_height(4.8)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.4)

        self.wait(2.5)
