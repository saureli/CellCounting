import numpy as np
import pylab
import mahotas as mh
import matplotlib.pyplot as plt

image = mh.imread('E_pozzo1-1-d_2995.png')
image2=image[:,:,2]
imageB = mh.imread('E_pozzo1-1-b_2994.png')
imageB2=imageB[:,:,0]

max_objects=0
parameterC=0

imagefixed = mh.gaussian_filter(image2, 10)
imagefixedB2 = mh.gaussian_filter(imageB2, 4)
imagefixedB2ft=(imagefixedB2 < 150)
xmax = imagefixed.shape[1]
ymax = imagefixed.shape[0]

imagefixedB2border=np.empty([ymax,xmax])
for i in range(0,ymax):
   for j in range(0,xmax-1):
     if (imagefixedB2ft[i,j]!=imagefixedB2ft[i,j+1]):
#     if (imagefixedB2ft[i,j]!=imagefixedB2ft[i,j+1] and imagefixedB2ft[i,j]==True ):
        imagefixedB2border[i,j]=True
     else:
        imagefixedB2border[i,j]=False
for i in range(0,ymax):
   imagefixedB2border[i,xmax-1]=False


for i in range(0,101):
  labeled,nr_objects = mh.label(imagefixed > i)
#  print('parameter = ', i)
#  print('dapi cells = ',nr_objects)
  if (max_objects<nr_objects):
    max_objects=nr_objects
    parameterC=i
#print('dapi cells = ',max_objects)

#pylab.imshow(imagefixed > parameterC)
#pylab.show()

#xmax = imagefixed.shape[1]
#ymax = imagefixed.shape[0]

imagefixed2=np.empty([ymax,xmax])
for i in range(0,ymax):
   for j in range(0,xmax):
     if (imagefixed[i,j]<parameterC):
       imagefixed2[i,j]=0
     else:
       imagefixed2[i,j]=imagefixed[i,j]

maxima=np.empty([ymax,xmax])

for i in range(1,ymax-1):
   for j in range(1,xmax-1):
     if (imagefixed2[i,j]>imagefixed2[i,j-1] and imagefixed2[i,j]>imagefixed2[i,j+1] and imagefixed2[i,j]>imagefixed2[i-1,j] and imagefixed2[i,j]>imagefixed2[i+1,j]):
       maxima[i,j]=200
     else:
       maxima[i,j]=0

result=np.where(maxima == 200)
listOfCoordinates= list(zip(result[0], result[1]))
#print(listOfCoordinates)
seeds,nr_nuclei = mh.label(maxima)
#print(nr_nuclei)
print('dapi cells = ',nr_nuclei)

plt.rc('axes.formatter', useoffset=False)
fig = plt.figure()
ax = fig.add_subplot(223)
ax.imshow(mh.overlay(image2, maxima))
for cell in listOfCoordinates:
  y, x = cell
  c = plt.Circle((x, y), 2, color='red', linewidth=2, fill=False)
  ax.add_artist(c)

ax = fig.add_subplot(221)
ax.imshow(image)

ax = fig.add_subplot(222)
ax.imshow(imageB)

ax = fig.add_subplot(224)
ax.imshow(mh.overlay(image2, imagefixedB2ft))
#ax.imshow(mh.overlay(image2, imagefixedB2border))
for cell in listOfCoordinates:
  y, x = cell
  c = plt.Circle((x, y), 2, color='gold', linewidth=2, fill=False)
  ax.add_artist(c)

def calcDistance(x1,y1,x2,y2):
  dist = np.sqrt((x2-x1)**2 + (y2 - y1)**2)
  return dist

contatoreXGAL=0
giacontate=[]
resultxGal=np.where(imagefixedB2border == True)
listOfxGal= list(zip(resultxGal[0], resultxGal[1]))
for cell in listOfCoordinates:
  y, x = cell
  for xGalpixel in listOfxGal:
    yXG, xXG = xGalpixel
#    d = plt.Circle((xXG, yXG), 2, color='black', linewidth=2, fill=False)
#    ax.add_artist(d)
    if (calcDistance(x,y,xXG,yXG) < 50):
       if cell not in giacontate:
         giacontate.append(cell)
         contatoreXGAL +=1
         c = plt.Circle((x, y), 2, color='aqua', linewidth=2, fill=False)
         ax.add_artist(c)
print('senescent cells = ',contatoreXGAL)
plt.show()
