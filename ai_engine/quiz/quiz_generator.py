import random
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


# ================================================================
# LANGUAGE CONSTANTS (generic English function words, no topic data)
# ================================================================

ARTICLES = {"the", "a", "an"}

DETERMINERS = ARTICLES | {
    "this", "that", "these", "those", "its", "their", "each", "every",
    "some", "any", "all", "most", "many",
}

PREPOSITIONS = {
    "in", "on", "at", "by", "for", "from", "to", "of", "with", "within",
    "into", "onto", "through", "during", "over", "under", "between",
    "among", "across", "along", "about", "after", "before", "without",
    "via", "around", "near", "inside", "outside", "toward", "towards",
}

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "being",
    "been", "of", "to", "in", "on", "for", "from", "by", "with",
    "and", "or", "but", "as", "at", "into", "through", "during",
    "while", "that", "this", "these", "those", "it", "they",
    "them", "their", "its", "which", "who", "what", "when",
    "where", "why", "how", "can", "may", "might", "could", "would",
    "should", "will", "also", "than", "then", "there", "here",
    "one", "some", "any", "all", "other", "another", "more",
    "most", "very", "important", "mainly", "generally",
}

MEANING_STOP = STOPWORDS | PREPOSITIONS | ARTICLES
END_STOP = MEANING_STOP | {"not", "very", "so", "if"}

VAGUE_STARTS = {
    "it", "they", "them", "he", "she", "we", "you", "this", "these",
    "those", "that", "such", "there", "here", "which", "who", "whom",
    "what", "its", "their", "his", "her", "another", "other", "both",
    "however", "also", "thus", "then", "so",
}

DANGLING_PRONOUNS = {"it", "them", "they", "this", "these", "those"}

SUBJECT_BLOCK = {
    "that", "which", "who", "whom", "when", "if", "while", "because",
    "although", "since", "as", "than", "but", "whereas", "unless",
    "not", "also", "can", "may", "might", "could", "should", "would",
    "will", "must", "does", "do", "did", "have", "has", "had", "be",
    "been", "being", "is", "are", "was", "were",
}

BAD_OPTION_STARTS = {
    "and", "or", "but", "so", "because", "which", "that", "whereas",
}

BAD_OPTION_TEXT = ("all of the above", "none of the above", "both a and b")

BAD_QUESTION_PATTERNS = (
    "what is it",
    "what is this",
    "what does it",
    "what are they",
)

DISCOURSE_PREFIX = re.compile(
    r"^(?:however|therefore|thus|also|additionally|moreover|furthermore|"
    r"in addition|for example|for instance|in fact|overall|finally|"
    r"consequently|similarly|as a result|in general|generally)\s*,?\s+",
    re.IGNORECASE,
)

OBJECT_CUT = re.compile(
    r",?\s+(?:which|that|where|when|while|because|since|although|whereas|"
    r"unless|if|during|using|so that|in order to|but|and then|"
    r"as well as)\s+|;|\s+-\s+",
    re.IGNORECASE,
)

SUBJECT = r"(?P<s>[^,;:]{3,90}?)"


# ================================================================
# RELATION TABLES (grammar only: verb forms and answer categories)
# ================================================================

# (singular form, plural form, base form, answer group)
_RELATIONS = [
    ("requires", "require", "require", "input"),
    ("needs", "need", "need", "input"),
    ("uses", "use", "use", "input"),
    ("depends on", "depend on", "depend on", "input"),
    ("relies on", "rely on", "rely on", "input"),
    ("absorbs", "absorb", "absorb", "input"),
    ("contains", "contain", "contain", "part"),
    ("consists of", "consist of", "consist of", "part"),
    ("includes", "include", "include", "part"),
    ("has", "have", "have", "part"),
    ("stores", "store", "store", "part"),
    ("produces", "produce", "produce", "output"),
    ("creates", "create", "create", "output"),
    ("forms", "form", "form", "output"),
    ("generates", "generate", "generate", "output"),
    ("releases", "release", "release", "output"),
    ("results in", "result in", "result in", "output"),
    ("leads to", "lead to", "lead to", "output"),
    ("causes", "cause", "cause", "output"),
    ("supports", "support", "support", "output"),
    ("controls", "control", "control", "output"),
    ("regulates", "regulate", "regulate", "output"),
    ("provides", "provide", "provide", "output"),
]

# surface form -> (base, group, is_singular)
_REL_LOOKUP: Dict[str, Any] = {}
for _sing, _plur, _base, _group in _RELATIONS:
    _REL_LOOKUP[_sing] = (_base, _group, True)
    _REL_LOOKUP[_plur] = (_base, _group, False)

_PURPOSE_TAIL_VERBS = {
    "produce": "produce", "create": "create", "make": "make",
    "form": "form", "generate": "generate", "release": "release",
    "build": "build",
}

