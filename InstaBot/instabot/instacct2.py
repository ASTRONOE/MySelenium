#import libraries
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


#edge profile path
edge_profile_path = r"C:\Users\user\AppData\Local\Microsoft\Edge\User Data"
#domain
url = 'https://www.instagram.com/'

#options for cedge
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

#activate driver and its associate components
#uncomment to choose driver
#driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Edge(options=edge_options)
#action = ActionChains(driver) #action sequence
#wait = WebDriverWait(driver, 60) #driver wait
presence = EC.presence_of_element_located #presence
visibility = EC.visibility_of_element_located #visibility


#instagram login page






class InstagramDriver(webdriver.Chrome):
	def __init__(self, profile, wait_time, *args, **kwargs):
		#options for chrome
		chrome_profile_path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
		chrome_options = ChromeOptions()
		#chrome_options.use_chromium = True
		#chrome_options.add_argument("--headless")
		#chrome_options.add_argument("--window-size=1980x1020")
		#chrome_options.add_argument("--log-level=3")
		chrome_options.add_experimental_option('detach', True)
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6367.78 Safari/537.36")
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		chrome_options.add_argument("--profile-directory=Profile 12")
		chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
		chrome_options.add_argument(f"--profile-directory={profile}")

		super().__init__(options=chrome_options, *args, **kwargs)
		self.action = ActionChains(self)
		self.wait = WebDriverWait(self, wait_time)

	def normal_login(self, account):
		"""
		Inserts user's login details -- the username and password into the the log in page.
		Then it pushes the login button to sign in.
		Argument:
		- account:the user's account
		"""
		signin = self.wait.until(presence((By.NAME, 'username')))
		pass_word = self.wait.until(presence((By.NAME, 'password')))
		signin.send_keys(account[0])
		pass_word.send_keys(account[1])      
		login_button = self.find_elements(By.TAG_NAME, 'button')[1]
		login_button.click()

	#the login navbar
	def login_again(self):
		"""
		In case the login nav bar and javascript pops up, you have to login again.
		Click the button to go back to the login page,
		"""
		nav = self.wait.until(visibility((By.CSS_SELECTOR, 'div._acum')))
		login = nav.find_element(By.CSS_SELECTOR, 'div._acus')
		button = login.find_elements(By.TAG_NAME, 'a')[0]
		button.click()

	#the save login page
	def save_login(self, choice):
		"""
		After signing in, the page requesting you to save your login details will pop up.
		Arguments:
			- choice: Choices can be 'yes' to save the log in otherwise 'no'
		Exceptions:
			ValueError: Any other value will raise an error.
		"""
		main = self.wait.until(visibility((By.TAG_NAME, 'main')))
		save_info = main.find_element(By.TAG_NAME, 'button')
		not_now = main.find_element(By.CSS_SELECTOR, 'div._ac8f')
		if choice == 'yes':
			save_info.click()
		elif choice == 'no':
			not_now.click()
		else:
			raise ValueError('Choice should be "yes" or "no"')
		
	#the notification pop-up box
	def notify(self, choice):
		"""
		On getting to the dashboard or any page, the blocking pop up to request notifications will appear.
		You have to choose 'yes' to accept notifications, otherwise 'no'.
		"""
		choose = self.wait.until(visibility((By.CSS_SELECTOR, 'div._a9-z')))
		turn_on = choose.find_elements(By.TAG_NAME,'button')[0]
		not_now = choose.find_elements(By.TAG_NAME, 'button')[1]
		if choice == 'no':
			not_now.click()
		elif choice == 'yes':
			turn_on.click()
		else:
			raise ValueError('Choice should be "yes" or "no"')
		
	#follow an account
	def follow(self, visit):
		"""
		To follow an account, click on the "Follow" button.
		Arguments:
		- visit:the username to visit
		"""
		self.get(f'{url}{visit}/')
		main = self.wait.until(visibility((By.TAG_NAME, 'main')))
		header = main.find_element(By.TAG_NAME, 'header')
		section = header.find_elements(By.TAG_NAME, 'section')[1]
		button = section.find_element(By.TAG_NAME, 'button')
		is_followed = self.find_element(By.CSS_SELECTOR, 'div._ap3a._aaco._aacw._aad6._aade').text
		if is_followed == 'Follow': #ensure that the account is not followed already
			button.click()
		
	def unfollow(self, account):
		"""
		If account is followed, click to unfollow
		"""
		self.get(f'{url}{account}/')
		main = self.wait.until(visibility((By.TAG_NAME, 'main')))
		header = self.find_element(By.TAG_NAME, 'header')
		section = header.find_elements(By.TAG_NAME, 'section')[1]
		button = section.find_element(By.TAG_NAME, 'button')
		is_followed = self.find_element(By.CSS_SELECTOR, 'div._ap3a._aaco._aacw._aad6._aade').text
		if is_followed != 'Following': #ensure that the account is not unfollowed already
			button.click()
			time.sleep(5)
			unfollow_box_button = self.find_element(By.XPATH,
				'/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]/div[2]')
			self.action.move_to_element(unfollow_box_button).click().perform()

	#launch post    
	def launch_post(self, visit, newtab=False):
		"""
		Visit a url; a certain instagram URL.
		Arguments:
		- visit: the url.
		- newtab: if newtab is set to True, it will open that URL in a new tab.
		"""
		if newtab == True:
			self.execute_script(f"window.open('{visit}');")
		else:
			self.get(f'{visit}')

	#like post        
	def like_post(self):
		"""
		To like a post, hover over the heart button and click to like or love.
		"""
		right_segment = self.wait.until(visibility((By.CSS_SELECTOR, 'div.x4h1yfo')))
		interact = right_segment.find_element(By.CSS_SELECTOR, 'div.x78zum5')
		love_button = interact.find_element(By.CSS_SELECTOR, 'span.xp7jhwk')
		love_button_hover = love_button.find_element(By.TAG_NAME, 'svg')
		self.action.move_to_element(love_button_hover).click().perform()

	#save post
	def save_post(self):
		"""
		Hover over the bookmark button and click to save.
		"""
		segment = self.wait.until(visibility((By.XPATH,
		'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]')))
		save_post = segment.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.x1gryazu')
		save_post_button = save_post.find_element(By.TAG_NAME, 'svg')
		self.action.move_to_element(save_post_button).click().perform()

	#Comment on post
	def comment_on_post(self, message=None):
		"""
		To drop a comment on the post
		Argments:
		- message: the message should be a formatted string that will be dropped in the comment box.
		Exceptions:
		- NoSuchElementException:In case commenting is disabled, a javascript alert should pop up
		"""
		right_segment = self.wait.until(visibility((By.CSS_SELECTOR, 'div.x4h1yfo')))
		form = right_segment.find_element(By.TAG_NAME, 'form')
		text_area = form.find_element(By.TAG_NAME, 'textarea')
		if message is None:
			print("Drop a message below")
			message = input()
		try: #ensure that comments are enabled
			self.action.move_to_element(text_area) #move to the text area
			self.action.click(text_area) #click the text area
			self.action.send_keys(f'''{message}''') #drop the formatted comment
			self.action.send_keys(Keys.RETURN) #use the enter key
			self.action.perform() #execute the action chain
		except NoSuchElementException:
			self.execute_script('alert("Cannot post comment. Check if commenting is available or enabled");')

	#switch tabs
	def switch_tabs(self, i):
		"""
		To switch tabs
		Args:
		- tab index
		Exception:
		- Exception ensures that tabs are within range.
		"""
		handles = self.window_handles
		if i > len(handles):
			raise Exception('tab handles out of range')
		else:
			self.switch_to.window(handles[i])

if __name__ == "__main__":
	print()
   #Example. It has been done already
	
