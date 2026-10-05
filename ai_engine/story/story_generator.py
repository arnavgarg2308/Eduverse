from __future__ import annotations

import re

# EduMorphModel is only needed at runtime when generate() is called.
# Importing it here as a string annotation avoids requiring torch/transformers
# at import time (useful for testing with a mock model).
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ai_engine.core.model import EduMorphModel


# ──────────────────────────────────────────────────────────────
# VISUAL TYPE DISPATCH RULES
# ──────────────────────────────────────────────────────────────

VISUAL_RULES = [
    # (visual_type, animation, [trigger keywords])
    ("equation", "reveal_steps", [
        "formula", "equation", "=", "theorem", "law", "calculate",
        "सूत्र", "समीकरण", "प्रमेय", "नियम", "गणना",
        "f = m", "e = mc", "v = u", "a² + b²",
    ]),
    ("process_flow", "sequential_arrows", [
        "process", "step", "stage", "cycle", "sequence", "flow",
        "first", "then", "next", "finally", "after", "before",
        "चरण", "क्रम", "प्रक्रिया", "पहले", "फिर", "बाद",
        "photosynthesis", "respiration", "digestion", "metabolism",
        "प्रकाश संश्लेषण", "श्वसन", "पाचन",
    ]),
    ("cycle", "rotate_cycle", [
        "cycle", "circular", "repeat", "loop", "rotation",
        "water cycle", "carbon cycle", "life cycle",
        "चक्र", "जल चक्र", "कार्बन चक्र", "जीवन चक्र",
    ]),
    ("timeline", "appear_left_to_right", [
        "history", "year", "century", "era", "period", "date",
        "timeline", "event", "war", "revolution", "independence",
        "इतिहास", "वर्ष", "शताब्दी", "युग", "काल", "तारीख",
        "स्वतंत्रता", "युद्ध", "क्रांति",
    ]),
    ("comparison", "split_reveal", [
        "compare", "difference", "versus", "vs", "unlike", "whereas",
        "on the other hand", "contrast", "similar", "both",
        "तुलना", "अंतर", "बनाम", "जबकि", "समान", "दोनों",
    ]),
    ("real_world_example", "zoom_in", [
        "example", "for instance", "such as", "like", "application",
        "real", "everyday", "daily life", "used in", "real-world",
        "include", "self-driving", "medical", "recommendation",
        "उदाहरण", "जैसे", "जैसा", "उपयोग", "दैनिक जीवन",
    ]),
    ("diagram", "label_appear", [
        "diagram", "structure", "organ", "cell", "part", "layer",
        "heart", "lung", "brain", "plant", "root", "leaf", "stem",
        "atom", "molecule", "nucleus", "electron",
        "आरेख", "संरचना", "अंग", "कोशिका", "भाग", "परत",
        "हृदय", "फेफड़ा", "मस्तिष्क", "पौधा", "जड़", "पत्ती",
        "परमाणु", "अणु", "नाभिक", "इलेक्ट्रॉन",
    ]),
    ("physics_motion", "animate_motion", [
        "force", "motion", "velocity", "acceleration", "gravity",
        "friction", "momentum", "newton", "projectile", "orbit",
        "बल", "गति", "वेग", "त्वरण", "गुरुत्वाकर्षण",
        "घर्षण", "संवेग", "न्यूटन", "प्रक्षेप्य",
    ]),
    ("graph", "draw_axes", [
        "graph", "plot", "axis", "x-axis", "y-axis", "curve",
        "increase", "decrease", "trend", "data", "statistics",
        "ग्राफ", "अक्ष", "वक्र", "वृद्धि", "कमी", "डेटा",
    ]),
    ("concept_map", "expand_nodes", [
        "concept", "idea", "topic", "related", "connection",
        "branch", "category", "type", "kind", "classification",
        "अवधारणा", "विचार", "विषय", "संबंध", "शाखा", "वर्गीकरण",
    ]),
    ("mathematical_steps", "step_by_step", [
        "solve", "proof", "derive", "calculate", "find", "simplify",
        "expand", "factor", "integrate", "differentiate",
        "हल", "सिद्ध", "व्युत्पन्न", "गणना", "सरल",
    ]),
    ("summary", "fade_in_list", [
        "summary", "conclusion", "recap", "review", "remember",
        "key points", "important", "in short", "therefore",
        "सारांश", "निष्कर्ष", "पुनरावलोकन", "महत्वपूर्ण", "इसलिए",
    ]),
    ("nature_scene", "pan_scene", [
        "sun", "moon", "star", "sky", "river", "mountain", "tree",
        "flower", "bird", "animal", "nature", "environment",
        "सूरज", "चाँद", "तारा", "आकाश", "नदी", "पहाड़", "पेड़",
        "फूल", "पक्षी", "जानवर", "प्रकृति", "पर्यावरण",
        "सूरज की किरण", "जलधारा", "लता",
    ]),
    ("bullet_explanation", "bullet_appear", [
        "learn", "सीखो", "सीखना", "सीखें",
        "teaches", "shows", "tells", "explains",
        "सिखाता", "बताता", "दर्शाता",
    ]),
]

