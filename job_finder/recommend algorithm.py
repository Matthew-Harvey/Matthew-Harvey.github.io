import re
import random
import sqlite3 as sql


def mean(arr, postition):
    __all = 0
    for a in arr:
        __all = __all + float(a[postition])
    return __all / len(arr)
    
def sd(arr, postition, mean):
    __all = 0
    for b in arr:
        __all = __all + (float(b[postition]) - mean)**2
    return (__all / len(arr))**0.5

def algorithhm(array, idealcorrelation):
    handle = sql.connect("RecommendDATA.db")
    cursor = handle.cursor()
    allratings = []
    for x in range(0, 315):
        cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (x, 0))
        rating = cursor.fetchall()
        if rating == []:
            allratings.append(3)
        else:
            for rate in rating:
                rate = re.sub('[^0-9]', '', str(rate))
                allratings.append(rate)
    length = len(allratings)
    handle.commit()
    allratings = re.sub('[^0-9]', '', str(allratings))
    total = 0
    for rate in allratings:
        total = total + int(rate)
    MeanRating = total / length

    cursor.execute("SELECT COUNT FROM JOBS")
    allcount = cursor.fetchall()
    length = len(allcount)
    handle.commit()
    handle.close()
    allcounts = 0
    for count in allcount:
        count = str(count)
        count = count[1:len(count)-2]
        if count == "'.'":
            count = 0
        count = int(count)
        allcounts = allcounts + count
    MeanViews = allcounts / length

    info = []
    weight_arr = []
    weight_arr2 = []
    for jobname in array:
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+jobname+"%", 0))
        jobid = cursor.fetchall()
        try:
            jobid = str(jobid)
            jobid = jobid[2:len(jobid)-3]
            jobid = int(jobid)
            handle.commit()
        except:
            jobid = jobid.split(",")
            allids = []
            if len(jobid) >= 3:
                count = 0
                odds = [1, 3, 5, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
                for ids in jobid:
                    ids = str(ids)
                    if count not in odds:
                        cont = True
                    else:
                        if ids == " (256":
                            jobid.remove(jobid[count-1])
                        else:
                            jobid.remove(jobid[count])
                    count += 1
            for ids in jobid:
                ids = re.sub('[^0-9]', '', str(ids))
                allids.append(ids)
            lens = []
            lens_sort = []
            for ids in allids:
                cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND IDLE = ?", (int(ids), 0))
                name = cursor.fetchall()
                name = str(name)
                len1 = len(name) - len(jobname)
                lens.append(len1)
                lens_sort.append(len1)
            lens_sort.sort()
            for p in range(0, len(lens_sort)):
                if lens_sort[p] < 0:
                    lens_sort[p] = lens_sort[p] - lens_sort[p] - lens_sort[p]
            for p in range(0, len(lens)):
                if lens[p] < 0:
                    lens[p] = lens[p] - lens[p] - lens[p]                
            for i in range(0, len(lens)):
                if lens_sort[0] == lens[i]:
                    position = i
            jobid = allids[position]

        cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (jobid, 0))
        ratings = cursor.fetchall()
        handle.commit()
        total = 0
        ratings = re.sub('[^0-9]', '', str(ratings))
        if ratings == " ":
            total = 1
        elif ratings == "":
            total = 1
        else:
            for rate in ratings:
                total = total + int(rate)
        try:
            Rating = total / len(ratings)
        except:
            Rating = 3
            
        cursor.execute("SELECT COUNT FROM JOBS WHERE JOBID = ? AND JOBID > ?", (jobid, 0))
        amount = cursor.fetchall()
        handle.commit()
        handle.close()
        amount = re.sub('[^0-9]', '', str(amount))
        if amount == "":
            amount = 0
        Views = int(amount)
        
        m = MeanViews
        v = Views
        R = MeanRating
        C = Rating
        try:
            weight1 = (v/m)*(R/v)
            weight2 = (v/R)*(C/m)
        except:
            weight1 = (v+m)*(R+v)-25
            weight2 = (v+R)*(C+m)-25
        weight = weight1 + weight2 + (random.random()*2)
        weight_arr.append(weight)
        weight_arr2.append(weight)
        arr = [weight, jobid, jobname]
        info.append(arr)
        
    #when weighted is identical integer, use total pythag distance for central nodes into a top 6
    for u in range(0, len(info)):
        xval = info[u][0]
        yval = info[u][1]
        _all = 0
        for v in range(0, len(info)):
            xval2 = info[v][0]
            yval2 = info[v][1]
            changey = float(yval) - float(yval2)
            changex = float(xval) - float(xval2)
            result = ((changex**2)+(changey**2))**0.5
            _all = _all + result
        info[u].append(_all)

 
    #cut down info list into top 20
    if len(info) > 20:
        info2 = []
        weights2 = []
        weight_arr2.sort()
        cut = weight_arr2[len(weight_arr2)-21]
        for arr in info:
            if cut < arr[0]:
                info2.append(arr)
        info = info2

    def combinations(array, tuple_length, prev_array=[]):
        if len(prev_array) == tuple_length:
            return [prev_array]
        combs = []
        for i, val in enumerate(array):
            prev_array_extended = prev_array.copy()
            prev_array_extended.append(val)
            combs += combinations(array[i+1:], tuple_length, prev_array_extended)
        return combs

    if len(info) < 7:
        n = len(info)
    else:
        n = 7
    _all = []
    _all2 = []
    tests = []
    while n > 1:
        hold = -11
        test = combinations(info, n)

        meanx = mean(info, 0)
        meany = mean(info, 1)
        meanz = mean(info, 3)
        sdx = sd(info, 0, meanx)
        sdy = sd(info, 1, meany)
        sdz = sd(info, 3, meanz)

        allcorelations = []
        for j in range(0, len(test)):
            totalx = 0
            totaly = 0
            totalz = 0
            totalxyz = 0
            totalx2 = 0
            totaly2 = 0
            totalz2 = 0
            for k in range(0, len(test[j])):
                xcord = float(test[j][k][0])
                ycord = float(test[j][k][1])
                zcord = float(test[j][k][3])
                totalx = totalx + xcord
                totaly = totaly + ycord
                totalz = totalz + zcord
                totalxyz = totalxyz + (ycord*xcord*zcord)
                totalx2 = totalx2 + (xcord**2)
                totaly2 = totaly2 + (ycord**2)
                totalz2 = totalz2 + (zcord**2)
            numerator = (len(test[j])*totalxyz)-(totalx*totaly*totalz)
            denominator = ((len(test[j])*totalx2)*(len(test[j])*totaly2)*(len(test[j])*totalz2))**0.5
            r = numerator / denominator
            if r < 0:
                r = 0 - r
            if hold < r:
                hold = r
            test[j].append(r)
            allcorelations.append(r)
        _all.append(allcorelations)
        _all2.append(hold)
        tests.append(test)
        n = n-1

    maximum = -2
    count = 0
    hold = 0
    for corelation in _all2:
        if corelation > maximum:
            maximum = corelation
            hold = count
        count = count +1 
    saved_data = ""
    for g in range(0, len(tests[hold])):
        for data in tests[hold][g]:
            if data == maximum:
                saved_data = tests[hold][g]
    saved_data.remove(saved_data[len(saved_data)-1])

    eucleans = []
    for array in saved_data:
        eucleans.append(array[3])
    eucleans.sort()
    x = 1
    allnames = []
    for x in range(0, len(eucleans)):
        for array in saved_data:
            if eucleans[x] == array[3]:
                allnames.append(array[2])

    return allnames
    