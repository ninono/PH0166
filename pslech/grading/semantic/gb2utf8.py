import codecs
import sys
def main(iF,oF):
    iFile=codecs.open(iF,'r','gb18030')
    oFile=codecs.open(oF,'w','utf8')
    for line in iFile:
        oFile.write(line)
    iFile.close()
    oFile.close()
if __name__=="__main__":
    main(sys.argv[1],sys.argv[2])
