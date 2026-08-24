from manim import *
import os


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

        content = (
            title + " " + description
        ).lower()

        # --------------------------------------------------------
        # Generic educational visual
        # No topic-specific Photosynthesis hardcoding
        # --------------------------------------------------------

        self.educational_animation(
            title,
            description,
            content
        )

        self.wait(0.5)

    # ============================================================
    # GENERIC EDUCATIONAL ANIMATION
    # ============================================================

    def educational_animation(
        self,
        title,
        description,
        content
    ):

        # --------------------------------------------------------
        # Central concept
        # --------------------------------------------------------

        concept = Circle(
            radius=1.0,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_width=5
        )

        self.play(
            Create(concept),
            run_time=0.8
        )

        # --------------------------------------------------------
        # Input / supporting concepts
        # --------------------------------------------------------

        inputs = VGroup()

        positions = [
            LEFT * 4 + UP * 1.5,
            LEFT * 4,
            LEFT * 4 + DOWN * 1.5
        ]

        for position in positions:

            node = Circle(
                radius=0.45,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.8
            )

            node.move_to(position)

            inputs.add(node)

        self.play(
            *[
                FadeIn(node)
                for node in inputs
            ],
            run_time=0.8
        )

        # --------------------------------------------------------
        # Input → concept arrows
        # --------------------------------------------------------

        arrows_in = VGroup()

        for node in inputs:

            arrow = Arrow(
                node.get_right(),
                concept.get_left(),
                buff=0.15,
                stroke_width=4
            )

            arrows_in.add(arrow)

        self.play(
            *[
                GrowArrow(arrow)
                for arrow in arrows_in
            ],
            run_time=0.8
        )

        # --------------------------------------------------------
        # Output concepts
        # --------------------------------------------------------

        outputs = VGroup()

        output_positions = [
            RIGHT * 4 + UP * 0.9,
            RIGHT * 4 + DOWN * 0.9
        ]

        for position in output_positions:

            node = Circle(
                radius=0.5,
                color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.8
            )

            node.move_to(position)

            outputs.add(node)

        self.play(
            *[
                FadeIn(node)
                for node in outputs
            ],
            run_time=0.8
        )

        # --------------------------------------------------------
        # Concept → outputs
        # --------------------------------------------------------

        arrows_out = VGroup()

        for node in outputs:

            arrow = Arrow(
                concept.get_right(),
                node.get_left(),
                buff=0.15,
                stroke_width=4
            )

            arrows_out.add(arrow)

        self.play(
            *[
                GrowArrow(arrow)
                for arrow in arrows_out
            ],
            run_time=0.8
        )

        # --------------------------------------------------------
        # Animate information flow
        # --------------------------------------------------------

        particles = VGroup()

        for node in inputs:

            particle = Dot(
                color=WHITE,
                radius=0.08
            )

            particle.move_to(
                node.get_center()
            )

            particles.add(particle)

        self.play(
            FadeIn(particles),
            run_time=0.3
        )

        self.play(
            *[
                particle.animate.move_to(
                    concept.get_center()
                )
                for particle in particles
            ],
            run_time=1.2
        )

        self.play(
            FadeOut(particles),
            run_time=0.3
        )

        # --------------------------------------------------------
        # Concept activation
        # --------------------------------------------------------

        self.play(
            Indicate(
                concept,
                color=YELLOW,
                scale_factor=1.15
            ),
            run_time=1
        )

        # --------------------------------------------------------
        # Output particles
        # --------------------------------------------------------

        output_particles = VGroup()

        for node in outputs:

            particle = Dot(
                color=WHITE,
                radius=0.08
            )

            particle.move_to(
                concept.get_center()
            )

            output_particles.add(particle)

        self.play(
            FadeIn(output_particles),
            run_time=0.3
        )

        self.play(
            *[
                particle.animate.move_to(
                    node.get_center()
                )
                for particle, node
                in zip(output_particles, outputs)
            ],
            run_time=1.2
        )

        self.play(
            FadeOut(output_particles),
            run_time=0.3
        )

        # --------------------------------------------------------
        # Final visual emphasis
        # --------------------------------------------------------

        self.play(
            Indicate(
                outputs,
                color=GREEN,
                scale_factor=1.1
            ),
            run_time=0.8
        )

        self.wait(0.5)
