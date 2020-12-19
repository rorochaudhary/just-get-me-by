def get_target_percentage(target_letter: str, grade_scheme: list) -> float:
    """Returns the percentage required to achieve the target letter grade."""
    for grade in grade_scheme:
        if grade['name'].lower() == target_letter.lower():
            return grade['value'] * 100
