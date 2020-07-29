from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
image_list=[]
resized_list=[]
'''
for filename in glob.glob("F:/Final_prjt-2020-1/LicPlateImages/*.jpg"):
    print(filename)
    img=Image.open(filename)
    image_list.append(img)
for image in image_list:
    image=image.resize((1347,1347))
    resized_list.append(image)
i=84
for (i,new) in enumerate(resized_list):
    new.save('{}{}{}'.format('F:/Final_prjt-2020-1/LicPlateImages/img',i+1,'.png'))
'''
from glob import glob
import cv2
pngs = glob('F:/Final_prjt-2020-1/LicPlateImages/data/*.*')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'png', img)

