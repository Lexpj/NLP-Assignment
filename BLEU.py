import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import os
import sys


def getCorpus():
    """
    Tokenizes a text. Replace this with any related dataset to your text generation
    prompt in order to make use of a useful BLEU score.
    """
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
    
    
    def score(self, sentence):
        """
        Scores a sentence based on the reference in self.corpus
        :param sentence: sentence to be scored
        :return: float score between 0 and 1
        """
        tokens = nltk.word_tokenize(sentence)
        s = sentence_bleu(self.corpus, tokens, auto_reweigh=True, smoothing_function=self.smoothingFunction.method0)
        print(s)
        return s



