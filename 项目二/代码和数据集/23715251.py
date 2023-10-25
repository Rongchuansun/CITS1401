'''21/10/2022 Rongchuan Sun 23715251'''

'''This function is to get data from the file.'''
def getFileAll(csvfile):
    try:
        infile = open(csvfile,'r')
        data = infile.read()
        data_list = data.split("\n")
        dataF = []
        for da in data_list:
            dataF.append(da.split(","))
        headings = dataF[0]
        dataF.pop(0)
        infile.close()
        return dataF, headings
    except FileNotFoundError:
        print('The file',csvfile,'seems not exist.')
        return None
    except PermissionError:
        print('The file',csvfile,'cannot be opened.')
        return None    

'''This function is to get SubjID.'''
def get_titlenum(csvfile, option):
    infile = open(csvfile, 'r')
    title = infile.readline()
    titles = title.strip().split(",")
    for ti in titles:
        if ti == option:
            return titles.index(ti)


'''This function is to calculate asymmetry of landmark for SubjID.'''
def asymmetry(headings,data):
    value = ((float(data[headings.index('OX')])-float(data[headings.index('MX')]))**2 +
             (float(data[headings.index('OY')])-float(data[headings.index('MY')]))**2 +
             (float(data[headings.index('OZ')])-float(data[headings.index('MZ')]))**2)**0.5
    return round(value,4)

'''This function is to calculate asymmetry according to ID and landmark.'''
def asy(data,headings,ID,landmark):
    for da in data:
        if da == ['']:
            return 0
        if (ID in da) and (landmark in da):
            value = ((float(da[headings.index('OX')]) - float(da[headings.index('MX')]))**2
                    + (float(da[headings.index('OY')]) - float(da[headings.index('MY')]))**2
                    + (float(da[headings.index('OZ')]) - float(da[headings.index('MZ')]))**2)**0.5
            return value

'''This function is to calculate 3D_distance.'''            
def euclidean_dis(headings,data1,data2):
    value = ((float(data1[headings.index('OX')])-float(data2[headings.index('OX')]))**2
             +(float(data1[headings.index('OY')])-float(data2[headings.index('OY')]))**2
             +(float(data1[headings.index('OZ')])-float(data2[headings.index('OZ')]))**2)**0.5
    return round(value,4)

'''This function is to calculate similarity of both ID.'''
def similarity(A, B):
    numerator = 0
    V1 = list(A.values())
    V2 = list(B.values())
    for i in range(len(V1)):
        numerator += V1[i]*V2[i]
        
    sum1=0
    sum2=0
    for value in A.values():
        sum1 += value ** 2
    for value in B.values():
        sum2 += value ** 2
    
    result = numerator/((sum1**0.5)*(sum2**0.5))
    return round(result,4)


