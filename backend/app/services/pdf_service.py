import re
from io import BytesIO

# ─────────────────────────────────────────────────────────────
# KRUTI DEV → UNICODE DEVANAGARI MAPPING
# Covers the full Kruti Dev 010 / 011 / 016 character set
# used in most legacy Hindi government textbooks.
# ─────────────────────────────────────────────────────────────

_KRUTI_MAP = {
    # Vowels (independent)
    'v': 'अ', 'vk': 'आ', 'b': 'इ', 'bZ': 'ई',
    'm': 'उ', 'Å': 'ऊ', '_': 'ऋ', ',': 'ए',
    ',s': 'ऐ', 'vks': 'ओ', 'vkS': 'औ', 'va': 'अं', 'v%': 'अः',

    # Consonants
    'd': 'क', '[k': 'ख', 'x': 'ग', 'Ä': 'घ', 'M+': 'ङ',
    'p': 'च', 'N': 'छ', 't': 'ज', '>': 'झ', '¥': 'ञ',
    'V': 'ट', 'B': 'ठ', 'M': 'ड', '<': 'ढ', '.k': 'ण',
    'r': 'त', 'Fk': 'थ', 'n': 'द', '/k': 'ध', 'u': 'न',
    'i': 'प', 'Q': 'फ', 'c': 'ब', 'Hk': 'भ', 'e': 'म',
    'y': 'ल', 'o': 'व', '\"k': 'श', ';k': 'ष', 'l': 'स',
    'g': 'ह', '{k': 'क्ष', 'K': 'ज्ञ', 'J': 'श्र',
    'f=': 'त्र', 'j': 'र', 'y+': 'ळ',

    # Matras (vowel signs)
    'k': 'ा', 'f': 'ि', 'h': 'ी', 'q': 'ु', 'w': 'ू',
    '^': 'ृ', 's': 'े', 'S': 'ै', 'ks': 'ो', 'kS': 'ौ',
    'a': 'ं', '%': 'ः', '~': '्',

    # Halant and special
    '~j': 'र्', 'Z': 'र्', 'z': 'र्',
    'Ø': 'क्र', 'Ý': 'फ्र', 'Þ': 'ड्र', 'ß': 'ढ्र',

    # Digits
    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९',

    # Punctuation
    '¼': '(', '½': ')', '&': '-', ',d': 'एक',
}

# Single-char fast lookup for the most common substitutions
_KRUTI_SINGLE = {
    'v': 'अ', 'b': 'इ', 'm': 'उ', 'Å': 'ऊ',
    'd': 'क', 'x': 'ग', 'p': 'च', 'N': 'छ',
    't': 'ज', '¥': 'ञ', 'V': 'ट', 'B': 'ठ',
    'M': 'ड', 'r': 'त', 'n': 'द', 'u': 'न',
    'i': 'प', 'Q': 'फ', 'c': 'ब', 'e': 'म',
    'y': 'ल', 'o': 'व', 'l': 'स', 'g': 'ह',
    'j': 'र', 'K': 'ज्ञ', 'J': 'श्र',
    'k': 'ा', 'f': 'ि', 'h': 'ी', 'q': 'ु',
    'w': 'ू', '^': 'ृ', 's': 'े', 'S': 'ै',
    'a': 'ं', '%': 'ः', '~': '्', 'Z': 'र्',
    'y': 'ल', ',': 'ए', ';': 'य',
}


def _is_kruti_encoded(text: str) -> bool:
    """
    Heuristic: if text has very few Unicode Devanagari chars but
    contains patterns typical of Kruti Dev romanisation, return True.
    """
    if not text:
        return False
    total_alpha = len(re.findall(r'[A-Za-z]', text))
    hindi_unicode = len(re.findall(r'[\u0900-\u097F]', text))
    if total_alpha < 20:
        return False
    # Kruti Dev signatures: 'fganh', 'd{kk', 'ikB', 'dfo', 'xqfM'
    kruti_patterns = ['fganh', 'd{kk', 'ikB', 'dfo', 'xqfM', 'frryh',
                      'fo"k;', 'o.kZ', 'dkO;', 'dgkuh', 'Hkk"kk']
    has_pattern = any(p in text for p in kruti_patterns)
    return has_pattern and hindi_unicode == 0


