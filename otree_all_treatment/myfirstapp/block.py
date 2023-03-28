from typing import List


class Block:
    """Describes a single block consisting of multiple choices
    """

    def __init__(self,
                 interest_rates: List[float],
                 initial_payout_delay: int,
                 initial_to_last_payout_delay: int,
                 number_of_intermediate_choices: int,
                 show_least_initial_value_first: bool = False):
        """Create a new block consisting of multiple choices. All delays are treated as WEEKS.

        :param interest_rates: List with interest rate values to use per block
        :param initial_payout_delay: Number of days until initial payout
        :param initial_to_last_payout_delay: Number of days between initial and last payout (delay)
        :param number_of_intermediate_choices: Number of intermediate choices (apart from edge choices)
        :param show_least_initial_value_first: Set to `True` in order to show the least amount of initial
        payout money as the first option
        """
        if type(interest_rates) is not list:
            raise ValueError("interest_rates must be a list, e.g. [1.05, 1.03]")
        if (type(initial_payout_delay) is not int
                or type(initial_payout_delay) is not int
                or type(number_of_intermediate_choices) is not int):
            raise ValueError("parameters initial_payout_delay, initial_to_last_payout_delay, "
                             "and number_of_intermediate_choices must be integers")
        if number_of_intermediate_choices < 0:
            raise ValueError("number of intermediate choices must be >= 0")

        self.interest_rates = interest_rates
        self.initial_payout_delay = initial_payout_delay
        self.initial_to_last_payout_delay = initial_to_last_payout_delay
        self.number_of_intermediate_choices = number_of_intermediate_choices
        self.show_least_initial_value_first = show_least_initial_value_first

    def text_delay_start(self) -> str:
        """Returns a human readable text describing the start of the block (e.g. in 2 days) from today.

        :return: Human readable start of block from today
        """
        return self._days_to_text(self.initial_payout_delay)

    def text_total_end(self) -> str:
        """Returns a human readable text describing the end of the block (e.g. in 6 weeks) from today.

        :return: Human readable end of block from today
        """
        return self._days_to_text(self.initial_payout_delay + self.initial_to_last_payout_delay)

    def questions(self) -> List['Question']:
        """Get the list of Questions described by this block

        :return: List of Questions
        """
        from .question import Question
        return [Question(self, i) for i in range(len(self.interest_rates))]

    @staticmethod
    def _days_to_text(value: int) -> str:
        """Interprets the given value as number of days in the future and returns a human readable presentation

        :param value: Number of days in the future
        :return: Human readable presentation
        """
        if value == 0:
            return "today"
        if value % 7 == 0:
            if value == 7:
                return "一周之后"
            return "{0:.0f} weeks later".format(value / 7)
        if value == 1:
            return "一天之后"
        return "{0:.0f} 天之后".format(value)