TITLE_VISUAL = "title_card"
DEFAULT_VISUAL = "text_explanation"


def detect_visual_type(narration: str, index: int):
    """Return (visual_type, animation) by matching narration keywords."""
    if index == 0:
        return TITLE_VISUAL, "fade_in"

    text = narration.lower()
    for vtype, anim, keywords in VISUAL_RULES:
        if any(kw in text for kw in keywords):
            return vtype, anim

    return DEFAULT_VISUAL, "fade_in_text"


def extract_keywords(narration: str, max_kw: int = 6) -> list:
    """Pull meaningful words (length ≥ 4) from narration as keywords."""
    stop = {
        "this", "that", "with", "from", "have", "will", "been",
        "they", "their", "there", "what", "when", "where", "which",
        "यह", "वह", "इस", "उस", "और", "के", "की", "का", "में",
        "से", "को", "पर", "है", "हैं", "था", "थे", "एक", "भी",
    }
    words = re.findall(r"[\w\u0900-\u097F]{4,}", narration)
    seen = set()
    result = []
    for w in words:
        wl = w.lower()
        if wl not in stop and wl not in seen:
            seen.add(wl)
            result.append(w)
        if len(result) >= max_kw:
            break
    return result


def extract_equations(narration: str) -> list:
    """Pull equation-like substrings (contain = and operators)."""
    eqs = re.findall(
        r"[A-Za-z\u0900-\u097F\d\s\+\-\*\/\^=²³]{3,30}=[^,।.!?\n]{1,30}",
        narration
    )
    return [e.strip() for e in eqs[:3]]


def extract_objects(narration: str, visual_type: str) -> list:
    """Return a short list of concrete objects relevant to the visual type."""
    caps = re.findall(r"\b[A-Z][a-z]{2,}\b", narration)
    hindi_words = re.findall(r"[\u0900-\u097F]{3,}", narration)

    structural = {
        "nature_scene": ["sun", "tree", "river", "flower", "bird"],
        "physics_motion": ["block", "force_arrow", "velocity_arrow", "surface"],
        "process_flow": ["start", "process", "result"],
        "cycle": ["stage_1", "stage_2", "stage_3", "stage_4"],
        "comparison": ["item_A", "item_B"],
        "equation": ["left_side", "equals", "right_side"],
        "graph": ["x_axis", "y_axis", "curve"],
        "concept_map": ["central_concept", "branch_1", "branch_2", "branch_3"],
    }
    base = structural.get(visual_type, [])
    content_words = caps + hindi_words
    return list(dict.fromkeys(base + content_words))[:6]


def extract_labels(narration: str, keywords: list) -> list:
    """Use keywords as labels, capped at 5."""
    return keywords[:5]


def detect_language(text: str) -> str:
    """Detect dominant language: 'hi' for Hindi, 'en' for English."""
    hindi_chars = len(re.findall(r"[\u0900-\u097F]", text))
    total_alpha = len(re.findall(r"[A-Za-z\u0900-\u097F]", text))
    if total_alpha == 0:
        return "en"
    return "hi" if (hindi_chars / total_alpha) > 0.3 else "en"


def _make_title_from_content(text: str, language: str) -> str:
    """
    Extract a meaningful title from the first non-trivial line of text.
    Falls back to first sentence fragment.
    """
    for line in text.split('\n'):
        line = line.strip()
        if 5 < len(line) < 80:
            alpha = re.findall(r'[A-Za-z\u0900-\u097F]', line)
            if len(alpha) >= 4:
                return line
    # Fallback: first 60 chars of first sentence
    first = re.split(r'[।.!?\n]', text)[0].strip()
    return first[:60] if first else ("पाठ" if language == "hi" else "Lesson")


