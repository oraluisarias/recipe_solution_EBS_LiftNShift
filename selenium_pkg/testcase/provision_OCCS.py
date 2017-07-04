# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest, time, re

class ProvisionOCCS(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.PhantomJS()
        binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver.implicitly_wait(30)
        self.base_url = "https://demo.oracle.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_provision_o_c_c_s(self):
        driver = self.driver
        driver.get(self.base_url + "/apex/f?p=355:15:103154011050465::NO::P15_INSTANCE_NAME:metcs-gse00003045")
        driver.find_element_by_link_text("Login to Oracle Cloud Home").click()
        driver.find_element_by_id("signin").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("cloud.admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("fuzzy@7Seat")
        driver.find_element_by_id("signin").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=8cpeiitmc_1 | ]]
        driver.find_element_by_id("pt1:sections:it4:gdash-svc-icon-bg:status-icon").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=162i4g08s4_1 | ]]
        driver.find_element_by_id("r1:0:pt1:sections:icb112").click()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:def_iter:0:i3_r12def::content").clear()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:def_iter:0:i3_r12def::content").send_keys("GSE-OCCS")
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:def_iter:1:i3_r12def::content").clear()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:def_iter:1:i3_r12def::content").send_keys("Default GSE instance")
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:def_iter:2:keyeditdef").click()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:keyname::content").click()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:itkeyname::content").clear()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:itkeyname::content").send_keys("ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA8tfC+SBr+O7Cw+LXPjVjg0q3hOJ87Pn/xTb6tw4xe0PU5SACucgJNIonOx3jNHG2D+mn1QvAQKeE75OVuJSFUkDgcSV6MnAYk+KdSNCOco1gRCECiOHuuZPVsq1v60c5AS++hiTyfzalJQXgq/VfNerNpIUIoucug31Bj05A2p7eFI8NrCCgZr5hTAgIRhRBt77QEE/fi/XJzf81W9GfI2hpZ6+0R+62E1t3fCFq/u+u77SyrFB1+P35K5wo/mMRk/m4kSiw/w3vnZJCBgUSJ8xos4iaesxp7EeWkO5PhoS+3HRrabQELl88veHszYdDiOpi4F85LQJnCgriAfwm6w== root@demo003.us.oracle.com")
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:definitionPage:keydialog::ok").click()
        driver.find_element_by_id("r1:1:pt1ins:pt1ProvFlow:rightBtn").click()
        driver.find_element_by_id("r1:2:pt1det:pt1ProvFlow:detailsPage:leftIterator:0:i3:1:i3_r12::content").clear()
        driver.find_element_by_id("r1:2:pt1det:pt1ProvFlow:detailsPage:leftIterator:0:i3:1:i3_r12::content").send_keys("fuzzy@7Seat")
        driver.find_element_by_id("r1:2:pt1det:pt1ProvFlow:detailsPage:leftIterator:0:i3:2:i3_r12::content").clear()
        driver.find_element_by_id("r1:2:pt1det:pt1ProvFlow:detailsPage:leftIterator:0:i3:2:i3_r12::content").send_keys("fuzzy@7Seat")
        driver.find_element_by_id("r1:2:pt1det:pt1ProvFlow:rightBtn").click()
        driver.find_element_by_id("r1:3:ptcfrm:pt1ProvFlow:rightBtn").click()
    
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
