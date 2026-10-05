import json
import subprocess
import sys
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
VOICE_MODEL = BASE_DIR / "en_US-lessac-medium.onnx"
INPUT_DIR = BASE_DIR / "input"
AUDIO_DIR = BASE_DIR / "audio"
VIDEO_DIR = BASE_DIR / "videos"
SUBTITLE_DIR = BASE_DIR / "subtitles"
OUTPUT_DIR = BASE_DIR / "outputs"

SCENE_PLAN = INPUT_DIR / "scene_plan.json"
VISUAL_RENDERER = BASE_DIR / "visual_renderer.py"

AUDIO_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
SUBTITLE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# CHECK INPUT
# ============================================================

def load_scene_plan():

    if not SCENE_PLAN.exists():
        raise FileNotFoundError(
            f"Scene plan not found:\n{SCENE_PLAN}"
        )

    with open(SCENE_PLAN, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "scenes" not in data:
        raise ValueError(
            "scene_plan.json must contain a 'scenes' list."
        )

    return data["scenes"]


# ============================================================
# GENERATE AUDIO USING PIPER
# ============================================================

def generate_audio(scene):

    scene_number = scene["scene_number"]
    narration = scene.get("narration", "").strip()

    if not narration:
        print(f"Skipping audio for Scene {scene_number}: empty narration")
        return None

    output_file = AUDIO_DIR / f"scene_{scene_number:03d}.wav"

    print(f"\n[1/4] Generating audio for Scene {scene_number}...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "piper",
            "-m",
str(VOICE_MODEL),
            "-f",
            str(output_file),
            "--",
            narration
        ],
        check=True
    )

    print(f"Audio saved: {output_file}")

    return output_file


# ============================================================
# RENDER MANIM VISUAL
# ============================================================

def render_visual(scene):

    scene_number = scene["scene_number"]

    print(f"\n[2/4] Rendering visual for Scene {scene_number}...")

    import os, json as _json
    env = dict()
    env.update(os.environ)

    # Pass the entire scene as JSON so the renderer can use every field
    env["EDU_SCENE_JSON"] = _json.dumps(scene, ensure_ascii=False)

    # Legacy vars kept for safety
    env["EDU_TITLE"] = scene.get("title", f"Scene {scene_number}")
    env["EDU_DESCRIPTION"] = scene.get("visual_description", scene.get("narration", ""))

    output_dir = VIDEO_DIR / f"scene_{scene_number:03d}"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    subprocess.run(
    [
        sys.executable,
        "-m",
        "manim",
        "-ql",
        str(VISUAL_RENDERER),
        "EducationalScene"
    ],
    env=env,
    check=True,
    cwd=str(BASE_DIR)
)
    rendered_video = (
        BASE_DIR
        / "media"
        / "videos"
        / "visual_renderer"
        / "480p15"
        / "EducationalScene.mp4"
    )

    if not rendered_video.exists():

        possible_files = list(
            (
                BASE_DIR
                / "media"
                / "videos"
            ).rglob("EducationalScene.mp4")
        )

        if not possible_files:
            raise FileNotFoundError(
                "Manim rendered video was not found."
            )

        rendered_video = possible_files[-1]

    final_scene_video = (
        output_dir / "visual.mp4"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(rendered_video),
            "-c",
            "copy",
            str(final_scene_video)
        ],
        check=True
    )

    print(f"Visual saved: {final_scene_video}")

    return final_scene_video


# ============================================================
# MERGE AUDIO + VIDEO
# ============================================================

