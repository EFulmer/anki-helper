"""Definition of the "Vocab Form" note type.

One note = one inflected form of a word. It produces:
  Card 1 "Meaning → Target"  (always)
  Card 2 "Target → Meaning"  (only when the OneWay field is empty)

Fill OneWay (with anything, e.g. "y") for forms whose spelling is ambiguous,
like сме́рти, so only the Meaning → Target direction is quizzed.
"""

from __future__ import annotations

from .ankiconnect import AnkiConnect

MODEL_NAME = "Vocab Form"

FIELDS = [
    "Target",    # the form itself, with stress marks: (ты) слы́шишь
    "Meaning",   # English meaning in the form's number/person: you hear
    "Grammar",   # grammar label: 2nd sing., impf.
    "Lemma",     # dictionary form: слы́шать
    "POS",       # part of speech: verb / noun / adj / ...
    "Language",  # ISO code: ru / uk / de / pt
    "OneWay",    # non-empty => suppress the Target → Meaning card
]

_PROMPT = """<div class="meaning">{{Meaning}}</div>
{{#Grammar}}<div class="grammar">({{Grammar}})</div>{{/Grammar}}"""

_TARGET = '<div class="target" lang="{{Language}}">{{Target}}</div>'

_LEMMA = '{{#Lemma}}<div class="lemma" lang="{{Language}}">{{Lemma}}</div>{{/Lemma}}'

TEMPLATES = [
    {
        "Name": "Meaning → Target",
        "Front": _PROMPT,
        "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n" + _TARGET + "\n" + _LEMMA,
    },
    {
        "Name": "Target → Meaning",
        "Front": "{{^OneWay}}" + _TARGET + "{{/OneWay}}",
        "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n" + _PROMPT + "\n" + _LEMMA,
    },
]

CSS = """\
.card {
  font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
  font-size: 30px;
  text-align: center;
  color: #1a1a1a;
  background-color: #ffffff;
}
.nightMode.card, .night_mode .card { color: #e8e8e8; background-color: #2b2b2b; }

.target  { font-size: 38px; }
.meaning { font-size: 30px; }
.grammar { font-size: 20px; color: #777; margin-top: 6px; }
.lemma   { font-size: 16px; color: #999; margin-top: 18px; }
.lemma::before { content: "dictionary form: "; }

.nightMode .grammar, .night_mode .grammar { color: #aaa; }
.nightMode .lemma,   .night_mode .lemma   { color: #888; }
"""


def ensure_note_type(ac: AnkiConnect) -> str:
    """Create the note type, or update its templates/styling if it already exists."""
    if MODEL_NAME not in ac.invoke("modelNames"):
        ac.invoke(
            "createModel",
            modelName=MODEL_NAME,
            inOrderFields=FIELDS,
            css=CSS,
            isCloze=False,
            cardTemplates=TEMPLATES,
        )
        return "created"

    existing = ac.invoke("modelFieldNames", modelName=MODEL_NAME)
    if existing != FIELDS:
        raise RuntimeError(
            f"Note type {MODEL_NAME!r} exists with fields {existing}, expected {FIELDS}. Not touching it."
        )
    ac.invoke(
        "updateModelTemplates",
        model={"name": MODEL_NAME, "templates": {t["Name"]: {"Front": t["Front"], "Back": t["Back"]} for t in TEMPLATES}},
    )
    ac.invoke("updateModelStyling", model={"name": MODEL_NAME, "css": CSS})
    return "updated"
