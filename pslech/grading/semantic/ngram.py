from preprocessor import Processor
from threshold_setting import *

class NGram(object):
    ngram_n=NGRAM_N

    def __init__(self,distinctWords,candidate,standard):

        self.distinctWords=distinctWords
        #Do make a copy since we are going to change it!
        self.candidate=[]
        self.candidate.extend(candidate)
        self.standard=[]
        self.standard.extend(standard)


        self.groupGrams(self.candidate)
        self.groupGrams(self.standard)

        self.wordOccurrenceMap(self.candidate)
        self.wordOccurrenceMap(self.standard)

        '''
        print "Candidate:"
        print self.candidate
        print "Standard:"
        print self.standard  '''

        self.similarSentIndexs=[]    #The most similar sentence in the candidate for each standard sentence.
        self.similarityScores=[]    #The similarity of the most similar sentence in the candidate for each standard sentence.

        for i in range(0,len(self.standard)):
            bestMatchIndex=0
            bestScore=0
            standardMap=self.standard[i]

            for j in range(0,len(self.candidate)):
                candidateMap=self.candidate[j]
                score=self.computeScore(candidateMap,standardMap)
                if score>bestScore:
                    bestScore=score
                    bestMatchIndex=j

            self.similarSentIndexs.append(bestMatchIndex)
            self.similarityScores.append(bestScore)

        '''
        print "Scores:"
        print self.similarityScores
        print "Best Matches:"
        print self.similarSentIndexs   '''

    def computeScore(self,candidateMap,standardMap):
        numerator=denominator=0.0
        for key in standardMap:
            denominator+=standardMap[key]
            #We add to numerator only if both standardMap and candidateMap have the key.
            if key in candidateMap:
                #Add the smaller one in candidateMap[key] and standardMap[key] to numerator.
                numerator+=candidateMap[key] if candidateMap[key]<standardMap[key] else standardMap[key]
        return numerator/denominator


    #Generate a map that shows the occurrence of each distinct word in a sentence
    def wordOccurrenceMap(self,sentTokenList):
        for i in range(0,len(sentTokenList)):
            newSents={}
            for token in sentTokenList[i]:
                if token in newSents:
                    newSents[token]+=1
                else:
                    newSents[token]=1
            sentTokenList[i]=newSents

    #Group ngram_n number of words into one token
    def groupGrams(self,sentWordList):
        for i in range(0,len(sentWordList)):
            newSents=[]
            #if len(sentWordList[i]) is smaller than ngram_n, there will be only one trimmed token
            if len(sentWordList[i])<self.ngram_n:
                newSents.append(" ".join(sentWordList[i]))
                #No i++ since the length shrinks
            else:

                for j in range(0,len(sentWordList[i])+1-self.ngram_n):
                    gramToken=[sentWordList[i][p] for p in range(j,j+self.ngram_n)]
                    newSents.append(" ".join(gramToken))
            sentWordList[i]=newSents


