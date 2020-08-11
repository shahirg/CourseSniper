from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 

def make_valid_dir(dir_name):
    delims = "<>*:|/\\?\""
    if dir_name =='':
        return ''
    if(dir_name[0] in delims):
        return '_' + make_valid_dir(dir_name[1:])
    return dir_name[0] + make_valid_dir(dir_name[1:])
def remove(dir_):
    ind = dir_.index('\\\\')
    while(ind>=0):
        dir_ = dir_[:ind] + dir_[ind+1:]

def element_test():
    driver = webdriver.Chrome('C:\Webdrive\chromedriver')
    driver.get('https://sis.rutgers.edu/soc/#courses?subject=332&semester=92020&campus=NB&level=U')
    course = '14:332:221'
    sleep(5)
    driver.find_element_by_xpath("//span[@id = 'courseId."+course+"']/..").click()
    sleep(2)
    instructor_tag = "//span[text() = '"+course+"']/../../../..//span[@class = 'instructors']"
    index_tag = "//span[text() = '"+course+"']/../../../..//span[@class = 'sectionIndexNumber']"
    section_tag = "//span[text() = '"+course+"']/../../../..//span[@class = 'sectionopen'] |//span[text() = '"+course+"']/../../../..// span[@class = 'sectionclosed']"

    
    indexes = driver.find_elements_by_xpath(index_tag)
    sections = driver.find_elements_by_xpath(section_tag)
    instructors = driver.find_elements_by_xpath(instructor_tag)

    sleep(5)
    for element in indexes:
        print(element.text)
    for element in sections:
        print(element)
    for element in instructors:
        print(element)
    print('done')
    sleep(500)


driver = webdriver.Chrome('C:\Webdrive\chromedriver')
driver.get('https://sis.rutgers.edu/soc/#home')
sleep(5)
driver.quit()
sleep(3)
driver.get('https://sis.rutgers.edu/soc/#home')