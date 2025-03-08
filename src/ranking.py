from constants import sortByFreq

def findURL(docID):
    with open("DictJsonFolder/final_dict.txt") as w:
        while True:
            line = w.readline()
            if not line:
                break
            doc = line.split('|')[0]
            if doc == docID:
                return line.split('|')[1][:line.split('|')[1].find('\n')]


def computeTF_IDFscore(intersection_list, index, idf_list):
    # tf given in index
    # get idf score from final index
    # multiply
    # returns top 5
    mydict = {}
    for i in intersection_list:
        sum = 0
        for key in index.keys():
            tf_idf_score = round(index[key][i] * idf_list[key],5)
            sum += tf_idf_score
        mydict[i] = sum
    sortedDict = sortByFreq(mydict)
    count = 0
    top_five = []
    for key,value in sortedDict.items():
        if count == 5:
            break
        top_five.append((key, value))
        count += 1
    # print(top_five)
    return top_five



