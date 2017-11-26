import numpy as np
import pylab as pl
import time
import datetime
import xml.etree.ElementTree as xml
import fnmatch
import os

#Read number of text files in a directory
file_count =  len(fnmatch.filter(os.listdir("/home/Dhananjaya/Prediction/O2 Sensor"), 'O2sensor*.txt'))

# Write to xml file
filename = "O2sensordata.xml"
root = xml.Element("O2sensor_data")

for sensor_no in range(file_count):
    file_name = "O2sensor" + str(sensor_no+1) + ".txt"

    # Read text file
    with open(file_name) as textFile:
        lines = [line.split() for line in textFile]

    # Declare two lists
    down = [[['0'],['0.1']]]
    up = [[['0'],['0.9']]]

    # Read text file's lines by line
    for line in lines:
        temp = [l.split() for l in line]

        if ( 0.45 > np.asarray(temp, dtype=np.float)[1] ):
            down.append(temp)
        
        else:
            up.append(temp)


    # Make lists as a array
    down = np.array(down)
    up = np.array(up)

    # x and y values for Min voltage linear line
    xd = down[:,0].astype(float).ravel()
    yd = down[:,1].astype(float).ravel()

    (md,bd) = pl.polyfit(xd,yd,1)

    # Calculate x value relative to Y = 0.45
    x_down = (0.45 - bd) / md

    #ypd = pl.polyval([md,bd],xd)

    # x and y values for Max voltage linear line
    xu = up[:,0].astype(float).ravel()
    yu = up[:,1].astype(float).ravel()

    (mu,bu) = pl.polyfit(xu,yu,1)

    # Calculate x value relative to Y = 0.45
    x_up = (0.45 - bu) / mu

    # Get least x value
    if x_down < x_up :
        least = x_down
    else :
        least = x_up

    start_date = datetime.datetime.now()

    least = int(round(least))

    predicted_date = start_date + datetime.timedelta(days=least)

    print 'Predicted failure date for O2 Sensor '+str(sensor_no+1)+' :', predicted_date.strftime("%d/%m/%Y")
    
    sensors = xml.SubElement(root,"O2sensor"+str(sensor_no+1))
    failure_date = xml.SubElement(sensors,"failure_date")
    failure_date.text = predicted_date.strftime("%d/%m/%Y")

tree = xml.ElementTree(root)
with open(filename, "w") as fh:
    tree.write(fh)



