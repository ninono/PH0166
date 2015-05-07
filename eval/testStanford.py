from nltk.tokenize.stanford_segmenter import StanfordSegmenter
import codecs
segmenter = StanfordSegmenter(path_to_jar="./resources/stanford-segmenter-2014-10-26/stanford-segmenter-3.5.0.jar",path_to_sihan_corpora_dict="./resources/stanford-segmenter-2014-10-26/data", path_to_model="./resources/stanford-segmenter-2014-10-26/data/pku.gz", path_to_dict="./resources/stanford-segmenter-2014-10-26/data/dict-chris6.ser.gz",java_options="-mx2g")
inputFile=codecs.open('./test.gb','r','gb18030')
outputFile=codecs.open('./hyp.gb','w','gb18030')
for line in inputFile:
    result=segmenter.segment(line)
    outputFile.write(result)
inputFile.close()
outputFile.close()


