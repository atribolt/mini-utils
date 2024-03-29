# Мини программы для решения некоторых рутинных задач

## 1. [Поиск дубликатов файлов](./find_duplicates.py)
  Утилита для поиска файлов с одинаковой хэш суммой. Для использования программы требуется
  входной файл, содержащий хэш сумму и абсолютный путь к файлу.

  Получить файл с хэш суммами в Linux можно утилитами `md5sum` или `shaXXXsum`. Например так:
  ```shell
  # хэши файлов с алгоритмом md5
  md5sum /your/folder/with/files/**/*.jpg > hashed_list.txt

  # или с алгоритмом sha
  sha512sum /your/folder/with/files/**/*.jpg > hashed_list.txt
  ```

  Далее, необходимо скормить полученный файл утилите `find_duplicates`
  ```shell
  python3 find_duplicates.py -i hashed_list.txt -o duplicates.yaml
  ```

  Эта утилита создаст YAML файл, где будут перечислены дублированные файлы и их хэш.
  Пример такого файла:
  ```yaml
  - files:
    - /tmp/program/any/data/102_FUJI/DSCF2038.AVI
    - /tmp/program/any/data/FIUJI/DSCF2038.AVI
    hash: 119d629d865f1ce7feef4a41a61bf2e44aa781de360f2f46c731a3d5c8219b95c1a74cedc23cfed0845875f40b582bb8a588a5862cfb01434cdf517c49498ea9
  - files:
    - /tmp/program/any/data/Camera/SL_MO_VID_20220126_173815.mp4
    - /tmp/program/any/data/SL_MO_VID_20220126_173815.mp4
    hash: 4068cbf6e7189873c43b87800b10a848f58b58c54a2fc1f0ae62214b689bee15dbabc5ee2f8194ef764f5882e09e43a6740c0d842a27f55e434e4841fd340ecf
  - files:
    - /tmp/program/any/data/Camera/VID_20201026_222413.mp4
    - /tmp/program/any/data/VID_20201026_222413.mp4
    hash: f3a01a287cdc3cd513e27c67660e915d1c9e66640c0dfdb9cd3439f608554c3c7595b8a06448531f77fce3f9cdcdb0410509263c89b019317624d4711a87d140
  ```

### 1.1 Аргументы запуска
  Актуальные аргументы запуска можно получить флагом `-h` (иногда забываю обновлять README)
  - `-i` `--input` -- входной файл с хэшами
  - `-o` `--output` -- выходной файл с дубликатами

---
## 2. [Удаление дубликатов файлов](./remove_duplicates.py)
  Утилита предназначена для удаления дубликатов. Для использования программы требуется входной
  файл с дубликатами. Такой файл создает утилита [find_duplicates](./find_duplicates.py). 

  Программу можно запустить без удаления, при этом в консоль будут выведены пути к файлам, 
  которые могут быть удалены:
  ```shell
  python3 remove_duplicates.py -i duplicates.yaml --stats --dry-run
  ```
  Команда выше, также выведет кол-во доступных для удаления файлов, а также их суммарный размер.
  ```
  Statistic
    Total files : 6288
    Total size  : 26179 Mb
  ```

  Для удаления файлов, необходимо убрать аргумент запуска `--dry-run`:
  ```shell
  python3 remove_duplicates.py -i duplicates.yaml --stats
  ```

### 2.1 Аргументы запуска
  Актульные аргументы запуска можно получить флагом `-h`
  - `-i` `--input` -- входной файл с описанием дубликатов
  - `-t` `--threads` -- кол-во потоков для удаления (по умолчанию 4).
                        При этом, на каждый поток выделяется по 10 файлов.
                        Одновременно удаляются 40 файлов по умолчанию. Или `threads * 10`
  - `--stats` -- вывести статистику после удаления (работает и для фейкового удаления)
  - `--dry-run` -- симулировать удаление, просто выводит в консоль пути к удаляемым файлам

---
## 3. [Удаление файлов по структуре каталога](./remove-by-folder.py)
  Эта утилита позволяет удалить файлы одного расположения, относительно другого. Например, у вас
  есть папка, в ней много файлов (возьмем корень системы). В этот корень вы распаковали архив программы,
  которая не предоставила скрипта удаления. Получается, вам надо вручную пройти по системе, найти распакованные
  файлы и удалить.

  Утилита позволяет этого избежать. Ей необходимо указать источник с файлами архива и путь, откуда эти 
  файлы надо удалить. Т.е вам останется распаковать архив в чистую папку и передать этот путь как источник,
  а для удаления указать корень фс.

  ```shell
  python3 ./remove-by-folder.py -s /tmp/compressed -r /
  ```

### 3.1 Аргументы запуска
  Актульные аргументы запуска можно получить флагом `-h`
  - `-s` `--source` -- папка с исходным содержимым (которое будет удаляться в другом)
  - `-r` `--remove` -- папка относительно которой искать файлы для удаления