

# -*- coding: utf-8 -*-




def EncodeUnicode(text):
     res=""
     for i in text:
          if str(i.encode("unicode_escape"))[2:-1]==i:
               res=res+"00"+str(i.encode("unicode_escape").hex())
          else:
               res=res+str(i.encode("unicode_escape"))[5:-1]
     res=res.upper()
     return(res)

print(EncodeUnicode(input("Input: ")))