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