def _decode_kruti_word(word: str) -> str:
    """
    Decode a single Kruti Dev encoded word to Unicode Devanagari.
    Uses a greedy multi-char match approach.
    """
    result = []
    i = 0
    while i < len(word):
        # Try longest match first (up to 3 chars)
        matched = False
        for length in (3, 2):
            chunk = word[i:i+length]
            if chunk in _KRUTI_MAP:
                result.append(_KRUTI_MAP[chunk])
                i += length
                matched = True
                break
        if not matched:
            ch = word[i]
            result.append(_KRUTI_SINGLE.get(ch, ch))
            i += 1
    return ''.join(result)


def _decode_kruti_text(text: str) -> str:
    """
    Decode a full Kruti Dev encoded string to Unicode Devanagari.
    Preserves spaces, newlines, digits, and punctuation.
    """
    lines = text.split('\n')
    decoded_lines = []
    for line in lines:
        words = line.split(' ')
        decoded_words = []
        for word in words:
            if re.search(r'[A-Za-z]', word):
                decoded_words.append(_decode_kruti_word(word))
            else:
                decoded_words.append(word)
        decoded_lines.append(' '.join(decoded_words))
    return '\n'.join(decoded_lines)


# ─────────────────────────────────────────────────────────────
# PDF METADATA ANALYSIS
# ─────────────────────────────────────────────────────────────

# Subject keyword sets for detection
_SUBJECT_KEYWORDS = {
    "mathematics": [
        "theorem", "equation", "algebra", "geometry", "calculus",
        "integer", "fraction", "triangle", "circle", "polynomial",
        "गणित", "समीकरण", "त्रिभुज", "वृत्त", "बीजगणित",
    ],
    "science": [
        "cell", "organism", "photosynthesis", "atom", "molecule",
        "force", "energy", "gravity", "chemical", "biology",
        "विज्ञान", "कोशिका", "परमाणु", "ऊर्जा", "रासायनिक",
    ],
    "history": [
        "war", "empire", "revolution", "century", "civilization",
        "king", "dynasty", "independence", "ancient", "medieval",
        "इतिहास", "युद्ध", "साम्राज्य", "स्वतंत्रता", "राजवंश",
    ],
    "geography": [
        "continent", "ocean", "climate", "latitude", "longitude",
        "mountain", "river", "population",
        # NOTE: "map" and "region" intentionally removed — too ambiguous
        # (e.g. "geo-location mapping", "regional languages" would false-match)
        "भूगोल", "महाद्वीप", "जलवायु", "पर्वत", "नदी",
    ],
    "hindi_literature": [
        "कविता", "कहानी", "पाठ", "गद्य", "पद्य", "निबंध",
        "वर्णमाला", "व्याकरण", "शब्द", "वाक्य", "भाषा",
        "poem", "story", "lesson", "grammar", "literature",
    ],
    "computer_science": [
        "algorithm", "program", "software", "hardware", "network",
        "database", "artificial intelligence", "machine learning",
        "कंप्यूटर", "प्रोग्राम", "सॉफ्टवेयर",
    ],
    # Tech/startup/project documents (hackathons, proposals, pitches)
    # Use multi-word and highly specific phrases — avoid single generic tokens
    # like "app", "ai", "cloud" that appear in any modern textbook.
    "technology": [
        "tech stack", "frontend:", "backend:", "rest api", "microservice",
        "mobile-first", "mvp", "prototype", "scalable cloud",
        "business model", "problem statement", "proposed solution",
        "feasibility", "viability", "stakeholder",
        "biosecurity", "livestock", "pig farm", "poultry farm",
        "smart portal", "digital portal", "hackathon", "idea submission",
        "iot sensor", "blockchain", "react", "node.js", "mongodb", "tensorflow",
    ],
    "civics": [
        "constitution", "democracy", "government", "parliament",
        "rights", "citizen", "election", "law", "policy",
        "संविधान", "लोकतंत्र", "सरकार", "संसद", "नागरिक",
    ],
    "economics": [
        "market", "demand", "supply", "gdp", "inflation",
        "trade", "currency", "bank", "investment", "poverty",
        "अर्थशास्त्र", "बाजार", "मांग", "आपूर्ति", "व्यापार",
    ],
}

