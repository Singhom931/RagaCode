from matplotlib import pyplot
from matplotlib import colors
from PIL import Image
import os
import cv2
import binascii

Pentcolours = ["[255 255 255]","[  0   0 255]","[  0 255   0]","[255   0   0]","[0 0 0]"]
colormap = colors.ListedColormap(["black","white"])
Pent = ["0","1","2","3","4"]
DataDimension = [1,2,3,4,5,6,7,8]
Data = [];SubData = []
binary = ""

BS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def to_base(s, b):
    res = ""
    while s:
        res+=BS[s%b]
        s//= b
    return res[::-1] or "0"

file = open("File.txt","r")
byte = str([*file])
byte = str(byte).replace("[", '').replace("]", '')
for char in byte:
    print(char)
#print(byte)
for char in byte:
    if char == " ": binary = binary + "0100000"
    elif char == "'": pass
    else: binary = binary + bin(ord(char)).replace('0b', '')

#binary = ''.join(format(ord(x), 'b') for x in byte)
print(binary)
#binary = "1" + binary
#binary = ''.join(format(x, 'b') for x in bytearray(byte, 'utf-8'))
integer = int(binary,2)
#integer = 7827897894342423424353646457
PentValue = to_base(integer, 5)
print(binary)
print("______________")
print(integer)
print("______________")
print(PentValue)
print("______________")
PentValue = "P" + PentValue
print(len(PentValue))

once = False
x = 0; y = 0
RC = 20
while x < RC:
    x = x + 1
    while y < RC:
        y = y + 1
        try:
            SubData.append(int(PentValue[(x-1)*RC+y],16))
        except:
            if once == False: SubData.append(1); once = True
            elif once == True: SubData.append(0)
    y = 0
    Data.append(SubData)
    SubData=[]
x = 0

#print(Data)

pyplot.figure(figsize=(RC,RC))
colormap = colors.ListedColormap(["white","red","#00FF00","blue","black"])
pyplot.imshow(Data,cmap=colormap)#tab20,tab20b,tab20c
pyplot.axis('off')
pyplot.tight_layout()
pyplot.savefig('foo.png', dpi = 1)
pyplot.show()


#os.chdir('D:\\hash lip\\test')
img=Image.open('foo.png')
a=img.convert("P", palette=Image.Palette.ADAPTIVE, colors=5)
a.save('foocompressed.png')

PixtoPent = ""
import cv2
image = cv2.imread("foocompressed.png")
pixel= image[0,0]
for row in image:
    for pixel in row:
        PixtoPent = PixtoPent + str(Pentcolours.index(str(pixel)))

# f = open('fileToWriteTo', 'wb')
# bitstreamObject.tofile(f)
while PixtoPent[-1] == "0":
    PixtoPent = PixtoPent.rstrip(PixtoPent[-1])
if PixtoPent[-1] == "1":
    PixtoPent = PixtoPent[:-1]

Decimal = int(PixtoPent,5)
print("______________")
print(PixtoPent)
print("______________")
print(Decimal)
print("______________")

Binary = to_base(Decimal,2)
#Binary = Binary.rstrip(Binary[0])
print(Binary)
print("______________")
BinArray = [];BinStr = "" ; Binlen = 0
ByteArray = []; ByteArray2 = []
for value in Binary:
    BinStr = BinStr + value
    Binlen = Binlen + 1
    if Binlen > 6: BinArray.append(BinStr);BinStr = "";Binlen = 0
print(BinArray)

for value in BinArray:
    ByteArray.append(int("0"+value,2))


#for value in BinArray:
    #ByteArray2.append(bytearray.fromhex('{:0192x}'.format(value)))
    #print(bytes(str((chr(int(value,2))))).encode(encoding='ascii'), encoding='ascii')
    #ByteArray2.append(bytes(chr(int(value, 2))))
    
print(ByteArray)
print(ByteArray2)
#text = binascii.b2a_uu(BinArray[1])
# print(text)
# newFile = open("FileGenerated.txt", "wb")
# write to file
# ByteArray = bytes(ByteArray)
# newFile.write(ByteArray)

if integer == Decimal:
    print("data is same as before")

f = open('FileGenerated.txt', 'w')
for value in ByteArray:
    if value == "32": f.write(" ")
    elif value == "92": commandtrigger = True
    elif value == "110" and commandtrigger == True: f.write(os.linesep)
    else: f.write(chr((value)))
    #f.write(chr((value)))


