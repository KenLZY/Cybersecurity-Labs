#!/opt/anaconda3/bin/python3
import argparse
import re  # regular expression module


# first, we create a function
def mainFunction(filein, fileout):
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode

    commonAlphabetOrdered = [
        "e",
        "t",
        "a",
        "o",
        "i",
        "n",
        "s",
        "h",
        "r",
        "d",
        "l",
        "c",
        "u",
        "m",
        "w",
        "f",
        "g",
        "y",
        "p",
        "b",
        "v",
        "k",
        "j",
        "x",
        "q",
        "z",
    ]

    commonBigramOrdered = [
        "th",
        "he",
        "in",
        "er",
        "an",
    ]

    common_words = {
        "sings",
        "heart",
        "having",
        "last",
        "season",
        "engaging",
        "thinking",
        "show",
        "the",
        "be",
        "to",
        "of",
        "and",
        "a",
        "in",
        "that",
        "have",
        "i",
        "it",
        "its",
        "strengths",
        "for",
        "not",
        "on",
        "with",
        "he",
        "as",
        "you",
        "do",
        "at",
        "this",
        "but",
        "his",
        "by",
        "from",
        "they",
        "we",
        "say",
        "her",
        "she",
        "or",
        "an",
        "will",
        "my",
        "one",
        "all",
        "would",
        "there",
        "their",
        "what",
        "so",
        "up",
        "out",
        "if",
        "about",
        "who",
        "get",
        "which",
        "go",
        "me",
        "when",
        "make",
        "can",
        "like",
        "time",
        "no",
        "just",
        "him",
        "know",
        "take",
        "people",
        "into",
        "year",
        "your",
        "good",
        "some",
        "could",
        "them",
        "see",
        "other",
        "than",
        "then",
        "now",
        "look",
        "only",
        "come",
        "its",
        "over",
        "think",
        "also",
        "back",
        "after",
        "use",
        "two",
        "how",
        "our",
        "work",
        "first",
        "well",
        "way",
        "even",
        "new",
        "want",
        "because",
        "any",
        "these",
        "give",
        "day",
        "most",
        "us",
        "never",
        "is",
        "missed",
        "honestly",
        "most",
        "both",
        "song",
        "moment",
        "for",
        "myself",
        "years",
        "am",
        "out",
        "looooong",
        "looong",
        "term",
        "what",
        "bothered",
        "wondered",
        "true",
        "yes",
        "are",
        "bad",
        "ones",
        "oh",
        "turned",
        "better",
        "worse",
        "may",
        "rare",
        "taken",
        "has",
        "maybe",
        "hearts",
        "try",
        "whenever",
        "very",
        "first",
        "episode",
        "ended",
        "wondered",
        "decided",
        "expect",
        "watching",
    }

    with open(filein, mode="r") as fin:

        text = fin.read()
        # count the number of letters in the text
        letterDict = {}
        for char in text:
            if char.isalpha():
                if char not in letterDict:
                    letterDict[char] = 1
                else:
                    letterDict[char] += 1
            else:
                continue

        sorted_dict = dict(
            sorted(letterDict.items(), key=lambda item: item[1], reverse=True)
        )

        oneWordFreqDict = {}
        # now, we count how many 1 letter words are there
        print("\nWe start off by counting how many one letter words are there...\n")
        oneWordList = [word for word in text.split() if len(word) == 1]
        for word in oneWordList:
            if word not in oneWordFreqDict:
                oneWordFreqDict[word] = 1
            else:
                oneWordFreqDict[word] += 1
        print(oneWordFreqDict)
        print(
            "\n 'Q' and 'Y' are the one letter words that appear in the ciphertext and based on "
            "Google, it could be 'a' or 'i', so we are replacing them respectively\n"
        )

        text = replaceFunc(text, "Y", "i")
        text = replaceFunc(text, "Q", "a")

        twoLetterFreq = {}
        print("Now, we are going to siphon out 2 letter words...\n")
        twoLetterWords = [word for word in text.split() if len(word) == 2]
        for word in twoLetterWords:
            if word not in twoLetterFreq:
                twoLetterFreq[word] = 1
            else:
                twoLetterFreq[word] += 1

        text = replaceFunc(text, "J", "t")
        text = replaceFunc(text, "I", "s")

        threeLetterFreq = {}
        print("Now, 3 letter words...")
        threeLetterWords = [word for word in text.split() if len(word) == 3]
        for word in threeLetterWords:
            if word not in threeLetterFreq:
                threeLetterFreq[word] = 1
            else:
                threeLetterFreq[word] += 1

        print("\n'tXU' appears the most, could be 'the'...\n")

        text = replaceFunc(text, "X", "h")
        text = replaceFunc(text, "U", "e")
        text = replaceFunc(text, "M", "w")
        text = replaceFunc(text, "H", "r")
        text = replaceFunc(text, "L", "v")
        text = replaceFunc(text, "D", "n")
        text = replaceFunc(text, "W", "g")
        text = replaceFunc(text, "O", "y")
        text = replaceFunc(text, "K", "u")
        text = replaceFunc(text, "T", "d")
        text = replaceFunc(text, "E", "o")
        text = replaceFunc(text, "V", "f")
        text = replaceFunc(text, "B", "l")
        text = replaceFunc(text, "C", "m")
        text = replaceFunc(text, "R", "b")
        text = replaceFunc(text, "S", "c")
        text = replaceFunc(text, "A", "k")
        text = replaceFunc(text, "N", "x")
        text = replaceFunc(text, "F", "p")
        text = replaceFunc(text, "Z", "j")
        text = replaceFunc(text, "P", "z")

        print(text)

        fout.write(text)


