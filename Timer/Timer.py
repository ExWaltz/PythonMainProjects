import time


def Timer(hours, minutes, seconds, prnt=False):
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    intTime = [int(e) for e in currentTime.split(':')]
    timeOffset = [int(hours), int(minutes), int(seconds)]
    timelimit = [curTime + offTime for curTime, offTime in zip(intTime, timeOffset)]
    if timelimit[0] >= 24:
        timelimit[0] = timelimit[0] - 24
    for num, limit in enumerate(timelimit[1:]):
        while limit >= 60:
            timelimit[num + 1] = limit - 60
            timelimit[num] += 1
            limit -= 60
    while timelimit > intTime:
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        intTime = [int(e) for e in currentTime.split(':')]
        timeLeft = [tLimit - curTime for curTime, tLimit in zip(intTime, timelimit)]
        if prnt:
            h, m, s = timeLeft
            sTime = "{}:{}:{}".format(h, m, s)
            print(sTime)
        yield timeLeft
    return True
