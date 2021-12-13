import checker.grm_checker as grm
import checker.executer as exc
import argparse

def openfile_grm(url):
    with open(url, 'r') as f:
        s = f.readlines()
        s = list(map(lambda s: s.strip(), s))
        s = ' '.join(s)
        s = s.strip()
    return s
# s는 string 형태로 받았다.

def openfile_exc(url):
    with open(url, 'r') as f:
        s = f.readlines()
        s = list(map(lambda s: s.strip(), s))
        s = ' '.join(s)
        s = s.split('}')
        s = list(filter(None, s))
    func = {}
    for i in s:
        temp = i.split('{')
        temp = list(map(lambda temp: temp.strip(), temp))
        func[temp[0]] = temp[1]
    return s, func
# s는 list로 받은 것, func는 dict 형태로 순서대로 넣은 것

# main은 하나, 없으면 오류메세지, 종료
if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('txtfile', help="location of txtfile")
    args = parser.parse_args()

    s_grm = openfile_grm(args.txtfile)
    if grm.start(s_grm):
        print("Syntax O.K.\n")
        s_exc, func_exc = openfile_exc(args.txtfile)
        exc.interpreter(func_exc)
    else:
        print("Syntax ERROR\n")
else:
    print("No starting function.")
