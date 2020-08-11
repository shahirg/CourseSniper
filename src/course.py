from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from get_depts import depts

class Course:
 
    def __init__(self,course_num,index = None,indexes = None,drop=None,drop_index=None):
        self.dept = depts[course_num[3:6]]
        self.course_num = course_num
        self.index = index
        self.indexes = indexes
        if(indexes != None):
            self.index = indexes[0]
        else:
            self.indexes = [index]
        self.drop = drop
        self.drop_index = drop_index

    def check_valid_course_num(self):
        try:
            dept = depts[self.course_num[3:6]]
        except KeyError:
            print("Invalid Course Number")
            return False
            

    def check_valid_course(self):
        driver = webdriver.Chrome('C:\Webdrive\chromedriver')
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
                dept.send_keys(self.dept+ Keys.ENTER)
                break
            except NoSuchElementException as err:
                print(err)   