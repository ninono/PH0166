import jieba
import codecs

inputFile=codecs.open('./dev.gb','r','gb18030')
outputFile=codecs.open('./hyp.gb','w','gb18030')
for line in inputFile:
    outputFile.write(' '.join(jieba.cut(line,cut_all=False)))
inputFile.close()
outputFile.close()