def merge_audio_video(
    scene_number,
    video_file,
    audio_file
):

    print(
        f"\n[3/4] Combining audio and visual "
        f"for Scene {scene_number}..."
    )

    output_file = (
        VIDEO_DIR
        / f"scene_{scene_number:03d}_final.mp4"
    )

    # Get audio duration using Python wave module (avoids ffprobe dependency)
    import wave as _wave
    with _wave.open(str(audio_file), 'rb') as _wf:
        audio_duration = _wf.getnframes() / _wf.getframerate()

    print(f"Audio duration: {audio_duration:.2f} seconds")

    # Loop the visual until the complete narration ends
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(video_file),
            "-i",
            str(audio_file),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-t",
            str(audio_duration),
            str(output_file)
        ],
        check=True
    )

    print(f"Scene video saved: {output_file}")

    return output_file

# ============================================================
# CREATE SUBTITLES
# ============================================================

def generate_subtitles(audio_files):

    print("\n[4/4] Generating subtitles...")

    try:

        from faster_whisper import WhisperModel

    except ImportError:

        print(
            "ERROR: faster-whisper is not installed."
        )

        return None

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    all_entries = []

    subtitle_index = 1
    time_offset = 0.0

    import wave

    for audio_file in audio_files:

        if not audio_file.exists():
            continue

        print(
            f"Transcribing {audio_file.name}..."
        )

        segments, info = model.transcribe(
            str(audio_file),
            beam_size=5
        )

        for segment in segments:

            text = segment.text.strip()

            if not text:
                continue

            start = segment.start + time_offset
            end = segment.end + time_offset

            all_entries.append(
                (
                    subtitle_index,
                    start,
                    end,
                    text
                )
            )

            subtitle_index += 1

        with wave.open(
            str(audio_file),
            "rb"
        ) as wav_file:

            duration = (
                wav_file.getnframes()
                / wav_file.getframerate()
            )

        time_offset += duration

    subtitle_file = (
        SUBTITLE_DIR / "subtitles.srt"
    )

    def format_time(seconds):

        hours = int(seconds // 3600)

        minutes = int(
            (seconds % 3600) // 60
        )

        secs = int(seconds % 60)

        milliseconds = int(
            (seconds - int(seconds)) * 1000
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d},"
            f"{milliseconds:03d}"
        )

    lines = []

    for index, start, end, text in all_entries:

        lines.append(
            f"{index}\n"
            f"{format_time(start)} --> "
            f"{format_time(end)}\n"
            f"{text}\n"
        )

    subtitle_file.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(
        f"Subtitles saved: {subtitle_file}"
    )

    return subtitle_file


# ============================================================
# COMBINE ALL SCENES
# ============================================================

def combine_scenes(scene_videos):

    print("\nCombining all scenes...")

    concat_file = (
        OUTPUT_DIR / "concat.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8"
    ) as f:

        for video in scene_videos:

            f.write(
                f"file '{video.resolve()}'\n"
            )

    final_video = (
        OUTPUT_DIR
        / "final_educational_video.mp4"
    )

    subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(final_video)
    ],
    check=True
)
    print(
        "\n========================================"
)

    print( 
        "FINAL VIDEO CREATED SUCCESSFULLY!"
     )

    print(
        "========================================"
    )

    print(
        f"\n{final_video}"
    )

    return final_video


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print(
        "\n========================================"
    )

    print(
        "      EDUVERSE MEDIA PIPELINE"
    )

    print(
        "========================================\n"
    )

    scenes = load_scene_plan()

    print(
        f"Found {len(scenes)} scenes."
    )

    scene_videos = []
    audio_files = []

    for scene in scenes:

        audio_file = generate_audio(scene)

        if audio_file is None:
            continue

        visual_file = render_visual(scene)

        final_scene = merge_audio_video(
            scene["scene_number"],
            visual_file,
            audio_file
        )

        audio_files.append(audio_file)
        scene_videos.append(final_scene)

    if not scene_videos:

        raise RuntimeError(
            "No scene videos were generated."
        )

    generate_subtitles(audio_files)

    final_video = combine_scenes(
        scene_videos
    )

    print(
        "\nPipeline completed."
    )

    print(
        f"Final output:\n{final_video}"
    )


if __name__ == "__main__":
    main()
