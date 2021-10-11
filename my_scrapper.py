# Refer Readme file for setup instruction

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

auton = webdriver.ChromeOptions()
auton.add_argument("headless")

###############  Change chromedriver.exe path here  #############
driver = webdriver.Chrome(options=auton, executable_path="C:/Users/Abhishek/Desktop/chromedriver.exe")
#################################################################
flag=1
def getSGPA(roll,str_ing,sems):
    global flag
    try:
        driver.find_element_by_id('txtrollno').clear()
        driver.find_element_by_id('txtrollno').send_keys(roll)
        driver.find_element_by_id('btnSearch').click()
        sl = Select(driver.find_element_by_id('ddlResult'))
        sl.select_by_visible_text(str_ing)
        driver.find_element_by_id('btnGo').click()
        try:
            obtmrk = driver.find_element_by_id('lblsgpaodddisp').text
        except:
            obtmrk=-1
        try:
            obtmark2=driver.find_element_by_id('lblsgpaevendisp').text
        except:
            obtmark2=-1
        obtmark3 = driver.find_element_by_id('lbltotlmarksDisp').text
        name = driver.find_element_by_id('lblname').text
        return [obtmrk,obtmark2,obtmark3,name]
    except:
        print("RESULT OF", roll, "FOR SEM:",end='')
        print(sems,'not available')
        return ["NA", "NA"]


while(True):
    print("ENTER YOUR BRANCH CODE- ")
    print("CE:1   CS:2   EE:3   EL:4  ME:5   IT:6")
    branch_code = int(input())
    if branch_code < 1 or branch_code > 6:
        print("WRONG CHOICE ENTERED! TRY AGAIN")
    else:
        break
branch_to_code={1:"CE",2:"CS",3:"EE",4:"EL",5:"ME",6:"IT"}


####### BATCH SELECTION############
while (True):
    print("ENTER YOUR BATCH( Ex: 2018-22 )")
    year = input()
    start_year = int(year[2:4])
    end_year = int(year[5:])
    if end_year-start_year != 4:
        print('WRONG VALUE ENTERED! TRY AGAIN')
    else:
        break


######## SEMESTER SELECTION #########
while(True):
    print("ENTER SEMESTER(should be a single digit number)-")
    sem=int(input())
    if sem < 1 or sem > 8:
        print("WRONG CHOICE ENTERED! TRY AGAIN")
    else:
        break
semester={1:"1-2",2:"1-2",3:"3-4",4:"3-4",5:"5-6",6:"5-6",7:"7-8",8:"7-8"}


########DON'T TOUCH THIS ###############################
if sem == 1 or sem == 2:
    s= str(2000+ start_year) + "-" + str(start_year+1)
elif sem==3 or sem==4 :
    s = str(2000 + start_year+1) + "-" + str(start_year + 2)
elif sem==5 or sem==6:
    s = str(2000 + start_year+2) + "-" + str(start_year + 3)
elif sem== 7 or sem == 8:
    s = str(2000 + start_year+3) + "-" + str(start_year + 4)
###########################################################


driver.get('https://govexams.com/knit/searchresult.aspx')
names = []
SGPA_odd = []
SGPA_even = []
CGPA = []
roll = []
roll_list = []

######### ROLL NO LIST GENERATION ###########
regular_start = start_year*1000 + branch_code * 100 + 1
regular_end = start_year*1000 + branch_code * 100 + 72
lateral_start = (start_year+1)*10000 + (start_year%10)*1000 + branch_code * 100 + 1
lateral_end = (start_year+1)*10000 + (start_year%10)*1000 + branch_code * 100 + 8
regular = [y for y in range(regular_start, regular_end)]
lateral = [x for x in range(lateral_start, lateral_end)]
regular.extend(lateral)
roll_list.extend(regular)
################################################

str_ing='REGULAR (' + s + ') Semester ' + semester[sem]

print("Fetching Result...")
for i in roll_list:
    temp = getSGPA(i,str_ing,semester[sem])
    if (temp[1] != "NA"):
        names.append(temp[3])
        SGPA_odd.append(temp[0])
        SGPA_even.append(temp[1])
        CGPA.append(temp[2])
        roll.append(i)
    # driver.execute_script("window.scrollTo(0,200)")
    # if(input("To see next press Enter : ")==""):
    #     driver.back()
    #     print("Currently Displaying :",i+1)
    #     continue
    driver.back()

dct={"Roll No.": pd.Series(roll).astype(int),"Name":pd.Series(names),"SGPA_odd":pd.Series(SGPA_odd),"SGPA_even":pd.Series(SGPA_even),"CGPA":pd.Series(CGPA)}
df = pd.DataFrame(dct)
nan_value = float("NaN")
df.replace(-1, nan_value, inplace=True)
df.dropna(how='all', axis=1, inplace=True)
file_name = 'Result_' + str(branch_to_code[branch_code]) + "_" + year + "_"+"Sem."+semester[sem]+ '.csv'
rslt_df = df.sort_values(by = 'CGPA', ascending = False)
rslt_df.to_csv(file_name, index=False)
print("DONE")
