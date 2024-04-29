import random
from math import log
from math import sqrt
from typing import Callable

from termcolor import colored


def table_print(
    array: list[float],
    header: str = "",
    select_top_value: bool = False,
    all_headers: bool = False,
) -> None:
    header_format = "{:^10}"
    value_format = "{:^10.0f}"

    top = max(array)

    to_print = [colored(header_format.format(header), "cyan")]
    for value in array:
        formatted = value_format.format(value)
        if select_top_value and top == value:
            formatted = colored(formatted, "green")
        if all_headers:
            formatted = colored(formatted, "cyan")
        to_print.append(formatted)

    print(*to_print, sep="|")


class Score:
    """Base class for scores"""

    answers = [2, 3, 4]
    SCORE_MULTI = 100

    PERCENTAGES = [1, 10, 20, 25, 30, 33.33333, 40, 50, 60, 65, 70, 75, 80, 90, 99]
    # misnomer, not necessarily confidences, just percentages normalized
    CONFIDENCES = [percent / 100 for percent in PERCENTAGES]
    split = "--------------------------------------"
    strong_split = "++++++++++++++++++++++++++++++++++++++"

    def __init__(self, eval_function: Callable[[float | int, int, bool], float]):
        self.scores: dict = {}
        self.calculate_reward_for_confidence = eval_function
        self.rule = eval_function.__name__

    def score_all(self, q: int) -> None:
        """Fill the dict SCORES"""
        for confidence in Score.CONFIDENCES:
            self.scores[confidence] = self.calculate_reward_for_confidence(
                confidence, q, False
            )

    def score_with_confidence(self, x: float, q: int) -> list:
        """Average score for X confidence, q answers and chances from CONFIDENCES(misnomer)"""
        other_answers_chance = 1 - x
        other_percent = other_answers_chance / (q - 1)
        # True here is for inverse in spherical rule only
        other_score = self.calculate_reward_for_confidence(other_percent, q, True)
        avg = []

        for confidence in Score.CONFIDENCES:
            score_times_percent_right = self.scores[x] * confidence
            score_times_percent_wrong = other_score * (1 - confidence)
            avg.append(score_times_percent_right + score_times_percent_wrong)

        return avg

    def result(self) -> None:
        print(Score.strong_split)
        print(colored(f"{self.rule}", "red"))
        print()
        for q in Score.answers:
            self.score_all(q)
            print(Score.split)
            print(colored(f"Answers quantity: {q}", "red"))
            print()
            table_print(Score.PERCENTAGES, "%", False, True)
            table_print(list(self.scores.values()), "score")
            print(Score.split, Score.split, Score.split, sep="\n")
            table_print(Score.PERCENTAGES, "succ\\cred", False, True)
            matrix = []
            for confidence in Score.CONFIDENCES:
                matrix.append(self.score_with_confidence(confidence, q))
            # transpose matrix
            transposed = [
                [matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]))
            ]
            for i, array in enumerate(transposed):
                table_print(array, str(Score.PERCENTAGES[i]), True, False)
        print(Score.strong_split, Score.strong_split, sep="\n")


def basic_log_q_score(confidence: float, q: int, noop: bool = True) -> float:
    return log(confidence) / log(q)


def adjusted_log_score(confidence: float, q: int, noop: bool = True) -> float:
    return (basic_log_q_score(confidence, q) + 1) * Score.SCORE_MULTI


def brier_score(confidence: float, q: int, noop: bool = True) -> float:
    return -((confidence - 1) ** 2) * Score.SCORE_MULTI


def spherical_denominator_sq(confidence: float, q: int, inverse: bool) -> float:
    if not inverse:
        total_confidence_in_other = 1 - confidence
        number_of_other_answers = q - 1
        confidence_in_any_other = total_confidence_in_other / number_of_other_answers
        return (confidence**2) + (
            number_of_other_answers * (confidence_in_any_other**2)
        )
    else:
        number_of_similar_answers = q - 1
        confidence_in_odd_one = 1 - (number_of_similar_answers * confidence)
        return (confidence_in_odd_one**2) + (
            number_of_similar_answers * (confidence**2)
        )


def spherical_zero_confidence(q: int) -> float:
    confidence = 1 / q
    return confidence / sqrt(q * (confidence**2))


# Non-inverse (7:1:1:1) or (1:7:7:7) and eval 1st. We're evaluating the odd toplevel.one
# Inverse: (1:1:1:7) or (7:1:7:7) and eval 1st
def spherical_score(confidence: float, q: int, inverse: bool = False) -> float:
    denominator_sq = spherical_denominator_sq(confidence, q, inverse)

    # Zero-confidence to 0 normalization
    actual_result = confidence / sqrt(denominator_sq)
    multi_for_normalization = 1 / (1 - spherical_zero_confidence(q))
    result_below_0 = actual_result - 1
    result_below_0_normalized = result_below_0 * multi_for_normalization
    result_normalized = result_below_0_normalized + 1

    return result_normalized * Score.SCORE_MULTI


Score(adjusted_log_score).result()
Score(spherical_score).result()


# Properness breaks at q>2
# Score(brier_score).result()


def randy(q: int, min: float, max: float) -> None:
    n = 100000
    log_s: float = 0
    spherical_s: float = 0
    for n in range(0, n):
        confidence = random.uniform(min, max)
        log_s += adjusted_log_score(confidence, q, False)
        spherical_s += spherical_score(confidence, q, False)

    log_s = int(log_s / n)
    spherical_s = int(spherical_s / n)
    print(
        f"{q} answers and credence {min}-{max}:   log score= {log_s},  |   sphere= {spherical_s},  |  log/sph= {log_s / spherical_s}"
    )


def randies() -> None:
    randy(2, 0, 1)
    randy(2, 0, 0.5)
    randy(2, 0.5, 1)
    print()
    randy(3, 0, 1)
    randy(3, 0, 0.333333)
    randy(3, 0.333333, 1)
    print()
    randy(4, 0, 1)
    randy(4, 0, 0.25)
    randy(4, 0.25, 1)
