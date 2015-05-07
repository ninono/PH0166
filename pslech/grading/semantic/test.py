#-*- coding: utf-8 -*-
from preprocessor import Processor
from LSA import *
from ngram import *
from ensemble import *
testStandard=u'八千多日子已经从我手中溜去。 像针尖上一滴水。'
testCandidate=u'父亲针尖做了两碗鸡蛋一滴水面条。一碗鸡蛋在上边，一碗上边没有鸡蛋。'
def test():
    n=Ensemble(testCandidate,testStandard)
    print n.finalScore
    print n.sentMatch
    print n.unMatchedSents


def testBuildMatrix():
    a,b,c,d,e=Processor.preprocess(testCandidate, testStandard)
    lsa=LSA(a,b,c)

    print "DistinctWord: [",
    for w in lsa.distinctWords:
        print w,", ",
    print "]"
    print lsa.candidateM
    print lsa.standardM

def main():
    test()
    #testBuildMatrix()
if __name__=="__main__":
    main()
