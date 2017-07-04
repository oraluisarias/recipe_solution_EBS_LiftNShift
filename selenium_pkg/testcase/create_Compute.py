# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class CreateCompute(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://myservices.em2.oraclecloud.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_compute(self):
        driver = self.driver
        driver.get(self.base_url + "/mycloud/faces/cloudHome.jspx?_afrLoop=1007396872103656&_afrWindowMode=0&_adf.ctrl-state=8cpeiitmc_4")
        driver.find_element_by_id("pt1:sections:it3:gdash-svc-icon-bg:status-icon").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | null | ]]
        driver.find_element_by_id("signin").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("cloud.admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("fuzzy@7Seat")
        driver.find_element_by_id("signin").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
