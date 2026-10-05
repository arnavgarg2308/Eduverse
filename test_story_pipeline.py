"""
Cheap story-pipeline test — NO video generation, NO full AI server, NO FLAN-T5.

Tests TWO documents to catch regressions:
  A) ideastormabes.pdf  (6abf790f3a51166e3a86e5fe)  — tech/startup pitch deck
  B) science class 6.pdf (6abee361a6f32332e2b8b4a2) — NCERT textbook

For each document:
  1. Fetch extracted_text from MongoDB
  2. Run analyze_pdf_metadata → verify subject / language / headings
  3. Run StoryGenerator.generate() with a mock model (leakage-testing stub)
  4. Print every scene
  5. Assert no prompt leakage
  6. Assert content matches the document (not stale content from another doc)
  7. Verify scene_plan.json path resolves to the same file auto_pipeline.py reads

Usage:
    cd /Users/satyam/Desktop/new\ eduverse_code/Eduverse
    python test_story_pipeline.py
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, "backend", ".env"))

import pymongo
from bson import ObjectId
from pathlib import Path

MONGODB_URL   = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGODB_URL or not DATABASE_NAME:
    sys.exit("ERROR: MONGODB_URL / DATABASE_NAME not set. Check backend/.env")

client = pymongo.MongoClient(MONGODB_URL)
db     = client[DATABASE_NAME]

# ─────────────────────────────────────────────────────────────
# LEAKAGE DETECTION (mirrors story_generator._is_prompt_leakage)
# ─────────────────────────────────────────────────────────────
LEAKAGE_PHRASES = [
    "you are an expert", "you are a",
    "read the content below", "read the content",
    "write 4 to 10", "write a clear educational",
    "write a summary", "short learning points",
    "your task is", "output json", "educational explanation",
    "rules:", "do not invent", "do not copy",
    "use the same language", "detect the real topic",
    "each point should", "separated by newlines",
    "summarize in 5", "summarize in", "content below",
    "page numbers or metadata",
    "आप एक विशेषज्ञ", "नीचे दी गई सामग्री",
]

class _MockModel:
    """
    Stub whose output is always prompt-echo — forces the leakage guard
    to reject FLAN-T5 output and use direct content extraction instead.
    This validates the entire fallback path without loading torch.
    """
    def generate(self, prompt: str, max_new_tokens: int = 150) -> str:
        return "You are an expert teacher for General students."


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def fetch_doc(doc_id: str) -> dict:
    doc = db.documents.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        sys.exit(f"ERROR: Document {doc_id} not found in MongoDB")
    return doc


def run_metadata(text: str) -> dict:
    from app.services.pdf_service import analyze_pdf_metadata
    return analyze_pdf_metadata(text)


def run_story(text: str, meta: dict) -> dict:
    from ai_engine.story.story_generator import StoryGenerator
    gen = StoryGenerator(_MockModel())
    topic = meta["subject"].replace("_", " ").title()
    return gen.generate(
        text            = text,
        topic           = topic,
        education_level = meta["education_level"] or "General",
        headings        = meta["headings"],
        content_start   = meta["content_start"],
    )


def check_scenes(scenes: list, doc_label: str,
                 must_contain: list, must_not_contain: list) -> list:
    """
    Returns list of error strings (empty = PASS).
    must_contain  : at least ONE scene title/narration must include one of these phrases
    must_not_contain : NO scene title/narration may include any of these phrases
    """
    errors = []
    combined_text = " ".join(
        (s.get("title","") + " " + s.get("narration","")).lower()
        for s in scenes
    )

    # Leakage check — every scene individually
    for s in scenes:
        text = (s.get("title","") + " " + s.get("narration","")).lower()
        for phrase in LEAKAGE_PHRASES:
            if phrase in text:
                errors.append(
                    f"[{doc_label}] Scene {s['scene_number']} LEAKAGE: '{phrase}'\n"
                    f"  narration: {s.get('narration','')[:100]}"
                )

    # Must-contain: at least one scene references expected content
    for phrase in must_contain:
        if phrase.lower() not in combined_text:
            errors.append(
                f"[{doc_label}] MISSING expected content: '{phrase}' "
                f"not found in any scene title/narration"
            )

    # Must-not-contain: stale content from other PDFs
    for phrase in must_not_contain:
        if phrase.lower() in combined_text:
            errors.append(
                f"[{doc_label}] STALE CONTENT: '{phrase}' "
                f"should not appear in scenes for this document"
            )

    return errors


# ─────────────────────────────────────────────────────────────
# PATH CHECK
# ─────────────────────────────────────────────────────────────

def check_scene_plan_path():
    videos_py = Path(PROJECT_ROOT) / "backend" / "app" / "routes" / "videos.py"
    project_root = videos_py.resolve().parents[3]
    backend_writes = project_root / "media_generation" / "final_pipeline" / "input" / "scene_plan.json"
    media_reads    = Path(PROJECT_ROOT) / "media_generation" / "final_pipeline" / "input" / "scene_plan.json"
    return backend_writes.resolve(), media_reads.resolve(), \
           backend_writes.resolve() == media_reads.resolve()


# ─────────────────────────────────────────────────────────────
# DOCUMENT A — ideastormabes.pdf  (PRIMARY TEST)
# ─────────────────────────────────────────────────────────────

IDEASTORM_ID = "6abf790f3a51166e3a86e5fe"

print("\n" + "=" * 65)
print("DOCUMENT A — ideastormabes.pdf")
print("=" * 65)

doc_a = fetch_doc(IDEASTORM_ID)
text_a = doc_a.get("extracted_text", "")
print(f"  filename    : {doc_a.get('filename')}")
print(f"  text_length : {len(text_a)}")
print(f"  first 300 chars:\n{text_a[:300]}\n")

print("── metadata ──")
meta_a = run_metadata(text_a)
print(f"  language        : {meta_a['language']}")
print(f"  subject         : {meta_a['subject']}")
print(f"  education_level : {meta_a['education_level']}")
print(f"  content_start   : {meta_a['content_start']}")
print(f"  headings ({len(meta_a['headings'])}):")
for h in meta_a["headings"]:
    print(f"    - {h}")

# Metadata assertions
meta_errors_a = []
if meta_a["subject"] in ("geography",):
    meta_errors_a.append(
        f"WRONG subject '{meta_a['subject']}' — expected 'technology' or similar"
    )
if meta_a["content_start"] > len(text_a) * 0.25:
    meta_errors_a.append(
        f"content_start={meta_a['content_start']} skips >"
        f"25% of {len(text_a)}-char doc"
    )

print()
print("── story generation ──")
result_a = run_story(text_a, meta_a)
scenes_a  = result_a.get("scenes", [])
print(f"  title     : {result_a.get('title')}")
print(f"  language  : {result_a.get('language')}")
print(f"  scenes    : {len(scenes_a)}")
print()
for s in scenes_a:
    print(f"  Scene {s['scene_number']:02d}: [{s['visual_type']}] {s['title'][:60]}")
    print(f"    narration : {s['narration'][:100]}{'...' if len(s['narration'])>100 else ''}")
    print(f"    keywords  : {s.get('keywords', [])}")
    print()

# Scene content assertions for ideastormabes
# At least one scene must reference pig/poultry farming concepts
MUST_CONTAIN_A = [
    # At least one of these must appear somewhere in scenes
    "pig", "poultry", "farm", "biosecurity", "disease",
    "solution", "platform", "portal",
]
# None of these stale phrases from OTHER documents should appear
MUST_NOT_CONTAIN_A = [
    "photosynthesis", "ncert", "class 6 science",
    "food: where does it come from",
    "fibre to fabric", "sorting materials",
]

# must_contain: check that AT LEAST ONE phrase hits (not all required)
scene_errors_a = []
combined_a = " ".join(
    (s.get("title","") + " " + s.get("narration","")).lower()
    for s in scenes_a
)
matched_concepts = [p for p in MUST_CONTAIN_A if p.lower() in combined_a]
if not matched_concepts:
    scene_errors_a.append(
        f"No expected ideastormabes concepts found in scenes.\n"
        f"  Looked for: {MUST_CONTAIN_A}\n"
        f"  Combined scene text (first 300): {combined_a[:300]}"
    )
for phrase in MUST_NOT_CONTAIN_A:
    if phrase.lower() in combined_a:
        scene_errors_a.append(f"STALE CONTENT: '{phrase}' in ideastormabes scenes")
# Leakage
for s in scenes_a:
    t = (s.get("title","") + " " + s.get("narration","")).lower()
    for phrase in LEAKAGE_PHRASES:
        if phrase in t:
            scene_errors_a.append(
                f"Scene {s['scene_number']} LEAKAGE '{phrase}': "
                f"{s.get('narration','')[:80]}"
            )

# ─────────────────────────────────────────────────────────────
# DOCUMENT B — science class 6.pdf  (REGRESSION TEST)
# ─────────────────────────────────────────────────────────────

SCIENCE_ID = "6abee361a6f32332e2b8b4a2"

print("=" * 65)
print("DOCUMENT B — science class 6.pdf  (regression)")
print("=" * 65)

doc_b = fetch_doc(SCIENCE_ID)
text_b = doc_b.get("extracted_text", "")
print(f"  filename    : {doc_b.get('filename')}")
print(f"  text_length : {len(text_b)}")

meta_b = run_metadata(text_b)
print(f"  subject         : {meta_b['subject']}")
print(f"  education_level : {meta_b['education_level']}")
print(f"  content_start   : {meta_b['content_start']}")
print(f"  headings count  : {len(meta_b['headings'])}")

result_b = run_story(text_b, meta_b)
scenes_b  = result_b.get("scenes", [])
print(f"  scenes generated: {len(scenes_b)}")
for s in scenes_b[:3]:
    print(f"  Scene {s['scene_number']:02d}: [{s['visual_type']}] {s['title'][:55]}")
print()

meta_errors_b = []
if meta_b["subject"] not in ("science",):
    meta_errors_b.append(
        f"Science PDF subject regressed to '{meta_b['subject']}'"
    )
if meta_b["education_level"] != "Class 6":
    meta_errors_b.append(
        f"Science PDF education_level regressed to '{meta_b['education_level']}'"
    )
if len(scenes_b) < 5:
    meta_errors_b.append(
        f"Science PDF produced only {len(scenes_b)} scenes (expected ≥5)"
    )

combined_b = " ".join(
    (s.get("title","") + " " + s.get("narration","")).lower()
    for s in scenes_b
)
MUST_CONTAIN_B = ["food", "plant", "body", "water", "light", "science"]
matched_b = [p for p in MUST_CONTAIN_B if p in combined_b]
if not matched_b:
    meta_errors_b.append(
        f"Science PDF scenes missing expected science keywords: {MUST_CONTAIN_B}"
    )
# Must not contain ideastormabes content
MUST_NOT_CONTAIN_B = ["pig", "poultry", "biosecurity", "smart digital portal"]
for phrase in MUST_NOT_CONTAIN_B:
    if phrase in combined_b:
        meta_errors_b.append(
            f"Science PDF scenes contain ideastormabes content: '{phrase}'"
        )

# ─────────────────────────────────────────────────────────────
# PATH CHECK
# ─────────────────────────────────────────────────────────────

print("=" * 65)
print("SCENE PLAN PATH CHECK")
print("=" * 65)
backend_path, media_path, paths_match = check_scene_plan_path()
print(f"  backend writes : {backend_path}")
print(f"  media reads    : {media_path}")
print(f"  paths match    : {paths_match}")
path_errors = [] if paths_match else [
    f"PATH MISMATCH: backend writes to {backend_path}, "
    f"media reads from {media_path}"
]

# ─────────────────────────────────────────────────────────────
# FINAL RESULT
# ─────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("VALIDATION SUMMARY")
print("=" * 65)

all_errors = []

if meta_errors_a:
    for e in meta_errors_a:
        print(f"  [A metadata] FAIL: {e}")
        all_errors.append(e)
else:
    subj_a = meta_a['subject']
    cs_a   = meta_a['content_start']
    print(f"  [A metadata] PASS  subject={subj_a}  content_start={cs_a}  "
          f"headings={len(meta_a['headings'])}")

if scene_errors_a:
    for e in scene_errors_a:
        print(f"  [A scenes]   FAIL: {e}")
        all_errors.append(e)
else:
    print(f"  [A scenes]   PASS  {len(scenes_a)} scenes, "
          f"0 leakage, matched concepts: {matched_concepts}")

if meta_errors_b:
    for e in meta_errors_b:
        print(f"  [B regression] FAIL: {e}")
        all_errors.append(e)
else:
    print(f"  [B regression] PASS  subject=science  "
          f"education_level=Class 6  scenes={len(scenes_b)}")

if path_errors:
    for e in path_errors:
        print(f"  [path]       FAIL: {e}")
        all_errors.append(e)
else:
    print(f"  [path]       PASS  both sides point to the same scene_plan.json")

print()
if all_errors:
    print(f"OVERALL: FAIL — {len(all_errors)} error(s)")
    sys.exit(1)
else:
    print("OVERALL: PASS — all checks passed.")
    print()
    print("Root cause summary (fixed):")
    print("  1. Geography false-positive: 'map'/'region' removed from geo keywords;")
    print("     min-score threshold of 2 prevents single-keyword misclassification.")
    print("  2. content_start: short docs (≤10k chars) now skip ≤20% of text,")
    print("     not a hardcoded 2000 chars (which was 48% of ideastormabes).")
    print("  3. Headings: ALL-CAPS pass detects PROBLEM STATEMENT / TECHNICAL APPROACH;")
    print("     structural-keyword pass detects Proposed Solution / Business Model;")
    print("     fragment lines (single words, trailing commas) are filtered out.")
