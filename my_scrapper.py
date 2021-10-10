#Refer Readme file for setup instruction

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

auton = webdriver.ChromeOptions()
auton.add_argument("headless");
driver = webdriver.Chrome(options=auton, executable_path="C:/Users/Abhishek/Desktop/chromedriver.exe")

def getSGPA(roll):
    try:
        driver.find_element_by_id('txtrollno').clear()
        driver.find_element_by_id('txtrollno').send_keys(roll)
        driver.find_element_by_id('btnSearch').click()
        sl = Select(driver.find_element_by_id('ddlResult'))
        sl.select_by_visible_text('REGULAR (2020-21) Semester 5-6')
        driver.find_element_by_id('btnGo').click()
#         obtmrk = driver.find_element_by_id('lblsgpaodddisp').text
#         obtmark2=driver.find_element_by_id('lblsgpaevendisp').text
        obtmark3=driver.find_element_by_id('lbltotlmarksDisp').text
        name = driver.find_element_by_id('lblname').text
#         return [obtmrk,obtmark2,obtmark3,name]
        return [obtmark3,name]
    except:
        print("Roll number ", roll, ' not available')
        return ["NA","NA"]

def main():


    ##### BRANCH SELECTION ######
    print("ENTER YOUR BRANCH CODE- ")
    print("CE:1   CS:2   EE:3   EL:4  ME:5   IT:6")
    branch_code = int(input())
    ########################
    
    
    print("Fetching Result...")
    driver.get('https://govexams.com/knit/searchresult.aspx')
    names=[]
    SGPA_odd=[]
    SGPA_even=[]
    CGPA=[]
    roll=[]
    focus=[]
    lim1=18000 + branch_code*100 + 1
    lim2=18000 + branch_code*100 + 70
    lim3=198000 + branch_code*100 + 1
    lim4=198000 + branch_code*100 + 8
    lateral=[y for y in range(lim3,lim4)]
    regular=[x for x in range(lim1,lim2)]
    regular.extend(lateral)
    focus.extend(regular)
    for i in focus:
        temp = getSGPA(i)
        if(temp[1] != "NA"):
#             names.append(temp[3])
            names.append(temp[1])
#             SGPA_odd.append(temp[0])
#             SGPA_even.append(temp[1])
#             CGPA.append(temp[2])
            CGPA.append(temp[0])
            roll.append(i)
        driver.execute_script("window.scrollTo(0,200)")
        # if(input("To see next press Enter : ")==""):
        #     driver.back()
        #     print("Currently Displaying :",i+1)
        #     continue
        driver.back()
#     dct={"Roll No.": pd.Series(roll).astype(int),"Name":pd.Series(names),"SGPA_odd":pd.Series(SGPA_odd),"SGPA_even":pd.Series(SGPA_even),"CGPA":pd.Series(CGPA)}
    dct={"Roll No.": pd.Series(roll).astype(int),"Name":pd.Series(names),"CGPA":pd.Series(CGPA)}
    df=pd.DataFrame(dct);
    file_name='Result_'+str(branch_code)+'.csv'
    df.to_csv(file_name,index=False)
    print("DONE")

if __name__ == "__main__":
    main()
