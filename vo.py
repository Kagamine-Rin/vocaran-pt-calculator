from bs4 import BeautifulSoup
import urllib.request
import datetime
import sys


def tonum(s):
    b = 0
    for a in s:
        if a.isdigit():
            b = b * 10 + int(a)
    return b


def getint(a):
    ans = ''
    sostr = str(a)
    for ch in sostr:
        if ch == '.':
            break
        else:
            ans = ans + ch
    return str(ans)


def getint2(a):
    ans = ''
    fl1 = False
    fl2 = 0
    sostr = str(a)
    for ch in sostr:
        if ch == '.':
            fl1 = True
        elif not fl1:
            ans = ans + ch
        elif fl1 and fl2 == 0:
            ans = ans + '.' + ch
            fl2 = 1
        elif fl1 and fl2 == 1:
            ans = ans + ch
            break
    return ans


def getVdata(smnum):
    url = "http://ext.nicovideo.jp/thumb/sm" + str(smnum)
    then = [0, 1, 1]
    noww = datetime.datetime.now()
    now = [noww.year - 2000, noww.month, noww.day]
    if noww.hour == 23:
        now[2] += 1
    try:
        data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(data, "html.parser")
        a = soup.find_all('strong')
        nowdata = [tonum(str(x)) for x in a[0:3]]
        u = str(a[4])
        then = [int(u[8:10]), int(u[11:13]), int(u[14:16])]
    except urllib.error.HTTPError:
        nowdata = [0, 0, 0]
    url2 = 'http://vocaran.jpn.org/movie/sm' + str(smnum)
    try:
        data2 = urllib.request.urlopen(url2).read()
        soup2 = BeautifulSoup(data2, "html.parser")
        kkk = soup2.find_all('li')[11]
        kk = str(kkk)
        if 'strong' not in kk:
            kkk = soup2.find_all('li')[10]
            kk = str(kkk)
        soup3 = BeautifulSoup(kk, "html.parser")
        temp = soup3.find_all('strong')
        lastdata = [tonum(str(x)) for x in temp]
    except urllib.error.HTTPError:
        print('warning: This song has never entered the vocaran.')
        print('data may not be correct.')
        lastdata = [0, 0, 0]
    except IndexError:
        print('error: This song has only entered the vocaran ED.')
        print("error: unable to read last week's data.")
        quit()
    ddays = 33
    if now[0] == then[0] and now[1] == then[1]:
        ddays = now[2] - then[2]
    elif now[0] == then[0] and now[1] - then[1] == 1:
        if then[1] in [1, 3, 5, 7, 8, 10, 12]:
            ddays = 31 - then[2] + now[2]
        elif then[1] == 2:
            if now[0] % 4 == 0:
                ddays = 29 - then[2] + now[2]
            else:
                ddays = 28 - then[2] + now[2]
        else:
            ddays = 30 - then[2] + now[2]
    elif now[0] - then[0] == 1 and now[1] == 1 and then[1] == 12:
        ddays = 31 - then[2] + now[2]
    kc = 1.4 - (ddays / 40)
    if kc < 1:
        kc = 1
    views = nowdata[0] - lastdata[1]
    comms = nowdata[1] - lastdata[2]
    mys = nowdata[2] - lastdata[0]
    ka = (views + mys) / (views + mys + comms)
    ka = ka ** 10
    kb = 2 * (mys / views * 100)
    if kb * mys > 5 * views:
        kb = 5 * views / mys
    pts = views * kc + ka * comms + kb * mys
    print('This Week--View:  ', nowdata[0],
          "  Comments:  ", nowdata[1], "  Mylist:  ", nowdata[2])
    print('Last Week--View:  ', lastdata[1],
          "  Comments:  ", lastdata[2], "  Mylist:  ", lastdata[0])
    print("PTs:  ", getint(pts), '   view *', getint2(kc), '   comment *',
          getint2(ka), '   mylist *', getint2(kb))


def hint():
    print('usage: python(3) xx.py A where A is the sm number')
    quit()


if __name__ == '__main__':
    try:
        s = int(sys.argv[1])
    except Exception:
        hint()
    if s == 0:
        hint()
    else:
        getVdata(s)
