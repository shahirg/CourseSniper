from twilio.rest import Client

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from mydata import credentials as cred
from mydata import get_data
from get_depts import depts
from course import Course

from time import sleep
from datetime import datetime
from timeit import default_timer as timer

import os,sys,time





class CourseSniper:
    def __init__(self,course):
        
        self.start = time.time()
        self.registered = False #true : open and regustered
        self.app_status = 'initializing'
        self.course = course

    
        self.options = Options()
        self.options.headless = True
        self.set_up_driver()

        while(not self.registered):
            current_time = float(datetime.now().strftime("%H.%M"))
            if current_time < 2.00 or current_time > 6.30:
                self.driver.refresh()
                self.open_course()
                print(self.app_status+' - Time: '+datetime.now().strftime("%I:%M:%S %p %m/%d/%y")+ ' - Up Time: ' +self.up_time()+'\n')
                sleep(10)
            else:
                self.going_to_sleep(current_time)
                self.set_up_driver()
                
        print('\n'+self.app_status)
        self.driver.quit()
    
    def going_to_sleep(self,current_time):
        #self.send_text("Course Sniper going to Sleep at " + str(current_time))
        self.driver.quit()
        print('SLEEPING')
        sleep(60*60*(6-int(current_time)) + (30-((current_time-float(int(current_time)))*100))*60 + 5)
        post_sleep = datetime.now().strftime("%H:%M")
        #self.send_text("Course Sniper reactivating at " + post_sleep)

    def set_up_driver(self):
        self.driver = webdriver.Chrome('C:\Webdrive\chromedriver', options = self.options)
        self.driver.get('https://sis.rutgers.edu/soc/#home')
        self.open_semester() 

    def up_time(self):
        end = time.time()
        days,rem = divmod(end - self.start,3600*24)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        return str("{:0>1}:{:0>2}:{:0>2}:{:05.2f}".format(int(days),int(hours),int(minutes),seconds)) 

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
        #self.open_course()
        self.enter_course()

    def enter_course(self):
        while(True):
            try: 
                sleep(.5)  
                self.driver.find_element_by_xpath("//div[@id = 'widget_dijit_form_FilteringSelect_0']").click()
                dept = self.driver.find_element_by_xpath("//input[@id = 'dijit_form_FilteringSelect_0']")
                dept.send_keys(self.course.dept)
                sleep(2)
                dept.send_keys(Keys.ENTER)
                break
            except NoSuchElementException as err:
                print('Waiting on Frame to Load....')
        sleep(2)

    def open_course(self):  
        count = 0       
        while(True):
            sleep(.5)
            try:
                self.driver.find_element_by_xpath("//span[@id = 'courseId."+self.course.course_num+"']").click()
                break
            except NoSuchElementException:
                count+= 1
                if(count > 10):
                    self.driver.refresh()
                    print("TIMED OUT - Refreshing")
                    count = 0
                #print('Trying to Find Course...')
        self.get_coures_status()
               

    def get_coures_status(self):
        for section in self.course.indexes:
            status = self.driver.find_element_by_xpath("//span[text() = '"+section+"']/../span[@class ='sectionDataNumber']/span")
            self.app_status = 'Check Complete: Section Closed'
            
            if ("sectionopen" in status.get_attribute("class")):        
                self.driver.find_element_by_xpath("//span[text() = '"+section+"']/../span[@class= 'register']/a").click()
                #driver.find_element_by_xpath("//input[@id='submit']").click()            
                sleep(1)

                #login
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.log_in()

                if self.course.drop != None:
                    drop_course(driver,self.course.drop)
                sleep(2)

                self.register()
                break;
            
    def register(self):
        while(True):
            try:
                self.driver.find_element_by_xpath("//input[@id='submit']").click()
                break
            except NoSuchElementException:
                print("waiting on WebReg")
                sleep(1)
        self.send_text('Registration for '+self.course.course_num+' complete')
        self.send_text('Registration for '+self.course.course_num+' complete',num = "c")
        self.driver.find_element_by_xpath("//a[@href= 'logout.htm']").click()
        self.registered = True
        self.app_status = 'Registration Complete'

    def drop_course(self):  
        try:
            self.driver.find_element_by_xpath("//em[text()='["+self.course.drop.index+"]']/../../../..//input[@value='Drop']").click()
        except NoSuchElementException: 
            print(self.course.drop.course_num + ' is not in your schedule')
            return

        alert_obj = driver.switch_to.alert
        alert_obj.accept()
        send_text(self.course.drop.course_num + ' has been dropped')
        send_text(self.course.drop.course_num + ' has been dropped',num = "c")
        print(self.course.drop.course_num + ' has been dropped')

    def send_text(self,message,num = "me"):
        client = Client(cred.account_num,cred.auth_tok)
        client.messages.create(
            to=cred.numbers[num], 
            from_=cred.twilio_num,
            body=(message)) 
    
    def log_in(self):
        while(True):
            try:
                sleep(1)
                netid = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='username']")
                password = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='password']")
                break
            except NoSuchElementException:
                print('Waiting on Login Page')
        #netid.send_keys(get_data.username)

        try:
            netid.send_keys(get_data.username)
            password.send_keys(get_data.password)
        except StaleElementReferenceException:
            sleep(1)
            password = self.driver.find_element_by_xpath("//body/div/div/form/fieldset/div/input[@id ='password']")
            password.send_keys(get_data.password)
  

        
        #password.send_keys(Keys.ENTER)
        


soft_meth_sections = ['04672','04670','04671','04673']
net_sec = Course('14:332:424','10765')
soft_meth = Course('01:198:213',indexes = soft_meth_sections,drop = net_sec)
gen_psych = Course('01:830:101','07226',drop = net_sec)
net_sec.drop= gen_psych
soc_sections = ['07450', '07451', '07452', '07453', '07454', '07455']
soc = Course('01:920:101',index='07460')


if(__name__ == "__main__"):
    c = CourseSniper(soc)
