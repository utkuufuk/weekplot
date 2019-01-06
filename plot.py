import sys
import matplotlib.pyplot as plt
from namedlist import namedlist

HOURS_START = 7
HOURS_END = 23
HOURS_TICK_INTERVAL = 2
HOURS_RANGE = range(HOURS_START, HOURS_END + HOURS_TICK_INTERVAL, HOURS_TICK_INTERVAL)
DPI = 100
TITLE = 'Schedule'
DAYS = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

Event = namedlist('Event', 'name, days, start, end, color')

def getDay(prefix):
    for d in DAYS:
        if d.startswith(prefix):
            return d
    raise UserWarning("Invalid day: {0}".format(prefix))

def parseEvents(lines):
    events = []
    events.append(Event('', '', '', '', ''))
    index = 0
    for line in lines:
        line = line.rstrip()
        index += 1
        if index == 1:
            events[-1].name = line
        elif index == 2:
            events[-1].days = [getDay(d) for d in line.replace(' ', '').split(',')]
        elif index == 3:
            hours = line.replace(' ', '').split('-')
            events[-1].start = hours[0]
            events[-1].end = hours[1]
        elif index == 4:
            events[-1].color = line
        elif index == 5 and line == '':
            events.append(Event('', '', '', '', ''))
            index = 0
        else:
            raise UserWarning("Corrupted input file.")
    return events

def plotEvent(event):
    for day in event.days:
        d = DAYS.index(day) + 0.52
        start = event.start.split(':')
        startPos = float(start[0]) + float(start[1]) / 60
        end = event.end.split(':')
        endPos = float(end[0]) + float(end[1]) / 60
        plt.fill_between([d, d + 0.96], [startPos, startPos], [endPos, endPos], color=event.color)
        plt.text(d + 0.02, startPos + 0.02, '{0}:{1:0>2}'.format(start[0], start[1]), va='top', fontsize=9)
        plt.text(d + 0.48, (startPos + endPos) * 0.503, event.name, ha='center', va='center', fontsize=10)

if __name__ == '__main__':
    # set axis
    fig = plt.figure(figsize=(18, 9))
    plt.title(TITLE, y=1, fontsize=14)
    ax=fig.add_subplot(1, 1, 1)
    ax.set_xlim(0.5, len(DAYS) + 0.5)
    ax.set_xticks(range(1, len(DAYS) + 1))
    ax.set_xticklabels(DAYS)
    ax.set_ylim(HOURS_END, HOURS_START)
    ax.set_yticks(HOURS_RANGE)
    ax.set_yticklabels(["{0}:00".format(h) for h in HOURS_RANGE])
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    with open(sys.argv[1]) as fp:
        lines = fp.readlines()
    events = parseEvents(lines)
    for e in events:
        plotEvent(e)
    plt.savefig('{0}.png'.format(TITLE), dpi=DPI)
