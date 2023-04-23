import re
import yaml
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Входной файл, содержащий путь к файлу и его хэш. '
                                          'Такой файл можно получить из утилит: md5sum, shaXXXsum', required=True)
parser.add_argument('-o', '--output', help='Файл, куда вывести дубликаты файлов', required=True, type=str)

args = parser.parse_args()

ifile = Path(args.input)
ofile = Path(args.output)

assert ifile.exists(), 'Входного файла не существует'


def main():
  LINE_PATTERN = re.compile(r'^([0-9a-z]+)\s+(/.+)$')
  
  with ifile.open('r', encoding='utf-8') as file:
    matches = [m for line in file.readlines() if (m := re.match(LINE_PATTERN, line))]
    
  files = dict()
  
  for match in matches:
    file_hash = match.group(1)
    file_path = match.group(2)
    
    if file_hash not in files:
      files[file_hash] = []
    
    files[file_hash].append(file_path)
  
  yaml_out = []
  for k, v in files.items():
    if len(v) > 1:
      yaml_out.append({
        'hash': k,
        'files': files[k]
      })
    
  with ofile.open('w+', encoding='utf-8') as file:
    yaml.dump(yaml_out, file, encoding='utf-8', allow_unicode=True)
  
  
main()
