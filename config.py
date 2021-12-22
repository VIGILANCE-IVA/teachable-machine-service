from collections import OrderedDict
from os.path import abspath


class Config:
  def __init__(self):
    self.__dict__ = OrderedDict([
      ('model', './data/model.h5'),
      ('labels', './data/labels.txt'),
    ])


config = Config()
