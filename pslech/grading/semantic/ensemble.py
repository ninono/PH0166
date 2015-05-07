from LSA import LSA
from ngram import NGram
from bleu import BLEU
from preprocessor import Processor
from threshold_setting import *

class Ensemble(object):
    THRESHOLD=ensemble_threshold

    def __init__(self,a,b,c,d,e):
        distinctWords,candidate,standard,candidateSents,standardSents=a,b,c,d,e


        #print candidate
        #print '--------------------------'
        #print standard

        lsa=LSA(distinctWords,candidate,standard)
        ngram=NGram(distinctWords,candidate,standard)
        bleu = BLEU(candidate,standard)

        self.lsaScore=lsa.similarityScores
        self.ngramScore=ngram.similarityScores
        self.bleuScore=bleu.similarityScores

        self.similarityScores=[(self.lsaScore[i]+self.ngramScore[i]+self.bleuScore[i])/3.0 for i in range(len(self.lsaScore)) ]

        self.matchedSents=[]
        self.unmatchedSents=[]
        for i in range(0,len(self.similarityScores)):
            if self.similarityScores[i]>=self.THRESHOLD:
                self.matchedSents.append(standardSents[i])
            else:
                self.unmatchedSents.append(standardSents[i])





