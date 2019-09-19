from urllib.request import urlopen,Request
from bs4 import BeautifulSoup as soup
import openpyxl
import os,time

numbers=['1','2','3','4','5','6','7','8','9','0']
#-----URL-----------------------------------------------------

url='https://www.car.gr/classifieds/boats/?fs=1&condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&offer_type=sale&engine_power-from=%3E200&pg='
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

print("Hitting :",url,"\n\n")
print("The max pages availiable :",max_pages,"\n")
pages=int(input("How many pages you want to get ? :"))
cont=input("Continieu from another page [y/n]:")
if (cont=="y"):
    start=int(input("Where to start from : "))
    if (start<=0):
        start=1
    print("Running on : ",pages,"pages","\n","Started from :",start," page")
else:
    start=1
    print("Running on : ",pages," pages")
#-----------------------------------------------


#-----STARTING TO LOOP THROW THE PAGES---------------
urlk=url
for i in range(start,pages):
    time.sleep(1)
    urlk=url+str(i)
    client=Request(urlk,headers=hdr)
  
    page=urlopen(client)
    
    print('Reconectinig at :',i)
    client=Request(urlk,headers=hdr)
    page=urlopen(client)
    try:  
        page=soup(page,"html.parser")
    except:
        print("Error soped at :",i)
        break

    brand=page.findAll("div",{"class":"det_container"})
    money=page.findAll("span",{"itemprop":"price"})
    cronologia=page.findAll("span",{"itemprop":"releaseDate"})
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
        temp_h_m=i.text
        temp_m=''
        for y in temp_h_m:
            for k in numbers:
                if (y==k):
                    temp_m=temp_m+k
        if (temp_m==''):
            temp_m='0'
        money_a.append(int(temp_m))
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


#--------Excel-----------------
check_ex=input("Write in Excel File [y/n] :")
if (check_ex=="n"):
    exit

name=input("Type the name of the excel file :")
name=name+".xlsx"

wb = openpyxl.load_workbook(name)
sheet=wb.get_sheet_by_name('sheet1')

#--initiialinzing ---------
sheet['A1'].value='ONOMATA'
sheet['B1'].value='TΙΜΗ'
sheet['C1'].value='Khm'
sheet['D1'].value='Fuel Type'
sheet['E1'].value='Date of Man.'
sheet['F1'].value='Location-T.K.'
sheet['G1'].value='Auto/Manual'
sheet['H1'].value='Descrption'
        #----
sheet['P1'].value='ΜΕΣΗ ΤΙΜΗ'
sheet['P2'].value=sum(money_a)/len(money_a)



#--writing in excel ---
               
for i in range(0,len(brand_a)):
    sheet['A'+str(start+i+2)].value=brand_a[i]
for i in range(0,len(brand_a)):
    sheet['B'+str(start+i+2)].value=money_a[i]
for i in range(0,len(brand_a)):
    sheet['C'+str(start+i+2)].value=distance_a[i]    
for i in range(0,len(brand_a)):
    sheet['D'+str(start+i+2)].value=fuel_a[i]
for i in range(0,len(brand_a)):
    sheet['E'+str(start+i+2)].value=cronologia_a[i]
for i in range(0,len(brand_a)):
    sheet['F'+str(start+i+2)].value=region_a[i]
for i in range(0,len(brand_a)):
    sheet['G'+str(start+i+2)].value=auto_a[i]    
for i in range(0,len(brand_a)):
    sheet['H'+str(start+i+2)].value=discription_a[i]

wb.save(name)
 
