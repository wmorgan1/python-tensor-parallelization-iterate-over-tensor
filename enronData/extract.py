import sqlite3
import datetime
import sys


D = False


# ALL TIME CONVERSIONS ARE DONE USING UTC TIME


# ranges of each data
eidR = 157
nameR = 157
deptR = 3
ldeptR = 157
titleR = 157
genderR = 2
seniorityR = 2
midR = 21635
filenameR = 21635
msubR = 21635
recipientR = 57

# ranges of time
hoursR = 31803 # 11/12/1998 11:00 AM to 6/21/2002 10:00 AM:
           # (1326 - 2 [first, last are incomplete]) * 24 + 13 + 14
daysR = 1326 # 11/12/1998 to 6/21/2002: 18 + 31 + (365 * 3) + 31 + 29 [leap] + 31 + 30 + 31 + 30
weeksR = 191 # GMT weeks start on Sunday and stop on Saturday
           # 11/12/1998 is Friday, so that counts as a week of 2 days
           # 6/21/2002 is a Friday, so that counts as a week of 6 days
           # ((1326 - 2 - 6) / 7) + 2 
monthsR = 44 # 11/1998 to 6/2002: 2 + (3 * 12) + 6 = 44
yearsR = 5 # 98, 99, 00, 01, 02


'''
query:
select table.col1,table.col2,...,table1.col3 from table1 inner join table2 on 
table1.col2 = table2.col4;
Select Message.mid,Message.from_eid,Recipient.to_eid,Message.unix_time 
from Message inner join Recipient on Recipient.mid = Message.mid;

Have user select tables and columns. 
If data is from 2 tables, have user select the unifying col
Make query
Make file
'''

def printMenu():
    print("Please select your data, 1 at a time")
    print("\t1) Employee Info: employee id (1 - 156)")
    print("\t2) Employee Info: full name")
    print("\t3) Employee Info: department (Legal, Trading, or Other)")
    print("\t4) Employee Info: long department")
    print("\t5) Employee Info: title")
    print("\t6) Employee Info: gender (Female or Male)")
    print("\t7) Employee Info: seniority (Junior or Senior)")
    print("\t8) Message Info: message id (1 - 21635)")
    print("\t9) Message Info: filename")
    print("\t10) Message Info: unix time (seconds since Jan 1, 1970)")
    print("\t11) Message Info: message subject")
    print("\t12) Message Info: sender's employee id (1 - 156)")
    print("\t13) Recipient Info: message id (1 - 21635)")
    print("\t14) Recipient Info: recipient number (1 - 57)")
    print("\t15) Recipient Info: receiver's employee id (1 - 156)")
    print("\t Enter 16 if done")
    return


# performs an sql query with an inner join
# returns cursor that can be iterated thru for the query lines
def innerJoin(c, common, dList):
    query = "select "
    for i in dList:
        query = query + i + ","

    # remove trailing comma from above
    query = query[0:len(query) - 1]

    query = query + " from "

    # figure out first table for inner join
    temp = common[0]
    if temp[0] == "M":
        query = query + "Message "
    elif temp[0] == "E":
        query = query + "Employee "
    elif temp[0] == "R":
        query = query + "Recipient "

    query = query + "inner join "

    # figure out second table for inner join
    temp = common[1]
    if temp[0] == "M":
        query = query + "Message on "
    elif temp[0] == "E":
        query = query + "Employee on "
    elif temp[0] == "R":
        query = query + "Recipient on "

    # put in the common data between tables to aggregate(?) on
    query = query + common[0] + " = " + common[1] + ";"

    #perform sql query
    c.execute(query)
    if D: print("innerJoin: ", query)
    return c

# performs an sql query
# returns cursor that can be iterated thru for the query lines
def selectFrom(c, dList, table):
    query = "select "
    for i in dList:
        query = query + i + ","

    # remove trailing comma from above
    query = query[0:len(query) - 1]

    query = query + " from " + table + ";"

    # perform sql query
    c.execute(query)
    if D: print("selectFrom: ", query)
    return c


