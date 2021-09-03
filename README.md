# KNIT_Result_bot
Eager to see results of your classmates but toooo lazy to type each and every roll number. Then,this is comes to play.Run this and you are ready to go. 

####################################################################################################
Setup Instruction :
Install these libraries :

1: Selenium

2: pandas


###################################################################################################


Software needed :
Chromedriver.exe 

Link to download chrome driver : https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/

Or you can download from repo.


###################################################################################################


Some Changes you need to do in code :
1. The path of the downloaded chromedriver.exe file in code.(Needed)
2. Roll number range inside for loop.
3. Session and semester name in the code.


##################################################################################################
if you just want to save result in csv file then comment theses lines in code:

if(input("To see next press Enter : ")==""):
            driver.back()
            print("Currently Displaying :",i+1)
            continue
 
##### and in place of this add a line:
driver.back()

### and also you can uncomment the line :
auton.add_argument("headless");   //this make the browser to work in background



