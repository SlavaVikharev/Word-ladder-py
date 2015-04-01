#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def read_dictionary(dictionaryPath):
    """
    Считывает файл из 'dictionaryPath'
    Возвращает dict с ключами - длины слов,
    лежащих под этим ключом
    """
    dictionary = {}
    for word in open(dictionaryPath):
        word = word[:-1]
        if len(word) in dictionary:
            dictionary[len(word)].append(word)
        else:
            dictionary[len(word)] = [word]
    return dictionary


def find_similar(word, end, dictionary, visited, links):
    """
    Принимает слово, конечное слово,
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


def find_chain(start, end, dictionary):
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
        similar = find_similar(current, end, dictionary, visited, links)
        if similar == end:
            return build_chain(end, links)
        queue += similar
    return None


def build_chain(last, links):
    """
    Принимает последнее слово в цепи и dict зависимостей слово
    Возвращает лист из слов, составленных из зависимостей
    """
    chainList = []
    while True:
        chainList.append(last)
        try:
            last = links[last]
        except:
            break
    return chainList[::-1]


def write_result(chain):
    """
    Принимает лист слов
    Если лист пуст, выводит, что нельзя построить цепь
    Иначе выводит слова на экран
    """
    if not chain:
        print("There is no way to build the chain")
    print("\nHere is a result:")
    for word in chain:
        print(word)
    print("Count: %i" % len(chain))


def main():
    if len(sys.argv) == 1:
        print("Введите staircase.py --help, чтобы увидеть справку")
        quit()
    if sys.argv[1] == "--help":
        print("""
    Staircase
    ---------

    Вход (аргументы): исходное слово, целевое слово и словарь.
    Выход: цепочка однобуквенных преобразований, позволяющая получить
    из исходного слова целевое, при этом каждый промежуточный шаг
    также является словом.
            """)
        quit()
    dictionary = read_dictionary(sys.argv[3])
    start = sys.argv[1].strip()
    end = sys.argv[2].strip()
    dictionary = dictionary[len(start)]
    chainResult = find_chain(start, end, dictionary)
    write_result(chainResult)
    quit()


if __name__ == "__main__":
    main()
