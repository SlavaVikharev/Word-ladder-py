#!/usr/bin/env python3

import sys

REGISTER = True


class Staircase:
    def __init__(self):
        dictionary = self.read_dictionary(sys.argv[3])
        start = sys.argv[1].strip()
        end = sys.argv[2].strip()
        if not REGISTER:
            start = start.lower()
            end = end.lower()
        dictionary = dictionary[len(start)]
        chainResult = self.find_chain(start, end, dictionary)

    def read_dictionary(self, dictionary_path):
        """
        Считывает файл из 'dictionary_path'
        Возвращает dict с ключами - длины слов,
        лежащих под этим ключом
        """
        dictionary = {}
        try:
            file = open(dictionary_path, encoding="utf-8")
        except IOError:
            print("There is no this file")
            sys.exit(1)
        for word in file:
            word = word.strip()
            if not REGISTER:
                word = word.lower()
            if len(word) in dictionary:
                dictionary[len(word)].append(word)
            else:
                dictionary[len(word)] = [word]
        file.close()
        return dictionary

    def find_similar(self, word, end, dictionary, visited, links):
        """
        Принимает слово, конечное слово для остановки,
        словарь, посещенные слова, зависимости слов
        Возвращает множество слов, отличающееся от слова на 1 позицию
        Возвращает конечное слово, если оно было найдено в похожих
        """
        visited.add(word)
        similar = set()
        for suspect in dictionary:
            if suspect in visited:
                continue
            fail = False
            for i in range(len(word)):
                if word[i] != suspect[i]:
                    if fail:
                        break
                    fail = True
            else:
                links[suspect] = word
                if suspect == end:
                    return suspect
                visited.add(suspect)
                similar.add(suspect)
        return similar

    def find_chain(self, start, end, dictionary):
        """
        Принимает начальное слово, конечное слово, словарь
        Возвращает цепь из похожих друг на друга слов
        Возвращает None, если таких слов не найдено
        """
        if start == end:
            return [start]
        if len(start) != len(end):
            return None
        visited = set()
        queue = [start]
        links = {}
        for current in queue:
            similar = self.find_similar(current, end,
                                        dictionary, visited, links)
            if similar == end:
                return self.build_chain(end, links)
            queue += similar
        return None

    def build_chain(self, last, links):
        """
        Принимает последнее слово в цепи и dict зависимостей слово
        Возвращает лист из слов, составленных из зависимостей
        """
        chain_list = [last]
        while last in links:
            last = links[last]
            chain_list.append(last)
        return chain_list[::-1]

    def write_result(self, chain):
        """
        Принимает лист слов
        Если лист пуст, выводит, что нельзя построить цепь
        Иначе выводит слова на экран
        """
        if not chain:
            print("There is no way to build the chain")
            return
        print("\nHere is a result:")
        for word in chain:
            print(word)
        print("Count: %i" % len(chain))


def check_input(self):
    if "--register" in sys.argv:
        REGISTER = False
    if "--help" in sys.argv:
        print("""
    Staircase
    ---------

    python3 staircase.py [first] [last] [dictionary file]

    --register - Регистронезависимость
    --help     - Эта страница

    Вход (аргументы): исходное слово, целевое слово и словарь.
    Выход: цепочка однобуквенных преобразований, позволяющая получить
    из исходного слова целевое, при этом каждый промежуточный шаг
    также является словом.
            """)
        quit()
    if len(sys.argv) < 4:
        print("Введите staircase.py --help, чтобы увидеть справку")
        quit()
    if len(sys.argv[1]) != len(sys.argv[2]):
        print("Длины слов должны быть равными")
        quit()


def main():
    check_input()
    staircase = Staircase()
    write_result(staircase.chainResult)
    quit()


if __name__ == "__main__":
    main()
