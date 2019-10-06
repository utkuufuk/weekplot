import os
import sys
import yaml
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

def parseYml(filename):
    with open(filename, 'r') as stream:
        try:
            items = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise UserWarning("Invalid YML file: {0}".format(err))
    events = []
    latest = 0
    earliest = 24
    for event in items:
        for ocr in event["occurances"]:
            sh = ocr["start"] // 60
            sm = ocr["start"] % 60
            eh = ocr["end"] // 60
            em = ocr["end"] % 60
            days = [getDay(d) for d in ocr["days"]]
            events.append(Event(event["name"], days, sh, sm, eh, em, event["color"]))
            earliest = sh if sh < earliest else earliest
            latest = eh + 1 if eh > latest else latest
    return events, earliest, latest + 1

def parseTxt(lines):
    with open(sys.argv[1]) as fp:
        lines = fp.readlines()
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
            raise UserWarning("Invalid text input format.")
    return events, earliest, latest + 1

def plotEvent(e):
    for day in e.days:
        d = DAYS.index(day) + 0.52
        start = float(e.startH) + float(e.startM) / 60
        end = float(e.endH) + float(e.endM) / 60
        plt.fill_between([d, d + 0.96], [start, start], [end, end], color=e.color)
        plt.text(d + 0.02, start + 0.02, '{0}:{1:0>2}'.format(e.startH, e.startM), va='top', fontsize=8)
        plt.text(d + 0.48, (start + end) * 0.502, e.name, ha='center', va='center', fontsize=10)

if __name__ == '__main__':
    ext = sys.argv[1].split('.')[-1]
    fig = plt.figure(figsize=(18, 9))
    try:
        events, earliest, latest = parseTxt(sys.argv[1]) if ext == 'txt' else parseYml(sys.argv[1])
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
    plt.savefig('{0}.png'.format(os.path.splitext(sys.argv[1])[0]), dpi=200, bbox_inches='tight')