# Education level detection patterns (Arabic and Roman numerals, Hindi digits)
_LEVEL_PATTERNS = [
    (r'class\s*(\d+)',                          'Class {}'),
    (r'grade\s*(\d+)',                          'Grade {}'),
    (r'std\.?\s*(\d+)',                         'Class {}'),
    (r'standard\s*(\d+)',                       'Class {}'),
    (r'कक्षा\s*([\d\u0967-\u096F]+)',           'कक्षा {}'),
    # Roman numerals: CLASS VI, CLASS XII, etc.
    (r'class\s+(i{1,3}|iv|vi{0,3}|ix|xi{0,2}|xii)\b', 'Class {}'),
    (r'grade\s+(i{1,3}|iv|vi{0,3}|ix|xi{0,2}|xii)\b', 'Grade {}'),
]

_ROMAN_TO_INT = {
    'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5,
    'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10,
    'xi': 11, 'xii': 12,
}

_HINDI_DIGITS = {'\u0967': '1', '\u0968': '2', '\u0969': '3', '\u096a': '4', '\u096b': '5',
                 '\u096c': '6', '\u096d': '7', '\u096e': '8', '\u096f': '9', '\u0966': '0'}


def _normalize_digit(s: str) -> str:
    s = ''.join(_HINDI_DIGITS.get(c, c) for c in s)
    return str(_ROMAN_TO_INT.get(s.lower(), s))


# Lines that are definitely boilerplate — never chapter headings
_BOILERPLATE_PATTERNS = [
    r'^\d{4}[-–]\d{2,4}$',                          # "2018-19"
    r'^(january|february|march|april|may|june|july|august|september|october|november|december)',
    r'^(first|second|third|fourth|fifth|reprint)',   # "First Edition"
    r'^pd\s+\d',                                     # "PD 750T RPS"
    r'^isbn',                                        # "ISBN 81-..."
    r'^all rights reserved',
    r'^no part of this',
    r'^this book is sold',
    r'^the correct price',
    r'^offices of',
    r'^ncert campus',
    r'^cwc',
    r'^publication team',
    r'^head,',
    r'^chief',
    r'^printed on',
    r'^published at',
    r'^phone\s*:',
    r'^\d{3},',                                      # "108, 100 Feet Road"
    r'\d{6}',                                        # phone/pin codes
    r'^(foreword|preface|acknowledgement|contents)$',
    r'^©',
    r'national council of educational',
    r'research and training',
    r'\bncert\b',
    r'^cover and layout',
    r'^editor\s*:',
    r'^printed at',
    r'gita offset',
    r'okhla industrial',
    r'sri aurobindo marg',
    r'navjivan trust',
    r'hosdakere',
    r'banashankari',
    r'panihati',
    r'maligaon',
    r'guwahati',
    r'ahmedabad',
    r'bengaluru',
    r'kolkata',
    # Hindi boilerplate
    r'^पुनर्मुद्रण',
    r'^प्रथम संस्करण',
    r'^सर्वाधिकार',
    r'^राष्ट्रीय शैक्षिक',
]

# Chapter/heading indicator patterns — these lines ARE headings
_HEADING_INDICATORS = [
    r'^chapter\s+\d+',
    r'^unit\s+\d+',
    r'^lesson\s+\d+',
    r'^पाठ\s+\d+',
    r'^अध्याय\s+\d+',
    r'^इकाई\s+\d+',
    r'^part\s+\d+',
    r'^section\s+\d+',
]


def _is_boilerplate_line(line: str) -> bool:
    """Return True if this line is publication/copyright boilerplate."""
    ll = line.lower().strip()
    for pat in _BOILERPLATE_PATTERNS:
        if re.search(pat, ll):
            return True
    return False


def _is_heading_line(line: str) -> bool:
    """Return True if this line looks like a chapter/topic heading."""
    ll = line.lower().strip()
    for pat in _HEADING_INDICATORS:
        if re.match(pat, ll):
            return True
    return False


# Matches spaced-letter chapter headers like "C  H  A  P  T  E  R     1"
_SPACED_CHAPTER_RE = re.compile(
    r'C\s+H\s+A\s+P\s+T\s+E\s+R\s+(\d+)',
    re.IGNORECASE
)

# Matches Hindi chapter headers like "अध्याय 1" or "पाठ 1"
_HINDI_CHAPTER_RE = re.compile(
    r'(अध्याय|पाठ|इकाई)\s*(\d+|[\u0967-\u096F]+)',
    re.UNICODE
)


