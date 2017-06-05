# -*- coding: utf-8 -*-
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, opc, json
username = "cloud.admin"
identity_domain = sys.argv[1]
# identity_domain = "gse00011455"
password = sys.argv[2]
# password = "ablAtivE@4Iowa"
# demo_central = opc.DemoCentral()
opcc = opc.Compute(identity_domain, "z11", "", username, password)
datacenter = opcc.getDataCenterShort()
# password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]

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
		self.driver = webdriver.Firefox( )
		# self.driver = webdriver.Firefox(firefox_profile=profile)
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
		# print ("Logging to the domain: ", identity_domain)
		driver.find_element_by_id("tenantDisplayName").send_keys(identity_domain)
		driver.find_element_by_id("signin").click()
		driver.find_element_by_id("username").clear()
		# print ("Logging with the username: ", username)
		driver.find_element_by_id("username").send_keys(username)
		driver.find_element_by_id("password").clear()
		# print ("Logging with the password: ", password)
		driver.find_element_by_id("password").send_keys(password)
		driver.find_element_by_id("signin").click()
		driver.implicitly_wait(45)
		driver.find_element_by_id("siteButton").click()		
		time.sleep(3)
		driver.find_element_by_id("cancelBtn").click()
		time.sleep(3)		
		driver.find_element_by_id("siteButton").click()
		time.sleep(3)
		siteIndex = 0
		sitesFound = []
		sites = {}
		for siteIndex in range (0, 4):
			driver.implicitly_wait(25)
		# while siteIndex == 0:
			driver.find_element_by_id('ojChoiceId_siteSelect').click()
			driver.implicitly_wait(5)
			driver.find_element_by_id('ojChoiceId_siteSelect').send_keys(Keys.ARROW_DOWN);
			driver.find_element_by_id('ojChoiceId_siteSelect').send_keys(Keys.RETURN);
			driver.implicitly_wait(30)
			site = driver.find_element_by_id("ojChoiceId_siteSelect_selected").text
			site_parts = site.split("_")
			ocpu = driver.find_element_by_id('ocpuGauge').get_attribute("aria-label")
			memory = driver.find_element_by_id('memoryGauge').get_attribute("aria-label")
			ips = driver.find_element_by_id('ipReservationsGauge').get_attribute("aria-label")
			# if not hasattr(sites, site):
			siteArray = {
				"ocpu":ocpu.lstrip('Data Visualization: Gauge.').strip(), 
				"memory":memory.lstrip('Data Visualization: Gauge.').strip(), 
				"ips":ips.lstrip('Data Visualization: Gauge.').strip(), 
				"site":site,
				"datacenter":site_parts[0],				
			}
			
			if site_parts.length > 1 :
				siteArray["zone"] = site_parts[1]

			sites[site] = siteArray
			driver.implicitly_wait(10)			    
		print ( json.dumps( { identity_domain:sites } ) )		

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
