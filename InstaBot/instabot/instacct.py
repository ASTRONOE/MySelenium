#import libraries
import time
import json
from threading import Thread
import asyncio
import os
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
url = 'https://www.instagram.com/'

#configure driver options
# Optional settings (uncomment if needed)
#options for chrome
chrome_options = ChromeOptions()
chrome_options.add_experimental_option('detach', True)
#chrome_options.use_chromium = True
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6367.78 Safari/537.36")
#chrome_options.add_argument("--window-size=1980x1020")
#chrome_options.add_argument("--log-level=3")
#chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#options for chrome
edge_options = EdgeOptions()
edge_options.add_experimental_option('detach', True)
# Optional settings (uncomment if needed)
#edge_options.use_chromium = True
#edge_options.add_argument("--headless")
#edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.78 Safari/537.36")
#edge_options.add_argument("--window-size=1980x1020")
#edge_options.add_argument("--log-level=3")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#activate driver and its associate components
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Edge(options=edge_options)
action = ActionChains(driver)
wait = WebDriverWait(driver, 60)
presence = EC.presence_of_element_located
visibilty =EC.visibility_of_element_located

#the user's account
class InstagramAccount:
    #get sign in details to enter instagram
    def __init__(self, email=None, user=None, password=None, fb_password=None):
        self.user = user
        self.__password = password
        self.email = email
        self.__fb_password = fb_password
        self.profile = f'{url}{self.user}/'

    def __str__(self):
        return self.user

    #visit an instagram page
    def go_to_account(self, account, newtab=False):
        if newtab is True:
            driver.execute_script(f"window.open('{url}{account}/');")
        else:
            driver.get(f'{url}{account}/')
        
        
    #sign into instagram
    def normal_login(self):
        time.sleep(5)
        signin = wait.until(presence((driver.find_element(By.NAME, 'username'))))
        pass_word = wait.until(presence((driver.find_element(By.NAME, 'password'))))
        signin.send_keys(str(self.user))
        pass_word.send_keys(str(self.__password))      
        login_button = driver.find_elements(By.TAG_NAME, 'button')[1]
        login_button.click()
        self.normal_login()
    
    #incase of javascript, go back to login page
    def login_again(self):
        time.sleep(5)
        nav = wait.until(presence((driver.find_element(By.CSS_SELECTOR, 'div._acum'))))
        login = nav.find_element(By.CSS_SELECTOR, 'div._acus')
        button = login.find_elements(By.TAG_NAME, 'a')[0]
        button.click()
    
    #dismiss warning
    def warning(self):
        box = wait.until(presence((driver.find_element(By.CSS_SELECTOR, 'div.wbloks_1.wbloks_77'))))
        dismiss = box.find_element(By.CSS_SELECTOR, 'div.wbloks_1')
        dismiss.click()

    #signin using facebook details
    def facebook_login(self):
        time.sleep(10)
        facebook_login = driver.find_element(By.CSS_SELECTOR, 'span._ab37')
        facebook_login.click()
        block = wait.until(presence((driver.find_element(By.TAG_NAME, 'form'))))
        mail_box = block.find_elements(By.ID, 'email_container')
        mail_box.click()
        mail = mail_box.find_element(By.TAG_NAME, 'input')
        mail.send_keys(self.email)
        
        pass_block = block.find_elements(By.CSS_SELECTOR, 'div.clearfix._5466._44mg')[1]
        pass_block.click()
        passs = pass_block.find_elements(By.TAG_NAME, 'input')[0]
        passs.send_keys(self.fb_password)
        
        login = block.find_element(By.CSS_SELECTOR, 'div._xkt')
        button = login.find_element(By.TAG_NAME, 'button')
        button.click()

    #save login details after signing in?
    def save_login(self, choice):
        time.sleep(5)
        main = wait.until(presence((driver.find_element(By.TAG_NAME, 'main'))))
        save_info = main.find_element(By.TAG_NAME, 'button')
        not_now = main.find_element(By.CSS_SELECTOR, 'div._ac8f')
        if choice == 'yes':
            save_info.click()
        elif choice == 'no':
            not_now.click()
        else:
            raise ValueError('Choice should be "yes" or "no"')
        
    #receive notifications after sign in?
    def notify(self, choice):
        choose = wait.until(presence((driver.find_element(By.CSS_SELECTOR, 'div._a9-z'))))
        turn_on = choose.find_elements(By.TAG_NAME,'button')[0]
        not_now = choose.find_elements(By.TAG_NAME, 'button')[1]
        if choice == 'no':
            not_now.click()
        elif choice == 'yes':
            turn_on.click()
       
    #follow an account
    def follow(self, account:str):
        driver.get(f'{url}{account}/')
        main = wait.until(presence((driver.find_element(By.TAG_NAME, 'main'))))
        header = main.find_element(By.TAG_NAME, 'header')
        section = header.find_elements(By.TAG_NAME, 'section')[1]
        button = section.find_element(By.TAG_NAME, 'button')
        button.click()
        
    #unfollow an account
    def unfollow(self, account:str):
	    time.sleep(10)
        driver.get(f'{url}{account}/')
        main = wait.until(visibility((driver.find_element(By.TAG_NAME, 'main'))))
        header = driver.find_element(By.TAG_NAME, 'header')
        section = header.find_elements(By.TAG_NAME, 'section')[1]
        button = section.find_element(By.TAG_NAME, 'button')
		  is_followed = driver.find_element(By.CSS_SELECTOR, 'div._ap3a._aaco._aacw._aad6._aade').text
		  if is_followed != 'Follow'
           button.click()
        time.sleep(5)
		  
        unfollow_box_button = driver.find_element(By.XPATH,
            '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]/div[2]')
				
        action.move_to_element(unfollow_box_button).click().perform()
        
    #open multiple tabs in threads
    def start_thread(self, n):
        threads = []
        for i in range(n):
           x = Thread(target=lambda:driver.execute_script(f"window.open('{url}');"))
           threads.append(x)
           x.start()
        for t in threads:
            t.join()

    #open multiple tabs in a single thread
    def non_thread(self, n):
        for i in range(n):
            driver.execute_script(f"window.open('{url}');")
        
    #open multiple accounts in multiple tabs
    def load_accounts(self, accounts, asyn=False):
        if asyn is True:
            threads = []
            for user in users:
                x = Thread(target=lambda: self.driver.get(f'{url}{user}'))
                threads.append(x)
                x.start()
            for t in threads:
                t.join()
        else:
            for user in users:
                self.driver.get(f'{url}{user}')
            
    #load urls from stored json file
    def load_urls(self, account):
        with open(f'links/{account}.json', 'r') as read_file:
            urls = json.load(read_file)
            return urls
    
