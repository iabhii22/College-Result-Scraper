#Refer Readme file for setup instruction

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

auton = webdriver.ChromeOptions()
#auton.add_argument("headless");
driver = webdriver.Chrome(options=auton, executable_path="C:/Users/Abhishek/Desktop/chromedriver_win32/chromedriver.exe")

def getSGPA(roll):
    try:
        driver.find_element_by_id('txtrollno').clear()
        driver.find_element_by_id('txtrollno').send_keys(roll)
        driver.find_element_by_id('btnSearch').click()
        sl = Select(driver.find_element_by_id('ddlResult'))
        sl.select_by_visible_text('REGULAR (2019-20) Semester 3-4')
        driver.find_element_by_id('btnGo').click()
        obtmrk = driver.find_element_by_id('lbltotlmarksDisp').text
        name = driver.find_element_by_id('lblname').text
        return [obtmrk,name]
    except:
        print("Roll number ", roll, ' not available')
        return ["NA","NA"]

def main():
    print("Fetching Result...")
    driver.get('https://govexams.com/knit/searchresult.aspx')
    names=[]
    SGPA=[]
    roll=[]
    for i in range(18401, 18470):
        temp = getSGPA(i)
        names.append(temp[1])
        SGPA.append(temp[0])
        roll.append(i)
        driver.execute_script("window.scrollTo(0,200)")
        if(input("To see next press Enter : ")==""):
            driver.back()
            print("Currently Displaying :",i+1)
            continue
    dct={"Roll No.": pd.Series(roll).astype(int),"Name":pd.Series(names),"Marks/SGPA":pd.Series(SGPA)}
    df=pd.DataFrame(dct);
    df.to_csv('Result.csv',index=False)
    print("DONE")

if __name__ == "__main__":
    main()