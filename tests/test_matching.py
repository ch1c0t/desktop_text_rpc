"""Unit tests for matching policy, without initializing PaddleOCR or a display."""

def match_lines(lines, target, case_sensitive=False, min_confidence=0.5):
    normalize = (lambda value: value) if case_sensitive else str.casefold
    needle = normalize(target.strip())
    return [
        line for line in lines
        if line["confidence"] >= min_confidence
        and needle in normalize(line["text"])
    ]


def test_case_insensitive_substring():
    lines = [
        {"text": "Press a key to continue", "confidence": 0.91},
        {"text": "Loading", "confidence": 0.99},
    ]
    assert match_lines(lines, "PRESS A KEY") == [lines[0]]


def test_confidence_threshold():
    lines = [{"text": "Press a key", "confidence": 0.4}]
    assert match_lines(lines, "Press", min_confidence=0.5) == []
