"""
학생들의 시험 성적을 매기는 코드.
1. 시험은 여러 과목으로 구성되어 있음
2. 과목별로 점수가 있음
"""


class Exam:
    """Simple class using basic property and setter."""

    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError("Grade must be between 0 and 100")

    # We need @property and setter for every grade.
    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value: int):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value: int):
        self._check_grade(value)
        self._math_grade = value
