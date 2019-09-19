from urllib.request import urlopen,Request
from bs4 import BeautifulSoup as soup
import openpyxl
import os

numbers=['1','2','3','4','5','6','7','8','9','0']
#-----URL-TESTER----------------------------------------------------

url='https://www.car.gr/classifieds/bikes/?condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&engine_size-to=%3C150&lang=el&offer_type=sale&registration-from=%3E2013&pg='

#url=str(input('entre url :'))
#---2013-125cc
#url='https://www.car.gr/classifieds/bikes/?condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&offer_type=sale&registration-from=>2013&engine_size-to=<150&pg='
#url='https://www.car.gr/classifieds/cars/?condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&offer_type=sale&pg='
#url='https://www.car.gr/classifieds/cars/?sort=dm&price=%3E2500&offer_type=sale&make=4&make=298&model=1093&pg='
#url='https://www.car.gr/classifieds/vans/?condition=Καινούριο&condition=Μεταχειρισμένο&offer_type=sale&pg='




hdr={'User-Agent' : 'Firefox/5.0'}

#-----finding the amount of pages----------------------

client=Request(url,headers=hdr)
page=urlopen(client)
page=soup(page,'html.parser')

pages=page.findAll("a")
counter =0 
for i in pages:
    if(i.text=="«"):
        break
    counter += 1
max_pages=pages[counter+4].text
#-----------------------------------------
    

       
#------CREATING LISTS FOR Excel-------------------
brand_a=[]
money_a=[]
cronologia_a=[]
distance_a=[]
region_a=[]
fuel_a=[]
auto_a=[]
discription_a=[]
#----------------------------------------------

#-------SET UP THE AMOUNT OF DATA--------------

pages=15
print("The max pages availiable :",max_pages,"\n")
print("Running on : ",pages,"pages")
#-----------------------------------------------


#-----STARTING TO LOOP THROW THE PAGES---------------
urlk=url
for i in range(1,pages):
    urlk=url+str(i)
    client=Request(urlk,headers=hdr)
    try:    
        page=urlopen(client)
    except ConnectionResetError:
        print('Reconectinig...')
        client=Request(urlk,headers=hdr)
        page=urlopen(client)
      
    page=soup(page,"html.parser")
    
    
    brand=page.findAll("div",{"class":"det_container"})
    print(brand[0].text)
    money=page.findAll("span",{"itemprop":"price"})
    print(money[0].text)
    cronologia=page.findAll("span",{"itemprop":"releaseDate"})
    print(cronologia[0].text)
    distance=page.findAll("span",{"class":"lrmileage colorize"})
    fuel=page.findAll("span",{"class":"fueltype colorize"})
    auto=page.findAll("span",{"class":"transmision colorize"})
    region=page.findAll("span",{"itemprop":" addressRegion "})
    discription=page.findAll("div",{"class":"extras"})
    
    
    #---------------appends-----------

    for i in brand:
        brand_a.append(i.text)
    for i in cronologia:
        cronologia_a.append(i.text)
    for i in money:
        money_a.append(i.text)
    for i in distance:
        distance_a.append(i.text)
    for i in fuel:
        fuel_a.append(i.text)
    for i in auto:
        auto_a.append(i.text)
    for i in region:
        region_a.append(i.text)
    for i in discription:
        discription_a.append(i.text)
        
        
        
    
    urlk=url
#---CHECK PRINT
print(brand_a,cronologia_a,money_a,distance_a,fuel_a,auto_a,region_a)
print('\n')
print(len(brand_a),len(cronologia_a),len(money_a),len(distance_a),len(fuel_a),len(auto_a),len(region_a))

 #--------Excel-----------------


name=input("Type the name of the excel file :")
name=name+".xlsx"

wb = openpyxl.load_workbook(name)

creation=0
if (creation==0):
    creation=1
    wb.create_sheet(title='sheet1',index=0)
sheet=wb.get_sheet_by_name('sheet1')
#--initiialinzing ---------
sheet['A1'].value='ONOMATA'
sheet['B1'].value='TΙΜΗ'
sheet['C1'].value='Khm'
sheet['D1'].value='Fuel Type'
sheet['E1'].value='Date of Man.'
sheet['F1'].value='Location-T.K.'
sheet['G1'].value='Descrption'
sheet['J1'].value='Auto/Manual'

#--writing python in ---
for i in range(0,len(brand_a)):
    sheet['A'+str(i+2)].value=brand_a[i]
for i in range(0,len(brand_a)):
    sheet['B'+str(i+2)].value=money_a[i]
for i in range(0,len(brand_a)):
    sheet['C'+str(i+2)].value=distance_a[i]    
for i in range(0,len(brand_a)):
    sheet['D'+str(i+2)].value=fuel_a[i]
for i in range(0,len(brand_a)):
    sheet['E'+str(i+2)].value=cronologia_a[i]
for i in range(0,len(brand_a)):
    sheet['F'+str(i+2)].value=region_a[i]
for i in range(0,len(brand_a)):
    sheet['G'+str(i+2)].value=discription_a[i]


wb.save(name)
