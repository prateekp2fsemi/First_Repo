file = 'Review_Timing_path.txt'   # input file
# file = 'helo.txt' #Dummy file
startpoint = 'Startpoint'
slack = 'slack'
beginpoint = 'Beginpoint'


# counting the total number of line in input file
def counter():
    with open(file, 'r') as fb:
        for count, line in enumerate(fb, 1):
            pass
    return count

# Second format
def Format_2():
    print("Work in progress")


# Format Identifier
def formatIdentiFier():
    
    STARTPOINT = 0
    SLACK = 0
    PATH = 0
    flag = 0
    value = open(file, 'r')
    a = value.read()
    if startpoint in a and beginpoint in a:
        print("Sorry The format is Wrong")

    elif startpoint in a:    
        with open(file, 'r') as fb:
            lineOfdata = fb.read().splitlines()
            count = counter()
            for num in range(count):
                value = lineOfdata[num].strip(" ,rf") 
                slicedata = value[0:10]
                if slicedata == startpoint:
                    STARTPOINT+=1
                    for i in range(num, count):
                        get = lineOfdata[i].strip(" ,rf")
                        sec_slice_data = get[0:5]
                        app =  open('parseroutput2.csv','a')
                        if slack not in sec_slice_data:
                            app.write(get)
                            app.write("\n")
                        else:
                            SLACK+=1
                            PATH+=1
                            app.write(get)
                            app.write("\n")
                            app.close()
                            break
        print("total number of startpoint {},slack {},path {}".format(STARTPOINT,SLACK,PATH))
    elif beginpoint in a:
        Format_2() #Calling Another Format
                            
formatIdentiFier()