#load urls from json file and launch them on the browser    
    def read_urls(self, account,limit=3, asyn=False):
        urls = self.load_urls(account) #load in multiple threads
        urls = urls[account]
        if limit is not None:
            urls = urls[:limit] #it is recommended that you set limits
        if asyn is True:
            threads = []
            for u in urls:
                x = Thread(target=lambda: driver.execute_script(f"window.open('{u}');"))
                threads.append(x)
                x.start()
            for t in threads:
                t.join()
        else: #load in a sinfle thread
            for u in urls[:limit]:
                driver.execute_script(f"window.open('{u}');")
    
    #switch tabs
    def switch_tabs(self, i):
        handles = driver.window_handles
        if i < 0 or i >= len(handles):
            raise Exception('Tab out of range')
        else:
            driver.switch_to.window(handles[i])
            
    #number of tabs
    def len_tabs(self):
        return len(driver.window_handles)
        
    #get the list of the urls in all tabs
    def show_all_tabs(self):
        url_list = []
        for i, handle in enumerate(driver.window_handles):
            driver.switch_to.window(handle[i])   
            url_list.append(driver.current_url)            
        return url_list
        
    #browser actions
    def browser_action(self, action):
        if action == 'close':
            driver.close()
        elif action =='quit':
            driver.quit()
        elif action == 'forward':
            driver.forward()
        elif action == 'back':
            driver.back()
        elif driver == 'refresh':
            driver.refresh()
        elif action == 'minimize':
            driver.minimize_window()
        elif action == 'maximize':
            driver.maximize_window()
        elif action == 'fullscreen':
            driver.fullscreen_window()
        else:
            raise ValueError('Unknown action')
     
    #exit to login page
    #def logout(self):
        # settings = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[3]/span/div/a/div')
        # action.move_to_element(settings).pause(3)
        # action.click(settings)
        # action.perform()
        # settings_box = driver.find_element(By.CSS_SELECTOR, 'div.x1n2onr6') 
        # signout = settings_box.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[8]')
        # action.move_to_element(signout).pause(3)
        # action.click(signout)
        # action.perform()
        # more = driver.find_element(By.CSS_SELECTOR, 'div.xl5mz7h.xhuyl8g')
        # time.sleep(1)
        # more_h = more.find_elements(By.TAG_NAME, 'a')[-1]
        # action.move_to_element(more_h).click().perform()
        # time.sleep(2)
        
        # settings = driver.find_element(By.CSS_SELECTOR, 'div.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha')
        # signout  = settings.find_element(By.XPATH,
            # '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[8]')
        # signout.click()
         

