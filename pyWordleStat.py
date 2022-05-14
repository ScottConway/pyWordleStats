import argparse
import re
from operator import itemgetter

wordLetterStats = {}
firstLetterStats = {}
secondLetterStats = {}
thirdLetterStats = {}
fourthLetterStats = {}
fifthLetterStats = {}


def updateStatMap(letter, statMap):
    count = 0
    if letter in statMap:
        count = statMap[letter]

    statMap[letter] = count + 1


def updateLetterStats(letter, letterMap, totalsMap):
    updateStatMap(letter=letter, statMap=letterMap)
    updateStatMap(letter=letter, statMap=totalsMap)


def updateStats(word):
    updateLetterStats(letter=word[0], letterMap=firstLetterStats, totalsMap=wordLetterStats)
    updateLetterStats(letter=word[1], letterMap=secondLetterStats, totalsMap=wordLetterStats)
    updateLetterStats(letter=word[2], letterMap=thirdLetterStats, totalsMap=wordLetterStats)
    updateLetterStats(letter=word[3], letterMap=fourthLetterStats, totalsMap=wordLetterStats)
    updateLetterStats(letter=word[4], letterMap=fifthLetterStats, totalsMap=wordLetterStats)


def buildWordList(fileName):
    file = open(fileName, "r")
    wordList = list()

    for line in file:
        word = line.strip('\n')
        if re.match("[a-z]{5}", word):
            wordList.append(word)
            updateStats(word)
        else:
            print(f'{word} is invalid as all words must be five alphabetic letter.  Ignored from {fileName}')

    return wordList


def printMap(heading, statMap):
    print(f'\n{heading}\n====================================\n')
    for k, v in sorted(statMap.items(), key=itemgetter(1), reverse=True):
        print(f'{k}, {v}')
    print(f'{len(statMap)} : {statMap}')
    print(" ")


def calcWeight(mainWord, checkWord):
    usedLetters = set()
    score = 0
    for i in range(5):
        letter = mainWord[i]
        if letter not in usedLetters and letter == checkWord[i]:
            score += 3
        elif checkWord.find(letter) != -1:
            score += 2
        elif letter not in usedLetters:
            score += 1

        usedLetters.add(letter)

    return score


def findBestWords(wordlist):
    wordWeight = {}
    numWords = len(wordlist)
    wordCount = 0

    for w1 in wordlist:
        wordCount += 1
        if wordCount % 100 == 0:
            print(f'{wordCount} of {numWords}')

        for w2 in wordlist:
            if w1 == w2:
                continue
                
            weight=0
            if w1 in wordWeight:
                weight=wordWeight[w1]
            wordWeight[w1] = weight + calcWeight(mainWord=w1, checkWord=w2)

    loop = 0
    for k, v in sorted(wordWeight.items(), key=itemgetter(1), reverse=True):
        print(f'{k}, {v}')
        loop += 1
        if loop > 10:
            break

def main():
    parser = argparse.ArgumentParser(
        description='Helper program for wordle game.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    wordlist = buildWordList('words')

    print(f'Number of words are {len(wordlist)}')
    printMap(heading="first letter", statMap=firstLetterStats)
    printMap(heading="second letter", statMap=secondLetterStats)
    printMap(heading="third letter", statMap=thirdLetterStats)
    printMap(heading="fourth letter", statMap=fourthLetterStats)
    printMap(heading="fifth letter", statMap=fifthLetterStats)
    printMap(heading="all letters", statMap=wordLetterStats)

    # uncomment to find best start words (takes some time)
    #findBestWords(wordlist)


if __name__ == '__main__':
    main()