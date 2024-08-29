import json
import time
import mysql.connector as mycon
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

edge_profile_path = r"C:\Users\user\AppData\Local\Microsoft\Edge\User Data"
edge_options = EdgeOptions()
edge_options.add_experimental_option('detach', True)
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6367.78 Safari/537.36")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
edge_options.add_argument(f"user-data-dir={edge_profile_path}")
edge_options.add_argument(f"--profile-directory=Default")

driver = webdriver.Edge(options=edge_options)
action = ActionChains(driver)
wait = WebDriverWait(driver, 80)

driver.get("https://www.radarbox.com/data/airlines/APK")


def loading(load_next):
  if load_next == 'next':
    wait.until(visibility((By.XPATH, '/html/body/main/div/div/div/table/tbody/tr[1]/td/div/button'))).click()
  elif load_next == 'previous':
    wait.until(visibility((By.XPATH, '/html/body/main/div/div/button'))).click()
  else:
    raise ValueError("Value should be 'next' or 'previous'")
  
def flights_list():
  flight_table = wait.until(visibility((By.TAG_NAME, 'table')))
  #flight_header = flight_table.find_element(By.TAG_NAME, 'thead')
  flight_body = flight_table.find_element(By.TAG_NAME, 'tbody')
  driver.execute_script("arguments[0].scrollIntoView();", flight_body)
  flight_rows = flight_body.find_elements(By.TAG_NAME, 'tr')
  all_flights = []
  for row in flight_rows:
    driver.execute_script("arguments[0].scrollIntoView();", row)
    all_flights.append(row.get_attribute('id'))
  if all_flights[0] == '':
    del all_flights[0]
  return all_flights

def present(element, default):
  value = element if element else default
  return value

def flight_data(id):  # from flights_list
  default_text, default_link = "N/A", "#"
  flight_table = wait.until(visibility((By.TAG_NAME, 'table')))
  flight_body = flight_table.find_element(By.TAG_NAME, 'tbody')
  row = flight_body.find_element(By.ID, id)
  row_dict = {
    "date": default_text,
    "flight": {"id": default_text, "link": default_link},
    "departure": {"location": default_text, "link": default_link, "airport": default_text},
    "scheduled time of departure": default_text,
    "arrival": {"location": default_text, "link": default_link, "airport": default_text},
    "scheduled time of arrival": default_text,
    "aircraft": {"id": default_text, "link": default_link},
    "status": default_text,
    "duration": default_text
  }
  try:
    row_dict["date"] = present(row.find_element(By.ID, 'date').text, default_text)

    flight = row.find_element(By.ID, 'flight')
    flight_elements = flight.find_elements(By.TAG_NAME, 'a')
    row_dict["flight"]["id"] = present(flight_elements[1].text if len(flight_elements) > 1 else "", default_text)
    row_dict["flight"]["link"] = present(flight_elements[1].get_attribute('href') if len(flight_elements) > 1 else "", default_link)

    departure = row.find_element(By.ID, 'departure')
    row_dict["departure"]["location"] = present(departure.find_element(By.TAG_NAME, 'a').text, default_text)
    row_dict["departure"]["link"] = present(departure.find_element(By.TAG_NAME, 'a').get_attribute('href'), default_link)
    row_dict["departure"]["airport"] = present(departure.find_element(By.TAG_NAME, 'small').text, default_text)

    row_dict["scheduled time of departure"] = present(row.find_element(By.ID, 'std').text, default_text)

    arrival = row.find_element(By.ID, 'arrival')
    row_dict["arrival"]["location"] = present(arrival.find_element(By.TAG_NAME, 'a').text, default_text)
    row_dict["arrival"]["link"] = present(arrival.find_element(By.TAG_NAME, 'a').get_attribute('href'), default_link)
    row_dict["arrival"]["airport"] = present(arrival.find_element(By.TAG_NAME, 'small').text, default_text)

    row_dict["scheduled time of arrival"] = present(row.find_element(By.ID, 'sta').text, default_text)

    aircraft = row.find_element(By.ID, 'aircraft')
    row_dict["aircraft"]["id"] = present(aircraft.find_element(By.TAG_NAME, 'a').text, default_text)
    row_dict["aircraft"]["link"] = present(aircraft.find_element(By.TAG_NAME, 'a').get_attribute('href'), default_link)

    status = row.find_element(By.ID, 'status')
    row_dict["status"] = present(status.find_element(By.TAG_NAME, 'span').text, default_text)

    duration = row.find_element(By.ID, 'duration')
    row_dict["duration"] = present(duration.find_element(By.TAG_NAME, 'span').text, default_text)

  except (NoSuchElementException, StaleElementReferenceException):
      # Handle the exception and continue
    pass
  return row_dict
    

