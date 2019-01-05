import matplotlib.pyplot as plt

HOURS_START = 0
HOURS_END = 24
DPI = 100
TITLE = 'Weekly Plan'
DAYS = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
COLORS = ['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon']

# adds new event to weekly plan
def addEvent(name, day, start, end, color):
    plt.fill_between([day, day + 1], [start, start], [end, end], color=color)
    plt.text(day + 0.02, start + 0.1, '{0}:{1:0>2}'.format(start, 0), va='top', fontsize=9)
    plt.text(day + 0.5, (start + end) * 0.505, name, ha='center', va='center', fontsize=10)

if __name__ == '__main__':
    fig = plt.figure(figsize=(18, 9))
    addEvent("Swimming", 1.5, 11, 15, COLORS[1])
    addEvent("Body Weight\nTraining", 0.5, 9, 11, COLORS[0])

    # set axis
    ax=fig.add_subplot(1, 1, 1)
    ax.set_xlim(0.5, len(DAYS) + 0.5)
    ax.set_ylim(HOURS_END, HOURS_START)
    ax.set_yticks(range(HOURS_START, HOURS_END, 3))
    ax.set_xticks(range(1, len(DAYS) + 1))
    ax.set_xticklabels(DAYS)
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    plt.title(TITLE, y=1, fontsize=14)
    plt.savefig('{0}.png'.format(TITLE), dpi=DPI)