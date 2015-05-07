#-*- coding: utf-8 -*-
#This program makes use of numpy and scipy for math operation
from numpy import zeros,array,dot
from numpy.linalg import svd,inv,norm
from numpy import matrix
from preprocessor import *

class LSA:
    DIMENSION_REDUCTION=6

    def __init__(self,distinctWords,candidate,standard):
        self.distinctWords=distinctWords
        self.candidate=candidate
        self.standard=standard

        '''
        print "candidate:"
        print self.candidate
        print "standard:"
        print self.standard
        '''
        self.similarSentIndexs=[]    #The most similar sentence in the candidate for each standard sentence.
        self.similarityScores=[]    #The similarity of the most similar sentence in the candidate for each standard sentence.

        for i in range(0,len(self.standard)):
            bestMatchIndex=0
            bestScore=0
            for j in range(0,len(self.candidate)):
                score=LSA.cal(distinctWords,candidate[j],standard[i])
                if score>bestScore:
                    bestScore=score
                    bestMatchIndex=j
            self.similarSentIndexs.append(bestMatchIndex)
            self.similarityScores.append(bestScore)

        return



        self.rowNumber={}
        #A dictionary that maps a distinct word to its row number in the matrix
        for i in range(0,len(self.distinctWords)):
            self.rowNumber[self.distinctWords[i]]=i

        #Build candidate and standard matrix
        self.buildMatrix()

        #Do Singular Value Decomposition
        self.U,self.S,self.Vt = self.computeSVD(self.candidateM, self.DIMENSION_REDUCTION)


        self.similarSentIndexs=[]    #The most similar sentence in the candidate for each standard sentence.
        self.similarityScores=[]    #The similarity of the most similar sentence in the candidate for each standard sentence.
        self.standard_not=[]
        self.standard_t=[]
        self.candidate_t=[]
        self.candidate_not=[]
        self.candidate_t_custom = [matrix(self.getColumnVector(self.candidateM,j))*
                matrix(self.U)*inv(matrix(self.S)) for j in range(len(self.candidate))]

        #Process standard sentences one by one
        for i in range(0,len(self.standard)):
            #Get Standard Vector
            standardV=self.getColumnVector(self.standardM,i)
            self.standard_not.append(standardV)

            #U is a matrix represents the relation of terms(words)
            #Vt is a matrix represents the relation of documents(sentences)
            #Original term-document(word-sentence) Matrix O ~= U*S*Vt
            #Ot=V*St*Ut=V*S*Ut  (t means transpose)(S is a diagonal matrix, so S=St)
            #Thus V=V*S*Ut*U*S'=Ot*U*Si(i means inverse).

            #For standard sentence vector C, we modify it by C=C*U*Si
            #So that the standard vector also applies the same word relations generated from O.
            #Then we can compare the standard vector with the document vectors.

            s = max([i for i in range(self.S.shape[1]) if self.S[i,i]])+1
            self.U = self.U[:, :s]
            self.S = self.S[:s,:s]
            standardV=matrix(standardV)*matrix(self.U)*inv(matrix(self.S))

            standardV=standardV.getA()[0]
            self.standard_t.append(standardV)
            #Need to get the first row as a array of the resulting matrix
            #i.e get array([1,3,4]) form matrix([[1,3,4]])

            bestMatchIndex=0
            bestScore=0
            bestCandidateV=None
            bestCandidateV_not=None
            #Compare the candidate with standard sentence by sentence
            for j in range(0,len(self.candidate)):
                candidateV_not = self.getColumnVector(self.candidateM, j)
                candidateV=self.getColumnVector( self.Vt, j)[:s]
                #candidateV= dot(self.S, candidateV.transpose())
                #standardV=dot(self.S,standardV.transpose())
                #print standardV
                score=dot(standardV,candidateV)*1.0/(norm(standardV)*norm(candidateV)+10**(-10))

                if score>bestScore:
                    bestScore=score
                    bestMatchIndex=j
                    bestCandidateV=candidateV
                    bestCandidateV_not=candidateV_not
                    #The index of the best match sentence.

                '''print "Candidate"+str(i)+"----------------"
                print candidateV
                print "Standard"+str(j)+"----------------"
                print standardV
                print "Score------------------"
                print score'''

            self.similarSentIndexs.append(bestMatchIndex)
            self.similarityScores.append(bestScore)
            self.candidate_t.append(bestCandidateV)
            self.candidate_not.append(bestCandidateV_not)


    @staticmethod
    def cal(distinct,candidate,standard):
        candidateV=[0 for x in distinct]
        standardV=[0 for x in distinct]
        for e in candidate:
            candidateV[distinct.index(e)]+=1
        for e in standard:
            standardV[distinct.index(e)]+=1
        score=dot(standardV,candidateV)*1.0/(norm(standardV)*norm(candidateV)+10**(-10))
        return score


    def buildMatrix(self):
        self.candidateM=zeros([len(self.distinctWords),len(self.candidate)])
        self.standardM=zeros([len(self.distinctWords),len(self.standard)])

        for column in range(0,len(self.candidate)):
            for word in self.candidate[column]:
                self.candidateM[self.rowNumber[word]][column]+=1

        for column in range(0,len(self.standard)):
            for word in self.standard[column]:
                self.standardM[self.rowNumber[word]][column]+=1

    def getColumnVector(self,matrix,column):
        return array([r[column] for r in matrix])

    #The matrix, starting row(including), ending row(including), starting column, ending column
    def getSubmatrix(self,matrix,rows,rowe,cols,cole):
        compressRow=[False for i in range(0,len(matrix))]
        for i in range(0,len(compressRow)):
            if rows<=i<=rowe:
                compressRow[i]=True

        compressCol=[False for i in range(0,len(matrix[0]))]
        for i in range(0,len(compressCol)):
            if cols<=i<=cole:
                compressCol[i]=True

        matrix=matrix.compress(compressRow,axis=0)
        matrix=matrix.compress(compressCol,axis=1)

        return matrix

    def computeSVD(self,matrix,dimension):
            vecRank=[]

            Rows,Cols=matrix.shape
            #Get the num of rows/cols of the matrix
            min=Cols if Cols<Rows else Rows

            U, sValue, Vt = svd(matrix)
            S=diagsvd(sValue,Rows,Cols)


            if dimension<0 or dimension>min:
                dimension=min
            #Reduce the dimensions of the matrix

            U=self.getSubmatrix(U, 0, len(U)-1, 0, dimension-1)
            S=self.getSubmatrix(S, 0, dimension-1, 0, dimension-1)
            Vt=self.getSubmatrix(Vt, 0, dimension-1, 0, len(Vt[0])-1)

            return U,S,Vt

from numpy import asarray_chkfinite, asarray, zeros, r_, diag
#Originally, this file uses from scipy.linalg import svd,diagsvd,inv,norm
#Since scipy is hard to install in appfog
#we use svd,inv,norm in numpy==1.7.0
#and diagsvd copyed from scipy.linalg to here
def diagsvd(s, M, N):
    """
    Construct the sigma matrix in SVD from singular values and size M, N.

    Parameters
    ----------
    s : (M,) or (N,) array_like
        Singular values
    M : int
        Size of the matrix whose singular values are `s`.
    N : int
        Size of the matrix whose singular values are `s`.

    Returns
    -------
    S : (M, N) ndarray
        The S-matrix in the singular value decomposition

    """
    part = diag(s)
    typ = part.dtype.char
    MorN = len(s)
    if MorN == M:
        return r_['-1', part, zeros((M, N-M), typ)]
    elif MorN == N:
        return r_[part, zeros((M-N,N), typ)]
    else:
        raise ValueError("Length of s must be M or N.")

