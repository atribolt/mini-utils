#!/usr/bin/python3


import os
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-s', '--source', help='Путь содержащий иерархию, которую нужно удалить', required=True)
parser.add_argument('-r', '--remove', help='Путь, относительно которого будут удаляться файлы', required=True)


args = parser.parse_args()
args.source = os.path.abspath(args.source)
args.remove = os.path.abspath(args.remove)


assert os.path.exists(args.source), f'Путь "{args.source}" не существует'
assert os.path.exists(args.remove), f'Путь "{args.remove}" не сущетсвует'


source_list = []
length = len(args.source) + 1
for root, dirs, files in os.walk(args.source, True):
  root = os.path.join(args.remove, root[length:])
  if files:
    [source_list.append(os.path.join(root, file)) for file in files]


for file in source_list:
  try:
    os.remove(file)
  except Exception as ex:
    print(ex)