def store_flight_data(file_name):
  list_of_flights = flights_list()
  json_file = open(f'{file_name}.json', 'a')
  for flight_id in list_of_flights:
    flight = flight_data(flight_id)
    json.dump(flight, json_file, indent=3)
  json_file.close()

def store_flight_json(file_name):
  list_of_flights_dict = []
  for 
  with open(f'{file_name}.json', 'a') as json_file:
    json.dump(list)

def main_json(file_name, load, nexts=0):
  time.sleep(10)
  for _ in range(nexts):
    store_flight_data(file_name)
    loading(load)

# Step 3: Save to an SQL database
# def create_sql_table():
#   '''
#   CREATE TABLE Flights (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     flight_date VARCHAR(255),
#     flight_id VARCHAR(255),
#     flight_link VARCHAR(255),
#     departure_location VARCHAR(255),
#     departure_link VARCHAR(255),
#     departure_airport VARCHAR(255),
#     scheduled_departure VARCHAR(255),
#     arrival_location VARCHAR(255),
#     arrival_link VARCHAR(255),
#     arrival_airport VARCHAR(255),
#     scheduled_arrival VARCHAR(255),
#     aircraft_id VARCHAR(255),
#     aircraft_link VARCHAR(255),
#     status VARCHAR(255),
#     duration VARCHAR(255)
# );
#   '''

# def connect_to_database():
#   try:
#     connection = mycon.connect(
#       host='localhost',  # or your MySQL server address
#       database='flights_db',
#       user='your_username',
#       password='your_password'
#     )
#     if connection.is_connected():
#       print("Connected to MySQL database")
#       return connection
#   except mycon.Error as e:
#     print(f"Error: {e}")
#     return None

# def insert_flight_data_sql(connection, flight_data):
#   cursor = connection.cursor()
#   insert_query = """
#     INSERT INTO flights (
#       flight_date, flight_id, flight_link, departure_location,
#       departure_link, departure_airport, scheduled_departure,
#       arrival_location, arrival_link, arrival_airport,
#       scheduled_arrival, aircraft_id, aircraft_link, status, duration
#     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#   try:
#     cursor.execute(insert_query, (
#     flight_data['date'],
#     flight_data['flight']['id'], flight_data['flight']['link'],
#     flight_data['departure']['location'], flight_data['departure']['link'], flight_data['departure']['airport'],
#     flight_data['scheduled time of departure'],
#     flight_data['arrival']['location'], flight_data['arrival']['link'], flight_data['arrival']['airport'],
#     flight_data['scheduled time of arrival'],
#     flight_data['aircraft']['id'], flight_data['aircraft']['link'],
#     flight_data['status'], flight_data['duration']))
#     connection.commit()
#   except mycon.Error as e:
#     print(f"Failed to insert record into MySQL table: {e}")

# def store_flight_data_sql(connection):
#   for flight_id in flights_list():
#     flight = flight_data(flight_id)
#     insert_flight_data_sql(connection, flight)

# def main_sql(load, nexts=0):
#   connection = connect_to_database()
#   if connection is None:
#     return
#   for _ in range(nexts):
#     store_flight_data_sql(connection)
#     loading(load)
# connection.close()

if __name__ == "__main__":
  main_json(file_name='more_flights', load='previous', nexts=4)
  print("FINISHED")
