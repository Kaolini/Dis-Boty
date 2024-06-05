from datetime import datetime
import random
import csv
def getDuration(then, now=datetime.now(), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then  # For build-in functions
    print(f"now is{type(now)}")
    print(f"then is{type(then)}")
    print(f"dur is{type(duration)}")

    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 86400)  # Seconds in a day = 86400

    def hours(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 3600)  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 60)  # Seconds in a minute = 60

    def seconds(seconds=None):
        if seconds != None:
            return divmod(seconds, 1)
        return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return (int(y[0]), int(d[0]),int(h[0]), int(m[0]),int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]


def print_time(time_passed:tuple, user_id:str) -> str:
    if not time_passed[2] and time_passed[3]:
        return f"{user_id} woke up after {time_passed[3]} minutes and {time_passed[4]} second nap <:Wakege:1103576491889008711>"
    elif not time_passed[3] and not time_passed[2]:
        return f"{user_id} woke up after {time_passed[4]} second nap <:Wakege:1103576491889008711>"
    else:
        return f"{user_id} woke up after {time_passed[2]} hour, {time_passed[3]} minute and {time_passed[4]} second nap <:Wakege:1103576491889008711>"


def read_compl():
    with open("compl.csv", newline="") as f:
        spamreader = csv.reader(f, quotechar='\n')
        file = random.choice(list(spamreader))
        return file[0]