def segment_by_headings(text: str, headings: list) -> list:
    """
    Split text into sections using detected headings as boundaries.
    Returns list of (heading, section_text) tuples.
    Each section contains the content between consecutive headings.
    """
    if not headings:
        return []

    sections = []
    remaining = text

    for i, heading in enumerate(headings):
        # Find this heading in the text
        idx = remaining.find(heading)
        if idx == -1:
            continue

        # Content starts after the heading
        content_start = idx + len(heading)

        # Find where next heading starts (if any)
        next_idx = len(remaining)
        for next_heading in headings[i + 1:]:
            ni = remaining.find(next_heading, content_start)
            if ni != -1:
                next_idx = ni
                break

        section_text = remaining[content_start:next_idx].strip()
        if len(section_text) >= 30:
            sections.append((heading, section_text))

    return sections


def extract_quality_points(text: str, max_points: int = 12) -> list:
    """
    Extract meaningful educational sentences from text.
    Works for both Hindi and English content.
    Deduplicates repeated PDF pages.
    Rejects any sentence that looks like instruction/prompt text.
    """
    raw = re.split(r'[।.!?\n]+', text)
    points = []
    seen_keys = set()
    language = detect_language(text)

    for s in raw:
        s = re.sub(r'\s+', ' ', s).strip()
        # Strip leading figure/activity numbers: "3 flowers..." → "flowers..."
        # Patterns: "Fig 4", "1 Testing", "Activity 2", etc.
        s = re.sub(r'^(Fig\.?\s*\d+\s*|Activity\s*\d+\s*|\d+\s+(?=[A-Z\u0900]))', '', s).strip()
        # Length filter
        if len(s) < 20 or len(s) > 400:
            continue
        # Must have some alphabetic content
        alpha = re.findall(r'[A-Za-z\u0900-\u097F]', s)
        if len(alpha) < 8:
            continue
        # For Hindi text: require at least 25% Hindi chars
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', s))
        if language == "hi" and hindi_chars > 0 and hindi_chars / len(alpha) < 0.20:
            continue
        # Reject prompt/instruction leakage in extracted sentences too
        if _is_prompt_leakage(s):
            continue
        # Deduplicate by first 35 chars
        key = s[:35].lower()
        if key in seen_keys:
            continue
        seen_keys.add(key)
        points.append(s)
        if len(points) >= max_points:
            break

    return points


