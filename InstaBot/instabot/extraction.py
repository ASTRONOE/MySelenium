import time
import threading as thrd
from concurrent.futures import ThreadPoolExecutor as TPE
import asyncio as aio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as scex
from selenium.webdriver.common.action_chains import ActionChains

#domain
event = thrd.Event()
url = 'https://www.tiktok.com/'
#edge profile path
edge_profile_path = r"C:\Users\user\AppData\Local\Microsoft\Edge\User Data"


#chrome_options.add_argument("--log-level=3")

#options for chrome
# Optional settings (uncomment if needed)
edge_options = EdgeOptions()
edge_options.add_experimental_option('detach', True)
edge_options.use_chromium = True
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.78 Safari/537.36")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
edge_options.add_argument(f"user-data-dir={edge_profile_path}")
edge_options.add_argument("--profile-directory=Default")
#edge_options.use_chromium = True
#edge_options.add_argument("--headless")
#edge_options.add_argument("--window-size=1980x1020")
#edge_options.add_argument("--log-level=3")

#activate driver and its associate components. Uncomment the driver you want
driver = webdriver.Edge(options=edge_options)
action = ActionChains(driver) #action chains
wait = WebDriverWait(driver, 60) #driver wait
presence = EC.presence_of_element_located #presence
visibility = EC.visibility_of_element_located #visibility

def launch_post(visit, wait=None, newtab=False): #launch driver with url
	if newtab == True:
		driver.execute_script(f"window.open('{visit}');")
	else:
		driver.get(f'{visit}')
	if wait is not None:
		time.sleep(float(wait))

def go_to_comments(): #when the post loads, jump to the comments
	comments_section = driver.find_element(By.CSS_SELECTOR, "div.css-g6odvl-DivCommentContainer.ekjxngi0")
	driver.execute_script("arguments[0].scrollIntoView();", comments_section) #or use javascript scrolling

async def extract_users(q, cycle, scroll):
	try:
		comments_section = wait.until(presence((By.CSS_SELECTOR, "div.css-13revos-DivCommentListContainer.ekjxngi3"))) #the comments section
		
		for _ in range(cycle): #number of scrolling down to do
			comments_cells = comments_section.find_elements(By.CSS_SELECTOR, "div.css-1i7ohvi-DivCommentItemContainer.eo72wou0") #the loading comments cells in the comments
			driver.execute_script(f"window.scrollBy(0, {scroll});") #scroll down by a certain extent 
			
			for cells in comments_cells: #extract data from each comment cell
				inner_cell = cells.find_element(By.CSS_SELECTOR, "div.css-1mf23fd-DivContentContainer.e1g2efjf1") #the container
				persons_link = inner_cell.find_element(By.TAG_NAME, 'a').get_attribute('href') #the user's url
				persons_name = inner_cell.find_element(By.TAG_NAME, 'span').text #the user's name
				await q.put((persons_name, persons_link)) #enqueue the user's name and url as a tuple
				print(f"Enqueued {persons_name}, {persons_link}")
		
		if q.full(): #if the queue gets full end the queue immediately
			q.put_nowait(None)
		await q.put(None) #after the cycle, end the queue and stop iteration
	
	except scex.NoSuchElementException as ex: #in case there are no comments 
		print("It seems there are no visible comments or there is a blockage", ex)


async def get_users(q, store_names, store_links): #dequeue items
	while True:
		try:
			user = await q.get() #dequeue from queue
			
			if user is None:
				q.task_done()
				break 
			print(f"Dequeued {user[0]}, {user[1]}")
			
			store_names.write(user[0] + '\n') #store names to text file
			store_links.write(user[1] + '\n') #store links to text file
			q.task_done()
			
		except (TimeoutError, ValueError, TypeError) as ex:
			print("Something went wrong while waiting for value:", user, "\n", ex)
			
			
async def main(): #run coroutines 
	try:
		store_names = open("storenames.txt", "a", encoding="utf-8") #open files to put dequeued items
		store_links = open("storelinks.txt", "a", encoding="utf-8") #open files to write dequeued items
		
		sum_comments = wait.until(visibility((By.XPATH, #the sum of visible comments in the post
			'/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/button[2]/strong')))
			
		queue = aio.Queue(maxsize=int(sum_comments.text)) #Define queue with max being the number of comments 
		task1 = aio.create_task(extract_users(queue, cycle=65, scroll=350)) #run coroutine task to enqueue
		task2 = aio.create_task(get_users(queue, store_names, store_links)) #run corountine task to dequeue
		
		await task1 #awaiting asynchronous tasks,  
		await task2
		
		store_names.close() #finish and close both files
		store_links.close()
		ex_occur1, ex_occur2 = task1.exception(), task2.exception()  #handle exceptions
		
	except aio.CancelledError:
		print("The operation was cancelled", ex_occur1, "\n", ex_occur2)
	except KeyboardInterrupt as ex:
		print("The operation was cancelled from the keyboard", ex)
	except (IOError, FileNotFoundError) as file_error:
		print("An error occured while writing to the file", file_error)
	except scex.TimeoutException as ex:
		print("The operation is lagging", ex)
	except (scex.WebDriverException, scex.NoSuchWindowException) as ex:
		print("The driver or connection operation encounterd problems and has closed.", ex)
	
	
def start_driver(url): #start browser and go to post 
	launch_post(url)
	driver.maximize_window()
	go_to_comments()
	print("Passing control to coroutines")
	event.set()
	
def start_coroutines():
	event.wait()
	print("Beginning executions")
	aio.run(main())
	
def captcha():
	while True:
		try:
			captcha_box = driver.find_element(By.ID, 'captcha_verify_container CaptchaWrapper-u1rqd2-0 gmpebW')
			if captcha_box and captcha_box.get_attribute('style') == "visibility: visible;":
				print("Captcha is visible and blocking the program")
				continue  # Loop until captcha is resolved
			else:
				print("Captcha resolved")
				break
 # If captcha element is not found, break the loop
		finally:
			break
	

if __name__ == "__main__":
	#define threads
	webpage = thrd.Thread(target=start_driver, args=("https://www.tiktok.com/@abemarisentertainment/video/7403295853827378464",))
	run_main = thrd.Thread(target=start_coroutines)
	captcha_thread = thrd.Thread(target=captcha, daemon=True)
	#run programs 
	webpage.start(); run_main.start(), captcha_thread.start()
	webpage.join(); run_main.join()