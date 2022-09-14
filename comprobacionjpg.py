#Programa para comprobar que los fichero son jpg. y comprobación de categorías OK NOOK


import fnmatch
from itertools import count
import os

flag1 = 0
flag2 = 0

print(os.listdir('.'))
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'OK'):
        print("OK")
        flag1 = 1
    if fnmatch.fnmatch(file, 'NO OK'):
        print("NO OK")
        flag2 = 1
    

if flag1 == 1 and flag2 == 1:
    print("Ficheros encontrados, proceder")
    

else:
        print("missing folder with correct names, OK or NO OK")
        exit()


file = os.listdir('.')
print(file)
print(type(file))
print(len(file))
# is
# #Comprobar que las imagenes tienen el formato adecuado 
# for root, dirs, files in os.walk("./NO OK"):
#     print(os.listdir('./NO OK'))
#     # if fnmatch.fnmatch(file, '*.txt'):
#     #     print(file)

# for root, dirs, files in os.walk("./OK"):
#     print(files)
#     for file in files: 
#         if file.endswith(".jpg"):
#             print("correcto")
#         else:
#             print("error")
