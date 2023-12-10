'''
Simple Config Standard (Version: 2023DEC)

1. No blocks, One Config One Line: domain=apple.com //Notes added here will be ignored
2. All Space Will Be Ignored
3. "something" is not necessary, just something
4. Allowed Types: Int, Float(if . found), Str . Auto Detect.
5. Force string: "1241251", it will be a string
6. \/\/ if you want use // as text

Examples:
    domain=apple.com
    max_requests=5
    pi=3.1415926

How to Use:
    UserConfig("FilePath").read()  #return a dictionary
    UserConfig("FilePath").show() #print the config
    
'''

import sys

def isnum(str):
    try:
        float(str)
        return(True)
    except Exception as ex:
        return(False)
        
        
def ConfigFileFormatInit(array):
    res=[]
    for i in array:
        i=i.replace("\n","").replace(" ","")
        if i=="":
            pass
        res.append(i)
    return(res)

def ConfigParser(array):
    res={}
    for i in array:
        if "=" in i and "//" in i:
            part1=i[:i.find("=")]
            part2=i[:i.find("//")][i.find("=")+1:]
        elif "=" in i:
            part1=i[:i.find("=")]
            part2=i[i.find("=")+1:]
        else:
            continue
        if "\/\/" in part2:
            part2=part2.replace("\/\/","//")
        if part2.upper()=="TRUE":
            part2=True
        elif part2.upper()=="FALSE":
            part2=False
        elif isnum(part2)==True:
            if "." in part2:
                part2=float(part2)
            else:
                part2=int(part2)
        elif "\"" in part2[:1] and "\"" in part2[-1:]:
            part2=part2[1:-1]
        else:
            pass
        
        res[part1]=part2
    return(res)
    
            
    
class UserConfig():
    def __init__(self):
        self.version="2023DEC"
    def read(self, filepath):
        try:
            with open(filepath, "r") as f:
                filecontent=f.readlines()
            filecontent=ConfigFileFormatInit(filecontent)
            configs=ConfigParser(filecontent)
            return configs
            
        except Exception as ex:
            print(ex)
            sys.exit()
    def show(self, filepath):
        try:
            with open(filepath, "r") as f:
                filecontent=f.readlines()
            filecontent=ConfigFileFormatInit(filecontent)
            configs=ConfigParser(filecontent)
            print(configs)
            
        except Exception as ex:
            print(ex)
            sys.exit()