import re

filename = 'res.txt'

patternx = re.compile(r'x_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patterny = re.compile(r' y_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patternxk = re.compile(r'x_k_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patternyk = re.compile(r' y_k_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')

patternxlinear = re.compile(r'xlinear\w+ = 0(x|b)(\d+|\w+)')
patternylinear = re.compile(r'ylinear\w+ = 0(x|b)(\d+|\w+)')
patternxhead = re.compile(r'xhead_\d+_\w+ = 0(x|b)(\d+|\w+)')
patternyhead = re.compile(r'yhead_\d+_\w+ = 0(x|b)(\d+|\w+)')
patternxor = re.compile(r'XOR_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patternpr = re.compile(r'XOR_key_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patternr = re.compile(r'ROUNDFUNC_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')
patternc = re.compile(r'COPY_\d+_(\d+|-\d+) = 0(x|b)(\d+|\w+)')

xlist = []
ylist = []
xklist = []
yklist = []
xlinearlist = []
ylinearlist = []
xheadlist = []
yheadlist = []
xorlist = []
prlist = []
rlist = []
clist = []


with open(filename, 'r', encoding='utf-8') as f:
    text = f.readlines()
    for line in text:
        #line = re.sub(r'h', '-', line)
        x = patternx.search(line)
        y = patterny.search(line)
        xk = patternxk.search(line)
        yk = patternyk.search(line)
        xlinear = patternxlinear.search(line)
        ylinear = patternylinear.search(line)
        xhead = patternxhead.search(line)
        yhead = patternyhead.search(line)
        xor = patternxor.search(line)
        pr = patternpr.search(line)
        roundfunc = patternr.search(line)
        copy = patternc.search(line)
        if x:
            xlist.append(x.group())
        if y:
            ylist.append(y.group())
        if xk:
            xklist.append(xk.group())
        if yk:
            yklist.append(yk.group())

        if xlinear:
            xlinearlist.append(xlinear.group())
        if ylinear:
            ylinearlist.append(ylinear.group())
        if xhead:
            xheadlist.append(xhead.group())
        if yhead:
            yheadlist.append(yhead.group())
        if xor:
            xorlist.append(xor.group())
        if pr:
            prlist.append(pr.group())
        if roundfunc:
            rlist.append(roundfunc.group())
        if copy:
            clist.append(copy.group())


sorted_xlist = sorted(xlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_xlist,'\n')

sorted_ylist = sorted(ylist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_ylist,'\n')

sorted_xklist = sorted(xklist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
print(sorted_xklist,'\n')

sorted_yklist = sorted(yklist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
print(sorted_yklist,'\n')

sorted_xheadlist = sorted(xheadlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_xheadlist,'\n')

sorted_yheadlist = sorted(yheadlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_yheadlist,'\n')

sorted_xlinearlist = sorted(xlinearlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_xlinearlist,'\n')

sorted_ylinearlist = sorted(ylinearlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_ylinearlist,'\n')

sorted_xorlist = sorted(xorlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
print(sorted_xorlist,'\n')

sorted_prlist = sorted(prlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
#print(sorted_prlist,'\n')

sorted_rlist = sorted(rlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
print(sorted_rlist,'\n')

sorted_clist = sorted(clist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
#print(sorted_clist,'\n')