# asks for unix time to be broken
# returns range based on time intervals chosen
def unixRange():
    print("You selected unix time.", end = " ")
    print("Please indicate how you would like that broken down.")
    print("\t1) Years")
    print("\t2) Months")
    print("\t3) Weeks")
    print("\t4) Days")
    print("\t5) Hours")
    selection = int(input("Selection: "))

    if selection == 1:
        return yearsR
    if selection == 2:
        return monthsR
    if selection == 3:
        return weeksR
    if selection == 4:
        return daysR
    if selection == 5:
        return hoursR


# convert unix time stamps to indexed years in the tensor
def unixTimeToYears(timestamp):
    year = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y'))
    return (year - 1998)


# convert unix time stamps to indexed months in the tensor
def unixTimeToMonths(timestamp):
    year = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y'))
    month = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%m'))
    return (year - 1998) * 12 + month - 11


# convert unix time stamps to indexed weeks in the tensor
# uses the datetime isocalendar function
# weeks start on Monday and end on Sunday
# a year can have 52 or 53 weeks, with the split being in favor of the year
# that has 4 days of that week
def unixTimeToWeeks(timestamp):
    # weeks in each year + weeks in previous years
    # earliest timestamp is the 46 week
    w1998 = 7 # 53 - 46
    w1999 = 59 # 7 + 52
    w2000 = 111 # 59 + 52
    w2001 = 163 # 111 + 52

    year = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y'))
    month = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%m'))
    day = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%d'))
    isodate = datetime.date(year, month, day).isocalendar()
    
    if year == 1998:
        return isodate[1] - 46
    elif year == 1999:
        return isodate[1] + w1998
    elif year == 2000:
        return isodate[1] + w1999
    elif year == 2001:
        return isodate[1] + w2000
    elif year == 2002:
        return isodate[1] + w2001


# convert unix time stamps to indexed days in the tensor
# uses the julian calender, which returns the "i"th day of the year
def unixTimeToDays(timestamp):
    # days in each year + days in previous years
    # first day of timestamp range is 1998/11/13 which is 317th day of the year
    # in UTC time
    d1998 = 48 # 365 - 317
    d1999 = 413
    d2000 = 779
    d2001 = 1144

    year = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y'))
    month = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%m'))
    day = int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%d'))
    yearDay = datetime.date(year, month, day).timetuple().tm_yday
    if D: print("year = ", year, " month = ", month, " day = ", day, " yearDay = ", yearDay)

    if year == 1998:
        return yearDay - 317
    elif year == 1999:
        return yearDay + d1998
    elif year == 2000:
        return yearDay + d1999
    elif year == 2001:
        return yearDay + d2000
    elif year == 2002:
        return yearDay + d2001

    
# convert unix time stamps to indexed hours in the tensor
# uses unixTimeToDays
def unixTimeToHours(timestamp):
    # earliest TS is 4AM UTC time
    # days * 24 hours in a day, - 4 from above, + hour in current TS
    hour =  int(datetime.datetime.utcfromtimestamp(timestamp).strftime('%H'))
    '''print("hour = ", hour)
    print("unixtimeToDays = ", unixTimeToDays(timestamp))
    test = unixTimeToDays(timestamp) * 24 - 4 + hour
    print("test = ", test)'''
    return ((unixTimeToDays(timestamp) * 24) - 4 + hour)



