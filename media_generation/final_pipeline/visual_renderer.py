from manim import *
import os
import re


class EducationalScene(Scene):

    def construct(self):

        title = os.environ.get(
            "EDU_TITLE",
            "Educational Lesson"
        )

        description = os.environ.get(
            "EDU_DESCRIPTION",
            ""
        )

        narration = os.environ.get(
            "EDU_NARRATION",
            ""
        )

        # --------------------------------------------------
        # CLEAN SCRIPT
        # --------------------------------------------------

        narration = self.clean_text(narration)

        self.camera.background_color = "#F8FAFC"

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title_text = Text(
            title[:60],
            font_size=36,
            color="#0F172A",
            weight=BOLD
        )

        title_text.to_edge(UP, buff=0.5)

        self.play(
            Write(title_text),
            run_time=0.8
        )

        # Get useful chunks from narration
        points = self.extract_points(narration)

        # --------------------------------------------------
        # CREATE VISUAL FOR EACH SCRIPT PART
        # --------------------------------------------------

        for index, point in enumerate(points):

            self.show_scene_point(
                point,
                index
            )

        self.wait(0.5)

    # ============================================================
    # CLEAN TEXT
    # ============================================================

    def clean_text(self, text):

        text = re.sub(
            r"Reprint\s*\d{4}-\d{2}",
            "",
            text
        )

        text = re.sub(
            r"\b\d+\b",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ============================================================
    # EXTRACT SCRIPT POINTS
    # ============================================================

    def extract_points(self, narration):

        if not narration:
            return [
                "Let us understand this topic step by step."
            ]

        # Split Hindi/English sentences and lines
        raw_points = re.split(
            r"[।.!?\n]+",
            narration
        )

        points = []

        for point in raw_points:

            point = point.strip()

            # Avoid extremely short/noisy text
            if len(point) < 8:
                continue

            # Limit text so Manim doesn't overflow
            if len(point) > 100:
                point = point[:100] + "..."

            points.append(point)

        # Avoid generating an extremely long video
        # Increase this if you want more content
        if len(points) > 8:
            points = points[:8]

        if not points:
            points = [
                "Let us explore the important ideas."
            ]

        return points

    # ============================================================
    # SHOW ONE SCRIPT POINT
    # ============================================================

    def show_scene_point(
        self,
        point,
        index
    ):

        # --------------------------------------------------
        # REMOVE PREVIOUS CONTENT
        # --------------------------------------------------

        if index > 0:

            old_objects = VGroup(
                *[
                    mob
                    for mob in self.mobjects
                    if mob.get_top()[1] < 2.8
                ]
            )

            if len(old_objects) > 0:

                self.play(
                    FadeOut(old_objects),
                    run_time=0.5
                )

        # --------------------------------------------------
        # TEXT CARD
        # --------------------------------------------------

        text = Text(
            point,
            font_size=26,
            color="#0F172A",
            line_spacing=1.2
        )

        text.scale_to_fit_width(10)

        text_box = RoundedRectangle(
            width=11.5,
            height=max(
                2.0,
                text.height + 0.8
            ),
            corner_radius=0.25,
            color="#CBD5E1",
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=2
        )

        card = VGroup(
            text_box,
            text
        )

        text.move_to(text_box.get_center())

        card.move_to(ORIGIN + UP * 1)

        self.play(
            FadeIn(card, shift=UP * 0.3),
            run_time=0.6
        )

        # --------------------------------------------------
        # VISUAL TYPE CHANGES FOR EACH PART
        # --------------------------------------------------

        visual = self.create_visual(
            point,
            index
        )

        if visual:

            visual.move_to(
                DOWN * 1.9
            )

            self.play(
                FadeIn(
                    visual,
                    shift=UP * 0.3
                ),
                run_time=0.7
            )

            # Small animation so visuals feel alive
            self.play(
                Indicate(
                    visual,
                    scale_factor=1.04
                ),
                run_time=0.7
            )

        # Each narration point gets screen time
        self.wait(2.2)

    # ============================================================
    # CREATE VISUAL BASED ON SCRIPT
    # ============================================================

    def create_visual(
        self,
        point,
        index
    ):

        point_lower = point.lower()

        # ==================================================
        # FLOW / PROCESS VISUAL
        # ==================================================

        if any(
            word in point_lower
            for word in [
                "आगे",
                "बढ़",
                "journey",
                "process",
                "step"
            ]
        ):

            start = Circle(
                radius=0.45,
                color=BLUE,
                fill_opacity=0.5
            )

            middle = Circle(
                radius=0.45,
                color=YELLOW,
                fill_opacity=0.5
            )

            end = Circle(
                radius=0.45,
                color=GREEN,
                fill_opacity=0.5
            )

            start.shift(LEFT * 3)
            end.shift(RIGHT * 3)

            arrow1 = Arrow(
                start.get_right(),
                middle.get_left(),
                buff=0.2
            )

            arrow2 = Arrow(
                middle.get_right(),
                end.get_left(),
                buff=0.2
            )

            return VGroup(
                start,
                arrow1,
                middle,
                arrow2,
                end
            )

        # ==================================================
        # SUN
        # ==================================================

        if "सूरज" in point:

            sun = Circle(
                radius=0.8,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.8
            )

            rays = VGroup()

            for angle in range(0, 360, 30):

                ray = Line(
                    sun.get_center(),
                    sun.get_center()
                    + 1.4 * np.array([
                        np.cos(angle * DEGREES),
                        np.sin(angle * DEGREES),
                        0
                    ]),
                    color=ORANGE
                )

                rays.add(ray)

            return VGroup(
                rays,
                sun
            )

        # ==================================================
        # TREE / NATURE
        # ==================================================

        if any(
            word in point
            for word in [
                "पेड़",
                "तरु",
                "लता",
                "फूल",
                "प्रकृति"
            ]
        ):

            trunk = Rectangle(
                width=0.5,
                height=2,
                color="#92400E",
                fill_color="#92400E",
                fill_opacity=1
            )

            leaves = VGroup()

            for pos in [
                UP * 1.5,
                LEFT * 0.8 + UP,
                RIGHT * 0.8 + UP
            ]:

                leaf = Circle(
                    radius=0.9,
                    color=GREEN,
                    fill_color=GREEN,
                    fill_opacity=0.75
                )

                leaf.move_to(pos)

                leaves.add(leaf)

            return VGroup(
                trunk,
                leaves
            )

        # ==================================================
        # LIGHT / DARKNESS
        # ==================================================

        if any(
            word in point
            for word in [
                "दीपक",
                "अँधेरा",
                "प्रकाश",
                "रोशनी"
            ]
        ):

            lamp = RoundedRectangle(
                width=1.2,
                height=0.7,
                corner_radius=0.15,
                color=ORANGE,
                fill_color=ORANGE,
                fill_opacity=0.8
            )

            flame = Triangle(
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.9
            )

            flame.scale(0.5)
            flame.next_to(
                lamp,
                UP,
                buff=0
            )

            glow = Circle(
                radius=1.5,
                color=YELLOW,
                fill_opacity=0.15
            )

            return VGroup(
                glow,
                lamp,
                flame
            )

        # ==================================================
        # DEFAULT: KEY IDEA / CONCEPT
        # ==================================================

        concept = Circle(
            radius=0.9,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=4
        )

        dots = VGroup()

        for angle in [
            30,
            150,
            270
        ]:

            dot = Circle(
                radius=0.28,
                color=ORANGE,
                fill_color=ORANGE,
                fill_opacity=0.8
            )

            dot.move_to(
                2.2 * np.array([
                    np.cos(angle * DEGREES),
                    np.sin(angle * DEGREES),
                    0
                ])
            )

            dots.add(dot)

        arrows = VGroup()

        for dot in dots:

            arrows.add(
                Arrow(
                    dot.get_center(),
                    concept.get_center(),
                    buff=0.3,
                    color=GREY
                )
            )

        return VGroup(
            arrows,
            dots,
            concept
        )