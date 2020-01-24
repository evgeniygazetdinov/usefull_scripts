import os
import datetime
import random
import string
randoms = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(12)])



def log(phrase):
    import os
    f1=open('{}/a.txt'.format(os.getcwd()), 'a')
    f1.write('\n')
    f1.write(str(phrase))
    f1.write('\n')
    f1.write(str(randoms))
    f1.write('\n')
    f1.write(str("=")*30)
    f1.close()
