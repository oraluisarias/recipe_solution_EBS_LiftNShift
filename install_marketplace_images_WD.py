# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, opc
username = "cloud.admin"
identity_domain = sys.argv[1]
datacenter = sys.argv[2]
password = sys.argv[3]
# identity_domain = "gse00010217"
# zone = "z33"
# datacenter = "em3"
images = [
	{"id":"5248662","name":"EBS OS-Only Image"},
	{"id":"5514423","name":"EBS Provisioning Tools Image"},
	{"id":"10809286","name":"Oracle E-Business Suite Release 12.2.6 Demo"}
] 
# demo_central = opc.DemoCentral()
# password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]
# opcc = opc.Compute(identity_domain, zone, datacenter, username, password)

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
		# self.driver = webdriver.Firefox(firefox_profile=profile)
		self.driver = webdriver.Firefox( )
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
		time.sleep(20)
		try:
			print ("Accessing new instance menu...")
			driver.find_element_by_id("actionBtn").click()
			print ("Accessing marketplace...")
			driver.find_element_by_css_selector("#marketplaceimages > div.oj-navigationlist-item-content.oj-navigationlist-item-no-icon > span.oj-navigationlist-item-label").click()
		except Exception:
			driver.save_screenshot('screenshots/failure_'+identity_domain+'_access.png')
		for image in images:
			print ("Installing Image: ", image["id"], image["name"])
			try:
				driver.find_element_by_id("oj-inputsearch-input-searchCtrl").clear()
				driver.find_element_by_id("oj-inputsearch-input-searchCtrl").send_keys( image["name"] )
				driver.find_element_by_id("oj-inputsearch-input-searchCtrl").send_keys( Keys.ENTER )
				time.sleep(5)
				# driver.find_element_by_css_selector("div.oj-button-text").click()
				driver.find_element_by_id( image["id"] ).click()
				driver.find_element_by_id("oracleTerms").click()
				driver.find_element_by_id("actionBtn").click()
			except Exception:
				print ("Didn't find image in marketplace")
				driver.save_screenshot('screenshots/failure_' + identity_domain + '_' + image["name"] + '.png')

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
