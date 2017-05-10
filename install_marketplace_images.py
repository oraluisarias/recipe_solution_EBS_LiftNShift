# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class install_marketplace_images(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "https://computeui.emea.oraclecloud.com/mycompute/console/view.html?page=instances&tab=instances")
        self.selenium.start()
    
    def test_install_marketplace_images(self):
        sel = self.selenium
        sel.open("/mycompute/console/view.html?page=instances&tab=instances")
        sel.type("id=tenantDisplayName", "gse00010217")
        sel.click("id=signin")
        sel.wait_for_page_to_load("30000")
        sel.type("id=username", "cloud.admin")
        sel.type("id=password", "hAtched@3LimbO")
        sel.click("id=signin")
        sel.wait_for_page_to_load("30000")
        sel.click("id=actionBtn")
        sel.click("css=#marketplaceimages > div.oj-navigationlist-item-content.oj-navigationlist-item-no-icon > span.oj-navigationlist-item-label")
        sel.type("id=oj-inputsearch-input-searchCtrl", "EBS OS-Only Image")
        sel.send_keys("id=oj-inputsearch-input-searchCtrl", "${KEY_ENTER}")
        sel.click("id=5248662")
        sel.click("id=oracleTerms")
        sel.click("id=actionBtn")
        sel.type("id=oj-inputsearch-input-searchCtrl", "EBS Provisioning Tools Image")
        sel.send_keys("id=oj-inputsearch-input-searchCtrl", "${KEY_ENTER}")
        sel.click("id=5514423")
        sel.click("id=oracleTerms")
        sel.click("id=actionBtn")
        sel.type("id=oj-inputsearch-input-searchCtrl", "Oracle E-Business Suite Release 12.2.6 Demo")
        sel.send_keys("id=oj-inputsearch-input-searchCtrl", "${KEY_ENTER}")
        sel.click("id=10809286")
        sel.click("id=oracleTerms")
        sel.click("id=actionBtn")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
