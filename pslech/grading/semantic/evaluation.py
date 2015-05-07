import os.path
import xml.etree.ElementTree as ET
from preprocessor import Processor
from LSA import *
from ngram import *
from ensemble import *
from bleu import *
import pickle
import numpy as np

Number_of_test_data=60
class TestSet:
    def __init__(self,id,solution,solution_mark,response,response_mark):
        self.id=id
        self.solution=solution
        self.response=response
        self.solution_mark=solution_mark
        self.mark=response_mark*1.0/solution_mark
        self.a,self.b,self.c,self.d,self.e=Processor.preprocess(self.response,self.solution)
    def __unicode__(self):
        return self.solution[:7]+"\t"+self.response[:7]+"\t"+str(self.mark)

def extract_test_set(dom):
    test_set=[]
    for i in range(len(dom)):
        s=dom[i]
        test_set.append(TestSet(i,s.find('solution').text,float(s.find('solution').get('mark')),s.find('response').text,float(s.find('response').get('mark'))))
    return test_set

def build_test_data():
    tree=ET.parse('testdata.xml')
    root=tree.getroot()
    exact=extract_test_set(root[0])
    opposite=extract_test_set(root[1])
    student=extract_test_set(root[2])
    return exact,opposite,student


class Score:
    def __init__(self,i,s,exp,solution_mark):
        self.id=i
        self.score=s
        self.expectation=exp
        self.solution_mark=solution_mark
    def setScoreList(self,s):
        self.score=s
    def getSim(self):
        return sum(self.score)/len(self.score)
    def getExpSim(self):
        return self.expectation*1.0/self.solution_mark
    def getScore(self,t):
        sum=0
        count=0
        for s in self.score:
            if s>t:
                sum+=1
                count+=1
        if count==0:
            return 0
        return sum*1.0/len(self.score)
    def getAcc(self,t):
        accuracy=1-abs(self.getScore(t)-self.expectation)
        return accuracy

def call(func,a,b,c,d,e):
    if func=='lsa':
        return LSA(a,b,c)
    elif func=='ngram':
        return NGram(a,b,c)
    elif func=='ensemble':
        return Ensemble(a,b,c,d,e)
    elif func=='bleu':
        return BLEU(b,c)
def main(func):
    exact,opposite,student=build_test_data()
    thres=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]


    print "=====================exact======================"
    exact_score=[]
    for t in exact:
        f=call(func,t.a,t.b,t.c,t.d,t.e)
        exact_score.append(Score(t.id,f.similarityScores,t.mark,t.solution_mark))

    print "=====================opposite======================"
    opposite_score=[]
    for t in opposite:
        f=call(func,t.a,t.b,t.c,t.d,t.e)
        opposite_score.append(Score(t.id,f.similarityScores,t.mark,t.solution_mark))
        '''
        if opposite_score[-1].getAcc(0.5)<0.5:
            print opposite_score[-1].getScore(0.5)
            print t.solution
            print t.response
            print f.similarityScores
            print f.similarSentIndexs
            print "standard not"
            print np.matrix(f.standard_not)
            print "standard t"
            print np.matrix(f.standard_t)
            print "candidate not"
            print np.matrix(f.candidate_not)
            print "candidate t"
            print np.matrix(f.candidate_t)
            print 'candidate_t_custom'
            for ma in f.candidate_t_custom:
                print ma
            print "---------------------"
            return f
            '''

    print "=====================student======================"
    student_score=[]
    for t in student:
        f=call(func,t.a,t.b,t.c,t.d,t.e)
        student_score.append(Score(t.id,f.similarityScores,t.mark,t.solution_mark))

    print "====================outputing====================="
    all_score=exact_score+opposite_score+student_score
    response_sim=[s.getSim() for s in all_score]
    expert_sim=[s.getExpSim() for s in all_score]
    #cov=np.cov(response_sim,expert_sim)[0][1]
    #corr=cov/np.std(response_sim)/np.std(expert_sim)
    #print corr
    for th in thres:
        count=0
        for i in range(len(expert_sim)):
            if (abs(expert_sim[i]-response_sim[i])<th):
                count+=1
        print "threshold=",th,"\tAA=",count*1.0/len(expert_sim)


    '''
    print "--------------------exact-------------------------"
    print "Threshold\t"+func
    for t in thres:
        score=sum([x.getAcc(t) for x in exact_score])/len(exact_score)
        print t,"\t",score
    print "--------------------opposite-------------------------"
    print "Threshold\t"+func
    for t in thres:
        score=sum([x.getAcc(t) for x in opposite_score])/len(opposite_score)
        print t,"\t",score
    print "--------------------student-------------------------"
    print "Threshold\t"+func
    for t in thres:
        score=sum([x.getAcc(t) for x in student_score])/len(student_score)
        print t,"\t",score
        '''

if __name__=="__main__":
    main(sys.argv[1])


