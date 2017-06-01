# -*- coding: utf-8 -*-
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, opc
username = "cloud.admin"
identity_domain = "gse00002320"
# identity_domain = sys.argv[1]
demo_central = opc.DemoCentral()
opcc = opc.Compute(identity_domain, "z11")
datacenter = opcc.getDataCenterShort()
password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]

class InstallMarketplaceImagesWD(unittest.TestCase):
	def setUp(self): 
		# display = Display(visible=0, size=(800, 600)).start()

		PROXY = "www-proxy.us.oracle.com"
		PROXY_PORT = 80
		profile = webdriver.FirefoxProfile()
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.http", PROXY)
		profile.set_preference("network.proxy.http_port", PROXY_PORT)
		profile.set_preference("network.proxy.https", PROXY)
		profile.set_preference("network.proxy.https_port", PROXY_PORT)
		profile.set_preference("network.proxy.ssl", PROXY)
		profile.set_preference("network.proxy.ssl_port", PROXY_PORT)
		profile.update_preferences()
		self.driver = webdriver.Firefox(firefox_profile=profile)
		# self.driver = webdriver.Firefox( )
		# self.driver = webdriver.PhantomJS()
		self.driver.implicitly_wait(30)
		if( datacenter[:2] == "em" ):
			self.base_url = "https://computeui.emea.oraclecloud.com"				
		else:
			self.base_url = "https://computeui.us.oraclecloud.com"						
		self.verificationErrors = []
		self.accept_next_alert = True
    
	def test_install_marketplace_images_w_d(self):
		driver = self.driver
		driver.get(self.base_url + "/mycompute/console/view.html?page=instances&tab=instances")
		driver.find_element_by_id("tenantDisplayName").clear()
		print ("Logging to the domain: ", identity_domain)
		driver.find_element_by_id("tenantDisplayName").send_keys(identity_domain)
		driver.find_element_by_id("signin").click()
		driver.find_element_by_id("username").clear()
		print ("Logging with the username: ", username)
		driver.find_element_by_id("username").send_keys(username)
		driver.find_element_by_id("password").clear()
		print ("Logging with the password: ", password)
		driver.find_element_by_id("password").send_keys(password)
		driver.find_element_by_id("signin").click()
		driver.implicitly_wait(30)
		print (driver.find_element_by_id("siteButton").text)

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
	sys.argv = [sys.argv[0]]	
	unittest.main()
	display.stop()
