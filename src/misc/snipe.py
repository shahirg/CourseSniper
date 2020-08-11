from twilio.rest import Client

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

import credentials as cred
from get_depts import depts

from time import sleep
from datetime import datetime
from timeit import default_timer as timer

import os,sys

def get_password():
    with open('secrets.txt','r') as file:
        password = file.readline()
    return password

class Course:
 
    def __init__(self,course_num,index,drop=None,drop_index=None):
        self.dept = depts[course_num[3:6]]
        self.course_num = course_num
        self.index = index
        self.drop = drop
        self.drop_index = drop_index

    


    



def snipe():
    driver = webdriver.Chrome('C:\Webdrive\chromedriver')
    driver.get('https://sims.rutgers.edu/webreg/')

    driver.find_element_by_xpath("//a[@href = 'chooseSemester.htm?login=cas']").click()
    #login
    netid = driver.find_element_by_xpath("//input[@id = 'username']")
    password = driver.find_element_by_xpath("//input[@id = 'password']")

    netid.send_keys('sag315')
    password.send_keys(get_password())
    driver.find_element_by_xpath("//input[@class = 'btn-submit']").click()
   
    #Choose semester
    driver.find_element_by_xpath("//input[@id = 'semesterSelection4']").click()
    driver.find_element_by_xpath("//input[@id = 'submit']").click()

    driver.find_element_by_xpath("//a[@href = 'courseLookup.htm?_flowId=lookup-flow']").click()
    
    #Search NB U
    driver.switch_to_frame("iframe2")
    driver.find_element_by_xpath("//span[text()=' New Brunswick']").click()
    driver.find_element_by_xpath("//span[text()='Undergraduate']").click()
    driver.find_element_by_xpath("//button[@id = 'continueButton']").click()
    sleep(3)

    #find input and insert
    driver.switch_to_default_content()
    driver.switch_to_frame("iframe2")
    driver.find_element_by_xpath("//div[@id = 'widget_dijit_form_FilteringSelect_0']").click()
    dept = driver.find_element_by_xpath("//input[@id = 'dijit_form_FilteringSelect_0']")
    dept.send_keys(soft_meth.school+ Keys.ENTER)

    sleep(3)
    #driver.find_element_by_xpath("//span[@onclick = 'CourseService.expandOrCollapseCourse(\"01:198:213.8\");']").click()
    
    #get course
    driver.find_element_by_xpath("//span[@id = 'courseId."+soft_meth.course_num+"']").click()
    status = driver.find_element_by_xpath("//span[text() = '"+soft_meth.index+"']/../span[@class ='sectionDataNumber']/span")

    if "sectionclosed" in status.get_attribute("class"):
        driver.find_element_by_xpath("//span[text() = '"+soft_meth.index+"']/../span[@class= 'register']/a").click()
        driver.find_element_by_xpath("//input[@id='submit']").click()
        send_text('Registration for Software Meth complete')
        print('closed')
    sleep(3333)
    #driver.close

class CourseSniper:
    def __init__(self,course):
        self.registered = False #true : open and regustered
        self.app_status = 'initializing'
        if not self.check_connection():
            print('No able to Connect')
        else:
            self.course = course
            self.driver = webdriver.Chrome('C:\Webdrive\chromedriver')
            self.driver.get('https://sis.rutgers.edu/soc/#home')
            self.open_semester() 
            print('\n'+self.app_status)
            self.driver.quit()
            
        
    def check_connection(self):
        if(str(os.system("ping rutgers.edu")) == '1'):
            return False
        return True

    def open_semester(self):
        count = 0
        while (True):
            try:
                sleep(1)
                self.driver.find_element_by_xpath("//span[text()='Fall 2020']").click()
                self.driver.find_element_by_xpath("//span[text()=' New Brunswick']").click()
                self.driver.find_element_by_xpath("//span[text()='Undergraduate']").click()
                self.driver.find_element_by_xpath("//button[@id = 'continueButton']").click()
                break
            except NoSuchElementException:
                count += 1
                print('Waiting on Page to Load')
                if(count > 10):
                    print('Timed out on Term Page')
                    self.driver.refresh()
                    count = 0                   
            except ElementNotInteractableException:
                self.driver.refresh()
        self.open_course()
    
    def open_course(self):
        while(True):
            try: 
                sleep(1)  
                self.driver.find_element_by_xpath("//div[@id = 'widget_dijit_form_FilteringSelect_0']").click()
                dept = self.driver.find_element_by_xpath("//input[@id = 'dijit_form_FilteringSelect_0']")
                dept.send_keys(self.course.dept+ Keys.ENTER)
                break
            except NoSuchElementException as err:
                print('Waiting on Frame to Load')
            
        while(True):
            sleep(1)
            try:
                self.driver.find_element_by_xpath("//span[@id = 'courseId."+self.course.course_num+"']").click()
                break
            except NoSuchElementException:
                print('Trying to Find Course')
        self.get_coures_status()        

    def get_coures_status(self):
        status = self.driver.find_element_by_xpath("//span[text() = '"+self.course.index+"']/../span[@class ='sectionDataNumber']/span")
        print(status.get_attribute("class"))
        self.app_status = 'Check Complete: Section Closed'
        
        if "sectionopen" in status.get_attribute("class"):        
            self.driver.find_element_by_xpath("//span[text() = '"+self.course.index+"']/../span[@class= 'register']/a").click()
            #driver.find_element_by_xpath("//input[@id='submit']").click()            
            sleep(1)

            #login
            self.driver.switch_to.window(self.driver.window_handles[1])
            while(True):
                try:
                    netid = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='username']")
                    password = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='password']")
                    break
                except NoSuchElementException as err:
                    print('Waiting on Login page')
            
            netid.send_keys('sag315')
            password.send_keys(get_password() + Keys.ENTER)

            if self.course.drop != None:
                drop_course(driver,self.course.drop)
            sleep(2)
            self.driver.find_element_by_xpath("//input[@id='submit']").click()
            send_text('Registration for '+self.course.course_num+' complete')
            self.registered = True
            self.driver.find_element_by_xpath("//a[@href= 'logout.htm']").click()
            self.app_status = 'Check Complete: Registered'
            
        
    def drop_course(self):  
        try:
            self.driver.find_element_by_xpath("//em[text()='["+self.course.drop.index+"]']/../../../..//input[@value='Drop']").click()
        except NoSuchElementException: 
            print(self.course.drop.course_num + ' is not in your schedule')
            return

        alert_obj = driver.switch_to.alert
        alert_obj.accept()
        send_text(self.course.drop.course_num + ' has been dropped')
        print(self.course.drop.course_num + ' has been dropped')

    def send_text(self,message):
        client = Client(cred.account_num,cred.auth_tok)
        client.messages.create(
            to=cred.numbers["me"], 
            from_=cred.twilio_num,
            body=(message)) 
    
    def log_in(self):
        while(True):
            try:
                sleep(1)
                netid = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='username']")
                password = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='password']")
                break
            except NoSuchElementException as err:
                print(err)
        netid.send_keys('sag315')
        password.send_keys(get_password() + Keys.ENTER)

