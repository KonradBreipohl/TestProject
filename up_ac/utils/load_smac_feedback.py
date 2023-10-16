import dill
import os
import sys
from unified_planning.io import PDDLReader

reader = PDDLReader()


def get_feedback(config, instance, seed=0):

    path = os.getcwd().rsplit('up-ac', 1)[0]
    path += 'up-ac/up_ac/utils'
    sys.path.append(r"{}".format(path))

    fb = \
        dill.load(open(f'{path}/feedback.pkl', 'rb'))

    feedback = fb(config, instance, seed, reader)

    print(fb)

    return feedback
