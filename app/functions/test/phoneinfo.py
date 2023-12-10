from phone import Phone #pip install phone
findphone  = Phone()

def phoneinfo(num):
    try:
        if num.isdigit()==True and 7<=len(num)<=11:
             num=str(num)
             j=findphone.find(num)
             if j==None:
                 return({"Error","No Info Found"})
             else:
                 res={"Success",j["province"]+j["city"]+" "+j["phone_type"]}
                 return(res)
        else:
             return({"Error","Not Digital or not in length from 7 to 11"})
    except Exception as ex:
            return({"Error",str(ex)})

print(phoneinfo(input("Num:")))