# -*- coding: utf-8 -*-

#example="6211723153174EAC59295B8995E8"
example="00310039003300320037003500330039003400350039"
decode=""
i=0
res=""
while i<len(example)/4:
     res=res+"\\u"+example[4*i:4*i+4].lower()
     i+=1
res=res.encode('utf-8').decode('unicode_escape')
print(res)