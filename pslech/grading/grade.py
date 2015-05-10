#-*- coding: utf-8 -*-
from semantic.preprocessor import Processor
from semantic.LSA import *
from semantic.ngram import *
from semantic.ensemble import *
from semantic.threshold_setting import *
from syntactic.syntax import *
import math

semantic_mark_algos=["exact","lsa","ngram","ensemble","creative","mcq"]

def rounding(a):
    if(a-math.floor(a)>=0.75):
        return math.ceil(a)
    elif(a-math.floor(a)>=0.25):
        return math.floor(a)+0.5
    else:
        return math.floor(a)

def grade(method,solution,response,total_mark):
    if method not in semantic_mark_algos:
        raise KeyError("method does not exist")
    if method in ["exact","mcq"]:
        if solution==response:
            return {"score":total_mark}
        else:
            return {"score":0}
    sem_grade=sematic_grade(method,solution,response)
    syn_grade=syntactic_grade(response)
    g=rounding(sem_grade[0]*(0.5*syn_grade[0]+0.5)*total_mark)
    return {"score":g,"sematic":{"pos":sem_grade[1],"neg":sem_grade[2]},"syntactic":syn_grade[1]}

def syntactic_grade(response):
    errs= syntacticCheck(response)
    grade_in_percent=0 if errs['n_error']>=5 else (5-errs['n_error'])/5.0
    return grade_in_percent,errs['errors']

def sematic_grade(method,solution,response):
    distinctWords,candidate,standard,candidateSents,standardSents=Processor.preprocess(response,solution)
    if not candidate or not candidate[0]:
        return 0,["#未做答#"],["#未做答#"]
    if method=="ensemble":
        ensemble=Ensemble(distinctWords,candidate,standard,candidateSents,standardSents)
        count=len(ensemble.similarityScores)
        feedback_pos=ensemble.matchedSents
        feedback_neg=ensemble.unmatchedSents
        if count==0:
            return 0,feedback_pos,feedback_neg
        sum=0
        for s in ensemble.similarityScores:
            if s>ensemble_threshold:
                sum+=1
        sum=sum*1.0/count
        return sum,feedback_pos,feedback_neg

