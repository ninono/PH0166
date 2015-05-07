# -*- coding: utf-8 -*-
import nltk,os
from nltk.stem import WordNetLemmatizer
#Used to stem words

import sys
from nltk.corpus import wordnet
import codecs
import re
import numpy as np

import pdb
class Processor(object):

    @staticmethod
    def preprocess(candidate,standard):
        candidate,candidateSents = Processor.processText(candidate)
        standard,standardSents = Processor.processText(standard)

        distinctWords = []
        Processor.addDistinctWords(distinctWords,candidate)
        Processor.addDistinctWords(distinctWords,standard)


        distinctWords,candidate,standard=Processor.replaceSynonym(distinctWords,candidate,standard)

        return distinctWords,candidate,standard,candidateSents,standardSents

    '''
    Input a distinct word list and a 2-d list contains words in sents of a text, and add new words into the distinct word list
    '''
    @staticmethod
    def addDistinctWords(distinctList,sentWordList):
        for sent in sentWordList:
            for word in sent:
                if word not in distinctList:
                    distinctList.append(word)
                    #Remember to lower all words.

    @staticmethod
    def buildSynonymDict():
        dictFile=codecs.open('grading/resources/synonymDict.txt','r','utf8')
        #dictFile=codecs.open('../resources/synonymDict.txt','r','utf8')
        sDict={}
        lineNm=0
        for line in dictFile:
            words=line.strip().split()
            if (words[0][-1]!='='):
                continue
            else:
                words=words[1:]
            for word in words:
                if word not in sDict:
                    sDict[word]=[lineNm]
                else:
                    sDict[word].append(lineNm)
            lineNm+=1

        dictFile.close()
        sDict={k:set(sDict[k]) for k in sDict}
        return sDict

    synonymDict=buildSynonymDict.__func__()
    @staticmethod
    def replaceSynonym(distinctWords,candidate,standard):
        rDistinctWords=[]
        connectGraph=np.eye(len(distinctWords))
        for i in range(len(distinctWords)):
            for j in range(len(distinctWords)):
                if (distinctWords[i] in Processor.synonymDict and
                    distinctWords[j] in Processor.synonymDict and
                    len(Processor.synonymDict[distinctWords[i]].intersection(Processor.synonymDict[distinctWords[j]]))!=0):
                        connectGraph[i,j]=1
                        connectGraph[j,i]=1
        connectGraph=connectGraph**len(distinctWords)
        connectGraph=connectGraph>0
        wordToKeyDict={}
        connectionToWordDict={}
        for i in range(len(distinctWords)):
            wordToKeyDict[distinctWords[i]]=tuple(connectGraph[i,:])
            if tuple(connectGraph[i,:]) not in connectionToWordDict:
                connectionToWordDict[tuple(connectGraph[i,:])]=distinctWords[i]
                rDistinctWords.append(distinctWords[i])
        return (rDistinctWords, [[connectionToWordDict[wordToKeyDict[e]] for e in l] for l in candidate], [[connectionToWordDict[wordToKeyDict[e]] for e in l] for l in standard])


    @staticmethod
    def processText(text):
        # only a work-around, need to
        # add more sentence termintoror like ? and !
        orisents = re.split(u'[，。！；：,!;:]', text.strip(), flags=re.UNICODE)
        sents = [Processor.processSent(x) for x in orisents if x]
        return sents,orisents

    @staticmethod
    def processSent(sent):
        '''
        segmenter = StanfordSegmenter(path_to_jar="../resources/stanford-segmenter-2014-10-26/stanford-segmenter-3.5.0.jar",path_to_sihan_corpora_dict="../resources/stanford-segmenter-2014-10-26/data", path_to_model="../resources/stanford-segmenter-2014-10-26/data/pku.gz", path_to_dict="../resources/stanford-segmenter-2014-10-26/data/dict-chris6.ser.gz",java_options="-mx2g")
        #segmentation
        result=segmenter.segment(sent)

        #remove punctuation
        content=""
        for ch in result:
            if ch==" ":
                content+=ch
            if 0x4E00<=ord(ch)<=0x9FFF or 0x3400<=ord(ch)<=0x4DFF or 0x20000<=ord(ch)<=0x2A6DF or 0xF900<=ord(ch)<=0xFAFF or 0x2F800<=ord(ch)<=0x2FA1F or ord('0')<=ord(ch)<=ord('9'):
                content+=ch

        res=content.split()
        '''

        import jieba
        res=list(jieba.cut(sent,cut_all=False))
        for ch in res:
            if len(ch)==1 and (not 0x4E00<=ord(ch)<=0x9FFF) and (not 0x3400<=ord(ch)<=0x4DFF) and (not 0x20000<=ord(ch)<=0x2A6DF) and (not 0xF900<=ord(ch)<=0xFAFF ) and (not 0x2F800<=ord(ch)<=0x2FA1F) and (not ord('0')<=ord(ch)<=ord('9')):
                res.remove(ch)

        #remove stop words
        f=codecs.open('grading/resources/chinese_stopword.txt','r','UTF-8')
        #f=codecs.open('../resources/chinese_stopword.txt','r','UTF-8')
        stopwords=f.read().split()
        stopwords=[]
        res=[x for x in res if x not in stopwords]
        return res


def main():
    a=[[u"天气",u"晴朗"]]
    b=[[u"天气",u"晴空万里"]]
    dis=[u"天气",u"晴朗",u"晴空万里"]
    dis,a,b=Processor.replaceSynonym(dis,a,b)
    for ele in dis:
        print ele,
    print
    for ele in a:
        print ele,
    print
    for ele in b:
        print ele,
    print
