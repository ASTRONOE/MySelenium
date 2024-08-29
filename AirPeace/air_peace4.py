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
    departure_day = self.find_element(By.ID, id) #firstDepPort firstArrPort
    self.action.move_to_element(departure_day).click()
    self.action.send_keys(f"{place}")
    self.action.send_keys(Keys.ENTER).perform()
    #self.execute_script(f"arguments[0].value = '{place}';", departure)

  def calendar_popup(self):
    calendar = self.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[4]/div[2]/div[1]/table')
    time.sleep(1)
    date = calendar.find_elements(By.CSS_SELECTOR, 'div.filter-option-inner-inner')
    next_date = calendar.find_element(By.CSS_SELECTOR, 'th.next.available')
    self.action.move_to_element(next_date).perform()
    return date, next_date

  def departure_date(self, day:int, mon:int|str, year:int, id:str):
    departure = self.find_element(By.ID, id)
    date_str = f"{day} {mon} {year}"
    self.execute_script("""
      arguments[0].removeAttribute('readonly');
      arguments[0].setAttribute('data-allowed-manual', 'true');
      """, departure)
    #self.execute_script(f"arguments[0].value = '{date_str}';", departure)
    # dud_icon = self.find_element(By.CSS_SELECTOR, 'span.input-group-text.icon-departure-date')
    # self.action.move_to_element(dud_icon).click().perform()
    #self.execute_script("arguments[0].dispatchEvent(new Event('change'));", departure)
    self.execute_script("""
      var input = arguments[0];
      var value = arguments[1];
      
      // Set the value of the input field
      input.value = value;
      
      // Create and dispatch 'input' and 'change' events
      var event = new Event('input', { bubbles: true });
      input.dispatchEvent(event);
      event = new Event('change', { bubbles: true });
      input.dispatchEvent(event);
      """, departure, date_str)
    
  def search_flight_click(self):
    button = self.find_element(By.CSS_SELECTOR, 'div.col-12 > button')
    button.click()

  def use_miles(self, yes=True):
    if yes is False:
      miles_checkbox = self.find_element(By.XPATH,
        '/html/body/div[2]/div/div/div[1]/div[4]/div[3]/div[4]/div/div/div/form/div/div/div[2]/div[2]/div/div')
      toggle = miles_checkbox.find_element(By.CSS_SELECTOR, 'ins.iCheck-helper')
      self.action.move_to_element(toggle).click().perform()

  def passenger_count(self, adult=1, child=0, infant=0):
    passengers = self.find_element(By.ID, 'textPersonCount')
    self.action.move_to_element(passengers).click().perform()
    passenger_box = self.find_element(By.CSS_SELECTOR, 'div.search__bar_passengers')

    adult_counter = passenger_box.find_element(By.CSS_SELECTOR, 'span.counter__plus.adultCount.plus')
    child_counter = passenger_box.find_element(By.CSS_SELECTOR, 'span.counter__plus.childCount.plus')
    infant_counter = passenger_box.find_element(By.CSS_SELECTOR, 'span.counter__plus.infantCount.plus')

    for _ in range(1, adult):
      self.action.move_to_element(adult_counter).click().perform()
      time.sleep(0.5)
    for _ in range(child):
      self.action.move_to_element(child_counter).click().perform()
      time.sleep(0.5)
    for _ in range(infant):
      self.action.move_to_element(infant_counter).click().perform()
      time.sleep(0.5)
    
    self.action.move_to_element(passengers).click().perform()

if __name__ == "__main__":
  firstflight = AirPeaceDriver(profile="Default", wait_time=120)
  firstflight.get("https://book-airpeace.crane.aero/ibe/loyalty")
  #firstflight.login("110369534", "=Pwanahakay!123=", tick=True)
  firstflight.new_reservation()
  firstflight.trip_type(0)
  firstflight.execute_script("window.scrollBy(0, 70);")
  # time.sleep(3)
  # firstflight.departure_date(28, "Nov", 2024, 'roundTripDepartureDate')
  time.sleep(3)
  firstflight.passenger_count(adult=3, child=2)
  firstflight.departure_location("Lagos")
  time.sleep(3)
  firstflight.departure_location("Calabar", "firstArrPort")
  time.sleep(3)
  firstflight.departure_date(4, "Sep", 2024, 'oneWayDepartureDate')

  firstflight.search_flight_click()



# var input = arguments[0];
# var value = arguments[1];

# // Focus on the input field
# input.focus();

# // Set the value of the input field
# input.value = value;

# // Create and dispatch 'input' and 'change' events
# var event = new Event('input', { bubbles: true });
# input.dispatchEvent(event);
# event = new Event('change', { bubbles: true });
# input.dispatchEvent(event);

# // Blur the input field
# input.blur();


