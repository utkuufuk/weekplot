import sys
from math import ceil
import matplotlib.pyplot as plt
from namedlist import namedlist

DAYS = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
Event = namedlist('Event', 'name, days, startH, startM, endH, endM, color')

def getDay(prefix):
    for d in DAYS:
        if d.startswith(prefix):
            return d
    raise UserWarning("Invalid day: {0}".format(prefix))

def parseEvents(lines):
    index = 0
    latest = 0
    earliest = 24
    events = [Event('', '', '', '', '', '', '')]
    for line in lines:
        line = line.rstrip()
        index += 1
        if index == 1:
            events[-1].name = line
        elif index == 2:
            events[-1].days = [getDay(d) for d in line.replace(' ', '').split(',')]
        elif index == 3:
            hours = line.replace(' ', '').split('-')
            start = hours[0].split(':')
            end = hours[1].split(':')
            events[-1].startH = int(start[0])
            events[-1].startM = int(start[1])
            events[-1].endH = int(end[0])
            events[-1].endM = int(end[1])
            earliest = events[-1].startH if events[-1].startH < earliest else earliest
            latest = events[-1].endH + 1 if events[-1].endH > latest else latest
        elif index == 4:
            events[-1].color = line
        elif index == 5 and line == '':
            events.append(Event('', '', '', '', '', '', ''))
            index = 0
        else:
            raise UserWarning("Corrupted input file.")
    return events, earliest, latest

def plotEvent(e):
    for day in e.days:
        d = DAYS.index(day) + 0.52
        start = float(e.startH) + float(e.startM) / 60
        end = float(e.endH) + float(e.endM) / 60
        plt.fill_between([d, d + 0.96], [start, start], [end, end], color=e.color)
        plt.text(d + 0.02, start + 0.02, '{0}:{1:0>2}'.format(e.startH, e.startM), va='top', fontsize=8)
        plt.text(d + 0.48, (start + end) * 0.502, e.name, ha='center', va='center', fontsize=10)

if __name__ == '__main__':
    fig = plt.figure(figsize=(18, 9))
    with open(sys.argv[1]) as fp:
        lines = fp.readlines()
    try:
        events, earliest, latest = parseEvents(lines)
        for e in events:
            plotEvent(e)
    except UserWarning as e:
        print("ERROR:", str(e), file=sys.stderr)
        sys.exit(1)
    plt.title('Weekly Schedule', y=1, fontsize=14)
    ax=fig.add_subplot(1, 1, 1)
    ax.set_xlim(0.5, len(DAYS) + 0.5)
    ax.set_xticks(range(1, len(DAYS) + 1))
    ax.set_xticklabels(DAYS)
    ax.set_ylim(latest, earliest)
    ax.set_yticks(range(ceil(earliest), ceil(latest)))
    ax.set_yticklabels(["{0}:00".format(h) for h in range(ceil(earliest), ceil(latest))])
    ax.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.savefig('{0}.png'.format(sys.argv[1].split('.')[0]), dpi=200, bbox_inches='tight')

