from datetime import timedelta
from datetime import datetime


def Timer(h, m, s):
    nTime = datetime.now()
    fTime = nTime + timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    while fTime > nTime:
        nTime = datetime.now()
        sTime = fTime - nTime
        days, seconds = sTime.days, sTime.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        iTime = [hours, minutes, seconds]
        for e in iTime:
            if e < 0:
                break
            yield iTime
        # sTime = sTime.strftime("%H:%M:%S")
        # iTime = [e for e in str(sTime).split(":")]
    return True
