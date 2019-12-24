from socket import *

fTimeOutSec = 5.0
sNetworkAddress = '192.168.1'
aiHostAddresses = range(1,255)
aiPorts = [5900]

setdefaulttimeout(fTimeOutSec)
print "Starting Scan..."
for h in aiHostAddresses:
    for p in aiPorts:
        s = socket(AF_INET, SOCK_STREAM)
        address = ('%s.%d' % (sNetworkAddress, h))
        result = s.connect_ex((address,p))
        if ( 0 == result ):
            print "%s:%d - OPEN" % (address,p)
        elif ( 10035 == result ):
            #do nothing, was a timeout, probably host doesn't exist
            pass
        else:
            print "%s:%d - closed (%d)" % (address,p,result)

        s.close()
print "Scan Completed."
