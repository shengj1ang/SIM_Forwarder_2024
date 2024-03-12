def trim_spaces_in_bytes(input_bytes):
    """
    Trims spaces from the beginning and end of each line in the given bytes object.

    :param input_bytes: A bytes object potentially with spaces at the start and end of its lines.
    :return: A new bytes object with spaces removed from the start and end of each line.
    """
    # Split the bytes into lines, trim each line, and then join them back into a single bytes object
    #return b'\n'.join(line.strip()+bytes(f"/*{random.randint(100000000,999999999)}*/","utf-8") for line in input_bytes.splitlines())
    return b'\n'.join(line.strip() for line in input_bytes.splitlines())

def isnum(str):
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

def DecodeUnicode(str):
    i=0
    res=""
    if len(str)%4==0 and len(str)>6: #unicode需要可以被4整除
        if str.upper()==str: #全是大写字母才算短信的unicode，而且不能是纯数字
             while i<len(str)/4:
                 res=res+"\\u"+str[4*i:4*i+4].lower()
                 i+=1
             try:    
                 res=res.encode('utf-8').decode('unicode_escape')
                 return(res)
             except:
                 return(str)
        else:
             return(str)
    else:
        return(str)
   
def EncodeUnicode(text):
     res=""
     for i in text:
          if str(i.encode("unicode_escape"))[2:-1]==i:
               res=res+"00"+str(i.encode("unicode_escape").hex())
          else:
               res=res+str(i.encode("unicode_escape"))[5:-1]
     res=res.upper()
     return(res)
