import os
import urllib.request as ulib
from bs4 import BeautifulSoup as Soup
import ast
from selenium import webdriver
chromePath="E:/Softwares/chromedriver.exe"
driver=webdriver.Chrome(chromePath)
URL="https://www.google.com/search?rlz=1C1CHBF_enIN855IN855&biw=1536&bih=754&tbm=isch&sxsrf=ACYBGNQTD2x5SCFlYep3CPOCUxwWMw2IEw%3A1574619879203&sa=1&ei=58raXeKGDPOG4-EP5qOy4AE&q=gujrat+lorry+images+hd&oq=gujrat+lorry+images+hd&gs_l=img.3...172492.178032..178394...2.0..0.124.849.8j1......0....1..gws-wiz-img.......35i39.Bj-KmjPSehc&ved=0ahUKEwiilrmUvIPmAhVzwzgGHeaRDBwQ4dUDCAc&uact=5"
directory="ImagesData3"
def getURLs(URL):
    driver.get(URL)
    a=input()
    page=driver.page_source
    print(page)
    soup=Soup(page)
    desiredURLs=soup.findAll('div',{'class':'rg_meta notranslate'})
    ourURLs=[]
    for url in desiredURLs :
        theURL=url.text
        theURL=ast.literal_eval(theURL)['ou']
        ourURLs.append(theURL)
    return  ourURLs
def save_images(URLs,directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for i,url in enumerate(URLs):
        savePath=os.path.join(directory,'{:06}.jpg'.format(i))
        try:
            ulib.urlretrieve(url,savePath)
        except:
            print("Failed:",url)
URLs=getURLs(URL)
for url in URLs :
    print(url)
save_images(URLs,directory)