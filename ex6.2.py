import re

class Data :
    def __init__(self, fileName):
        self.dataFileName = fileName
        self.dataDictionary = self.processData()
        self.classIndices, self.classCount = self.getClassIndices()
        self.wordCount = self.countWordInEachClass()
        self.vocabSize = self.getVocabSize()

    def processData(self):
        dataFile = open(self.dataFileName, 'r')
        line_pattern = '(\w+) -> (.*)'
        doc_dictornary = dict()
        doc_no = 1

        for line in dataFile:
            matches = re.match(line_pattern, line)
            category = matches.group(1)
            words = matches.group(2).split(', ')
            doc_dictornary[doc_no] = words, category
            doc_no = doc_no + 1

        return doc_dictornary

    def getVocabSize(self):
        count = 0
        for keys in self.dataDictionary:
            count = count + len(self.dataDictionary[keys][0])
        return count

    def getClassIndices(self):
        classDictionary = dict()
        classCount = dict()
        elemIndex = 1

        for key in self.dataDictionary.keys():
            category = self.dataDictionary[key][1]

            if category in classDictionary:
                classDictionary[category] = classDictionary[category] + (key, )
                classCount[category] = classCount[category] + len(self.dataDictionary[key][0])
            else:
                classDictionary[category] = (key, )
                classCount[category] = len(self.dataDictionary[key][0])

            elemIndex = elemIndex + 1

        return classDictionary, classCount

    def countWordInEachClass(self):
        wordModel = dict()
        for c in self.classIndices.keys():
            for indices in self.classIndices[c]:
                for word in self.dataDictionary[indices][0]:
                    if (word, c) in wordModel:
                        wordModel[word, c] = wordModel[word, c] + 1
                    else:
                        wordModel[word, c] = 1

        return wordModel

    def getLikelihood(self, w, c):
        if (w, c) in self.wordCount:
            return (self.wordCount[w, c] + 1) * 1.0/ (self.classCount[c] + self.vocabSize)
        else:
            return 1.0/ (self.classCount[c] + self.vocabSize)

    def getClassPrior(self, c):
        return 1.0 * self.classCount[c]/self.classIndices.__len__()

    def getDocProbability(self, listofWords, c):
        p = 1.0
        for word in listofWords:
            p = p * self.getLikelihood(word, c)

        return p * self.getClassPrior(c)

    def predict(self, doc):
        p = 0.0
        pred_c = None
        for c in self.classIndices.keys():
            temp = self.getDocProbability(doc, c)
            if p < temp:
                p = temp
                pred_c = c

        return pred_c

def main():
    docs = Data('data/ex6.2.txt')
    input_doc = ['fly', 'fast', 'shoot', 'love']
    print docs.predict(input_doc)

if __name__ == '__main__':
    main()