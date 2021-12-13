import re
import sys
global s
global idt
global var
sys.setrecursionlimit(10000) 
reserved = ['variable', 'call', 'print_ari']
idt = []
var = []

# def openfile(url):
#     with open(url, 'r') as f:
#         s = f.readlines()
#         s = list(map(lambda s: s.strip(), s))
#         s = ' '.join(s)
#         s = s.strip()
#     return s
# # s는 string 형태로 받았다.

def start(s):
    # ASCII 32 이하 문자는 모두 공백으로 치환한다.
    s_clean  = ''
    for i in range(len(s)):
        if ord(s[i])>32:
            s_clean += s[i]
        else:
            s_clean += ' '
    functions(s_clean)
    #print("Syntax O.K.\n")
    return 1

def functions(s):
    #print('functions')
    if s.count('{') == s.count('}'):
        # 함수가 여러개일 경우에
        if s.count('{') > 1:
            idx = s.find('}')
            function(s[:idx+1])
            functions(s[idx+1:].strip())
        # 함수가 하나다
        else:
            function(s)
    else:
        print("ERROR: 괄호 상응하지 않음\n")
    return 0

def function(s):
    #print('function{}'.format(s))
    # identifier 이름 get
    idx = s.find('{')
    funcName = (s[:idx]).strip()
    var_local = []
    # 함수 재정의 불가
    if funcName in idt:
        print("ERROR:  Duplicate declaration of the function name: {}".format(funcName))
        exit()
    # 함수명은 변수명과 같을 수 없다
    elif funcName in var:
        print("ERROR: Duplicate declaration of the identifier or the function name: {}".format(funcName))
        exit()
    # identifier 저장
    else:
        idt.append(funcName)   
    # function_body 넘기기
    idx_fin = s.find('}')
    newS = (s[idx+1:idx_fin]).strip()
    function_body(newS, var_local)

    return 0

def function_body(s, var_local):
    # variable 선언이 없다.
    if reserved[0] not in s:
        statements(s, var_local)
        print(1)
    # variable 선언이 있다.
    else:
        # 뒤에서부터 var 선언 찾기
        idx = s.rfind(reserved[0])
        idx_semi = s[idx+1:].find(';')
        var_definitions((s[:idx_semi+1]).strip(), var_local)
        statements((s[idx_semi+1]).strip(), var_local)
    return 0

def var_definitions(s, var_local):
    # reserver word variable 개수 세기
    num = s.count(reserved[0])
    if num == 1:
        var_definition(s, var_local)
    else:
        # get first semicolon
        idx = s.find(';')
        var_definition(s[:idx+1], var_local)
        var_definitions(s[idx+1:], var_local)
    return 0

def var_definition(s, var_local):
    # reserved word variable
    s = s.replace('variable ', '')
    # semicolon rightmost
    s = s[:-1]
    # to var_list
    var_list(s, var_local)
    return 0

def var_list(s, var_local):
    # var이 여러개인지.
    if ',' in s:
        idx = s.find(',')
        # 쉼표 뒤 문자열은 재귀
        var_list(s[idx+1:], var_local)
        # 쉼표 앞 문자열만 남긴다.
        s = s[:idx]
    # var이 하나거나, 쉼표앞 문자열일 경우.
    # indentifier(var)로 보낸다.
    identifier(s.strip(), var_local)
    return 0

def statements(s, var_local):
    num = s.count(';')
    if num == 1:
        statement(s, var_local)
    else:
        idx = s.find(';')
        statement(s[:idx+1], var_local)
        statements(s[idx+1:], var_local)
    return 0

def statement(s, var_local):
    # call
    if reserved[1] in s:
        return 0
    # print_ari
    elif reserved[2] in s:
        return 0
    else:
        identifier(s, var_local)
    return 0

def identifier(s, var_local):
    # varName 검증
    varName = s
    # 변수 재정의 불가
    if varName in var_local:
        print("WARNING: Duplicate declaration of the identifier: {}".format(varName))
        # 삭제하고 진행가능
    # 변수명은 함수명과 같을 수 없다
    elif varName in var:
        print("ERROR: Duplicate declaration of the identifier or the function name: {}".format(varName))
        exit()
    return 0