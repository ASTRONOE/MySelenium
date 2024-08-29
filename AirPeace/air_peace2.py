import time
from threading import Thread as trd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

presence = EC.presence_of_element_located #presence
visibility = EC.visibility_of_element_located #visibility

class AirPeaceDriver(webdriver.Edge):
  def __init__(self, profile, wait_time, *args, **kwargs):
		#options for chrome
    edge_profile_path = r"C:\Users\user\AppData\Local\Microsoft\Edge\User Data"
    edge_options = EdgeOptions()
		#edge_options.use_chromium = True
		#edge_options.add_argument("--headless")
		#edge_options.add_argument("--window-size=1980x1020")
		#edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('detach', True)
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6367.78 Safari/537.36")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    edge_options.add_argument(f"user-data-dir={edge_profile_path}")
    edge_options.add_argument(f"--profile-directory={profile}")

    super().__init__(options=edge_options, *args, **kwargs)
    self.action = ActionChains(self)
    self.wait = WebDriverWait(driver=self, timeout=wait_time)

  def flightmenu(self, tab=0):
    self.execute_script("window.scrollTo(0, 300);")
    flight_menu = self.wait.until(visibility((By.XPATH,
      "/html/body/div[2]/div[1]/div/div/article/main/div/div[2]")))
    booktabs = flight_menu.find_elements(By.TAG_NAME, 'a')
    booktabs[tab].click()

  def bookflightpanel(self):
    bookflightpanel = self.find_element(By.ID, "bdt-tab-content-3d73657-1118")
    departure_panel = bookflightpanel.find_element(By.ID, "bdt-tab-1")
    return departure_panel
    
  def departure_choices(self, id:str, index=None):
    departure_choices = self.bookflightpanel()
    departure = departure_choices.find_element(By.ID, id)
    select = departure.find_elements(By.TAG_NAME, 'option')
    if index is not None:
      select[index].click()

  def travel_date(self, month, day, year):
    departure_choices = self.bookflightpanel()
    depart_date = departure_choices.find_element(By.ID, 'dateOfDepart')
    depart_date.send_keys(f"{month}/{day}{year}")

  def return_date(self, month, day, year):
    departure_choices = self.bookflightpanel()
    return_date = departure_choices.find_element(By.ID, 'dateOfReturn')
    return_date.send_keys(f"{month}/{day}{year}")

  def search_flight_button(self):
    departure_choices = self.bookflightpanel()
    search_flight = departure_choices.find_element(By.CSS_SELECTOR, 'span > button')
    search_flight.click()


  def login(self, member_id, password, tick=False):
    outer_loginform = self.find_element(By.CSS_SELECTOR, "div.login-form")
    loginform = outer_loginform.find_element(By.CSS_SELECTOR, "div.box.rounded-lg.p-0.inner-box")
    username_input = loginform.find_element(By.NAME, "username")
    password_input = loginform.find_element(By.NAME, "password")
    username_input.send_keys(member_id)
    password_input.send_keys(password)
    if tick == True:
      tickbox = loginform.find_element(By.NAME, 'isRemember')
      tickbox.click()
    loginbutton = loginform.find_elements(By.TAG_NAME, 'input')[-1]
    loginbutton.click()

  def new_reservation(self):
    loyalty_panel = self.find_element(By.CSS_SELECTOR, "div.loyalty-buttons-container")
    reservation_button = loyalty_panel.find_element(By.CSS_SELECTOR, "div.loyalty-new-reservation")
    button_click = reservation_button.find_element(By.TAG_NAME, 'a')
    button_click.click()

  # def reservation_container(self):
  #   container = self.find_element(By.CSS_SELECTOR, "div.box.new-reservation-container")
  #   container.find_element(By.ID, "availabilityForm")
  
  def trip_type(self, id):
    trip_checkboxes = self.find_element(By.CSS_SELECTOR, 'div.trip-type-wrapper')
    trip_checkbox = trip_checkboxes.find_elements(By.CSS_SELECTOR, 'ins.iCheck-helper')
    self.action.move_to_element(trip_checkbox[id]).click().perform()

  def departure_location(self, place, id='firstDepPort'):
    departure = self.find_element(By.ID, id) #firstDepPort firstArrPort
    self.action.move_to_element(departure).click()
    self.action.send_keys(f"{place}")
    self.action.send_keys(Keys.ENTER).perform()

  def departure_date(self, day:int, mon:int|str, year:int, id:str):
    departure = self.find_element(By.ID, id)
    self.action.move_to_element(departure).click().perform()
    calendar = self.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[2]/div[2]/div[1]/table')
    time.sleep(2)
    months_drop = calendar.find_element(By.CSS_SELECTOR, 'select.monthselect.dropdown-scroll-open')
    self.action.move_to_element(months_drop).click().perform()

    months_list = calendar.find_element(By.CSS_SELECTOR, 'div.os-padding')
    months_list_inner = months_list.find_element(By.CSS_SELECTOR, 'div.os-content')
    months = months_list_inner.find_elements(By.TAG_NAME, 'li')
    for month in months:
      if month.find_element(By.CSS_SELECTOR, 'span.text').text == mon:
        month.find_element(By.TAG_NAME, 'a').click()

    calendar = self.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[2]/div[2]/div[1]/table')
    time.sleep(2)

    years_drop = calendar.find_element(By.CSS_SELECTOR, 'select.yearselect.dropdown-scroll-open')
    self.action.move_to_element(years_drop).click().perform()

    years_list = calendar.find_element(By.CSS_SELECTOR, 'div.os-padding')
    years_list_inner = years_list.find_element(By.CSS_SELECTOR, 'div.os-content')
    years = years_list_inner.find_elements(By.TAG_NAME, 'li')
    for yer in years:
      if yer.find_element(By.CSS_SELECTOR, 'span.text').text == str(year):
        yer.find_element(By.TAG_NAME, 'a').click()

    calendar = self.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[2]/div[2]/div[1]/table')
    time.sleep(2)
    days = calendar.find_element(By.TAG_NAME, 'tbody')
    available_days = days.find_elements(By.CSS_SELECTOR, 'td.available, td.weekend.available')

    for select_day in available_days:
      if int(select_day.text) == day:
        self.action.move_to_element(select_day).click().perform()
        break

if __name__ == "__main__":
  firstflight = AirPeaceDriver(profile="Profile 5", wait_time=120)
  firstflight.get("https://book-airpeace.crane.aero/ibe/loyalty")
  #firstflight.login("110369534", "=Pwanahakay!123=")
  firstflight.new_reservation()
  firstflight.trip_type(1)
  firstflight.execute_script("window.scrollTo(0, 60);")

  firstflight.departure_location("Calabar")
  time.sleep(2)
  firstflight.departure_date(27, "Sep", 2024, 'oneWayDepartureDate')
  time.sleep(2)
  firstflight.departure_location("Lagos", 'firstArrPort')  
  time.sleep(2)
  firstflight.departure_date(11, "Jan", 2025, 'roundTripDepartureDate')





