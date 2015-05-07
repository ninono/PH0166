import codecs
import sys
def convert(inFile,outFile):
    iF=codecs.open(inFile,'r','utf-8')
    oF=codecs.open(outFile,'w','gb18030')
    for line in iF:
        oF.write(line)
    iF.close()
    oF.close()

if __name__=="__main__":
    convert(sys.argv[1],sys.argv[2])


