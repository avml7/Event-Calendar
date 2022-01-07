from Calendar import Calendar, m_names
import argparse

def main():
    args = getArgs()
    if args.fontsize is None:
        args.fontsize = 6
    if args.savepath is not None:
        if args.savepath[-1] != '/' or args.savepath[-1] != '\\':
            args.savepath += '/'
    if args.savepath is None:
        args.savepath = ""
    
    with open(args.filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    # read file with dates and events

    events, monthIndices = processLines(lines, args.numMonths)
    
    for monthlyEvents, monthNumber in zip(events, monthIndices):
        print(monthNumber, m_names[monthNumber-1])
        cal = addEvents(monthNumber, monthlyEvents, args.year, args.fontsize)
        filename = m_names[monthNumber-1] + str(args.year) + ".png"
        cal.save(filename, args.savepath)


def addEvents(month, events, year, fontsize):
    cal = Calendar(year, month, fontsize)
    for day, event, color in events:
        cal.add_event(day, event, color)
    return cal

def processLines(lines, numMonths):
    events = [[] for _ in range(numMonths)]
    indices = []
    for line in lines:
        splitLine = line.split(maxsplit=3)
        month = int(splitLine[0])
        day = int(splitLine[1])
        color = splitLine[2]
        event = splitLine[3]
        
        if month not in indices:
            indices.append(month)
        i = indices.index(month)
        events[i].append((day, event, color))

    return events, indices

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help="Year for calendar")
    parser.add_argument('numMonths', type=int, help="Number of months to be in calendar")
    parser.add_argument('filename', type=str, help="Filename with dates listed")
    parser.add_argument('--fontsize', type=int, required=False, help="Optional argument to specify font size of events")
    parser.add_argument('--savepath', type=str, required=False, help="Optional argument to specify where to save calendar pngs")
    return parser.parse_args()


if __name__ == '__main__':
    main()