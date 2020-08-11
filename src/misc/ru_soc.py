from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
import os
import csv
import shutil
from get_depts import depts

#depts = {'332':'ELECTRICAL AND COMPU. (332)'}
def scrape():
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
            break
        except NoSuchElementException as err:
            print(err)
    
    for value in depts.values():
        value =  strip_periods(valid_dir(value)) 
        driver.find_element_by_xpath("//div[@id = 'widget_dijit_form_FilteringSelect_0']").click()
        dept = driver.find_element_by_xpath("//input[@id = 'dijit_form_FilteringSelect_0']")
        dept.clear()
        dept.send_keys(value+ Keys.ENTER)

        try:
            os.mkdir('SOCData\\'+value)
        except FileExistsError:
            shutil.rmtree('SOCData\\'+ (value))
            os.mkdir('SOCData\\'+value)
        exists = os.path.exists('SOCData\\' + value + '\\' + value +'.csv')
        
        with open ('SOCData\\'+ value +'\\' + value + '.csv','w') as dept_file:
            print('SOCData\\'+ value +'\\' + value + '.csv')
            writer = csv.writer(dept_file, delimiter = ',')
            if exists == False:
                writer.writerow(['Course Id', 'Course Name'])
                exists = True
            sleep(2)
            course_ids = driver.find_elements_by_xpath("//span[@id = 'courseId']/span/span")
            course_names = driver.find_elements_by_xpath("//span[@class = 'courseTitle']/span")
            
            
                
            for i in range(len(course_ids)):
                c_name = strip_periods(valid_dir(course_names[i].text))
                c_id =  course_ids[i].text
                if(i-1>0 and (c_id == course_ids[i-1].text)):
                    print(c_id+'dupe')
                    continue
                sleep(1)
                clicks = driver.find_elements_by_xpath("//span[@id = 'courseId."+ c_id+"']/..")
                for element in clicks:
                    element.click()
                writer.writerow([ c_id, c_name])
                
                mode = 'w'
                try:
                    os.mkdir('SOCData\\'+value+'\\'+ c_id.split(':')[2]+ (c_name)) 
                except FileExistsError:
                    print('Dupe Class: '+ c_id+' '+c_name+' ')
                    mode = 'a'


               
                instructor_tag = "//span[text() = '"+ c_id+"']/../../../..//span[@class = 'instructors']"
                index_tag = "//span[text() = '"+ c_id+"']/../../../..//span[@class = 'sectionIndexNumber']"
                section_tag = "//span[text() = '"+ c_id+"']/../../../..//span[@class = 'sectionopen'] |//span[text() = '"+ c_id+"']/../../../..// span[@class = 'sectionclosed']"

                
                indexes = driver.find_elements_by_xpath(index_tag)
                sections = driver.find_elements_by_xpath(section_tag)
                instructors = driver.find_elements_by_xpath(instructor_tag)

                with open ('SOCData\\'+ value +'\\'+ c_id.split(':')[2]+ (c_name) +'\\'+ (c_name)+'.csv',mode) as course_file:
                   
                    sec_writer = csv.writer(course_file, delimiter = ',')
                    sec_writer.writerow(['Section','Index','Instructor'])
                    for j in range(len(indexes)):
                        sec_writer.writerow([sections[j].text,indexes[j].text,instructors[j].text])
                        
                    

              

            
          #driver.find_element_by_xpath("//span[@id = 'courseId."+ c_id+"']/..").click()
                
        
    print('Done')
    sleep(500)
def valid_dir(dir_name):
    delims = "<>*:|/\\?\""
    if dir_name =='':
        return ''
    if(dir_name[0] in delims):
        return '_' + valid_dir(dir_name[1:])
    return dir_name[0] + valid_dir(dir_name[1:])

def strip_periods(string):
    if '.' in (string[-1]):
        return strip_periods(string[:-1])
    return string
    

  
scrape()
#while True:
#    print(strip_periods(input()))

# sec_tag = "//span[text() = '"+ course_ids[i]+"']/../../..//span[@class = 'courseOpenSectionsDenominator']"
        # sections = ((driver.find_element_by_xpath(sec_tag).text).split(';'))[2]
        # num_sec = (f'{sections:02}')
        # for i in range (num_sec):
        #//span[@id = 'courseId']/span/span -- course_id
        #//span[@class = 'courseTitle']/span -- course_name
        #//span[text() = '33:010:272']/../../../..//div[@class = 'sectionListings']
        #//span[text() = '33:010:272']/../../../..//div[@class = 'sectionListings']
        #//span[text() = '33:010:272']/../../..//span[@class = 'courseOpenSectionsDenominator']
        #//span[text() = '33:010:272']/../../../..//span[@class = 'instructors']
        #//span[text() = '33:010:272']/../../../..//span[@class = 'sectionIndexNumber']
        #//span[text() = '33:010:272']/../../../..//span[@class = 'sectionopen'] |//span[text() = '33:010:272']/../../../..// span[@class = 'sectionclosed']    