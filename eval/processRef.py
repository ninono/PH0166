import codecs
inputFile=codecs.open("dev-ref.gb",'r','gb18030')
outputFile=codecs.open('ref.gb','w','gb18030')
for line in inputFile:
    a=line.strip().split(' ');
    for ch in a:
        if len(ch)==1 and (not 0x4E00<=ord(ch)<=0x9FFF) and (not 0x3400<=ord(ch)<=0x4DFF) and (not 0x20000<=ord(ch)<=0x2A6DF) and (not 0xF900<=ord(ch)<=0xFAFF ) and (not 0x2F800<=ord(ch)<=0x2FA1F):
            a.remove(ch)
    outputFile.write(' '.join(a)+'\n')
inputFile.close()
outputFile.close()

