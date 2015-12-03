#!/usr/bin/env python3

import sys

__all__ = ["StaircaseTools"]


class StaircaseTools:

    @classmethod
    def read_dictionary(cls, dictionary_path, regins=True):
        """
        Принимает
        путь до словаря, флаг регистронезависимости

        Возвращает
        dict: value - set слов одинаковой длины
              key   - длина слов в set по этому ключу
        """
        try:
            dictionary = {}
            with open(dictionary_path) as file:
                for word in file:
                    word = word.strip()
                    if regins:
                        word = word.lower()
                    if len(word) in dictionary:
                        dictionary[len(word)].add(word)
                    else:
                        dictionary[len(word)] = set([word])
            return dictionary
        except IOError as e:
            raise e

    @classmethod
    def correct_input(cls, start, end, dictionary):
        """
        Принимает
        начальное слово, конечное слово, словарь

        Возвращает
        bool, зависящий от корректности слов
        """
        correct = True
        if len(start) != len(end):
            correct = False
        if start not in dictionary:
            correct = False
        if end not in dictionary:
            correct = False
        return correct

    @classmethod
    def is_similar(cls, word, another):
        """
        Принимает
        два слова

        Возвращает
        bool, отличаются ли слова на 1 букву
        """
        fail = False
        for i in range(len(word)):
            if word[i] != another[i]:
                if fail:
                    return False
                fail = True
        return fail

    @classmethod
    def generate_all_chains(cls, word, end, dictionary, max_dep, trace):
        """
        Рекурсивная функция - генератор

        Принимает
        текущее слово, конечное слово, словарь,
        максимальную глубину поиска, путь

        Возвращает
        lists - цепи похожих слов, длиной не более max_dep,
        если первое слово цепи start, последнее - end
        """
        trace.append(word)
        if word == end:
            yield trace
            return
        if len(trace) >= max_dep:
            return
        for suspect in dictionary.difference(trace):
            if not cls.is_similar(word, suspect):
                continue
            for chain in cls.generate_all_chains(suspect, end, dictionary,
                                                 max_dep, list(trace)):
                yield chain

    @classmethod
    def find_all_chains(cls, start, end, dictionary, max_dep):
        """
        Принимает
        начальное слово, конечное слово,
        словарь, максимальную глубину поиска

        Возвращает
        list цепей похожих слов, длиной не более max_dep,
        если первое слово цепи start, последнее - end
        если цепей не существует, возвращает пустой list
        """
        if not cls.correct_input(start, end, dictionary):
            return []
        return list(cls.generate_all_chains(start, end, dictionary,
                                            max_dep, []))

    @classmethod
    def find_shortest_chain(cls, start, end, dictionary):
        """
        Принимает
        начальное слово, конечное слово, словарь

        Возвращает
        list - кратчайшую цепь похожих слов,
        с первым словом start, последним - end
        если цепи не существует, возвращает пустой list
        """
        if not cls.correct_input(start, end, dictionary):
            return []
        queue = [start]
        links = {start: None}
        for current in queue:
            for suspect in dictionary.difference(links):
                if cls.is_similar(current, suspect):
                    links[suspect] = current
                    if suspect == end:
                        return cls.build_chain(end, links)
                    queue.append(suspect)

    @classmethod
    def build_chain(cls, word, links):
        """
        Принимает
        слово, с которого начинать построение цепи,
        зависимости слов

        Возвращает
        list - цепь, составленная
        от введенного слова, до начала
        в обратном порядке
        """
        chain = [word]
        while links[word] is not None:
            word = links[word]
            chain.append(word)
        return chain[::-1]

    @classmethod
    def print_chains(cls, chains, depth):
        """
        Принимает
        list цепей

        Выполняет
        вызов print_chain для каждой цепи
        если цепей нет, сообщает об этом
        """
        if len(chains) == 0:
            print("Не удалось построить ни одну цепь длиной до %i слов" % depth)
            return
        for chain in chains:
            cls.print_chain(chain)
        print('Количество цепей: %i\n' % len(chains))

    @classmethod
    def print_chain(cls, chain):
        """
        Принимает
        цепь

        Выполняет
        вывод на экран слов цепи и длину цепи
        если цепи нет, сообщает об этом
        """
        if len(chain) == 0:
            print("Не удалось построить цепь")
            return
        for word in chain:
            print(word)
        print('Количество слов: %i\n' % len(chain))


def check_input():

    if '--help' in sys.argv:
        print('''
    Staircase
    ---------

    staircase.py first last dict_path [options...]

    Options:
        --all          - Поиск всех цепей
        --regins       - Регистронезависимость
        --depth <int>  - Максимальная глубина поиска при ключе --all
        --help         - Эта страница

    Вход (аргументы): исходное слово, целевое слово и словарь.
    Выход: цепочка однобуквенных преобразований, позволяющая получить
    из исходного слова целевое, при этом каждый промежуточный шаг
    также является словом.
''')
        quit()
    if len(sys.argv) < 4:
        print('Введите staircase.py --help, чтобы увидеть справку')
        quit()


def main():

    check_input()

    start, end, dict_path = sys.argv[1:4]
    regins = '--regins' in sys.argv
    all_chains = '--all' in sys.argv
    max_dep = int(sys.argv[sys.argv.index('--depth') + 1]) \
        if '--depth' in sys.argv else 5

    if regins:
        start = start.lower()
        end = end.lower()

    try:
        dictionary = StaircaseTools.read_dictionary(dict_path, regins)
    except IOError as e:
        print(e)
        sys.exit(1)

    dictionary = dictionary[len(start)]

    if all_chains:
        chains = StaircaseTools.find_all_chains(start, end, dictionary, max_dep)
        StaircaseTools.print_chains(chains, max_dep)
    else:
        chain = StaircaseTools.find_shortest_chain(start, end, dictionary)
        StaircaseTools.print_chain(chain)


if __name__ == '__main__':
    main()