def _build_scene(index: int, title: str, narration: str, language: str) -> dict:
    """Build a single scene dict from its content."""
    visual_type, animation = detect_visual_type(narration, index)
    keywords = extract_keywords(narration)
    equations = extract_equations(narration)
    objects = extract_objects(narration, visual_type)
    labels = extract_labels(narration, keywords)

    if language == "hi":
        vis_desc = (
            f"इस दृश्य में '{title}' को "
            f"{visual_type} के रूप में दिखाएं।"
        )
    else:
        vis_desc = (
            f"Show '{title}' as a {visual_type} "
            f"with labels: {', '.join(labels)}."
        )

    return {
        "scene_number": index + 1,
        "title": title,
        "narration": narration,
        "duration": max(8, min(20, len(narration) // 8)),
        "visual_type": visual_type,
        "visual_description": vis_desc,
        "objects": objects,
        "labels": labels,
        "animation": animation,
        "equations": equations,
        "keywords": keywords,
        "language": language,
    }


# ──────────────────────────────────────────────────────────────
# PROMPT-LEAKAGE DETECTION
# ──────────────────────────────────────────────────────────────

# Phrases that indicate the model echoed the instruction prompt
# rather than generating content from the document.
_LEAKAGE_PHRASES = [
    "you are an expert",
    "you are a",
    "read the content below",
    "read the content",
    "write 4 to 10",
    "write a clear educational",
    "write a summary",
    "short learning points",
    "your task is",
    "output json",
    "educational explanation",
    "rules:",
    "do not invent",
    "do not copy",
    "use the same language",
    "detect the real topic",
    "each point should",
    "separated by newlines",
    "summarize in 5",
    "summarize in",
    "content below",
    "page numbers or metadata",
    # Hindi equivalents
    "आप एक विशेषज्ञ",
    "नीचे दी गई सामग्री",
    "शैक्षिक व्याख्या",
]


def _is_prompt_leakage(text: str) -> bool:
    """
    Return True if this text looks like the model echoed an
    instruction prompt rather than generating educational content.
    """
    lower = text.lower().strip()
    return any(phrase in lower for phrase in _LEAKAGE_PHRASES)


# ──────────────────────────────────────────────────────────────
# STORY GENERATOR
# ──────────────────────────────────────────────────────────────

class StoryGenerator:

    def __init__(self, model: EduMorphModel):
        self.model = model

    def generate(
        self,
        text: str,
        topic: str,
        education_level: str = "General",
        headings: list = None,
        content_start: int = 0,
    ) -> dict:

        if not text or not text.strip():
            raise ValueError("Educational content cannot be empty.")

        # ── 1. Clean PDF noise ──────────────────────────────
        cleaned = re.sub(r"\s+", " ", text).strip()
        cleaned = re.sub(
            r"Reprint\s+\d{4}-\d{2}", "", cleaned, flags=re.IGNORECASE
        )

        # Skip front-matter (copyright, edition info, publication details)
        # Use content_start offset from metadata analysis
        if content_start > 0 and len(cleaned) > content_start:
            content_text = cleaned[content_start:]
        else:
            content_text = cleaned

        language = detect_language(cleaned)
        headings = headings or []

        print(f"\n[STORY] language        : {language}")
        print(f"[STORY] topic           : {topic}")
        print(f"[STORY] education_level : {education_level}")
        print(f"[STORY] headings count  : {len(headings)}")
        print(f"[STORY] text length     : {len(cleaned)}")
        print(f"[STORY] content_start   : {content_start}")
        print(f"[STORY] content_text len: {len(content_text)}")

        # ── 2. Try heading-based segmentation first ─────────
        scenes = []

        if headings:
            sections = segment_by_headings(content_text, headings)
            print(f"[STORY] sections found  : {len(sections)}")

            for i, (heading, section_text) in enumerate(sections):
                title = heading.strip()[:70]
                narration_points = extract_quality_points(section_text, max_points=2)
                narration = " ".join(narration_points) if narration_points else section_text[:200]
                if not narration.strip():
                    continue
                scenes.append(_build_scene(i, title, narration, language))

        # ── 3. If no heading-based scenes, try FLAN-T5 then fallback ──
        if len(scenes) < 2:
            content_for_ai = content_text[:3000]
            # Keep the prompt short so FLAN-T5-small doesn't echo it
            short_prompt = (
                f"Summarize in 5 educational points:\n\n{content_for_ai}"
            )

            ai_points = []
            try:
                explanation = self.model.generate(
                    short_prompt, max_new_tokens=300
                ).strip()
                raw_points = re.split(r"[।.!?\n]+", explanation)
                for p in raw_points:
                    p = p.strip(" -•\t1234567890.")
                    if len(p) < 20:
                        continue
                    # ── PROMPT-LEAKAGE GUARD ────────────────────────
                    if _is_prompt_leakage(p):
                        print(f"[STORY] REJECTED leaky output: {p[:60]}")
                        continue
                    ai_points.append(p)
            except Exception as exc:
                print(f"[STORY] FLAN-T5 error: {exc}")

            # If FLAN-T5 gave at least 2 clean points, use them;
            # otherwise fall back 100% to direct content extraction
            if len(ai_points) >= 2:
                print(f"[STORY] FLAN-T5 gave {len(ai_points)} clean points")
                points = ai_points
            else:
                print(
                    f"[STORY] FLAN-T5 produced {len(ai_points)} usable points "
                    "— using direct content extraction"
                )
                points = extract_quality_points(content_text, max_points=10)

            scenes = []
            for i, point in enumerate(points):
                title = point[:60].rstrip(",;:")
                scenes.append(_build_scene(i, title, point, language))

        # ── 4. Determine overall document title ─────────────
        if topic and topic.lower() not in ("general", "general education"):
            doc_title = topic
        elif headings:
            doc_title = headings[0][:70]
        elif scenes:
            doc_title = scenes[0]["title"]
        else:
            doc_title = _make_title_from_content(cleaned, language)

        # ── 5. Make scene 0 a title card ────────────────────
        if scenes:
            scenes[0]["visual_type"] = "title_card"
            scenes[0]["animation"] = "fade_in"
            scenes[0]["title"] = doc_title

        print(f"[STORY] scenes generated: {len(scenes)}")
        for s in scenes[:5]:
            print(f"  Scene {s['scene_number']}: [{s['visual_type']}] {s['title'][:50]}")
            print(f"    narration: {s['narration'][:80]}...")
            print(f"    keywords : {s['keywords']}")

        key_points = [s["narration"] for s in scenes]

        return {
            "title": doc_title,
            "education_level": education_level,
            "language": language,
            "explanation": key_points[0] if key_points else "",
            "key_points": key_points,
            "scenes": scenes,
            "recap": (
                key_points[-1] if key_points
                else "Review the important ideas from this lesson."
            ),
        }