_MOTION_PAIRS = [
    ("enters", "enter"), ("exits", "exit"), ("leaves", "leave"),
    ("passes", "pass"), ("flows", "flow"), ("moves", "move"),
    ("travels", "travel"), ("diffuses", "diffuse"),
    ("escapes", "escape"), ("spreads", "spread"),
]
_MOTION_LOOKUP: Dict[str, Any] = {}
for _sing, _base in _MOTION_PAIRS:
    _MOTION_LOOKUP[_sing] = (_base, True)
    _MOTION_LOOKUP[_base] = (_base, False)

_OCCUR_LOOKUP = {
    "occurs": ("occur", True), "occur": ("occur", False),
    "takes place": ("take place", True), "take place": ("take place", False),
    "happens": ("happen", True), "happen": ("happen", False),
    "develops": ("develop", True), "develop": ("develop", False),
    "lives": ("live", True), "live": ("live", False),
    "grows": ("grow", True), "grow": ("grow", False),
}


def _alternation(forms) -> str:
    ordered = sorted(forms, key=len, reverse=True)
    return "|".join(
        r"\s+".join(re.escape(part) for part in form.split())
        for form in ordered
    )


_PLACE_PREPS = (
    r"in|inside|within|at|on|near|throughout|beneath|under|around"
)

_LOCATION_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<aux>is|are)\s+"
    r"(?P<v>found|located|situated|stored|kept|held|present|contained)\s+"
    rf"(?P<prep>{_PLACE_PREPS})\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_OCCUR_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<v>{_alternation(_OCCUR_LOOKUP)})\s+"
    r"(?P<mod>(?:mainly|mostly|primarily|largely|only)\s+)?"
    rf"(?P<prep>{_PLACE_PREPS})\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_AGENT_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<aux>is|are|can be|may be|could be|might be|"
    r"must be|will be)\s+"
    r"(?P<v>\w+ed|made|given|taken|driven|held|known|shown|seen|built|"
    r"grown|chosen|broken)\s+by\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_MOTION_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<v>{_alternation(_MOTION_LOOKUP)})\s+"
    r"(?P<mid>(?:[\w-]+\s+){0,4}?)"
    r"(?P<prep>through|via|across|along)\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_PURPOSE_RE = re.compile(
    rf"^{SUBJECT}\s+(?:is|are)\s+"
    r"(?:(?:mainly|mostly|primarily|often|commonly)\s+)?used\s+"
    r"(?P<p>to|for)\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_RELATION_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<v>{_alternation(_REL_LOOKUP)})\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_BECAUSE_RE = re.compile(
    r"^(?P<e>.{15,160}?),?\s+because\s+(?!of\b)(?P<r>.{12,160})$",
    re.IGNORECASE,
)

_DEFINE_RE = re.compile(
    rf"^{SUBJECT}\s+(?P<aux>is|are)\s+(?P<o>.+)$",
    re.IGNORECASE,
)

_REFER_RE = re.compile(
    rf"^{SUBJECT}\s+(?:refers to|refer to|means|mean|is defined as|"
    r"are defined as|denotes|denote)\s+(?P<o>.+)$",
    re.IGNORECASE,
)


# ================================================================
# DATA STRUCTURES
# ================================================================

@dataclass
class _Fact:
    kind: str                 # definition, location, purpose, relation, reason
    subject: str
    answer: str
    sentence: str
    index: int
    stem: str
    group: str = ""
    items: List[str] = field(default_factory=list)
    prep: str = ""
    extra: Dict[str, str] = field(default_factory=dict)


@dataclass
class _Entity:
    text: str
    role: str                 # subject, object, item, location, definition, ...
    group: str
    index: int


@dataclass
class _Candidate:
    stem: str
    correct: str
    distractors: List[str]
    explanation: str
    kind: str
    index: int
    subject: str
    quality: float
    answer_parts: List[str]
    is_list: bool = False


@dataclass
class _Doc:
    text: str
    sentences: List[str]
    keys: List[str]           # padded, normalised sentence keys
    lower_vocab: Set[str]
    word_count: int
    entities: List[_Entity] = field(default_factory=list)


# ================================================================
# GENERATOR
# ================================================================

