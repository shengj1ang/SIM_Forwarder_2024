import re

def trim_spaces_in_bytes(input_bytes):
    """
    Trims spaces from the beginning and end of each line in the given bytes object.

    :param input_bytes: A bytes object potentially with spaces at the start and end of its lines.
    :return: A new bytes object with spaces removed from the start and end of each line.
    """
    # Split the bytes into lines, trim each line, and then join them back into a single bytes object
    #return b'\n'.join(line.strip()+bytes(f"/*{random.randint(100000000,999999999)}*/","utf-8") for line in input_bytes.splitlines())
    return b'\n'.join(line.strip() for line in input_bytes.splitlines())

def isNum(str):
    try:
        float(str)
        return True
    except Exception as e:
        return False

def inEnglish(text):
    en_uni=(
            "0","1","2","3","4","5","6","7","8","9",       
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
            " ","!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/",
            ":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~"
            )
    for i in text or "\n"in text:
        if i in en_uni:
            pass
        else:
            return False
    return True

def DecodeUnicode(text=""):
    i=0
    res=""
    if len(text)%4==0 and len(text)>4: #unicode需要可以被4整除
        if text.upper()==text: #全是大写字母才算短信的unicode，而且不能是纯数字
            while i<len(text)/4:
                res=res+"\\u"+text[4*i:4*i+4].lower()
                i+=1
            try:    
                res=res.encode('utf-8').decode('unicode_escape')
                return(res)
            except Exception as e:
                # print(f"An error in functions/unicode.py=>DecodeUnicode: {e}, input text: {text}") # Too much error may meet here.
                return(text)
        else:
            print(f"An error in functions/unicode.py=>DecodeUnicode: The input text does not meet the requirement, text.upper()==text, input text: {text}")
            return(text)
    else:
        print(f"An error in functions/unicode.py=>DecodeUnicode: The input text does not meet the requirement, len(text)%4==0 and len(text)>4, input text: {text}")
        return(text)


def DecodeUnicodePhonenumber(text=""):
    i=0
    res=""
    if len(text)%4==0 and len(text)>4: #unicode需要可以被4整除
        if text.upper()==text: #全是大写字母才算短信的unicode，而且不能是纯数字
            while i<len(text)/4:
                res=res+"\\u"+text[4*i:4*i+4].lower()
                i+=1
            try:    
                res=res.encode('utf-8').decode('unicode_escape')
                if isNum(res):
                    return(res)
                else:
                    return text
            except Exception as e:
                #print(f"An error in functions/unicode.py=>DecodeUnicodePhonenumber: {e}, input text: {text}") # Too much error may meet here.
                return(text)
        else:
            #print(f"An error in functions/unicode.py=>DecodeUnicodePhonenumber: The input text does not meet the requirement, text.upper()==text, input text: {text}")
            return(text)
    else:
        #print(f"An error in functions/unicode.py=>DecodeUnicodePhonenumber: The input text does not meet the requirement, len(text)%4==0 and len(text)>4, input text: {text}")
        return(text)
   

def EncodeUnicode(text=""):
    res=""
    for i in text:
        if str(i.encode("unicode_escape"))[2:-1]==i:
            res=res+"00"+str(i.encode("unicode_escape").hex())
        else:
            res=res+str(i.encode("unicode_escape"))[5:-1]
    res=res.upper()
    return(res)

def RemoveTextThatProducesUnexpectedConsequence(text=""):
    text_list=("verify code","verify")
    for i in text_list:
        text=text.replace(i,"")
    text=re.sub(r'【[^】]*】', '', text, count=1) # 移除第一个【】之间的文字，避免【4399】这种
    return text


def find_verification_code(text=""):
    try:
        lower_text = text.lower()
        if 'verif' in lower_text or '验证' in lower_text or 'code' in lower_text:
            pattern = r'\d{4,6}'
            # pattern = r'\b[a-zA-Z0-9]{4,6}\b'
            # Looking for 4 to 6 digits
            # pattern = r'\b\d{4,6}\b'
            match = re.search(pattern, RemoveTextThatProducesUnexpectedConsequence(lower_text))
            if match:
                return {"res": True, "content": match.group()}
            else:
                return {"res": False, "content": ""}
        else:
            return {"res": False, "content": ""}
    except Exception as e:
        return {"res": False, "content": f"Exception Caught in find_verification_code: {e}"}


'''
from bs4 import BeautifulSoup
import html       
def html_escape(text):
    """
    Escapes all characters in the text to their corresponding HTML entities.
    """
    return ''.join(f'&#{ord(char)};' for char in text)
'''