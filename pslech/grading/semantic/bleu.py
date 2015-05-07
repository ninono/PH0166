#-*- coding: utf-8 -*-
from preprocessor import Processor
import math

class BLEU:
    N=4
    def __init__(self,candidate,standard):
        self.candidate=candidate
        self.standard=standard

        self.similarSentIndexs=[]    #The most similar sentence in the candidate for each standard sentence.
        self.similarityScores=[]    #The similarity of the most similar sentence in the candidate for each standard sentence.

        for i in range(0,len(self.standard)):
            bestMatchIndex=0
            bestScore=0
            for j in range(0,len(self.candidate)):
                score=BLEU.bleu(candidate[j],standard[i])
                if score>bestScore:
                    bestScore=score
                    bestMatchIndex=j
            self.similarSentIndexs.append(bestMatchIndex)
            self.similarityScores.append(bestScore)


    @staticmethod
    def bleu(candidateSent,standardSent):
        return BLEU.p(candidateSent,standardSent)*BLEU.bp(candidateSent,standardSent)

    @staticmethod
    def p(candidate,standard):
        prod=1
        invcnt=1
        for i in range(1,BLEU.N+1):
            candidate_n_gram=BLEU.convert2ngram(i,candidate)
            standard_n_gram=BLEU.convert2ngram(i,standard)
            count=0
            for gram in candidate_n_gram:
                if gram in standard_n_gram:
                    count+=1
            if count==0:
                invcnt*=2
                count=1.0/invcnt
            prod*=count*1.0/len(candidate_n_gram)
        return prod**(1.0/BLEU.N)

    @staticmethod
    def convert2ngram(n,tokenlist):
        num=len(tokenlist)-n+1
        if num<=0:
            return [tokenlist]
        res=[]
        for i in range(num):
            ele=[]
            for j in range(n):
                ele.append(tokenlist[i+j])
            res.append(ele)
        return res
    @staticmethod
    def bp(candidate,standard):
        return min(1.0,math.exp(1-len(standard)*1.0/len(candidate)))

def main():
    response="当晚出席者可凭入场票参加幸运抽奖"
    solution="当晚出席者可凭入场票参加幸运抽奖"
    distinctWords,candidate,standard,candidateSents,standardSents=Processor.preprocess(response,solution)
    a=BLEU(candidate,standard)
    print a.similarityScores

def main1():
    print BLEU.convert2ngram(3,[1,2,3,4,5])
if __name__=="__main__":
    main1()
