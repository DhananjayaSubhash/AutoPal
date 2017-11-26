import numpy as np
import pylab as pl
import time
import datetime
import xml.etree.ElementTree as xml

# Read text file
data = np.loadtxt('MAFsensor.txt')


# x and y values for linear line
x = data[:,0].astype(float).ravel()
y = data[:,1].astype(float).ravel()

(m,b) = pl.polyfit(x,y,1)

num = 20

with open("MAFsensorgradient.txt", "a") as text_file:
    num = num + 1
    text_file.write("%s\t%s\n" % (num, str(round(m, 2))))


# Read text file
gradient_data = np.loadtxt('MAFsensorgradient.txt')


# x and y values for linear line
gx = gradient_data[:,0].astype(float).ravel()
gy = gradient_data[:,1].astype(float).ravel()

(mg,bg) = pl.polyfit(gx,gy,1)

# Calculate x value relative to Y = 0
x_gradient = (0 - bg) / mg

current_date = datetime.datetime.now()

p_date = int(round(x_gradient))

predicted_date = current_date + datetime.timedelta(days=p_date)
print 'Predicted failure date for MAF Sensor :', predicted_date.strftime("%d/%m/%Y")

# Write to xml file
filename = "MAFsensordata.xml"
root = xml.Element("MAFsensor_data")
userelement = xml.Element("failure_date")
userelement.text = predicted_date.strftime("%d/%m/%Y")
root.append(userelement)

tree = xml.ElementTree(root)
with open(filename, "w") as fh:
    tree.write(fh)
