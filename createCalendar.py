from Calendar import Calendar, m_names, page_sizes
import argparse

def main():
    args = getArgs()
    if args.fontsize is None:
        args.fontsize = 9
    if args.savepath is not None:
        if args.savepath[-1] != '/' or args.savepath[-1] != '\\':
            args.savepath += '/'
    if args.savepath is None:
        args.savepath = ""
    if args.pagesize is None:
        args.pagesize = 'letter'
    
    with open(args.filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    # read file with dates and events

    events, monthIndices = processLines(lines, args.numMonths)
    
    for monthlyEvents, monthNumber in zip(events, monthIndices):
        cal = addEvents(monthNumber, monthlyEvents, args.year, args.fontsize)
        filename = m_names[monthNumber-1] + str(args.year) + ".png"
        cal.save(filename, args.pagesize, args.savepath)


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
    parser.add_argument('--fontsize', type=int, required=False, help="Optional argument to specify font size of events (default is 9)")
    parser.add_argument('--savepath', type=str, required=False, help="Optional argument to specify where to save calendar pngs (default is current directory)")
    parser.add_argument('--pagesize', type=str, required=False, help="Optional argument to specify page size (default is letter) | Options are: "+str(page_sizes))
    return parser.parse_args()


if __name__ == '__main__':
    main()