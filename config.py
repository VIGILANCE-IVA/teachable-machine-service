import os
from collections import OrderedDict

path = './data'

if not os.path.exists(path): 
  os.makedirs(path)

class Config:
  def __init__(self):
    self.__dict__ = OrderedDict([
      ('model', f'{path}/model.h5'),
      ('labels', f'{path}/labels.txt'),
    ])


config = Config()
