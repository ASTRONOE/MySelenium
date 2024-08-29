import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

#domain
url = 'https://www.tiktok.com/'
presence = EC.presence_of_element_located #presence
visibility = EC.visibility_of_element_located #visibility


class TikTokDriver(webdriver.Chrome):
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
		The login sequence
		Arguments:
		- account: the test account to use
		"""
		#chrome profile path
		header = self.wait.until(visibility((By.ID, "app-header")))
		login_button = header.find_element(By.ID, 'header-login-button')
		login_button.click()
		dialog_box = self.wait.until(visibility((By.ID, 'loginContainer')))
		login_choices = dialog_box.find_element(By.CSS_SELECTOR, 'div.css-16b4kes-DivHomeContainer.exd0a431')
		#login with username or email
		logins = login_choices.find_elements(By.CSS_SELECTOR, 'div.css-17hparj-DivBoxContainer.e1cgu1qo0')[1] 
		logins.click()
		enter = self.find_element(By.LINK_TEXT, 'Log in with email or username')
		enter.click()
		enter_details = self.find_elements(By.TAG_NAME, 'input')
		#enter_details[1].send_keys(account[0]) #username
		enter_details[1].send_keys(account[2]) #email
		enter_details[2].send_keys(account[1]) #password
		log_in = self.find_elements(By.CSS_SELECTOR, 'form > button')[1]
		log_in.click()

	#start url
	def launch_post(self, visit, wait=None, newtab=False):
		"""
		Visit a url; a certain tiktok URL.
		Arguments:
		- visit: the url.
		- newtab: if newtab is set to True, it will open that URL in a new tab.
		"""
		if newtab == True:
			self.execute_script(f"window.open('{visit}');")
		else:
			self.get(f'{visit}')
		if wait is not None:
			time.sleep(float(wait))

	def follow_account(self, account):
		"""
		To instantly follow on visting the dashboard of the account
		Arguments:
		- account:the username of the account
		"""
		#to follow someone's account
		self.launch_post(f'{url}@{account}')
		title_header = self.wait.until(visibility((By.CSS_SELECTOR, 'div.css-1nbnul7-DivShareTitleContainer.ekmpd5l3')))
		follow = title_header.find_element(By.CSS_SELECTOR, 'div.css-1xwagd1-DivShareFollowContainer.e18e4obn0')
		follow_button = follow.find_element(By.TAG_NAME, 'button')
		if follow_button.text == 'Follow':
			self.action.move_to_element(follow_button).click().perform()
		time.sleep(5)

	def interact(self, click):
		"""
		To click on icons on the video
		Arguments:
		- click: The options will indicate to the action instance what button to click
		"""
		#the interacting column in the right side of the video
		post_column = self.wait.until(visibility((By.CSS_SELECTOR, 'div.css-1gi58p0-DivActionItemContainer.ees02z00')))
		#the buttons in the column
		buttons =post_column.find_elements(By.TAG_NAME, 'button')
		if click == 'check' and buttons[0].get_attribute('class') == 'eth6dzb1 css-34fn9b-Button-StyledAvatarFollowButton e1v8cfre0':
			self.action.move_to_element(buttons[0]).click().perform() #click the '+' button
		if click == 'uncheck' and buttons[0].get_attribute('class') == 'eth6dzb1 css-4n68zl-Button-StyledAvatarFollowButton e1v8cfre0':
			self.action.move_to_element(buttons[0]).click().perform() #if checked, click to uncheck
		if click == 'like' and buttons[1].get_attribute('aria-pressed') == 'false':
			self.action.move_to_element(buttons[1]).click().perform() #press the love button
		if click == 'unlike' and buttons[1].get_attribute('aria-pressed') == 'true':
			self.action.move_to_element(buttons[1]).click().perform() #press to unlike
		if click == 'bookmark': #bookmark button
			self.action.move_to_element(buttons[3]).click().perform()

	def drop_comment(self, message=None):
		"""
		On clicking the comment button, the post will instantly scroll down to the comment box below.
		Then it will click the comment box to start the stdin cursor
		Arguments
		- message: the comment to be posted. If you leave it empty, you must input from the command line.
		"""
		post_column = self.wait.until(visibility((By.CSS_SELECTOR, 'div.css-1gi58p0-DivActionItemContainer.ees02z00'))) #the interacting column
		buttons =post_column.find_elements(By.TAG_NAME, 'button') #the buttons in the column
		#find the comment button in the column
		#click to scroll down to comment section
		self.action.move_to_element(buttons[2]).click().perform()
		time.sleep(3) #wait so as not to clash with full screen button
		comment_section = self.wait.until(visibility((By.CSS_SELECTOR, 'div.css-x4xlc7-DivCommentContainer.e1a7v7ak0'))) #the comments
		comment_post = comment_section.find_element(By.CSS_SELECTOR, 'div.css-jvtqsz-DivCommentContainer.e1rzzhjk0') #the comment box
		#the steps to drop comment
		if message is None:
			print("Drop a comment below")
			message = input()
		text_box = comment_post.find_element(By.CSS_SELECTOR, 'div.notranslate.public-DraftEditor-content')
		self.action.move_to_element(text_box)
		self.action.click()
		self.action.send_keys(f'''{message}''')
		self.action.send_keys(Keys.RETURN)
		self.action.perform()

	def niches(self):	
		niche_bar = self.wait.until(visibility((By.CSS_SELECTOR, 'div.css-1av34ng-DivCategoryListContainer.e13i6o241'))) 
		niche_buttons = niche_bar.find_elements(By.TAG_NAME, 'button')
		niche_link = {}
		for button in niche_buttons:
			span = button.find_element(By.TAG_NAME, 'span')
			niche_link[span.text] = button
		return niche_link
	
	def find_niche(self, category):
		try:
			button = self.niches()
			categories = list(button.keys())
			if category in categories:
				button[category].click()
		except KeyError as ke:
			print(f"Category key error, {category} not found:", ke)
			self.execute_script(f'alert("Category key error, {category} not found");')
		except TypeError as te:
			print("Argument is missing or not valid", te)
		except ValueError as ve:
			print("An error occurred while querying element:", ve)
			self.execute_script('alert("An error occurred while querying element");')

	def catalogue(self, index=0):
		catalogue = self.wait.until(visibility((By.CSS_SELECTOR, "div.css-1qb12g8-DivThreeColumnContainer.eegew6e2")))
		catalogue_list = catalogue.find_element(By.CSS_SELECTOR, "div.css-3nyx92-DivVideoFeedV2.ecyq5ls0")
		catalogue_posts = catalogue_list.find_elements(By.CSS_SELECTOR, "div.css-x6y88p-DivItemContainerV2.e19c29qe8")
		openpost = catalogue_posts[index]
		click_video = openpost.find_element(By.CSS_SELECTOR, "div.css-10op4xt-DivContainer-StyledDivContainerV2.eq741c50")
		click_video.click()


if __name__ == "__main__":
	list1 = ['gangster_Beznika5', 'gangster_giver', 'gangster_in_love', 'gangsterpumpam82', 'nineteen_eighty_five','annie.conceptstv']
	list2 = ['chideratheo', 'tunde_joe', 'isaac.sammy.zz', 'yitchak_ekoko', 'swings.and.slides', 'ritter.dorothy',]
	list3 = ['clay_clinics', 'hot.teddy.dollar', 'farooq.haboob', 'sportfromfemi', 'arnold.neemom', 'joelo.romeo',]
	list4 = ['demetree_teskov', 'devanlovesalphabets', 'tinasexylove', 'charles.ex_saviour', 'ekenechinedu.michaels']

	gabby = TikTokDriver(wait_time=10, profile='Profile 10')
	for acc in list1:
		gabby.follow_account(acc)


	
	

