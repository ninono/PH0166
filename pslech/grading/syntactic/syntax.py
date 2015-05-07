#-*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import sys
import pdb
class SyntaxError:
    def __init__(self,context,contextoffset,errorlength,msg):
        self.context=context
        self.contextoffset=contextoffset
        self.errorlength=errorlength
        self.msg=msg
def syntacticCheck(txt):
    r=requests.post("http://localhost:8081",data={"language":"zh-CN","text":txt})
    res_xml=r.content
    root = ET.fromstring(res_xml)
    res={"n_error":len(root.findall('error')),"errors":[]}
    for ele in root.findall('error'):
        attr=ele.attrib
        res["errors"].append(SyntaxError(attr['context'],attr['contextoffset'],attr['errorlength'],attr['msg']).__dict__)
    return res


if __name__=="__main__":
    print syntacticCheck(sys.argv[1])


