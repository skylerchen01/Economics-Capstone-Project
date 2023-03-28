from typing import List

from .block import Block


class Question:
    """Represents a single question of a `Block`

    A Question represents a set of different choices where the values
    are linearly calculated taking into account the corresponding p value
    and of course the total available budget.
    """

    def __init__(self, block: Block, index: int):
        """Create a new Question
        """
        self.block = block
        self.index = index
        self.num_choices = block.number_of_intermediate_choices + 2
        self.interest_rate = self.block.interest_rates[self.index]

    def question_number(self) -> int:
        """Get the number of this question in the block

        :return: Question number
        """
        return self.index + 1

    def start_values(self) -> List[float]:
        """Get the list of initial payoff values (at point t)

        The list of values will start with `config.TOTAL_BUDGET / p` and end at `0`.
        All values will be rounded to one decimal.

        :return: List of initial payoffs
        """
        from .config import TOTAL_BUDGET
        start = round(TOTAL_BUDGET / self.interest_rate, 1)
        unrounded = [(self.num_choices - 1 - i) * start / (self.num_choices - 1) for i in range(self.num_choices)]
        return [round(v, 1) for v in unrounded]

    def end_values(self) -> List[float]:
        """Get the list of final payoff values (at point t + k)

        The list of values will start with `0` and end at `config.TOTAL_BUDGET`.
        All values will be rounded to one decimal.

        :return: List of final payoffs
        """
        from .config import TOTAL_BUDGET
        unrounded = [i * TOTAL_BUDGET / (self.num_choices - 1) for i in range(self.num_choices)]
        return [round(v, 1) for v in unrounded]

    def choice_index(self) -> range:
        """Range from 1 to the `num_choices` (including)
        """
        return range(1, self.num_choices + 1)
