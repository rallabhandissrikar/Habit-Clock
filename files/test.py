import datetime
from DatabaseConnection import *

blip = get_single_Data('HC-Ht', 'srikar', {'id':4})

print('-' in str(blip['sch']-datetime.datetime.now()))


