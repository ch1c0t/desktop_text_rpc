"""Text matching logic for OCR results."""


def find_matches(lines, target, case_sensitive, min_confidence):
    """Return OCR lines containing target and meeting confidence threshold."""
    normalize = (lambda value: value) if case_sensitive else str.casefold
    needle = normalize(target)
    return [line for line in lines
            if line["confidence"] >= min_confidence
            and needle in normalize(line["text"])]
