import os

square=[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961, 1024, 1089, 1156, 1225, 1296, 1369, 1444, 1521, 1600, 1681, 1764, 1849, 1936, 2025, 2116, 2209, 2304, 2401, 2500, 2601, 2704, 2809, 2916, 3025, 3136, 3249, 3364, 3481, 3600, 3721, 3844, 3969, 4096, 4225, 4356, 4489, 4624, 4761, 4900, 5041, 5184, 5329, 5476, 5625, 5776, 5929, 6084, 6241, 6400, 6561, 6724, 6889, 7056, 7225, 7396, 7569, 7744, 7921, 8100, 8281, 8464, 8649, 8836, 9025, 9216, 9409, 9604, 9801, 10000]
#0-100

prime=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
#100 primes

def tryfit(thing,size):
    stronk = str(thing)

    if len(stronk)>size:
        return stronk

    elif len(stronk)<size:
        return " "*(2-len(stronk))+stronk

    return stronk

def forcefit(thing,size,pos="l"):
    stronk = str(thing)

    if len(stronk)>size:
        if pos=="l":
            return stronk[:size]
        else:
            return stronk[-1-size:]

    if pos=="l":
        return " "*(size-len(stronk))+stronk
    else:
        return stronk+(" "*(size-len(stronk)))

def simp(nums,returnFactor=False):
    index=0
    cops=[nums[0],num[1]]
    factor=1
    while index!=100:
        p=prime[index]
        if cops[0]%p==0 and cops[1]%p==0:
            cops=[cops[0]/p,cops[1]/p]
            index=-1
            if returnFactor:
                factor*=p
        index+=1

    out=[int(c) for c in cops]

    if returnFactor:
        out.append(factor)

    return out

def filePrint(text,file="output.txt"):
    path=os.getcwd()+"/"+str(file)
    try:
        open(path,"x").close()
    except:
        pass
    with open(path,"a") as fl:
        if type(text) == list:
            fl.write("\n"+", ".join([str(e) for e in text]))
        else:
            fl.write("\n"+str(text))
        fl.close()

def digDex(thing,path):
    if type(thing) == string or len(path)==0:
        return thing
    try:
        return digDex(thing[path[0]],path[1:])
    except:
        return thing

def mapl(lst,depth=False):
    out = []
    deep = 0
    if type(lst)!=list:
        return lst
    for item in lst:
        if type(item)==list:
            ret = mapl(item,depth=depth)
            if depth:
                out.append(ret[0])
                deep+=ret[1]
            else:
                out.append(ret)
        else:
            deep = 1
            out.append(item)

    if depth:
        return [out,deep]

    return out

def stripe(tol):#turn tuple/list from ?a,b,c? to a,b,class
    return str(tol)[1:-1]

def absol(num):
    return (num*num)**.5

def between2d(point,mn,mx):
    return mn[0]<point[0]<mx[0] and mn[1]<point[1]<mx[1]
