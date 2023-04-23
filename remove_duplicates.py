import yaml
from threading import Lock
from pathlib import Path
from argparse import ArgumentParser
from progress import Infinite
from progress.bar import IncrementalBar
from multiprocessing.pool import ThreadPool

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Входной файл, содержащий вывод утилиты find_duplicates', required=True)
parser.add_argument('-t', '--threads', help='Кол-во потоков для удаления', required=False, type=int, default=4)
parser.add_argument('--dry-run', help='Не удалять, а только вывести пути к удаляемым файлам', action='store_true')
parser.add_argument('--stats', help='Отобразить статистику', action='store_true')

args = parser.parse_args()


ifile = Path(args.input)
simulate = args.dry_run
show_stats = args.stats
threads = args.threads

assert ifile.exists(), f'Файла не существует: {ifile}'


class Remover:
  def __init__(self):
    Infinite.hide_cursor = False
    self.total_files = 0
    self.total_size_b = 0
    self.remove_per_thread = 10
    self.progress = IncrementalBar()
    
  @property
  def total_size_mb(self):
    return self.total_size_b // 1024 // 1024
  
  def _remove(self, files: list[Path]): pass
  
  def remove(self, files: list[Path]):
    self.total_files += len(files)
    self.progress = IncrementalBar(max=len(files))
    
    pool = ThreadPool(processes=threads)
    
    files_per_thread = []
    for i in range(0, len(files), self.remove_per_thread):
      f = files[i:i+self.remove_per_thread]
      files_per_thread.append(f)
      self.total_size_b += sum(file.stat().st_size for file in f)
    
    self.progress.start()
    pool.map(self._remove, files_per_thread)
    self.progress.finish()


class RealRemover(Remover):
  def __init__(self):
    super().__init__()
    
  def _remove(self, files: list[Path]):
    for file in files:
      file.unlink()
      self.progress.next()
      self.progress.update()


class FakeRemover(Remover):
  def __init__(self):
    super().__init__()
    self.lock = Lock()
    
  def _remove(self, files: list[Path]):
    with self.lock:
      for file in files:
        print(file)
    

def main():
  with ifile.open('r', encoding='utf-8') as file:
    duplicates = yaml.full_load(file)
  
  if simulate:
    remover = FakeRemover()
  else:
    remover = RealRemover()
  
  for_remove = []
  for duplicate in duplicates:
    files = [Path(x) for x in duplicate['files'][1:]]
    for_remove += files
    
  remover.remove(for_remove)
  
  if show_stats:
    print(f'Statistic')
    print(f'  Total files : {remover.total_files}')
    print(f'  Total size  : {remover.total_size_mb} Mb')


main()
