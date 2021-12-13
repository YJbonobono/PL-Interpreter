import re
global s
global ARIstack
rsv = ['variable', 'call', 'print_ari']
ARIstack = []
funcstack = []

def interpreter(func):
    # 메인함수부터 시작
    s = func['main']
    funcstack.append('main')
    slist = s.split(';')
    slist = list(filter(None, slist))
    i = 0
    for sentence in slist:
        ss = sentence.strip()
        if rsv[0] in ss:  # variable
            snew = (ss[8:]).strip()
            if ',' not in snew:
                ARIstack.append(['main', snew.strip(), i])
                i+=1
            else:
                newlist = snew.split(',')
                for k in range(snew.count(',')+1):
                    ARIstack.append(['main', 'Local variable', (newlist[k]).strip(), i])
                    i+=1
        elif rsv[1] in ss: # call
            newName = (ss[4:]).strip()
            callFunc('main', newName, func)
        elif rsv[2] in ss:
            printAri()
        else:
            for i in range(len(ARIstack)):
                if ARIstack[i][2] == ss:
                    link_count = abs(funcstack.index('main')-funcstack.index(ARIstack[i][0]))
                    print('{}:{} => {}, {}\n'.format('main', ss, link_count, ARIstack[i][3]))
                    break
    return 0

def callFunc(orname, funcName, func):
    local_var = []
    s = func[funcName]
    funcstack.append(funcName)
    slist = s.split(';')
    slist = list(filter(None, slist))
    i = 0
    ARIstack.append([funcName, 'Return Address', orname, i])
    i+=1
    ARIstack.append([funcName, 'Dynamic Link', i])
    i+=1
    for sentence in slist:
        ss = sentence.strip()
        if rsv[0] in ss:  # variable
            snew = (ss[8:]).strip()
            if ',' not in snew:
                ARIstack.append([funcName, snew.strip(), i])
                i+=1
            else:
                newlist = snew.split(',')
                for k in range(snew.count(',')+1):
                    ARIstack.append([funcName, 'Local variable', (newlist[k]).strip(), i])
                    i+=1
        elif rsv[1] in ss: # call
            newName = (ss[4:]).strip()
            callFunc(funcName, newName, func)
        elif rsv[2] in ss:
            printAri()
        else:
            for i in range(len(ARIstack)):
                if ARIstack[i][2] == ss:
                    link_count = abs(funcstack.index(funcName)-funcstack.index(ARIstack[i][0]))
                    print('{}:{} => {}, {}\n'.format(funcName, ss, link_count, ARIstack[i][3]))
                    break
    return 0

def printAri():
    tmp = -1
    for i in range(len(ARIstack)-1, -1, -1):
        if tmp != ARIstack[i][0]:
            print('{}:'.format(ARIstack[i][0]), end='')
            tmp = ARIstack[i][0]
        if ARIstack[i][1]== 'Return Address':
            print('\t{}: {}:1'.format(ARIstack[i][1], ARIstack[i][2]))
        else:
            print('\t{}: {}'.format(ARIstack[i][1], ARIstack[i][2]))
    print("")
    return 0
