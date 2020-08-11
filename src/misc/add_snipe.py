from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_depts import depts
class AddSnipe:
    def __init__(self):
        print("Rutgers Course Sniper\n")
        course_num = input("Enter Course Number (XX:XXX:XXX): ")
        while (True):
            try:
                dept = depts[course_num[3:6]]
                break;
            except KeyError:
                course_num = input("Invalid Course Number\nEnter Course Number (XX:XXX:XXX): ")

        index = input("Enter Section Index (XXXXX): ")
        drop_index = input("Drop Course index (XXXXX:")
    
    def get_course_data():
        course_num = input("Enter Course Number (XX:XXX:XXX): ")
        index = input("Enter Section Index (XXXXX): ")
        drop_index = input("Drop Course index (XXXXX:")

AddSnipe()
    