class QuizGenerator:
    """
    Source-grounded MCQ generator.

    Pipeline: clean text -> split sentences -> extract structured facts
    (definition, location, function, inputs/outputs, agent, reason, ...)
    -> build questions with distractors taken from other entities in the
    same document -> validate -> pick a diverse subset.

    Nothing here depends on the subject matter of the document, and no
    external model is required (the `model` argument is kept only for
    interface compatibility).
    """

    MIN_QUESTIONS = 2
    MAX_QUESTIONS = 10

    def __init__(self, model=None):
        self.model = model
        self._rng = random.Random()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def generate(
        self,
        text: str,
        education_level: str = "Grade 9",
        number_of_questions: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Returns {"questions": [...], "requested_questions": int,
        "generated_questions": int}.

        Each question is {"question", "options", "correct_answer",
        "explanation"}. If `number_of_questions` is given it is honoured
        (clamped to 2-10) as far as the document supports it; otherwise the
        count is derived from the document. `education_level` is accepted
        for interface compatibility.
        """

        if not text or not str(text).strip():
            raise ValueError("Input educational text cannot be empty.")

        doc = self._prepare(str(text))

        if len(doc.sentences) < 2:
            raise ValueError(
                "The educational content does not contain enough information "
                "to create a reliable quiz."
            )

        facts = self._extract_facts(doc)
        doc.entities = self._build_entities(facts)

        candidates: List[_Candidate] = []
        for fact in facts:
            candidate = self._build_candidate(fact, doc)
            if candidate and self._validate(candidate):
                candidates.append(candidate)

        target = self._target_count(doc, number_of_questions)
        selected = self._select(candidates, target, len(doc.sentences))

        questions = [self._finalize(candidate) for candidate in selected]

        if len(questions) < self.MIN_QUESTIONS:
            raise ValueError(
                "The uploaded content does not contain enough distinct "
                "source-grounded facts to create at least two reliable "
                "multiple-choice questions."
            )

        return {
            "questions": questions,
            "requested_questions": target,
            "generated_questions": len(questions),
        }

    # ============================================================
    # TEXT PREPARATION
    # ============================================================

    def _prepare(self, text: str) -> _Doc:
        clean = self._clean_text(text)
        sentences = self._split_sentences(clean)

        keys = [f" {self._key(s)} " for s in sentences]
        lower_vocab = set(re.findall(r"\b[a-z][a-z-]*\b", clean))

        return _Doc(
            text=clean,
            sentences=sentences,
            keys=keys,
            lower_vocab=lower_vocab,
            word_count=len(clean.split()),
        )

    def _clean_text(self, text: str) -> str:
        text = text.replace("\x00", " ").replace("\r", "\n")
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
        lines = [line for line in lines if line]

        starts_new = re.compile(r"^(?:[A-Z0-9\"'(]|[-•*–])")
        output: List[str] = []

        for position, line in enumerate(lines):
            following = lines[position + 1] if position + 1 < len(lines) else ""
            words = line.split()
            ends_cleanly = line[-1] in ".!?:\"')”"
            next_starts_new = (not following) or bool(starts_new.match(following))

            # Short unpunctuated lines followed by a new line are headings.
            if not ends_cleanly and len(words) <= 8 and next_starts_new:
                continue

            line = re.sub(r"^\s*(?:[-•*–]+|\d+[.)])\s+", "", line)

            if not ends_cleanly and next_starts_new:
                line += "."

            output.append(line)

        return re.sub(r"\s+", " ", " ".join(output)).strip()

    def _split_sentences(self, text: str) -> List[str]:
        protected = re.sub(
            r"\b(e\.g|i\.e|vs|Mr|Mrs|Ms|Dr|Prof|Fig|approx)\.",
            lambda m: m.group(1) + "§",
            text,
            flags=re.IGNORECASE,
        )
        protected = re.sub(r"\b([A-Z])\.", r"\1§", protected)

        parts = re.split(
            r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])|(?<=[.!?][\"')])\s+(?=[A-Z])",
            protected,
        )

        sentences: List[str] = []
        seen: Set[str] = set()

        for part in parts:
            sentence = part.replace("§", ".").strip()
            words = sentence.split()

            if not 6 <= len(words) <= 60 or len(sentence) > 300:
                continue
            if sentence.endswith("?"):
                continue
            if sum(c.isalpha() for c in sentence) < 0.6 * len(sentence):
                continue

            key = self._key(sentence)
            if key in seen:
                continue

            seen.add(key)
            sentences.append(sentence)

        return sentences

    def _work_sentence(self, sentence: str) -> str:
        work = re.sub(r"\([^)]*\)", "", sentence)
        work = DISCOURSE_PREFIX.sub("", work)
        work = re.sub(r"\s+", " ", work).strip().rstrip(".!?:;")
        return work if len(work.split()) >= 5 else ""

    # ============================================================
    # QUESTION COUNT
    # ============================================================

    def _target_count(self, doc: _Doc, requested: Optional[int]) -> int:
        if requested is not None:
            try:
                count = int(requested)
            except (TypeError, ValueError):
                count = None
            if count is not None:
                return max(self.MIN_QUESTIONS, min(self.MAX_QUESTIONS, count))

        thresholds = [
            (120, 2), (220, 3), (400, 4), (650, 5),
            (900, 6), (1200, 7), (1600, 8), (2200, 9),
        ]
        for limit, count in thresholds:
            if doc.word_count < limit:
                return count
        return self.MAX_QUESTIONS

    # ============================================================
    # FACT EXTRACTION
    # ============================================================

    def _extract_facts(self, doc: _Doc) -> List[_Fact]:
        extractors = (
            self._location_facts,
            self._reason_facts,
            self._agent_facts,
            self._motion_facts,
            self._purpose_facts,
            self._relation_facts,
            self._definition_facts,
        )

        facts: List[_Fact] = []

        for index, sentence in enumerate(doc.sentences):
            work = self._work_sentence(sentence)
            if not work:
                continue

            for extractor in extractors:
                facts.extend(extractor(work, sentence, index, doc))

        return facts

    def _location_facts(self, work, sentence, index, doc) -> List[_Fact]:
        facts = []

        match = _LOCATION_RE.match(work)
        if match:
            subject = self._clean_subject(match.group("s"))
            place = self._clean_object(match.group("o"), 10)
            if subject and place:
                aux = match.group("aux").lower()
                verb = match.group("v").lower()
                stem = (
                    f"According to the material, where {aux} "
                    f"{self._stem_subject(subject, doc)} {verb}?"
                )
                facts.append(self._location_fact(
                    subject, place, match.group("prep"), sentence, index, stem,
                ))

        match = _OCCUR_RE.match(work)
        if match:
            subject = self._clean_subject(match.group("s"))
            place = self._clean_object(match.group("o"), 10)
            if subject and place:
                base, _ = _OCCUR_LOOKUP[
                    re.sub(r"\s+", " ", match.group("v").lower())
                ]
                modifier = (match.group("mod") or "").lower()
                stem = (
                    f"According to the material, where does "
                    f"{self._stem_subject(subject, doc)} {modifier}{base}?"
                )
                facts.append(self._location_fact(
                    subject, place, match.group("prep"), sentence, index, stem,
                ))

        return facts

    def _location_fact(self, subject, place, prep, sentence, index, stem):
        prep = prep.lower()
        return _Fact(
            kind="location",
            subject=subject,
            answer=f"{prep} {place}",
            sentence=sentence,
            index=index,
            stem=stem,
            group="location",
            prep=prep,
            extra={"place": place},
        )

    def _reason_facts(self, work, sentence, index, doc) -> List[_Fact]:
        match = _BECAUSE_RE.match(work)
        if not match:
            return []

        effect = self._clean_clause(match.group("e"), 4, 22)
        reason = self._clean_clause(match.group("r"), 4, 22)

        if not effect or not reason:
            return []
        if effect.split()[0].lower() in VAGUE_STARTS | {"if", "when"}:
            return []

        stem = (
            "According to the material, which of the following explains why "
            f"{self._stem_subject(effect, doc)}?"
        )

        return [_Fact(
            kind="reason",
            subject=effect,
            answer=reason,
            sentence=sentence,
            index=index,
            stem=stem,
            group="reason",
        )]

    def _agent_facts(self, work, sentence, index, doc) -> List[_Fact]:
        match = _AGENT_RE.match(work)
        if not match:
            return []

        subject = self._clean_subject(match.group("s"))
        agent = self._clean_object(match.group("o"), 10)

        if not subject or not agent:
            return []
        if agent.split()[0].lower().endswith("ing"):
            return []

        aux = match.group("aux").lower()
        verb = match.group("v").lower()
        stem_subject = self._stem_subject(subject, doc)

        if aux in ("is", "are"):
            stem = (
                f"According to the material, by what {aux} "
                f"{stem_subject} {verb}?"
            )
        else:
            modal = aux.split()[0]
            stem = (
                f"According to the material, by what {modal} "
                f"{stem_subject} be {verb}?"
            )

        return [self._relation_fact(
            subject, agent, "agent", sentence, index, stem,
        )]

    def _motion_facts(self, work, sentence, index, doc) -> List[_Fact]:
        match = _MOTION_RE.match(work)
        if not match:
            return []

        subject = self._clean_subject(match.group("s"))
        route = self._clean_object(match.group("o"), 8)
        if not subject or not route:
            return []

        base, singular = _MOTION_LOOKUP[match.group("v").lower()]
        aux = "does" if singular else "do"
        middle = match.group("mid").strip()
        tail = f" {middle}" if middle else ""
        prep = match.group("prep").lower()

        stem = (
            f"According to the material, {prep} what {aux} "
            f"{self._stem_subject(subject, doc)} {base}{tail}?"
        )

        return [self._relation_fact(
            subject, route, "motion", sentence, index, stem,
        )]

    def _purpose_facts(self, work, sentence, index, doc) -> List[_Fact]:
        match = _PURPOSE_RE.match(work)
        if not match:
            return []

        subject = self._clean_subject(match.group("s"))
        purpose = self._clean_object(match.group("o"), 14)
        if not subject or not purpose:
            return []
        if purpose.split()[0].lower() in ARTICLES:
            return []

        form = match.group("p").lower()
        stem = (
            "According to the material, what is the purpose of "
            f"{self._stem_subject(subject, doc)}?"
        )

        return [_Fact(
            kind="purpose",
            subject=subject,
            answer=f"{form} {purpose}",
            sentence=sentence,
            index=index,
            stem=stem,
            group=form,
        )]

    def _relation_facts(self, work, sentence, index, doc) -> List[_Fact]:
        match = _RELATION_RE.match(work)
        if not match:
            return []

        subject = self._clean_subject(match.group("s"))
        if not subject:
            return []

        base, group, singular = _REL_LOOKUP[
            re.sub(r"\s+", " ", match.group("v").lower())
        ]
        aux = "does" if singular else "do"
        raw_object = match.group("o")

        # "X uses A and B to produce C": keep inputs and the stated output.
        purpose_tail = None
        if base == "use":
            pieces = re.split(r"\s+to\s+", raw_object, maxsplit=1)
            raw_object = pieces[0]
            if len(pieces) == 2:
                purpose_tail = pieces[1]

        answer = self._clean_object(raw_object, 14)
        if not answer:
            return []
        if answer.split()[0].lower() in {"not", "been", "to", "become", "also"}:
            return []

        stem_subject = self._stem_subject(subject, doc)
        facts = [self._relation_fact(
            subject, answer, group, sentence, index,
            f"According to the material, what {aux} {stem_subject} {base}?",
        )]

        if purpose_tail:
            tail = re.match(r"^(\w+)\s+(.+)$", purpose_tail.strip())
            if tail and tail.group(1).lower() in _PURPOSE_TAIL_VERBS:
                verb = _PURPOSE_TAIL_VERBS[tail.group(1).lower()]
                product = self._clean_object(tail.group(2), 10)
                if product:
                    facts.append(self._relation_fact(
                        subject, product, "output", sentence, index,
                        f"According to the material, what {aux} "
                        f"{stem_subject} {verb}?",
                    ))

        return facts

    def _relation_fact(self, subject, answer, group, sentence, index, stem):
        items = self._split_items(answer)
        return _Fact(
            kind="relation",
            subject=subject,
            answer=self._join_items(items),
            sentence=sentence,
            index=index,
            stem=stem,
            group=group,
            items=items,
        )

    def _definition_facts(self, work, sentence, index, doc) -> List[_Fact]:
        facts = []

        for pattern, needs_article in ((_DEFINE_RE, True), (_REFER_RE, False)):
            match = pattern.match(work)
            if not match:
                continue

            subject = self._clean_subject(match.group("s"))
            definition = self._clean_clause(match.group("o"), 3, 30)

            if not subject or not definition:
                continue

            first = definition.split()[0].lower()
            if needs_article and first not in ARTICLES | {"one", "any", "each"}:
                continue
            if first in VAGUE_STARTS | {"not", "also"}:
                continue

            aux = "are" if re.search(
                rf"\s+are\s+", work[: len(subject) + 6], re.IGNORECASE
            ) else "is"
            if pattern is _DEFINE_RE:
                aux = match.group("aux").lower()

            described = (
                definition[0].lower() + definition[1:]
                if first in DETERMINERS else definition
            )

            facts.append(_Fact(
                kind="definition",
                subject=subject,
                answer=definition,
                sentence=sentence,
                index=index,
                stem=(
                    f"According to the material, what {aux} "
                    f"{self._stem_subject(subject, doc)}?"
                ),
                group="definition",
                extra={
                    "term_stem": (
                        "Which of the following terms is described in the "
                        f"material as {described}?"
                    )
                },
            ))
            break

        return facts

    # ============================================================
    # PHRASE CLEANING
    # ============================================================

    def _clean_phrase(self, phrase: str) -> str:
        phrase = re.sub(r"\s+", " ", phrase).strip()
        phrase = re.sub(r"^[\s,;:\-–—\"'“”]+", "", phrase)
        return re.sub(r"[\s,;:\-–—\"'“”]+$", "", phrase)

    def _clean_subject(self, raw: str) -> Optional[str]:
        subject = self._clean_phrase(raw)
        words = subject.split()

        if not 1 <= len(words) <= 9:
            return None

        lowered = [w.lower() for w in words]

        if lowered[0] in VAGUE_STARTS or lowered[-1] in END_STOP:
            return None
        if any(w in SUBJECT_BLOCK for w in lowered):
            return None
        if not self._tokens(subject):
            return None

        return subject

    def _clean_object(self, raw: str, max_words: int) -> Optional[str]:
        text = self._clean_phrase(OBJECT_CUT.split(raw, maxsplit=1)[0])
        return self._check_phrase(text, 1, max_words)

    def _clean_clause(self, raw: str, min_words: int, max_words: int):
        text = self._clean_phrase(re.split(r";", raw, maxsplit=1)[0])
        return self._check_phrase(text, min_words, max_words)

    def _check_phrase(self, text, min_words, max_words) -> Optional[str]:
        words = text.split()

        if not min_words <= len(words) <= max_words:
            return None

        lowered = [w.lower().strip(",") for w in words]

        if lowered[0] in VAGUE_STARTS - {"that"} and lowered[0] != "its":
            return None
        if lowered[0] in {"not", "been", "to", "become", "also"}:
            return None
        if set(lowered) & DANGLING_PRONOUNS:
            return None
        if lowered[-1] in END_STOP:
            return None
        if text.count("(") != text.count(")"):
            return None
        if not self._tokens(text):
            return None

        return text

    def _split_items(self, phrase: str) -> List[str]:
        parts = [
            p.strip()
            for p in re.split(r",\s*(?:and\s+)?|\s+and\s+", phrase)
            if p.strip()
        ]

        if len(parts) < 2:
            return [phrase]
        if any(len(p.split()) > 5 for p in parts):
            return [phrase]
        if any(p.split()[0].lower() in {"a", "an"} for p in parts[1:]):
            return [phrase]
        if len({self._key(p) for p in parts}) != len(parts):
            return [phrase]

        return parts

    def _join_items(self, items: List[str]) -> str:
        if len(items) == 1:
            return items[0]
        return ", ".join(items[:-1]) + " and " + items[-1]

    def _stem_subject(self, subject: str, doc: _Doc) -> str:
        first, _, rest = subject.partition(" ")
        lowered = first.lower()

        should_lower = lowered in DETERMINERS or (
            first[:1].isupper()
            and not first.isupper()
            and lowered in doc.lower_vocab
        )

        if should_lower:
            return lowered + (f" {rest}" if rest else "")
        return subject

    # ============================================================
    # ENTITY POOL (source of distractors)
    # ============================================================

    def _build_entities(self, facts: List[_Fact]) -> List[_Entity]:
        entities: List[_Entity] = []
        seen: Set[tuple] = set()

        def add(text: str, role: str, group: str, index: int, max_words=6):
            text = text.strip()
            key = self._key(text)
            if not key or len(text.split()) > max_words:
                return
            if (role, key) in seen:
                return
            seen.add((role, key))
            entities.append(_Entity(text, role, group, index))

        for fact in facts:
            if fact.kind != "reason":
                add(fact.subject, "subject", "subject", fact.index, 5)

            if fact.kind == "relation":
                if len(fact.items) == 1:
                    add(fact.answer, "object", fact.group, fact.index)
                else:
                    for item in fact.items:
                        add(item, "item", fact.group, fact.index)
            elif fact.kind == "location":
                add(fact.extra["place"], "location", "location", fact.index, 8)
            elif fact.kind == "definition":
                add(fact.answer, "definition", "definition", fact.index, 30)
            elif fact.kind == "purpose":
                add(fact.answer, "purpose", fact.group, fact.index, 16)
            elif fact.kind == "reason":
                add(fact.answer, "reason", "reason", fact.index, 22)

        return entities

    def _foreign_ok(
        self,
        entity: _Entity,
        fact: _Fact,
        doc: _Doc,
        strict: bool,
    ) -> bool:
        """An entity may be a distractor only if the document does not tie
        it to the question (so it can never also be a correct answer)."""

        key = self._key(entity.text)
        if not key or entity.index == fact.index:
            return False

        padded = f" {key} "
        if padded in doc.keys[fact.index]:
            return False

        if strict:
            subject_key = f" {self._key(fact.subject)} "
            for sentence_key in doc.keys:
                if subject_key in sentence_key and padded in sentence_key:
                    return False

        return True

    def _pick_distractors(
        self,
        fact: _Fact,
        correct: str,
        roles,
        doc: _Doc,
        strict: bool,
        same_group: bool = False,
        count: int = 3,
    ) -> List[str]:

        correct_len = len(correct.split())
        ranked = []

        for entity in doc.entities:
            if entity.role not in roles:
                continue
            if same_group and entity.group != fact.group:
                continue
            if not self._foreign_ok(entity, fact, doc, strict):
                continue
            if self._overlaps(entity.text, correct):
                continue
            if self._similarity(entity.text, correct) >= 0.5:
                continue

            length = len(entity.text.split())
            if abs(length - correct_len) > max(3, 0.7 * correct_len):
                continue

            ranked.append((
                roles.index(entity.role),
                0 if entity.group == fact.group else 1,
                abs(length - correct_len),
                entity.text,
            ))

        ranked.sort(key=lambda row: row[:3])

        chosen: List[str] = []
        for *_, text in ranked:
            if any(
                self._overlaps(text, other)
                or self._similarity(text, other) >= 0.5
                for other in chosen
            ):
                continue
            chosen.append(text)
            if len(chosen) == count:
                break

        return chosen

    def _recombine(self, fact: _Fact, doc: _Doc) -> List[str]:
        """Near-miss lists: swap items of the correct list for entities that
        the document never ties to this subject."""

        items = fact.items
        correct_keys = {self._key(i) for i in items}

        foreign: List[str] = []
        for entity in doc.entities:
            if entity.role not in ("item", "object", "subject"):
                continue
            if len(entity.text.split()) > 4:
                continue
            if self._key(entity.text) in correct_keys:
                continue
            if not self._foreign_ok(entity, fact, doc, strict=True):
                continue
            foreign.append(entity.text)

        foreign = list(dict.fromkeys(foreign))
        needed = 4 if len(items) >= 2 else 3
        if len(foreign) < needed:
            return []

        last = len(items) - 1
        swaps = [{0: foreign[0]}, {last: foreign[1]}]

        if len(items) >= 3:
            swaps.append({0: foreign[2], 1: foreign[3]})
        else:
            swaps.append({0: foreign[2], 1: foreign[3]})

        results = []
        for swap in swaps:
            variant = list(items)
            for position, replacement in swap.items():
                variant[position] = replacement
            results.append(self._join_items(variant))

        return results

    # ============================================================
    # CANDIDATE CONSTRUCTION
    # ============================================================

    def _build_candidate(self, fact: _Fact, doc: _Doc) -> Optional[_Candidate]:
        builder = {
            "definition": self._definition_candidate,
            "location": self._location_candidate,
            "purpose": self._purpose_candidate,
            "reason": self._reason_candidate,
            "relation": self._relation_candidate,
        }[fact.kind]

        return builder(fact, doc)

    def _definition_candidate(self, fact, doc):
        distractors = self._pick_distractors(
            fact, fact.answer, ("definition",), doc, strict=False,
        )
        if len(distractors) == 3:
            return self._make_candidate(
                fact, fact.stem, fact.answer, distractors, quality=10,
            )

        # Not enough comparable definitions: ask for the term instead.
        if len(fact.subject.split()) > 5:
            return None
        if self._tokens(fact.subject) & self._tokens(fact.answer):
            return None

        distractors = self._pick_distractors(
            fact, fact.subject, ("subject", "object", "item"), doc,
            strict=False,
        )
        if len(distractors) < 3:
            return None

        return self._make_candidate(
            fact, fact.extra["term_stem"], fact.subject, distractors,
            quality=9,
        )

    def _location_candidate(self, fact, doc):
        place = fact.extra["place"]
        pool = self._pick_distractors(
            fact, place, ("location", "subject", "object", "item"), doc,
            strict=True,
        )
        if len(pool) < 3:
            return None

        distractors = [f"{fact.prep} {text}" for text in pool]
        return self._make_candidate(
            fact, fact.stem, fact.answer, distractors, quality=9,
        )

    def _purpose_candidate(self, fact, doc):
        distractors = self._pick_distractors(
            fact, fact.answer, ("purpose",), doc, strict=False,
            same_group=True,
        )
        if len(distractors) < 3:
            return None

        return self._make_candidate(
            fact, fact.stem, fact.answer, distractors, quality=8,
        )

    def _reason_candidate(self, fact, doc):
        distractors = self._pick_distractors(
            fact, fact.answer, ("reason",), doc, strict=False,
        )
        if len(distractors) < 3:
            return None

        return self._make_candidate(
            fact, fact.stem, fact.answer, distractors, quality=7,
        )

    def _relation_candidate(self, fact, doc):
        if len(fact.items) >= 2:
            distractors = self._recombine(fact, doc)
        else:
            distractors = self._pick_distractors(
                fact, fact.answer, ("object", "item", "subject"), doc,
                strict=True,
            )

        if len(distractors) < 3:
            return None

        quality = 9 if fact.group in ("output", "input") else 8
        return self._make_candidate(
            fact, fact.stem, fact.answer, distractors, quality=quality,
        )

    def _make_candidate(self, fact, stem, correct, distractors, quality):
        correct = self._format_option(correct)
        distractors = [self._format_option(d) for d in distractors]

        is_list = fact.kind == "relation" and len(fact.items) >= 2
        parts = (
            [self._format_option(i) for i in fact.items] if is_list
            else [correct]
        )

        sentence = fact.sentence.strip()
        if sentence[-1] not in ".!?":
            sentence += "."

        explanation = (
            f'The material states: "{sentence}" Therefore, the correct '
            f'answer is "{correct}". The other options are not what the '
            f"material says in answer to this question."
        )

        return _Candidate(
            stem=re.sub(r"\s+", " ", stem).strip(),
            correct=correct,
            distractors=distractors,
            explanation=explanation,
            kind=fact.kind,
            index=fact.index,
            subject=fact.subject,
            quality=quality,
            answer_parts=parts,
            is_list=is_list,
        )

    def _format_option(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip().rstrip(".;,:")
        return text[:1].upper() + text[1:]

    # ============================================================
    # VALIDATION
    # ============================================================

    def _validate(self, candidate: _Candidate) -> bool:
        stem = candidate.stem

        if len(stem.split()) < 6 or not stem.endswith("?"):
            return False
        if stem.count('"') % 2:
            return False
        if self._normalize(stem).startswith(BAD_QUESTION_PATTERNS):
            return False

        options = [candidate.correct] + candidate.distractors
        if len(options) != 4:
            return False

        keys = [self._key(option) for option in options]
        if "" in keys or len(set(keys)) != 4:
            return False

        if not all(self._is_complete_option(option) for option in options):
            return False

        limit = 0.85 if candidate.is_list else 0.6
        for i in range(4):
            for j in range(i + 1, 4):
                if self._similarity(options[i], options[j]) >= limit:
                    return False
                if not candidate.is_list and self._overlaps(
                    options[i], options[j]
                ):
                    return False

        # The stem must not give the answer away.
        stem_tokens = self._tokens(stem)
        for part in candidate.answer_parts:
            part_tokens = self._tokens(part)
            if part_tokens and part_tokens <= stem_tokens:
                return False

        # Balanced option length.
        distractor_lengths = [len(d.split()) for d in candidate.distractors]
        average = sum(distractor_lengths) / len(distractor_lengths)
        if len(candidate.correct.split()) > 1.6 * average + 2:
            return False

        return True

    def _is_complete_option(self, option: str) -> bool:
        words = option.split()

        if not 1 <= len(words) <= 40:
            return False
        if option[0] in ",;:-":
            return False
        if option.count("(") != option.count(")"):
            return False
        if words[0].lower() in BAD_OPTION_STARTS:
            return False
        if words[-1].lower() in END_STOP:
            return False
        if any(bad in option.lower() for bad in BAD_OPTION_TEXT):
            return False

        return True

    # ============================================================
    # SELECTION
    # ============================================================

    def _select(
        self,
        candidates: List[_Candidate],
        target: int,
        sentence_count: int,
    ) -> List[_Candidate]:

        chosen: List[_Candidate] = []
        remaining = list(candidates)
        spread = max(sentence_count / max(target, 1), 1.0)

        def score(candidate: _Candidate) -> float:
            value = float(candidate.quality)
            value -= 2.0 * sum(1 for c in chosen if c.kind == candidate.kind)
            value -= 3.0 * sum(1 for c in chosen if c.index == candidate.index)
            if chosen:
                nearest = min(abs(c.index - candidate.index) for c in chosen)
                value += 2.0 * min(nearest, spread) / spread
            return value

        while remaining and len(chosen) < target:
            best = max(remaining, key=score)
            chosen.append(best)
            remaining = [
                c for c in remaining
                if c is not best and not self._is_duplicate(c, best)
            ]

        chosen.sort(key=lambda c: c.index)
        return chosen

    def _is_duplicate(self, first: _Candidate, second: _Candidate) -> bool:
        if self._similarity(first.stem, second.stem) >= 0.7:
            return True

        if self._similarity(first.correct, second.correct) >= 0.6:
            if first.index == second.index:
                return True
            if self._key(first.subject) == self._key(second.subject):
                return True

        return False

    # ============================================================
    # OUTPUT
    # ============================================================

    def _finalize(self, candidate: _Candidate) -> Dict[str, Any]:
        options = [candidate.correct] + candidate.distractors
        self._rng.shuffle(options)

        return {
            "question": candidate.stem,
            "options": options,
            "correct_answer": candidate.correct,
            "explanation": candidate.explanation,
        }

    # ============================================================
    # TEXT UTILITIES
    # ============================================================

    def _normalize(self, text: str) -> str:
        text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _light_stem(token: str) -> str:
        if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
            return token[:-1]
        return token

    def _key(self, text: str) -> str:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        return " ".join(
            self._light_stem(t) for t in tokens if t not in ARTICLES
        )

    def _tokens(self, text: str) -> Set[str]:
        return {
            self._light_stem(t)
            for t in re.findall(r"[a-z0-9]+", text.lower())
            if len(t) > 2 and t not in MEANING_STOP
        }

    def _similarity(self, first: str, second: str) -> float:
        a, b = self._tokens(first), self._tokens(second)
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def _overlaps(self, first: str, second: str) -> bool:
        a, b = self._tokens(first), self._tokens(second)
        if not a or not b:
            return False
        return a <= b or b <= a