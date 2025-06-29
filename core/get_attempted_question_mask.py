import re
from itertools import chain

# Constants
PHRASES_TO_CLEAN = [
    "do not write in the shaded area or below",
    "do not write in the shaded area or beyond",
]

def generate_phrase_patterns(phrases, min_words=4):
    """
    Generate all sub-phrases (n-grams) of length >= min_words from given phrases.
    """
    all_phrases = []
    for phrase in phrases:
        words = phrase.lower().split()
        for n in range(min_words, len(words) + 1):
            all_phrases.extend(' '.join(words[i:i+n]) for i in range(len(words) - n + 1))
    return all_phrases

def build_phrase_pattern(phrases):
    """
    Build a compiled regex pattern from a list of phrases.
    """
    escaped_phrases = [re.escape(p) for p in phrases]
    return re.compile(r'\b(?:' + '|'.join(escaped_phrases) + r')\b', re.IGNORECASE)

def clean_text(text):
    """
    Clean common noise patterns from OCR text.
    """
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove markdown image links
    text = re.sub(r'DO NOT WRITE IN THE SHADED AREA OR (BELOW|BEYOND)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(^|\n)[# ]*\d*[\s#]*\n?', '', text)  # Remove isolated headings or symbols
    return re.sub(r'\n{2,}', '\n', text).strip()

# Build the pattern once
PHRASE_PATTERN = build_phrase_pattern(generate_phrase_patterns(PHRASES_TO_CLEAN))

def get_attempted_question_mask(ocr_result):
    """
    Returns a mask indicating which questions have been attempted based on cleaned OCR text.
    """
    attempted_mask = {}
    for question_number, text in ocr_result.items():
        text = text.lower().strip().replace("sample", "")
        text = PHRASE_PATTERN.sub('', text)
        text = clean_text(text)
        attempted_mask[question_number] = len(text) > 30 and not text.isspace()
    return attempted_mask
