from otree.api import *

from typing import Optional, List

import random
import json

from .block import Block
from .config import BLOCKS, RANDOMIZE_BLOCKS, VISUALIZE_CHOICES_AS_SLIDER

from . import ret_functions

author = ""

doc = """
第一个otree app
"""


class B():
    questions = list()

class C(BaseConstants):
    NAME_IN_URL = 'myfirstapp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # PLAYERS_PER_GROUP = 1
    ENDOWMENT = cu(1000)
    page = 'myfirstapp/includes/js_work_page.html'
    page2 = 'myfirstapp/ret_modules/countzeroes.html'
    pay = 100
    bodys = [ret_functions.CountZeroes() for i in range(100)]
    questions= [list() for i in range(100)]

# def creating_session(subsession):
#     import random
#     for player in subsession.get_players():
#         player.flag = random.choice(['A', 'B', 'C'])
#         print('set time_pressure to', player.flag)

    # subsession.vars['task_fun'] = getattr(ret_functions, subsession.config['task'])
    # # If a task generator gets some parameters (like a level of difficulty, or number of rows in a matrix etc.)
    # # these parameters should be set in 'task_params' settings of an app, in a form of dictionary. For instance:
    # # 'task_params': {'difficulty': 5}
    # subsession.vars['task_params'] = subsession.config.get('task_params', {})
    # # for each player we call a function (defined in Player's model) called get_or_create_task
    # # this is done so that when a RET page is shown to a player for the first time they would already have a task
    # # to work on
    # for p in subsession.get_players():
    #     p.get_or_create_task()


class Subsession(BaseSubsession):

    block_order = models.StringField(initial=" ")

    def des(self) -> None:
        """Initializes the session and creates the order in which the Blocks should be run through
        """
        block_order = [i for i in range(len(BLOCKS))]
        if RANDOMIZE_BLOCKS:
            random.shuffle(block_order)

        self.block_order = json.dumps(block_order)

    def get_block_order(self) -> List[int]:
        """Get the order in which blocks should be run through

        The elements of the list represent the 0-based index in the `config.BLOCKS` list.

        :return: List of Block indexes
        """

        self.des()

        return json.loads(self.block_order)


class Group(BaseGroup):
    total_contribution = models.CurrencyField()


class Player(BasePlayer):
    title1 = models.StringField(initial="0")
    title2 = models.StringField(initial="0")
    flag = models.StringField()
    b1 = models.StringField(initial="0")
    b2 = models.StringField(initial="0")

    major = models.StringField(
        label="What's your major?",
        blank=True,

    )
    nationality = models.StringField(
        label="What's your nationality?",
        blank=True,

    )
    school = models.StringField(
        blank=True,
        label="What's your high school location?",
    )
    age = models.IntegerField(
        blank=True,
        label="What's your age?",
    )
    born = models.StringField(
        blank=True,
        label="What's your birthplace?",
    )
    gender = models.StringField(
        blank=True,
        choices=[[1, 'Male'], [2, 'Female']],
        label='Please indicate your gender:',
        widget=widgets.RadioSelect,
    )

    Recipes = models.IntegerField(
        choices=[
            [1, 'A.Fried Pork Slices'],
            [2, 'B.Braised Pork Ribs'],
            [3, 'C.Sauteed Lamb with Scallion'],
            [4, 'D.Braised Pork with Preserved Vegetable']
        ],
        label='What dish does the audio describe?',
        widget=widgets.RadioSelect,
        initial=0,
    )

    part5 = models.IntegerField(initial=0)
    part5_wrong = models.IntegerField(initial=0)

    part1 = models.IntegerField(initial=0)

    part2 = models.IntegerField(initial=0)

    volume = models.IntegerField(initial=0)
    volume2 = models.IntegerField(initial=0)
    today = models.FloatField(initial=0)
    future1 = models.FloatField(initial=0)
    future2 = models.FloatField(initial=0)



    #     otime
    current_step = models.IntegerField(initial=0)

    block_answers = models.StringField(initial="")

    def goto_next_step(self) -> None:
        """Advances the player to the next step
        """
        self.current_step = self.current_step + 1

    def get_current_step(self) -> int:
        """The player's current step

        :return: Current step
        """
        return self.current_step

    def get_current_block_index(self) -> int:

        if self.current_step < len(BLOCKS):
            block_order = self.subsession.get_block_order()
            return block_order[self.current_step]
        else:
            return -1

    def get_current_block(self) -> Optional[Block]:
        """Get the current Block to display

        This function returns `None` if there is nothing left to display.

        :return: Block to display or `None`
        """
        block_index = self.get_current_block_index()
        if 0 <= block_index < len(BLOCKS):
            return BLOCKS[block_index]
        else:
            return None

    #     0
    tasks_dump = models.LongStringField(doc='to store all tasks with answers, diff level and feedback')

    body = ret_functions.CountZeroes()


# 统计金额
def set_payoffs(player):
    player.payoff = player.payoff + C.ENDOWMENT
    if player.Recipes == 2:
        player.payoff = player.payoff + 500
        player.part1 = 500
        player.today += 5
    player.today += 10
    player.payoff = player.payoff + player.part5
    player.payoff = player.payoff + int(player.b1) + int(player.b2)
    player.payoff = player.payoff-player.volume
    player.future2 += int(player.b2)/100
    if player.title1=="today":
        player.today += int(player.b1)/100
    else:
        player.future1 += int(player.b1)/100
    player.today-=player.volume/100
    player.today += player.part5/100

    player.today=round(player.today,2)
    player.future1=round(player.future1,2)
    player.future2 = round(player.future2, 2)

    print(player.payoff)


