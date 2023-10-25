'''18/09/2022 Rongchuan Sun 23715251'''

'''These functions defined below is to get OP1, OP2, OP3 and OP4'''
'''This function is to filter data by adultID'''
def getFile(csvfile, adultID):
    infile = open(csvfile,'r')
    data = infile.read()
    data_list = data.split("\n")
    x = []
    for line in data_list:
        temp = line.split(",")
        if temp[0] == adultID:
            x.append(temp) 
    infile.close()
    return x

'''This function is to filter  GDis and LDis by distance''' 
def getGDis_LDis(data, distance) :
    GDis = []
    LDis = []
    for i in data :
        if distance == i[2] :
            GDis.append(round(float(i[3]), 4))
            LDis.append(round(float(i[4]), 4))
    return [GDis,LDis]

'''This function is to calculate difference between
GDis and LDis by expression and distance'''
def getdif(data, distance, expression):
    for i in data:
        if i[1] == expression and int(i[2]) == distance:
            return round(float(i[3])-float(i[4]),4)

'''This function is to get GDis by expression and distance'''
def getGDis(data, distance, expression):
    for i in data:
        if i[1] == expression and int(i[2]) == distance:
            return float(i[3])

'''This function is to calculate average by same distance and difference expression'''
def avg(list) :
    result = sum(list) / len(list)
    return round(result, 4)

'''This function is to get LDis by distance'''
def getLDis(data, distance) :
    LDis = []
    for i in data :
        if int(i[2]) == distance :
            LDis.append(float(i[4]))
    return LDis

'''This function is calculate deviation'''
def deviation(Value) :
    sumX = 0
    valueAverage=avg(Value)
    for i in Value:
        sumX = sumX + (i - valueAverage) ** 2
    return (sumX/len(Value)) ** 0.5


'''These functions defined below is to get ID and cossim'''
'''This function is to convert original file to list'''
def list_file(csvfile):
    infile = open(csvfile, 'r')
    data = infile.read()
    list_data = data.split("\n")
    list_File = []
    for line in list_data:
        if line != '':
           temp = line.split(",")
           list_File.append(temp)
    infile.close()
    list_File.pop(0)
    return list_File
                
'''This function defined below is to get distance by sorting by distance'''
def GDis_sorted(data, ID, expression):
    list_data = []
    for line in data:
        if line[0] == ID and line[1] == expression:
            list_data.append(line)
    list_sorted = sorted(list_data, key=(lambda x:x[2]))
    GDis = []
    for line in list_sorted:
        GDis.append(line[3])
  
    return GDis

'''to replace zero and negative number in GDis by 50'''
def replace(data):
    for line in data:
        if line[3] <= '0':
            line[3] = '50'
            
    return data

'''to calculate similarity'''
def similarity(A, B):
    numerator = 0.0
    denominator1 = 0.0
    denominator2 = 0.0
    
    for i in range(len(A)):
        numerator = numerator + float(A[i]) * float(B[i])
        denominator1 = denominator1 + float(A[i]) ** 2
        denominator2 = denominator2 + float(B[i]) ** 2
    result = numerator / ((denominator1 ** 0.5) * (denominator2 ** 0.5))
    
    return round(result, 4)
    
            
def main(csvfile, adultID, option):
    if option == "stats":
        a = getFile(csvfile, adultID)
           
        OP1 = []
        for i in range(1, 9) :
            TheList = []
            TheList.append(min(getGDis_LDis(a, str(i))[0]))
            TheList.append(max(getGDis_LDis(a, str(i))[0]))
            TheList.append(min(getGDis_LDis(a, str(i))[1]))
            TheList.append(max(getGDis_LDis(a, str(i))[1])) 
            OP1.append(TheList)
               
        OP2 = []
        dataDif = []
        for i in range(1, 9) :
            dataDif.append(getdif(a, i, 'Neutral'))
        OP2.append(dataDif)
        dataDif = []
        for i in range(1, 9) :
            dataDif.append(getdif(a, i, 'Angry'))
        OP2.append(dataDif)
        dataDif = []
        for i in range(1, 9) :
            dataDif.append(getdif(a, i, 'Disgust'))
        OP2.append(dataDif)
        dataDif = []
        for i in range(1, 9) :
            dataDif.append(getdif(a, i, 'Happy'))
        OP2.append(dataDif)
           
    
        OP3 = []
        for i in range(1, 9) :
            dataG = []
            dataG.append(getGDis(a, i, 'Neutral'))
            dataG.append(getGDis(a, i, 'Angry'))
            dataG.append(getGDis(a, i, 'Disgust'))
            dataG.append(getGDis(a, i, 'Happy'))
            OP3.append(avg(dataG))
           
           
        OP4 = []
        for i in range(1, 9) :
            ListLD = getLDis(a, i)
            OP4.append(round(deviation(ListLD), 4))
           
        return OP1, OP2, OP3, OP4
    
    elif option == 'FR':
        '''to process original file'''
        list_File = list_file(csvfile)
        
        '''to replace zero or negative number by 50 in file'''
        list_File = replace(list_File)
        
        '''to get ID and remove duplicates'''
        ID_list = []
        for line in list_File:
            ID_list.append(line[0])
        ID_list = set(ID_list)
        ID_list = list(ID_list)
        
        '''to get GDis of adultID in four expressions'''
        adult_GDN = GDis_sorted(list_File, adultID, 'Neutral')
        adult_GDA = GDis_sorted(list_File, adultID, 'Angry')
        adult_GDD = GDis_sorted(list_File, adultID, 'Disgust')
        adult_GDH = GDis_sorted(list_File, adultID, 'Happy')
        
        '''to get ID from others'''
        ID_others = []
        for line in ID_list:
            if line != adultID:
                ID_others.append(line)
        
        '''to calculate maximum similarity between adultID and others by Neutral'''
        max_others = 0
        i = 0
        for line in ID_others:
            others_GDN = GDis_sorted(list_File, line, 'Neutral')
            result = similarity(adult_GDN, others_GDN)
            if result > max_others:
                max_others = result
                real_i = i
            i += 1
        
        '''to get maximum similarity between Neutral and other expressions of adultID'''
        list_adultID = []
        list_adultID.append(similarity(adult_GDN, adult_GDA))
        list_adultID.append(similarity(adult_GDN, adult_GDD))
        list_adultID.append(similarity(adult_GDN, adult_GDH))
        max_adultID = max(list_adultID)
        
        '''to compare these two maximum values'''
        if max_others > max_adultID:
            cossim = max_others
            ID = ID_others[real_i]
            return ID, cossim
        
        elif max_others < max_adultID:
            cossim = max_adultID
            ID = adultID
            return ID, cossim
        
        else:
            ID = adultID + " " + ID_others[real_i]
            cossim = max_others
            return ID, cossim
           
    else:
        ID = ""
        cossim = 0
        return ID, cossim
    
                
    
    