#the sliding dialog box that shows images
class  ViewBox:
    #load account
    def __init__(self, account):
        self.account = account

    #launch URL at once   
    def launch_post(self):
        if driver.current_url != f'{url}{self.account}/':
            #driver.execute_script(f"window.open('{url}{self.account}/');")
            driver.get(f'{url}{self.account}')
    
    #click on a picture to view it in the slider
    def select_photo(self, index=0):
        #move to photos position
        collection = driver.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[2]')
        driver.execute_script('arguments[0].scrollIntoView();', collection)
        try:
            photos = wait.until(presence((collection.find_elements(By.TAG_NAME, 'a'))))
            action.move_to_element(photos[index]).click().perform()
            time.sleep(4)
        except (NoSuchElementException, StaleElementReferenceException):
            driver.execute_script("alert(Image not seen. Please check to ensure that such image exists in the viewport);")
    
    #close view box
    def deselect_photo(self):
        driver.back()
    
    #cycle through photos
    def cycle_post(self, cycle=None):
        box = driver.find_element(By.CSS_SELECTOR,'div._aear')
        cycle_button = box.find_element(By.CSS_SELECTOR, 'button._abl-') #the buttons at the first and end
        cycle_buttons = box.find_elements(By.CSS_SELECTOR, 'button._abl-') #the buttons in between
        if cycle == None:
            action.move_to_element(cycle_button).click().perform()
            time.sleep(1)
        if cycle == 'r': #go right
            action.move_to_element(cycle_buttons[1]).click().perform()
            time.sleep(1)
        if cycle == 'l': #go right
            action.move_to_element(cycle_buttons[0]).click().perform()
            time.sleep(1)
        else:
            return None     
    
    #cycle through inner photos in posts    
    def cycle_photos(self, cycle=None):
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        left_segment = dialog_box.find_element(By.CSS_SELECTOR, 'div._aamm')
        button = left_segment.find_element(By.TAG_NAME, 'button')  #the buttons at the first and end
        next_button = left_segment.find_elements(By.TAG_NAME, 'button') #the buttons in between
        if cycle == None:
            action.move_to_element(button).click().perform()  
            time.sleep(1)            
        if cycle == 'r': #go right
            action.move_to_element(next_button[1]).click().perform()
            time.sleep(1)
        if cycle == 'l': #go left
            action.move_to_element(next_button[0]).click().perform()
            time.sleep(1)
        else:
            return None
    
    #does it contain inner photos
    def single(self):
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        left_segment = dialog_box.find_element(By.CSS_SELECTOR, 'div._aamm')
        button = left_segment.find_element(By.TAG_NAME, 'button')
        next_button = left_segment.find_elements(By.TAG_NAME, 'button')
        if button.is_displayed() or next_button().is_displayed():
            return False
            
    #click the love button
    def like_post(self):
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        love_button = dialog_box.find_element(By.CSS_SELECTOR, 'span.x1rg5ohu.xp7jhwk')
        love_button_svg = love_button.find_element(By.TAG_NAME, 'svg')
        action.move_to_element(love_button_svg).click().perform()
    
    #is the post liked already?
    def is_liked(self):
        like = 'Unliked'
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        love_button = dialog_box.find_element(By.CSS_SELECTOR, 'span.x1rg5ohu.xp7jhwk')
        love_button_svg = love_button.find_element(By.TAG_NAME, 'svg')
        if love_button_svg.get_attribute('aria-label') == "Unlike":
            like = 'Liked'
        return like

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
        dialog_box = driver.find_element(By.CSS_SELECTOR, 'article._aatb._aate._aatg._aath._aati')
        save_button = dialog_box.find_elements(By.CSS_SELECTOR, 'svg.x1lliihq.x1n2onr6.x5n08af')[3]
        action.move_to_element(save_button).click().perform()
    
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
    
    #automatically go through the photo slides    
    def go_through_posts(self, viewtime, howfar):
        self.launch_post() #launch
        time.sleep(5) #wait
        self.select_photo() #pick first post
        time.sleep(viewtime) #wait
        self.cycle_post() #move to next posts
        for i in range(howfar): 
            self.cycle_post('r') #go right
            time.sleep(viewtime)
        driver.back() #exit loop
     #generator to get links from cycled posts      
    
    #yield the urls while sliding through
    def instagram_link_gen(self, howfar):
        self.launch_post()  # Launch the initial post
        time.sleep(5)  # Wait for the post to load
        self.select_photo()  # Pick the first post
        time.sleep(3)  # Wait for the photo to be viewed
        self.cycle_post()  # Move to the next post  
        yield driver.current_url  # Yield the link of the first post
        for _ in range(howfar):
            self.cycle_post('r')  # Move to the next post
            time.sleep(3)  # Wait for the post to be viewed
            yield driver.current_url  # Yield the current URL
        driver.back()
    
    #get the links and store them in json
    def save_links_to_json(self, howfar):
        links = list(self.instagram_link_gen(howfar))
        data = {self.account: links}
        print(data)
        with open(f'links/{self.account}.json', 'w') as f:
            json.dump(data, f, indent=2)