# PAGES
class survey(Page):
    form_model = "player"
    form_fields = ['gender',"age", 'major', "nationality",'born', 'school']


class ResultsWaitPage(WaitPage):
    pass


class notice(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.flag = random.choice(['A', 'B', 'C'])
        print(player.flag)
        return True



class adapt(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.flag == "C"


class adapt2(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.flag == "C"


class adapt3(Page):
    form_model = "player"
    form_fields = ['Recipes']

    @staticmethod
    def is_displayed(player: Player):
        return player.flag == "C"


class adapt4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.flag == "C"



# otime

class BlockPage1(Page):
    pass


class BlockPage2(Page):





    @staticmethod
    def vars_for_template(player):
        import random
        questions = random.choice(C.questions[player.id_in_group-1])
        print(questions)
        title = questions[0]
        title = title.split("-")
        player.title1 = title[0]
        player.title2 = title[1]
        question = random.choice(questions[1:])
        question = question.split("-")
        player.b1 = question[0]
        player.b2 = question[1]
        print(player.title1, player.title2, player.b1, player.b2)


class BlockPage(Page):

    @staticmethod
    def js_vars(player):



        return dict(
            flag=player.flag,
        )

    """Displays a `Block` to the player

    This page will automatically retrieve the current `Block` to be displayed
    to the player from the player's current block.
    """


    form_model = 'player'
    form_fields = ['block_answers']

    # 接收otime
    @staticmethod
    def live_method(player, data):
        question = json.loads(data)
        print("question",question)
        # if len(C.questions[player.id_in_group-1]) and player.isFirst==1:
        #     player.isFirst=0
        #     C.questions[player.id_in_group - 1]=[]
        C.questions[player.id_in_group-1].append(question)
        print(player.id_in_group-1,"--",player.id_in_group-1)
        print("all question",C.questions[player.id_in_group-1])
        print()
        player.get_current_step()
        return {player.id_in_group: player.body.get_body()}

    @staticmethod
    def vars_for_template(player):

        step = player.get_current_step() + 1

        # player.current_step=player.current_step + 1
        block_index = player.get_current_block_index() + 1
        current_block = player.get_current_block()
        num_blocks = len(BLOCKS)
        player.goto_next_step()
        return {
            'step': step,
            'block_index': block_index,
            'num_blocks': num_blocks,
            'progress': round(step * 100 / num_blocks),
            'curr_block': current_block,
            'use_slider': VISUALIZE_CHOICES_AS_SLIDER,
            'num_choices': current_block.number_of_intermediate_choices + 2
        }
class workpage1(Page):
    pass

class WorkPage(Page):
    timeout_seconds = 600

    @staticmethod
    def js_vars(player):
        return dict(
            volume=0.99*(player.volume/1000)*(player.volume/1000)- 1.98 * (player.volume/1000) + 1,
        )




    @staticmethod
    def vars_for_template(player):
        player.body = C.bodys[player.id_in_group - 1]
        print(player.body.get_correct_answer())
        return player.body.get_context_for_body()
    # 接收答案
    @staticmethod
    def live_method(player, data):
        player.body = C.bodys[player.id_in_group - 1]
        print(player.body.get_correct_answer())
        if int(data) == int(player.body.get_correct_answer()):
            print(data,player.body.get_correct_answer(),data == player.body.get_correct_answer())
            player.part5 = player.part5 + C.pay
        else:
            player.part5_wrong+=1
        return {player.id_in_group: player.body.get_body()}


class workpage2(Page):
    pass


class audio1(Page):
    pass

class intro1(Page):
    pass


class intro2(Page):
    pass


class audio(Page):
    # 接收答案
    @staticmethod
    def live_method(player, data):
        player.volume = data
        print(data)
        return {player.id_in_group: data}

    pass


class audio2(Page):

    @staticmethod
    def js_vars(player):

        return dict(
            volume=(1 - (player.volume / 1000)),
        )

    pass


class ResultsAB_f(Page):
    @staticmethod
    def vars_for_template(player):
        set_payoffs(player)
        return dict(
            test="123",
        )
    def is_displayed(player: Player):
        return (player.flag == "A" or player.flag == "B") and player.title1!='today'

class ResultsC_f(Page):

    @staticmethod
    def vars_for_template(player):
        set_payoffs(player)
        return dict(
            test="123",
        )
    def is_displayed(player: Player):
        return player.flag == "C" and player.title1!='today'

class ResultsAB_t(Page):
    @staticmethod
    def vars_for_template(player):
        set_payoffs(player)
        return dict(
            test="123",
        )
    def is_displayed(player: Player):
        return (player.flag == "A" or player.flag == "B") and player.title1=='today'

class ResultsC_t(Page):

    @staticmethod
    def vars_for_template(player):
        set_payoffs(player)
        return dict(
            test="123",
        )
    def is_displayed(player: Player):
        return player.flag == "C" and player.title1=='today'


# notice, adapt, adapt2,
#
page_sequence =  [ notice,intro1, intro2, adapt, adapt2, adapt3, BlockPage1] +[BlockPage] * len(BLOCKS) + [BlockPage2, audio1,audio,
                                                                                                  audio2,

                                                                                                   workpage1, WorkPage,
                                                                                                   workpage2,
                                                                                                   survey,ResultsWaitPage,ResultsAB_t,ResultsAB_f,ResultsC_f,ResultsC_t]
