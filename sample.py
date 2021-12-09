import sys, time
import numpy as np
import datetime


class Sample():
    def __init__(self, demo=True):
        self.name = 'CoNiPt'
        self.ID = ''
        self.composition = {'Co' : 0.0, 'Ni': 0.0, 'Pt': 0.0}
        self.demo = demo

    def initialise(self, name='', ID=''):
        self.name = name
        self.ID = ID
        if not self.demo:
            self.composition = {'Co' : 0.2, 'Ni': 0.3, 'Pt': 0.5}
        else:
            self.name = 'dummy'
            self.ID = '001'

