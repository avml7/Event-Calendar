from Calendar import Calendar, m_names
import argparse

def main():
    args = getArgs()
    with open(args.filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    # read file with dates and events
    events, monthIndices = processLines(lines, args.numMonths)
    
    for monthlyEvents, monthNumber in zip(events, monthIndices):
        cal = addEvents(monthNumber-1, monthlyEvents, args.year)
        filename = m_names[monthNumber-1] + str(args.year) + ".png"
        cal.save(filename)


def addEvents(month, events, year):
    cal = Calendar(year, month)
    for day, event in events:
        cal.add_event(day, event)
    return cal

def processLines(lines, numMonths):
    events = [[] for _ in range(numMonths)]
    indices = []
    for line in lines:
        splitLine = line.split(maxsplit=2)
        month = int(splitLine[0])
        day = int(splitLine[1])
        event = splitLine[2]
        
        if month not in indices:
            indices.append(month)
        i = indices.index(month)
        events[i].append((day, event))

    return events, indices

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type = int, help = "Year for calendar")
    parser.add_argument('numMonths', type = int, help = "Number of months to be in calendar")
    parser.add_argument('filename', type = str, help = "Filename with dates listed")
    return parser.parse_args()


if __name__ == '__main__':
    main()