# parses the sql query line by line, creates output file
# returns True or False to indicate success or failure
def parseQuery(c, outFile, Dims):
    if D:
        print("parseQuery")

    # write tensor type to file
    outFile.write("sptensor\n")

    # write dimension of tensor to file
    outFile.write(str(len(Dims)) + "\n")

    # write ranges of each dimension
    temp = "" # used to not leave trailing whitespace on the line
    j = 0 # counts for where in the returned query unix time is
    unixLoc = -1 # where in the tuple of the sql query unix timestamp is
                # used in processing sql query
    unixInterval = 0
    for i in Dims:
        if i == "unix":
            # the lenth of the unix time vector (dimension) of the tensor
            # found by prompting the user to make a choice between
            # years, months, weeks, days, hours
            unixInterval = unixRange()

            temp = temp + str(unixInterval) + " "
            unixLoc = j
        else:
            temp = temp + str(i) + " "
        j += 1
    temp = temp[0:len(temp) - 1] + "\n"
    outFile.write(temp)
    

    # this block of code can, in theory, handle n-dimensional tensors
    tensor = {}
    i = 0 # counts the number of data, needed for next line in input file
    lineList = [] # ordered list of the tuples from c. Lets me write to file in order
    unixTimeAdjusted = 0 # new "index" of the vector of adjusted unix time
    adjQuery = () # new tuple
    # iterate thru the returned sql query, each "line" is a line in the query
    # given as a tuple
    for line in c:
        '''if i == 20:
            break'''
        # count data
        i += 1

        if D: print(line)

        # test if unix time is part of query
        if unixLoc != -1:
            # process unix time into years
            if unixInterval == yearsR:
                # remember that "line" is a tuple made from the query
                # line[unixLoc] is the part of the tuple that is unixTime
                unixTimeAdjusted = unixTimeToYears(line[unixLoc])

            elif unixInterval == monthsR:
                unixTimeAdjusted = unixTimeToMonths(line[unixLoc])

            elif unixInterval == weeksR:
                unixTimeAdjusted = unixTimeToWeeks(line[unixLoc])

            elif unixInterval == daysR:
                unixTimeAdjusted = unixTimeToDays(line[unixLoc])

            elif unixInterval == hoursR:
                unixTimeAdjusted = unixTimeToHours(line[unixLoc])

            # remake the tuple/query
            adjQuery = line[0:unixLoc] + (unixTimeAdjusted,) + line[unixLoc + 1:]
        else:
            adjQuery = line # no adjustment required    
                
        if D: print(adjQuery)
        
                
        # this calculates the counts in each cell
        # entry already in tensor
        if adjQuery in tensor:
            tensor[adjQuery] += 1
        # new entry in tensor
        else:
            tensor[adjQuery] = 1
            # for ordered writing to file
            lineList.append(adjQuery)
            
        if D: print(tensor[adjQuery])

        
    outFile.write(str(i) + "\n") # write total number of data to file

    
    # write tensor to file
    for i in tensor:
        tempList = []
        temp = ""

        # split the tuple and strip out parenthesis and commas
        tempList = str(i).strip('()').split(',')

        # append entries in tuple to string
        # remember, the tuple is merely a 'location' in the tensor
        for j in tempList:
            temp = temp + j

        # write location and count to the file
        outFile.write(temp + " " + str(tensor[i]) + "\n")

    

    return True