def checkUpperCase(text: str):
    print(
        "Now to check if there are any uppercase letters left (i.e. undeciphered letters)...\n"
    )
    upperList = []
    for letter in text:
        if letter.isalpha():
            if letter.isupper() and letter not in upperList:
                upperList.append(letter)
    if len(upperList) == 0:
        return "All's done! Ready to write to output file...\n"
    else:
        return f"Remaining undeciphered letters:\n{upperList}\n"


def replaceFunc(text: str, target: str, replacement: str) -> str:
    """
    This function replaces the target letter with the replacement letter
    and returns the new text
    """
    print(f"'{target}' could be '{replacement}'...\n")
    newText = text.replace(target, replacement)
    print(checkUpperCase(newText))
    return newText


def getTop7Char(dictionary):
    return list(dictionary.keys())[:7]


def findCommonBigram(textFile):
    """
    This function counts and returns the top 5 common bigrams
    in the ciphertext
    """
    # create an empty dictionary for counting
    commonPairs = {}
    # split the text up with spaces into a list
    wordList = textFile.split(" ")
    # iterate through the list
    for word in wordList:
        for i in range(len(word) - 1):
            bigram = word[i : i + 2]
            if bigram not in commonPairs.keys():
                commonPairs[bigram] = 1
            else:
                commonPairs[bigram] += 1

    sortedPairs = dict(
        sorted(commonPairs.items(), key=lambda item: item[1], reverse=True)
    )
    return list(sortedPairs.keys())[:5]


def findCommonTrigram(textFile):
    # create an empty dictionary for mapping
    commonPairs = {}
    # split the text up with spaces into a list
    wordList = textFile.split(" ")
    # iterate through the list
    for word in wordList:
        if len(word) == 3:  # if the word is 3 characters
            if word not in commonPairs.keys():
                commonPairs[word] = 1
            else:
                commonPairs[word] += 1

    sortedPairs = dict(
        sorted(commonPairs.items(), key=lambda item: item[1], reverse=True)
    )

    return list(sortedPairs.keys())[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")

    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout

    mainFunction(filein, fileout)
