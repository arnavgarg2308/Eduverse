import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"

AUDIO_DIR.mkdir(exist_ok=True)

VOICE_MODEL = "en_US-lessac-medium"


def generate_audio(scene):
    number = scene["scene_number"]
    text = scene["narration"]

    output = AUDIO_DIR / f"scene_{number:03d}.wav"

    print(f"\nGenerating audio for Scene {number}...")

    subprocess.run(
        [
            "python",
            "-m",
            "piper",
            "-m",
            VOICE_MODEL,
            "-f",
            str(output),
            "--",
            text
        ],
        check=True
    )

    print(f"Saved: {output}")

    return output


def main():
    with open("scene_plan.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    scenes = data["scenes"]

    # Test only Scene 1
    audio_file = generate_audio(scenes[0])

    print("\n========== AUDIO TEST COMPLETE ==========")
    print(audio_file)


if __name__ == "__main__":
    main()

