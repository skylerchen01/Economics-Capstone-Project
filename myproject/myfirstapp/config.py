"""
This file includes all available configuration options for the otime app.

Modify this file to set all your preferences - also modify `templates/otime/Results.html` to your liking
which will be displayed after all questions of all blocks have been answered.

It's not recommended to edit any of the other files.

Be sure to also check the README.md file!
"""

from .block import Block

#: The total budget available for each choice
TOTAL_BUDGET = 5000

#: Set to True if you want blocks to be randomized in order
RANDOMIZE_BLOCKS = False

#: Set to True if the choices per question in a block should be visualized as a slider
#: as opposed to single radio buttons
VISUALIZE_CHOICES_AS_SLIDER = False

#: The configuration for all blocks to be displayed to the user
#: Note:
#: - The given delays are treated as WEEKS where an initial delay of 0 means today.
#: - The order of interest_rates given is the order in which they will be display, i.e.
#:      to change the order of display just change the order of values here
BLOCKS = [
    Block(
        interest_rates=[1.05, 1.11, 1.18, 1.25, 1.43, 1.82],
        initial_payout_delay=0,
        initial_to_last_payout_delay=35,
        number_of_intermediate_choices=4
    ),
    Block(
        interest_rates=[1.00, 1.05, 1.18, 1.33, 1.67, 2.22],
        initial_payout_delay=0,
        initial_to_last_payout_delay=63,
        number_of_intermediate_choices=4
    ),
Block(
        interest_rates=[1.05, 1.11, 1.18, 1.25, 1.43, 1.82],
        initial_payout_delay=35,
        initial_to_last_payout_delay=35,
        number_of_intermediate_choices=4
    ),
Block(
        interest_rates=[1.00, 1.05, 1.18, 1.33, 1.67, 2.22],
        initial_payout_delay=35,
        initial_to_last_payout_delay=63,
        number_of_intermediate_choices=4
    )
]
