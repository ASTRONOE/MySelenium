import time
import threading as trd
import multiprocessing as mp
import asyncio as aio
import concurrent.futures as cf
from tiktok_act import follow_account, launch_post
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://www.tiktok.com/'
#chrome profile path
chrome_profile_path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
#edge profile path
edge_profile_path = r"C:\Users\user\AppData\Local\Microsoft\Edge\User Data"

# Optional settings (uncomment if needed)
#options for chrome
chrome_options = ChromeOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6367.78 Safari/537.36")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
#chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
#chrome_options.use_chromium = True
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1980x1020")
#chrome_options.add_argument("--log-level=3")

#options for chrome
# Optional settings (uncomment if needed)
edge_options = EdgeOptions()
edge_options.add_experimental_option('detach', True)
edge_options.use_chromium = True
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.78 Safari/537.36")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# edge_options.add_argument(f"user-data-dir={edge_profile_path}")
# edge_options.add_argument("--profile-directory=Profile 5")
#edge_options.use_chromium = True
#edge_options.add_argument("--headless")
#edge_options.add_argument("--window-size=1980x1020")
#edge_options.add_argument("--log-level=3")

class TikTokProfile:
	def __init__(self, user_profile, browser='chrome'):
		if browser == 'chrome':
			chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
			chrome_options.add_argument(f"--profile-directory={user_profile}")
		elif browser == 'edge':
			edge_options.add_argument(f"user-data-dir={edge_profile_path}")
			edge_options.add_argument(f"--profile-directory={user_profile}")
		else:
			raise ValueError("Unidendified driver")

	def switch_tabs(i):
		handles = driver.window_handles
		if i > len(handles):
			raise Exception('tab handles out of range')
		else:
			driver.switch_to.window(handles[i])
		
	def launch(self, browser='chrome'):
		if browser == 'chrome':
			driver = webdriver.Chrome(options=chrome_options)
		elif browser == 'edge':
			driver =  webdriver.Edge(option=edge_options)
		else:
			raise ValueError("Unidentified driver")
		return driver
	
	def action(self):
		if self.launch():
			action = ActionChains(self.launch())
		return action


			
if __name__ == "__main__":
	list_of_accounts = [
		'gabby7__435', 'gangster_giver', 'gangster_in_love', 'gangsterpumpam82', 'nineteen_eighty_five',
		'annie.conceptstv', 'chideratheo', 'tunde_joe', 'isaac.sammy.zz', 'yitchak_ekoko', 'swings.and.slides', 'ritter.dorothy',
		'clay_clinics', 'hot.teddy.dollar', 'farooq.haboob', 'sportfromfemi', 'arnold.neemom', 'joelo.romeo',
		'demetree_teskov', 'devanlovesalphabets', 'tinasexylove', 'charles.ex_saviour', 'ekenechinedu.michaels'
	]
	giver = TikTokProfile('Profile 12')
	driver = giver.launch()
	driver.maximize_window()
	for account in list4:
		driver.execute_script(f"window.open('{url}@{account}');")
