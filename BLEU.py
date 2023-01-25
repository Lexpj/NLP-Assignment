import nltk
from nltk.translate.bleu_score import sentence_bleu
import os
import sys


def getCorpus():
    with open(os.path.dirname(__file__)+f"/../poems.txt","r") as f:
        return [nltk.word_tokenize(line) for line in f.readlines()]


class BLEU:
    def __init__(self):
        self.corpus = getCorpus()
    
    def score(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return sentence_bleu(self.corpus, tokens)


    