#interact with instagram posts
class InstagramPost:
    def __init__(self, post_url):        
        self.post_url = post_url #the url
    
    #visit post
    def launch_post(self, go_to=True):
        if go_to == False:         
            driver.execute_script(f"window.open('{self.post_url}');")
        else:
            driver.get(self.post_url)
        time.sleep(10)

    #click the heart to like the post
    def like_post(self):
        time.sleep(5)
        right_segment = driver.find_element(By.CSS_SELECTOR, 'div.x4h1yfo')
        interact = right_segment.find_element(By.CSS_SELECTOR, 'div.x78zum5')
        love_button = interact.find_element(By.CSS_SELECTOR, 'span.xp7jhwk')
        love_button_hover = love_button.find_element(By.TAG_NAME, 'svg')
        action.move_to_element(love_button_hover).click().perform()

    #unlike the post if liked already
    def unlike_post(self):
        if self.is_liked() == 'Liked':
            right_segment = driver.find_element(By.CSS_SELECTOR, 'div.x4h1yfo')
            interact = right_segment.find_element(By.CSS_SELECTOR, 'div.x78zum5')
            love_button = interact.find_element(By.CSS_SELECTOR, 'span.xp7jhwk')
            love_button_hover = love_button.find_element(By.TAG_NAME, 'svg')
            action.move_to_element(love_button_hover).click().perform()
        return None

    #is the post liked already?
    def is_liked(self):
        like = 'Unliked'
        right_segment = driver.find_element(By.CSS_SELECTOR, 'div.x4h1yfo')
        interact = right_segment.find_element(By.CSS_SELECTOR, 'div.x78zum5')
        love_button = interact.find_element(By.CSS_SELECTOR, 'span.xp7jhwk')
        love_button_hover = love_button.find_element(By.TAG_NAME, 'svg')
        if love_button_hover.get_attribute('aria-label') == "Unlike":
            like = 'Liked'
        return like

    #click the bookmark icon to save the post
    def save_post(self):
        time.sleep(5)
        segment = driver.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]')
        save_post = segment.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.x1gryazu')
        save_post_button = save_post.find_element(By.TAG_NAME, 'svg')
        action.move_to_element(save_post_button).click().perform()
        time.sleep(5)

    #unsave the post
    def unsave_post(self):
        if self.is_saved() == 'Saved':
            segment = driver.find_element(By.XPATH,
                '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]')
            save_post = segment.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.x1gryazu')
            save_post_button = save_post.find_element(By.TAG_NAME, 'svg')
            action.move_to_element(save_post_button).click().perform()
        return None
    
    #is the post saved already?
    def is_saved(self):
        save = "Not saved"
        segment = driver.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]')
        save_post = segment.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.x1gryazu')
        save_post_button = save_post.find_element(By.TAG_NAME, 'svg')
        if save_post_button.get_attribute('aria-label') == "Remove":
            save = "Saved"
        return save
    
    #drop a comment on the post
    def comment_on_post(self, message=None):
        time.sleep(5)
        right_segment = driver.find_element(By.CSS_SELECTOR, 'div.x4h1yfo')
        get_form = right_segment.find_element(By.TAG_NAME, 'form')
        text_area = get_form.find_element(By.TAG_NAME, 'textarea')
        if message is None:
            message = input()
        try: #ensure that comments are enabled
            action.move_to_element(text_area)
            action.click(text_area)
            action.send_keys(f'''{message}''')
            action.send_keys(Keys.RETURN)
            action.perform
        except NoSuchElementException:
            driver.execute_script('alert("Cannot post comment. Check if commenting is available or enabled");')
    
    #get the permalinks of photos
    def get_permalinks(self):
        start = self.post_url.find('/p/') + 3
        end = self.post_url.find('/', start)
        link = self.post_url[start:end]
        return link
    
    #to go through inner photos to and fro
    def cycle_photos(self, cycle=None):
        left_segment = driver.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]')
        photo = left_segment.find_element(By.CSS_SELECTOR, 'div._aamn')
        button = photo.find_element(By.TAG_NAME, 'button')
        next_button = photo.find_elements(By.TAG_NAME, 'button')
        if cycle == None:
            action.move_to_element(button).click().perform()
        if cycle == 'r':
            action.move_to_element(next_button[1]).click().perform()
        if cycle == 'l':
            action.move_to_element(next_button[0]).click().perform()
        else:
            return None
    
    #get the links of inner photos
    def get_album_links(self):
        #ensure that it is an album
        assert 'img_index=' in self.post_url, 'Album expected. This is just one photo or video'
        #get link to the first photo
        self.post_url = self.post_url[:-1]
        self.post_url += '1'
        driver.get(self.post_url) #the current url
        time.sleep(10)
        photo_list = []
        #go to photo sement
        left_segment = driver.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]')
        photo = left_segment.find_element(By.CSS_SELECTOR, 'div._aamn')
        first_right_button = photo.find_element(By.TAG_NAME, 'button')
        #get first photo
        photo_list.append(driver.current_url)
        action.move_to_element(first_right_button).click().perform()
        time.sleep(2)
        #get next photos
        others = photo.find_element(By.XPATH,
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div[2]')
        other_photos = others.find_elements(By.TAG_NAME, 'div')
        next_right_buttons = photo.find_elements(By.TAG_NAME, 'button')[1]
        #cycle through photos and get their url
        for i in range(1, len(other_photos)-1):
            photo_list.append(driver.current_url)
            time.sleep(1)
            action.move_to_element(next_right_buttons).click().perform()
        #get the last photo
        photo_list.append(driver.current_url)
        #the complete set of photos is ready;
        return photo_list
    
    #store data of inner photos in json
    def store_album_links(self):
        name = driver.find_element(By.XPATH, #account username as key
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div/span/span/div/a/div/div/span').text
        data = {name:self.get_album_links()}
        with open(f'links/{name}.json', 'w') as f:
            json.dump(data, f, indent=2)
    
if __name__ == "__main__": 
    driver.get(url)
    me = InstagramAccount(user='bridget7fci', password='062b0263')
    post = ViewBox('wikidayo')
    me.go_to_account('wizkidayo', True)
    me.switch_tabs(1)
    me.login_again()
    me.normal_login()
    me.save_login('yes')
    #post.instagram_link_gen()
    post.save_links_to_json(15)