from pathlib import Path
from moviepy import TextClip, ColorClip, CompositeVideoClip


def generate_video_from_text(
    text: str,
    output_path: str
):

    try:
        # Limit text for demo video
        video_text = text[:500]

        # Create background
        background = ColorClip(
            size=(1280, 720),
            color=(30, 30, 30),
            duration=10
        )

        # Create text
        text_clip = TextClip(
            text=video_text,
            font_size=40,
            color="white",
            size=(1100, None),
            method="caption",
            duration=10
        )

        # Center text
        text_clip = text_clip.with_position("center")

        # Combine clips
        final_video = CompositeVideoClip(
            [background, text_clip]
        )

        # Create output directory
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Generate MP4
        final_video.write_videofile(
            output_path,
            fps=24,
            audio=False
        )

        return output_path

    except Exception as e:
        raise Exception(
            f"Video generation failed: {str(e)}"
        )