def main():

    try:
        # dbstring = input("Enter location of database: ")
        # conn = sqlite3.connect(dbstring)
        conn = sqlite3.connect('/home/will/Documents/thesis/enronData/enron.db')
        c = conn.cursor()

        # open an output file
        output = input("Enter name of desired output file: ")
        outputFile = open(output, "w")

    except:
        print("Error connecting to database or opening output file")
        sys.exit(1)

    
    # list of data desired for n dimensions
    selection = []
    dList = []
    
    # number of dimensions
    Dims = []

    # loop bool
    loop = True

    # bools to keep track of what tables I'm drawing from
    employee = False
    message = False
    recipient = False

    # returned query
    query = ""

    
    while loop:
        printMenu()
        e = int(input("Selection: "))
        if e == 16:
            print("You entered: ")
            for i in selection:
                print(i)
            tmp = input("Is this correct? (y | n) ")
            if tmp == "y":
                loop = False
            else:
                print("Starting over.")
                selection = []
        else:
            selection.append(e)

    for e in selection:
        if e == 1:
            employee = True
            dList.append("Employee.eid")
            Dims.append(eidR)
        elif e == 2:
            employee = True
            dList.append("Employee.name")
            Dims.append(eidR)
        elif e == 3:
            employee = True
            dList.append("Employee.department")
            Dims.append(deptR)
        elif e == 4:
            employee = True
            dList.append("Employee.longdepartment")
            Dims.append(ldeptR)
        elif e == 5:
            employee = True
            dList.append("Employee.title")
            Dims.append(titleR)
        elif e == 6:
            employee = True
            dList.append("Employee.gender")
            Dims.append(genderR)
        elif e == 7:
            employee = True
            dList.append("Employee.seniority")
            Dims.append(seniorityR)
        elif e == 8:
            message = True
            dList.append("Message.mid")
            Dims.append(midR)
        elif e == 9:
            message = True
            dList.append("Message.filename")
            Dims.append(filenameR)
        elif e == 10:
            message = True
            dList.append("Message.unix_time")
            Dims.append("unix")
        elif e == 11:
            message = True
            dList.append("Message.subject")
            Dims.append(midR)
        elif e == 12:
            message = True
            dList.append("Message.from_eid")
            Dims.append(eidR)
        elif e == 13:
            recipient = True
            dList.append("Recipient.mid")
            Dims.append(midR)
        elif e == 14:
            recipient = True
            dList.append("Recipient.rno")
            Dims.append(recipientR)
        elif e == 15:
            recipient = True
            dList.append("Recipient.to_eid")
            Dims.append(eidR)


    # figure out if we are using unix time and if so, how it should be split
    '''if unix:
        print("You have selected unix time as a data point.")
        print("'''
            
    # figure out if we are merging multiple tables
    count = 0
    if employee: count += 1
    if message: count += 1
    if recipient: count += 1
    # if merging multiple tables, find the data that is in common with them
    if count == 2:
        common = []
        print("You have selected data from multiple tables.")
        print("Please select the common data points for correlation between tables.")

        # select the common data
        loop = True
        cList = []
        while loop:
            if count == 2:
                printMenu()
                cList.append(int(input("First table selection: ")))
                count -= 1
            elif count == 1:
                printMenu()
                cList.append(int(input("Second table selection: ")))
                count -= 1
            else:
                if loop:
                    print("You entered: ")
                    for i in cList:
                        print(i)
                    tmp = input("Is this correct? (y | n) ")
                    if tmp == "y":
                        loop = False
                    else:
                        print("Starting over.")
                        cList = []
                        count = 2
            print("count = ", count, " loop = ", loop)

        for e in cList:
            if e == 1:
                common.append("Employee.eid")
            elif e == 2:
                common.append("Employee.name")
            elif e == 3:
                common.append("Employee.department")
            elif e == 4:
                common.append("Employee.longdepartment")
            elif e == 5:
                common.append("Employee.title")
            elif e == 6:
                common.append("Employee.gender")
            elif e == 7:
                common.append("Employee.seniority")
            elif e == 8:
                common.append("Message.mid")
            elif e == 9:
                common.append("Message.filename")
            elif e == 10:
                common.append("Message.unix_time")
            elif e == 11:
                common.append("Message.subject")
            elif e == 12:
                common.append("Message.from_eid")
            elif e == 13:
                common.append("Recipient.mid")
            elif e == 14:
                common.append("Recipient.rno")
            elif e == 15:
                common.append("Recipient.to_eid")

        # an inner join is required if count > 1
        innerJoin(c, common, dList)
    # inner join of more than two tables, not supported
    elif count > 2:
        print("Inner join of more than 2 tables not supported")
        sys.exit(1)
    # no inner join required
    else:
        if employee:
            c = selectFrom(c, dList, "Employee")            
        elif  message:
            c = selectFrom(c, dList, "Message")
        elif recipient:
            c = selectFrom(c, dList, "Recipient")
                               

    if not parseQuery(c, outputFile, Dims):
        print("Query failed to be parsed")
        sys.exit(1)

    outputFile.close()
main()
