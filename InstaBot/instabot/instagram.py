import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import  Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# Change this to your own chromedriver path!
FirefoxDriver_path = "geckodriver.exe"
options = Options()
profile_path = r"C:\Users\USER\AppData\Roaming\Mozilla\Firefox\Profiles\glvkqpk8.instagram-1"
options.set_preference("profile", profile_path)
# Load the profile using FirefoxProfile
profile = webdriver.FirefoxProfile(profile_path)
driver = webdriver.Firefox(firefox_profile=profile, options=options)
action = ActionChains(driver)


accounts = [["carmelo30huelshoz@hotmail.com","a5c2130e"]]

follow_accts = ["extacy_ng","boymettrothemovement","pmcfashionworld_"]

like_posts = ["https://www.instagram.com/reel/C7OdrxvIl8y/"]


url = "https://www.instagram.com/accounts/login/?hl=en"

def normal_login(account):
    #driver.get("https://www.instagram.com/accounts/login/?hl=en")
    time.sleep(6)
    signin = driver.find_element(By.NAME, 'username')
    pass_word = driver.find_element(By.NAME, 'password')
    signin.send_keys(str(account[0]))
    pass_word.send_keys(str(account[1]))      
    login_button = driver.find_elements(By.TAG_NAME, 'button')[1]
    login_button.click()
    time.sleep(2)



def follow(account):
   driver.get(f"https://www.instagram.com/{account}")
   main = driver.find_element(By.TAG_NAME, 'main')
   header = main.find_element(By.TAG_NAME, 'header')
   section = header.find_elements(By.TAG_NAME, 'section')[1]
   button = section.find_element(By.TAG_NAME, 'button')
   button.click()


    
#drop a comment on the post
def comment_on_post(self, message=None):
    dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
    comment_box = dialog_box.find_element(By.TAG_NAME, 'form')
    text_area = comment_box.find_element(By.TAG_NAME, 'textarea')
    if message is None:
        message = input()       
    try:
        action.move_to_element(text_area)
        action.click(text_area)
        action.send_keys(f'''{message}''')
        action.send_keys(Keys.RETURN)
        action.perform()
    except NoSuchElementException:
        driver.execute_script('alert("Cannot post comment. Check if commenting is available or enabled");')

    
    
#click the love button
def like_post(self):
    dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
    love_button = dialog_box.find_element(By.CSS_SELECTOR, 'span.x1rg5ohu.xp7jhwk')
    love_button_svg = love_button.find_element(By.TAG_NAME, 'svg')
    action.move_to_element(love_button_svg).click().perform()


#if liked already, click the red heart to unlike
def unlike_post(self):
    if self.is_liked() == 'Liked':
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        love_button = dialog_box.find_element(By.CSS_SELECTOR, 'span.x1rg5ohu.xp7jhwk')
        love_button_svg = love_button.find_element(By.TAG_NAME, 'svg')
        action.move_to_element(love_button_svg).click().perform()
    return None
    

#click the bookmark button to save
def save_post(self):
    time.sleep(5)
    segment = driver.find_element(By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]')
    save_post = segment.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.x1gryazu')
    save_post_button = save_post.find_element(By.TAG_NAME, 'svg')
    action.move_to_element(save_post_button).click().perform()
    time.sleep(5)



#is the post saved already
def is_saved(self):
    # return save
    save = "Not saved"
    dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
    save_button = dialog_box.find_elements(By.CSS_SELECTOR, 'svg.x1lliihq.x1n2onr6.x5n08af')[3]
    if save_button.get_attribute('aria-label') == 'Remove':
        save = 'Saved'


#if the post is already saved, click to unsave
def unsave_post(self):
    if self.is_saved() == 'Saved':
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        save_button = dialog_box.find_elements(By.CSS_SELECTOR, 'svg.x1lliihq.x1n2onr6.x5n08af')[3]
        action.move_to_element(save_button).click().perform()







