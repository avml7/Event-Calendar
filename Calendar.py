"""
Credit to:
https://stackoverflow.com/questions/42171990/create-a-one-month-calendar-with-events-on-it-in-python

with some changes made to add color functionality and save image instead of show
"""

import calendar
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

calendar.setfirstweekday(calendar.SUNDAY)
w_days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
m_names = ['January', 'February', 'March', 'April',
           'May', 'June', 'July', 'August', 'September',
           'October', 'November', 'December']
page_sizes = {'letter': (11.0, 8.5),
              'legal': (14.0, 8.5),
              'extraLarge': (20.0, 15.0)}

class Calendar(object):
    def __init__(self, year, month, fontsize=9):
        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(year, month)
        self.events = [[[] for day in week] for week in self.cal]
        self.fontsize = fontsize
    
    def _monthday_to_index(self, day):
        'The index of the day in the list of lists'
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
         # couldn't find the day
        raise ValueError("There aren't {} days in the month".format(day))
    
    def add_event(self, day, event_str, color):
        'insert a string into the events list for the specified day'
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append((event_str, color))
    
    def save(self, filename, pagesize="letter", path=""):
        'create the calendar'
        f, axs = plt.subplots(len(self.cal), 7, sharex=True, sharey=True)
        f.set_size_inches(page_sizes[pagesize])
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                bbox = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
                wrapSize = f.dpi*bbox.width+10
                if self.cal[week][week_day] != 0:
                    ax.text(.02, .98,
                            str(self.cal[week][week_day]),
                            verticalalignment='top',
                            horizontalalignment='left')
                    # text
                # add date
                if len(self.events[week][week_day]) > 0:
                    prevItem = 0
                    pos = 1
                    for event, textColor in self.events[week][week_day]:
                        prev = ax.get_children()[prevItem]
                        r = f.canvas.get_renderer()
                        bb = prev.get_window_extent(renderer=r)
                        pos -= bb.height/100
                        ax.text(.03, pos, event, #.03, .85
                            verticalalignment='top',
                            horizontalalignment='left',
                            fontsize=self.fontsize,
                            color=textColor,
                            wrap=True)._get_wrap_line_width = lambda : wrapSize
                        prevItem += 1
                    # for event
                # if events
            # for week day
        # for week

        # use the titles of the first row as the weekdays
        for n, day in enumerate(w_days):
            axs[0][n].set_title(day)

        # Place subplots in a close grid
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        f.suptitle(m_names[self.month-1] + ' ' + str(self.year),
                   fontsize=20, fontweight='bold')
        plt.savefig(path+filename)