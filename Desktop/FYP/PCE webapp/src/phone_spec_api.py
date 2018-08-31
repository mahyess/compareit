

from fonAPI import FonApi

fon = FonApi('880232b5ecde964cbeaf16add69a727726c6a8f0878b9263')

device = 'nokia 3210'

phones = fon.getdevice(device)
try:
    for phone in phones:
        print(phone['DeviceName'])
        print (phone['weight'])
        print (phone['resolution'])
except:
    print (phones)