def _extract_spaced_chapter_headings(text: str) -> tuple:
    """
    Extract chapter titles from spaced-letter format (NCERT-style PDFs).
    Pattern: 'C  H  A  P  T  E  R     N\nCHAPTER TITLE\nPAGE_NUMBER'
    Returns (headings_list, content_start_offset).
    content_start is set to just after the last TOC entry.
    """
    headings = []
    last_toc_end = 0
    seen = set()

    for m in _SPACED_CHAPTER_RE.finditer(text):
        # The chapter title is on the next non-empty line after the match
        after = text[m.end():m.end() + 200]
        lines_after = after.split('\n')
        for ln in lines_after:
            ln = ln.strip()
            # Skip blank lines and pure page numbers
            if not ln or re.match(r'^[\d\s]+$', ln):
                continue
            # Skip year markers like "2018-19"
            if re.match(r'^\d{4}-\d{2}$', ln):
                continue
            # This is the chapter title
            key = ln[:35].lower()
            if key not in seen:
                seen.add(key)
                headings.append(ln)
            last_toc_end = m.end() + after.find(ln) + len(ln)
            break

    return headings, last_toc_end


def _find_content_start(text: str) -> int:
    """
    Find the character offset where actual educational content begins.
    Priority:
    1. Spaced-letter CHAPTER pattern (NCERT-style) — use end of last TOC entry
    2. Plain 'Chapter N' heading
    3. Hindi chapter heading
    4. Fallback: skip first 2000 chars ONLY for long documents (>10000 chars).
       For short documents (<= 10000 chars) skip at most 20% to avoid
       cutting into actual content (e.g. a 4000-char pitch deck).
    """
    # Strategy 1: spaced-letter CHAPTER (NCERT)
    _, last_toc_end = _extract_spaced_chapter_headings(text)
    if last_toc_end > 0:
        tail = text[last_toc_end:last_toc_end + 50]
        extra = re.match(r'[\s\d\-–]+', tail)
        skip = extra.end() if extra else 0
        return last_toc_end + skip

    # Strategy 2: plain 'Chapter N' or Hindi chapter heading
    for pat in [r'\bChapter\s+1\b', r'\bCHAPTER\s+1\b',
                r'अध्याय\s*1', r'पाठ\s*1', r'इकाई\s*1']:
        m = re.search(pat, text)
        if m:
            return m.start()

    # Fallback: cap the skip at 20% of text length for short docs
    if len(text) > 10000:
        return 2000
    return min(500, len(text) // 5)


def analyze_pdf_metadata(text: str) -> dict:
    """
    Analyze extracted PDF text to detect:
    - language (hi/en)
    - subject
    - education_level
    - chapter/topic headings (boilerplate filtered)
    Returns a dict used to guide AI scene generation.
    """
    # Language detection
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    total_alpha = len(re.findall(r'[A-Za-z\u0900-\u097F]', text))
    language = "hi" if total_alpha > 0 and (hindi_chars / total_alpha) > 0.3 else "en"

    text_lower = text.lower()

    # Subject detection — score each subject by keyword hits
    subject_scores = {}
    for subject, keywords in _SUBJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            subject_scores[subject] = score

    # Require at least 2 keyword hits to claim a subject; otherwise "general".
    # This prevents a single generic word ("map", "river") from mislabelling
    # a tech/startup document as "geography".
    strong = {s: sc for s, sc in subject_scores.items() if sc >= 2}
    if strong:
        detected_subject = max(strong, key=strong.get)
    elif subject_scores:
        # Only one subject has any hits AND score == 1 — use it only if unique
        if len(subject_scores) == 1:
            detected_subject = next(iter(subject_scores))
        else:
            detected_subject = "general"
    else:
        detected_subject = "general"

    # Education level detection
    detected_level = None
    for pattern, template in _LEVEL_PATTERNS:
        m = re.search(pattern, text_lower)
        if m:
            num = _normalize_digit(m.group(1))
            detected_level = template.format(num)
            break

    # Chapter/topic heading extraction
    # Try spaced-letter NCERT format first
    spaced_headings, last_toc_end = _extract_spaced_chapter_headings(text)
    if spaced_headings:
        headings = spaced_headings
        # content_start = just after the last TOC entry
        tail = text[last_toc_end:last_toc_end + 50]
        extra = re.match(r'[\s\d\-\u2013]+', tail)
        skip = extra.end() if extra else 0
        content_start = last_toc_end + skip
    else:
        content_start = _find_content_start(text)
        content_text = text[content_start:]
        headings = []
        seen = set()

        # ── Pass 1: ALL-CAPS lines (presentation/pitch-deck style) ──────
        # e.g. "PROBLEM STATEMENT", "TECHNICAL APPROACH", "BUSINESS MODEL"
        # Must be 6–60 chars, mostly uppercase alpha, not pure boilerplate.
        for line in content_text.split('\n'):
            line = line.strip()
            if len(line) < 6 or len(line) > 60:
                continue
            alpha = re.findall(r'[A-Za-z]', line)
            if len(alpha) < 4:
                continue
            if _is_boilerplate_line(line):
                continue
            upper = sum(1 for c in alpha if c.isupper())
            # ≥ 80% uppercase letters → treat as a section heading
            if upper / len(alpha) >= 0.80:
                key = line[:35].lower()
                if key not in seen:
                    seen.add(key)
                    headings.append(line)

        # ── Pass 2: Mixed-case heading indicators ────────────────────────
        # e.g. "Proposed Solution", "Challenges Faced", "Business Model"
        # Heuristic: 4–60 chars, starts with capital, ≥ 2 words, no
        # sentence punctuation (no period/comma mid-line).
        _HEADING_START_RE = re.compile(
            r'^[A-Z\u0900-\u097F❖•][^\n]{3,58}$'
        )
        for line in content_text.split('\n'):
            line = line.strip()
            # Remove leading bullet/arrow chars
            line = re.sub(r'^[❖•▶➤→\-–]+\s*', '', line).strip()
            if len(line) < 6 or len(line) > 60:
                continue
            # Must start with capital or Hindi char
            if not _HEADING_START_RE.match(line):
                continue
            alpha = re.findall(r'[A-Za-z\u0900-\u097F]', line)
            if len(alpha) < 5:
                continue
            if _is_boilerplate_line(line):
                continue
            # Reject lines that look like sentence fragments or list items:
            # - ends with a comma, has only 1 word, or contains a full stop mid-line
            words = line.split()
            if len(words) < 2:
                continue
            if line.endswith(',') or line.endswith(':'):
                continue
            # Must be _is_heading_line OR look like a title (Title Case / ALL CAPS)
            # OR match common structural heading keywords
            _STRUCTURAL_KW = re.compile(
                r'\b(problem|solution|approach|model|impact|benefit|'
                r'challenge|feasib|viabilit|prototype|overview|introduc|'
                r'background|objective|scope|method|result|conclusion|'
                r'summary|recommend|implement|architecture|design|system|'
                r'feature|requirement|technical|business|financial|'
                r'market|vision|mission|team|participant|title)\b',
                re.IGNORECASE
            )
            is_title_case = sum(1 for w in words if w and w[0].isupper()) >= len(words) * 0.6
            is_structural = bool(_STRUCTURAL_KW.search(line))
            if not (is_title_case or is_structural or _is_heading_line(line)):
                continue
            key = line[:35].lower()
            if key not in seen:
                seen.add(key)
                headings.append(line)
            if len(headings) >= 20:
                break

    return {
        "language": language,
        "subject": detected_subject,
        "education_level": detected_level,
        "headings": headings,
        "content_start": content_start,
        "text_length": len(text),
    }


# ─────────────────────────────────────────────────────────────
# MAIN EXTRACTION FUNCTION
# ─────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_data: bytes) -> str:
    """
    Extract text from PDF bytes.
    1. Try pymupdf (fitz) first — handles most PDFs.
    2. Fall back to pypdf.
    3. If extracted text looks like Kruti Dev encoding, decode it.
    """
    text = ""

    # ── Try pymupdf ──────────────────────────────────────────
    try:
        import fitz
        pdf_doc = fitz.open(stream=file_data, filetype="pdf")
        for page in pdf_doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        pdf_doc.close()
    except Exception:
        text = ""

    # ── Fall back to pypdf ───────────────────────────────────
    if not text.strip():
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(file_data))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    text = text.strip()

    if not text:
        raise Exception("No text could be extracted from the PDF")

    # ── Decode Kruti Dev if detected ─────────────────────────
    if _is_kruti_encoded(text):
        text = _decode_kruti_text(text)

    return text