'''This function is to calculate OP1,OP2,OP3 and OP4.'''
def main(csvfile,SubjIDs):
    OP1 = []
    OP2 = []
    OP3 = []
    data, headings = getFileAll(csvfile)
    
    '''to get a list including all IDs in file.'''
    landmark = ['Ft','Ex', 'En', 'Al', 'Sbal', 'Ch', 'Prn']
    ID_list = []
    ID = headings.index('SubjID')
    for i in data:
        if i[ID] != '':
            ID_list.append(i[ID])
    ID_list = set(ID_list)
    
    '''to remove corrupted data in file.'''
    OX = headings.index('OX')
    OY = headings.index('OY')
    OZ = headings.index('OZ')
    MX = headings.index('MX')
    MY = headings.index('MY')
    MZ = headings.index('MZ')
    
    data2 = []
    for da in data:
        if (da != ['']) and ('' not in da):
            for i in [OX,OY,OZ,MX,MY,MZ]:
                if float(da[i]) > 200 or float(da[i]) < -200:
                    da[i] = ''
            data2.append(da)
    
    processed_da = []
    for da in data2:
        if (da != ['']) and ('' not in da):
            processed_da.append(da)
    
    '''to get IDs that have complete data and normal values.'''
    ID_value = []
    processed_ID = []
    for ID in ID_list:
        for da in processed_da:
            if da[headings.index('SubjID')] == ID:
                ID_value.append(da)
        if len(ID_value) == 7:
            processed_ID.append(ID)
        ID_value = []
        
    list1 = []
    list2 = []
    for i in data:
        if SubjIDs[0] in i:
            list1.append(i)
        elif SubjIDs[1] in i:
            list2.append(i)
    
    '''to calculate OP3.'''
    D5={}
    total_asy = 0
    for ID in processed_ID:
        for i in landmark:
            total_asy = total_asy + asy(processed_da, headings, ID, i)
        D5[ID] = round(total_asy, 4)
        total_asy = 0
    
    sort_D5 = sorted(D5.items(), key = lambda x:x[1])
    OP3 = sort_D5[:5]
    
    '''to get output according to judging SunjIDs.'''
    value_prn1 = asy(data, headings, SubjIDs, 'Prn')
    value_prn2 = asy(data, headings, SubjIDs, 'Prn')
    if SubjIDs[0] not in ID_list or SubjIDs[1] not in ID_list:
        OP1 = 'None'
        OP2 = 'None'
        OP3 = 'None'
        OP4 = 'None'
        print('This subject is not in the file.')
        return OP1,OP2,OP3,OP4
    else:
        if SubjIDs[0] not in processed_ID or SubjIDs[1] not in processed_ID:
            OP1 = 'None'
            OP2 = 'None'
            OP4 = 'None'
            print('This subject is corrupted.')
            return OP1, OP2, OP3, OP4
        else:
            if value_prn1 != 0 or value_prn2 != 0:
                OP1 = 'None'
                OP2 = 'None'
                OP4 = 'None'
                print('The facial asymmetry at nose tip is not zero.')
                return OP1, OP2, OP3, OP4
            else:
                '''to get OP1.'''
                D1 = {}
                D2 = {}
                if len(list1) == 7 and len(list2) == 7:
                    for i in list1:
                        if len(i) == 8:
                            if 'Ft' in i:
                                D1['FT'] = asymmetry(headings,i)
                            elif 'Ex' in i:
                                D1['EX'] = asymmetry(headings,i)
                            elif 'En' in i:
                                D1['EN'] = asymmetry(headings,i)
                            elif 'Al' in i:
                                D1['AL'] = asymmetry(headings,i)
                            elif 'Sbal' in i:
                                D1['SBAL'] = asymmetry(headings,i)
                            elif 'Ch' in i:
                                D1['CH'] = asymmetry(headings,i)
                    for i in list2:
                        if len(i) == 8:
                            if 'Ft' in i:
                                D2['FT'] = asymmetry(headings,i)
                            elif 'Ex' in i:
                                D2['EX'] = asymmetry(headings,i)
                            elif 'En' in i:
                                D2['EN'] = asymmetry(headings,i)
                            elif 'Al' in i:
                                D2['AL'] = asymmetry(headings,i)
                            elif 'Sbal' in i:
                                D2['SBAL'] = asymmetry(headings,i)
                            elif 'Ch' in i:
                                D2['CH'] = asymmetry(headings,i)
    
                if len(D1) == 6 and len(D2) == 6:
                   OP1.append(D1)
                   OP1.append(D2)
                
                '''to get OP2.'''
                for i in list1:
                    if 'Ex' in i:
                        Ex1 = i
                    elif 'En' in i:
                        En1 = i
                    elif 'Al' in i:
                        Al1 = i
                    elif 'Ft' in i:
                        Ft1 = i
                    elif 'Sbal' in i:
                        Sbal1 = i
                    elif 'Ch' in i:
                        Ch1 = i
    
                for i in list2:
                   if 'Ex' in i:
                      Ex2 = i
                   elif 'En' in i:
                      En2 = i
                   elif 'Al' in i:
                      Al2 = i
                   elif 'Ft' in i:
                      Ft2 = i
                   elif 'Sbal' in i:
                      Sbal2 = i
                   elif 'Ch' in i:
                      Ch2 = i
                
                D3 = {}
                D4 = {}
    
                D3['EXEN'] = euclidean_dis(headings,Ex1, En1)
                D3['ENAL'] = euclidean_dis(headings,En1, Al1)
                D3['ALEX'] = euclidean_dis(headings,Al1, Ex1)
                D3['FTSBAL'] = euclidean_dis(headings,Ft1, Sbal1)
                D3['SBALCH'] = euclidean_dis(headings,Sbal1, Ch1)
                D3['CHFT'] = euclidean_dis(headings,Ch1, Ft1)
    
                D4['EXEN'] = euclidean_dis(headings,Ex2, En2)
                D4['ENAL'] = euclidean_dis(headings,En2, Al2)
                D4['ALEX'] = euclidean_dis(headings,Al2, Ex2)
                D4['FTSBAL'] = euclidean_dis(headings,Ft2, Sbal2)
                D4['SBALCH'] = euclidean_dis(headings,Sbal2, Ch2)
                D4['CHFT'] = euclidean_dis(headings,Ch2, Ft2)
    
                OP2.append(D3)
                OP2.append(D4)
                
                '''to get OP4.'''
                OP4 = similarity(D3, D4)
                
                return OP1,OP2,OP3,OP4

