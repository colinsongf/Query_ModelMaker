import os, rw

content = ""

for i in xrange(1600,2050):
    content += (str(i) + '\r\n')

rw.writeFile("../NE/Time.txt", content)
