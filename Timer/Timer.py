from datetime import timedelta
from datetime import datetime


def Timer(h, m, s):
    """ Number 8 of my: Let's make 9 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects
    """
    nTime = datetime.now()  # Get Current Time
    fTime = nTime + timedelta(hours=int(h), minutes=int(m), seconds=int(s))     # Get time offset
    while fTime > nTime:    # Run code until current time is greater than time offset
        nTime = datetime.now()      # Update current time
        sTime = fTime - nTime       # Calculate the time difference between time offset and current time
        # Convert time difference into hours, minutes and seconds
        days, seconds = sTime.days, sTime.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        iTime = [hours, minutes, seconds]
        for e in iTime:
            if e < 0:       # Incase of error break of this loop
                break
            yield iTime     # Return Time left
    return True     # To indicate that the timer is done

if __name__ == '__main__':
    hours = input("Hours:")
    mins = input("Minutes:")
    secs = input("Seconds:")
    if hours == '': hours = 0
    if mins == '': mins = 0
    if secs == '': secs = 0
    for h, m, s in Timer(hours, mins, secs):
        print(f"{h}:{m}:{s}")
