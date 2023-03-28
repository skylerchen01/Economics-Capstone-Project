# this is the module responsible for generation functions for different rets
# if you need new rets you need to define generating functions here and attach them to corresponding tasks

import random
from random import randint
# from django.utils.safestring import mark_safe
# from django.template.loader import render_to_string
from string import digits, ascii_lowercase
import logging

logger = logging.getLogger(__name__)


# function slices a list with n elements in each sublist (if possible)
def slicelist(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


# slices a list into n parts  of an equal size (if possible)
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def get_random_list(max_len):
    low_upper_bound = 50
    high_upper_bound = 99
    return [randint(10, randint(low_upper_bound, high_upper_bound)) for i in range(max_len)]


# Shared properties for the tasks collected under the TaskGenerator Class
class TaskGenerator:
    path_to_render = None
    def __init__(self, **kwargs):
        self.body = self.get_body(**kwargs)
        self.correct_answer = self.get_correct_answer()
        self.html_body = self.get_html_body()


    def get_context_for_body(self):
        return {}

    def get_html_body(self):
        # return mark_safe(render_to_string(self.path_to_render, self.get_context_for_body()))
        pass

    def get_body(self, **kwargs):
        pass

    def get_correct_answer(self):
        pass



class CountZeroes(TaskGenerator):
    path_to_render = 'realefforttask/ret_modules/countzeroes.html'
    name = 'Count 0s in the matrix of digits'
    def get_correct_answer(self):
        return self.data.count(str(self.value_to_count))

    def get_body(self, **kwargs):
        num_rows = kwargs.get('num_rows', 5)
        num_columns = kwargs.get('num_columns', 20)
        selection_set = kwargs.get('selection_set', [0, 1])
        self.value_to_count = kwargs.get('value_to_count', 0)
        nxm = num_rows * num_columns
        self.data = [str(random.choice(selection_set)) for _ in range(nxm)]
        self.mat = chunkify(self.data, num_rows)
        return {'mat': self.mat}

    def get_context_for_body(self):
        return {
            "mat": self.mat,
            "value_to_count": self.value_to_count,
        }




