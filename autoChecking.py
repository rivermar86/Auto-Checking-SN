#Marco A. Razo
#Program to automate SN check proccess
#01/2021

from selenium import webdriver
import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox 

myWin = Tk()
textArea = Text(myWin, width='18', height='11')
driver = webdriver.Chrome('C:\\Users\\MarcoA_Rivera.FOX-GDL\\Desktop\\Python\\AutomateCheking\\chromedriver.exe')
#driver = webdriver.Chrome('.exe\\selenium\\webdriver')
imgtitle = PhotoImage(file=r"C:/Users/MarcoA_Rivera.FOX-GDL/Desktop/Python/AutomateCheking/Title.gif")
#imgtitle = PhotoImage(file=r".gif\\Title.gif")

def theWindow():
    global lstBox, textArea
    myWin.geometry('376x380')
    textArea.config(font=('Consolas',17))
    btnDone = Button(myWin, text='Process', command=autoChecking)
   
    imgFrame = Label(myWin,image=imgtitle)
    labQty = Label(myWin,text='Qty:')
    lstBox = ttk.Combobox(myWin, width=10,height=12,state='readonly')
    lstBox.set('1')
    lstBox['value'] = ['1','2','3','4','5','6','7','8','9','10']
    lstBox.bind('<<ComboboxSelected>>', selection_changed)
     
    imgFrame.place(x=1,y=1) 
    labQty.place(x=253,y=70)
    textArea.place(x=4,y=70)
    lstBox.place(x=283,y=70)
    btnDone.place(x=283,y=98)
    return myWin

def selection_changed(event):
    textArea.delete(1.0,END)
    textArea.focus()
    
def autoChecking(): 
    selection = int(lstBox.get())
    dataText = textArea.get(1.0, END)  #get all values from textArea
    dataList = dataText.split()        #convert String to List
    #
    driver.maximize_window()
    try:
        driver.get('http://10.12.176.30:8080/GDLSFC/index.html')
    except:
        driver.execute_script("alert('Page not found, check the Internet Connection')")
        time.sleep(14)
        pass
   
    userBox = driver.find_element_by_name('Uname')
    userBox.send_keys('SFC')

    passBox = driver.find_element_by_name('Pwd')
    passBox.send_keys('SFC')

    btnLogin = driver.find_element_by_name('button')
    btnLogin.click()
    #time.sleep(2)
    
    driver.switch_to_frame(driver.find_element_by_name("contentFrame"))
    driver.switch_to_frame(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/iframe"))

    x=driver.find_element_by_xpath("/html/body/div[2]/div[1]/a[2]")
    x.click()
    
    y=driver.find_element_by_id('node2101005')
    y.click()

    #return again to switch to another frame
    driver.switch_to_default_content()
    driver.switch_to_frame(driver.find_element_by_name("contentFrame"))
    driver.switch_to_frame(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[3]/iframe"))
    driver.switch_to_frame(driver.find_element_by_xpath('/html/frameset/frame[1]'))  
    tag=[]
    screen =[]
    
    for x in range(len(dataList)):
        #type SerialNumber
        btnSN = driver.find_element_by_name('PPID')
        btnSN.send_keys(dataList[x])
        #press button
        btnSubmit = driver.find_element_by_name('query')
        btnSubmit.click()
        time.sleep(6.8)
        btnSN = driver.find_element_by_name('PPID').clear()
        
        driver.switch_to_default_content()
        driver.switch_to_frame(driver.find_element_by_name("contentFrame"))    
        driver.switch_to_frame(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[3]/iframe"))
        driver.switch_to_frame(driver.find_element_by_xpath('/html/frameset/frame[2]'))
        try:
            result = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[4]/td[3]/b/font').text
            tag.append(result)                                      #save tag result in the list
            screen.append(str(dataList[x] + '  - ' ) + str(tag[x])) #do a variable with spaces to print when for done
        except:
            #if SN haven't info
            tag.append('No Data')                                      #save tag result in the list
            screen.append(str(dataList[x] + '  - ' ) + str(tag[x]))
            pass
        #return to first frame to can get the PPID
        driver.switch_to_default_content()
        driver.switch_to_frame(driver.find_element_by_name("contentFrame"))
        driver.switch_to_frame(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[3]/iframe"))
        driver.switch_to_frame(driver.find_element_by_xpath('/html/frameset/frame[1]')) 
       
    screen = '\n\n'.join(screen)  
    tkinter.messagebox.showinfo(' * RESULT *',screen)
    #driver.switch_to_frame(driver.find_element_by_name("contentFrame"))
    #driver.switch_to_frame(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/iframe"))
myWin = theWindow()
myWin.mainloop()