def snipeV2(course_):
    driver = webdriver.Chrome('C:\Webdrive\chromedriver')
    
    #driver.minimize_window()
    driver.get('https://sis.rutgers.edu/soc/#home')
    

    #driver.switch_to_frame("iframe2")
    sleep(1)
    driver.find_element_by_xpath("//span[text()='Fall 2020']").click()
    driver.find_element_by_xpath("//span[text()=' New Brunswick']").click()
    driver.find_element_by_xpath("//span[text()='Undergraduate']").click()
    driver.find_element_by_xpath("//button[@id = 'continueButton']").click()

    while(True):
        try:
            sleep(1)
            driver.find_element_by_xpath("//div[@id = 'widget_dijit_form_FilteringSelect_0']").click()
            dept = driver.find_element_by_xpath("//input[@id = 'dijit_form_FilteringSelect_0']")
            dept.send_keys(course_.dept+ Keys.ENTER)
            break
        except NoSuchElementException as err:
            print('Waiting on Frame to Load')
    
    
    sleep(2)
    while(True):
        try:
            driver.find_element_by_xpath("//span[@id = 'courseId."+course_.course_num+"']").click()
            break
        except NoSuchElementException:
            print('Trying to Find Course')

    status = driver.find_element_by_xpath("//span[text() = '"+course_.index+"']/../span[@class ='sectionDataNumber']/span")

    print(status.get_attribute("class"))
    if "sectionopen" in status.get_attribute("class"):
        
        driver.find_element_by_xpath("//span[text() = '"+course_.index+"']/../span[@class= 'register']/a").click()
        #driver.find_element_by_xpath("//input[@id='submit']").click()
        
        sleep(1)
        #login
        driver.switch_to.window(driver.window_handles[1])
        while(True):
            try:
                sleep(1)
                netid = driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='username']")
                password = driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='password']")

                break
            except NoSuchElementException as err:
                print(err)
        
        netid.send_keys('sag315')
        password.send_keys(get_password() + Keys.ENTER)

        if course_.drop != None:
            drop_course(driver,course_.drop)
        sleep(2)
        driver.find_element_by_xpath("//input[@id='submit']").click()
        send_text('Registration for '+course_.course_num+' complete')
        driver.find_element_by_xpath("//a[@href= 'logout.htm']").click()
    print('check complete')
    driver.close()
    
    


def drop_course(driver,course_):
    try:
        driver.find_element_by_xpath("//em[text()='["+course_.index+"]']/../../../..//input[@value='Drop']").click()
    except NoSuchElementException: 
        print(course_.course_num + ' is not in your schedule')
        return

    alert_obj = driver.switch_to.alert
    alert_obj.accept()
    send_text(course_.course_num + ' has been dropped')
    print(course_.course_num + ' has been dropped')


def send_text(message):
    client = Client(cred.account_num,cred.auth_tok)
    client.messages.create(
        to=cred.numbers["me"], 
        from_=cred.twilio_num,
        body=(message))

#def log_in(driver):

net_sec = Course('14:332:424','10765')
soft_meth = Course('01:198:213','04672',drop = net_sec)
gen_psych = Course('01:830:101','07226',drop = net_sec)
net_sec.drop= gen_psych

while(True):
    current_time = float(datetime.now().strftime("%H.%M"))
    if current_time < 2.00 or current_time > 6.30:
        start = timer()
        #snipeV2(soft_meth) 
        c = CourseSniper(soft_meth)
        print("Run Time:" + str(timer()-start))
        print(datetime.now().strftime("%B %d %Y %I:%M:%S %p"))
        if(c.registered):
            break
        sleep(300)
    else:
        print(str(current_time))
        print('sleeping')
        sleep(60*60)