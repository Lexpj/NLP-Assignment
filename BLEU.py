import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import os
import sys


def getCorpus():
    with open(os.path.dirname(__file__)+f"/../bbclines.txt","r") as f:
        sentences = []
        for paragraph in f.readlines():
            lines = paragraph.split('.')
            for line in lines:
                try:
                    sentences.append(nltk.word_tokenize(line))
                except:
                    pass

        return sentences

class BLEU:
    def __init__(self):
        self.corpus = getCorpus()
        self.smoothingFunction = SmoothingFunction()
        print(self.corpus[:2])
    
    def score(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        s = sentence_bleu(self.corpus, tokens, auto_reweigh=True, smoothing_function=self.smoothingFunction.method0)
        print(s)
        return s



