import bs4
from selenium import webdriver
import time

DESTINATION_TARGET = "fsc-destination-search"
ONE_WAY_BUTTON = "BpkRadio_bpk-radio__3J6D-.TripTypeSelector_TripTypeSelector__1qmS8"
DEPART_DATE_BUTTON = "depart-fsc-datepicker-button"
RETURN_DATE_PICKER = "return-fsc-datepicker-button"
DATE_PICKER = "BpkCalendarGrid_bpk-calendar-grid__date__3Dy_6"
NO_PASSANGERS_BOX = "CabinClassTravellersSelector_CabinClassTravellersSelector__triggertext__3e3km"
PASSANGERS_ADD_BUTTON = "BpkButtonBase_bpk-button__3QGRV.BpkButtonBase_bpk-button--icon-only__3Ww9s.BpkButtonSecondary_bpk-button--secondary__1quDO.BpkNudger_bpk-nudger__button__1RgFI"
PASSANGERS_DONE_XPATH = '//*[@id="cabin-class-travellers-popover"]/footer/button'
START_SEARCH_XPATH = '//*[@id="flights-search-controls-root"]/div/div/form/div[3]/button'


NON_STOP_CONT = "BpkText_bpk-text__2VouB.BpkText_bpk-text--lg__1PdnC.BpkText_bpk-text--bold__NhE9P"

def input_number(prompt):
    while True:
        try:
            result = int(input(prompt))
            break
        except TypeError:
            print('Please input a number')

    return result

class Flight_Parameters():
    
    def __init__(self):
   
        self.where = input("Where to? ")
    
        one_way = input("One Way? (Y/N) ")
 
        if one_way.lower() == 'y':
            self.oneway = True
            self.return_date = None
        
        else:
            self.oneway = False
            
        
        self.depart_date = input_number("Depart ")
        
        if not self.oneway:
            self.return_date = input_number("Return ")
    
        self.passengers = input_number("Nos. of passengers ")
    

class Sky_Scraper:
    
    def __init__(self, where = '', one_way = False, dep = 0, ret = 0, passengers = 1):
        self.where = where
        self.one_way = one_way
        self.dep = dep
        self.ret = ret
        self.passengers = passengers
    
    def set_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        #options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://www.skyscanner.co.il/')
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        self.driver = driver
        self.soup = soup
        
    def set_destination(self,sleep_time = 1):
        to = self.driver.find_element_by_id(DESTINATION_TARGET)
        to.send_keys(" " + self.where.title())
        time.sleep(sleep_time)
        
    def set_one_way(self, sleep_time = 2):
        if self.one_way:
         oneway = self.driver.find_elements_by_class_name(ONE_WAY_BUTTON)[1]
         oneway.click()
         time.sleep(sleep_time)   
            
    def set_depart_day(self,sleep_time = 3):
        departure = self.driver.find_element_by_id(DEPART_DATE_BUTTON)
        departure.click()
        time.sleep(sleep_time)
        dep_dates = self.driver.find_elements_by_class_name(DATE_PICKER)
        dep_date = dep_dates[self.dep-1]
        dep_date.click()
        time.sleep(sleep_time)
    
    def set_return_day(self,sleep_time = 1):
        ret = self.driver.find_element_by_id(RETURN_DATE_PICKER)
        ret.click()
        time.sleep(sleep_time)
        ret_dates = self.driver.find_elements_by_class_name(DATE_PICKER)
        ret_date = ret_dates[self.ret-1]
        ret_date.click()
        time.sleep(sleep_time)
        
    def set_no_of_passengers(self, sleep_time = 1):
        pas = self.driver.find_element_by_class_name(NO_PASSANGERS_BOX)    
        pas.click()
        time.sleep(sleep_time)
        more = self.driver.find_elements_by_class_name(PASSANGERS_ADD_BUTTON)[1]
        for passenger in range(self.passengers-1):
            more.click()
            time.sleep(sleep_time)
        done = self.driver.find_element_by_xpath(PASSANGERS_DONE_XPATH)
        done.click()
        time.sleep(sleep_time+1)
            
    def flight_search(self): 
        
        self.set_destination()
        
        self.set_depart_day()
        
        if self.one_way:
            self.set_one_way()
        else:
            self.set_return_day()
        
        if self.passengers > 1:
            self.set_no_of_passengers()
        
        go = self.driver.find_element_by_xpath(START_SEARCH_XPATH)
        go.click()
        
    def close_login_popup(self):
        try:
            self.driver.find_element_by_class_name("LoginPrompt_LoginPrompt__sKBi6")
            close = self.driver.find_element_by_class_name("BpkCloseButton_bpk-close-button__1GhbM.BpkModalDialog_bpk-modal__close-button__3hxI0.BpkNavigationBar_bpk-navigation-bar__trailing-item__3MCMV")  
            close.click()
            time.sleep(1)
            self.get_new_URL()
        except:
            pass
    
    def check_for_no_flights(self):
      if 'Sorry, we found no results on these dates' in self.soup.text:
          print("No flights found for this destination on these dates")
          return True
      elif "Want non-stop flights" or "Want a non-stop flight" in self.soup.text:
          go = self.driver.find_element_by_class(NON_STOP_CONT)
          go.click()
          self.get_new_URL()        
          self.close_login_popup()
          
    def get_new_URL(self, sleep_time = 5):
        time.sleep(sleep_time)
        newURl = self.driver.window_handles[0]
        self.driver.switch_to_window(newURl)
        soup = bs4.BeautifulSoup(self.driver.page_source, 'lxml')
        self.soup = soup
        
    def set_to_cheap(self, sleep_time = 5):
        buttons = self.driver.find_elements_by_class_name("DangerouslyUnstyledButton_container__xKSmg.DangerouslyUnstyledButton_enabled__2yl7j.FqsTabs_fqsTabWithSparkle__1PIoz")
        cheap = buttons[1]
        cheap.click()
        time.sleep(sleep_time)
        
    def get_ticket_info(self, cycle = 0):
        ticket = self.driver.find_elements_by_class_name("EcoTicketWrapper_itineraryContainer__1VGlu")[cycle]
        ticket_info = ticket.text
        return ticket_info
    
    def get_ticket_URL(self,sleep_time = 5, cycle = 0):
            go = self.driver.find_elements_by_class_name("BpkTicket_bpk-ticket__paper__2gPSe")[cycle+1]
            go.click()
            time.sleep(sleep_time)
            self.get_new_URL()
            links = self.driver.find_elements_by_tag_name("a")
            urls= [link.get_attribute('href') for link in links]
            flights = [url for url in urls if isinstance(url,str) and ('transport_deeplink' in url or 'checkliveprice' in url)]
            ticket_URL = flights[0]
            return ticket_URL
    
    def return_to_results(self,sleep_time = 5):
        back = self.driver.find_element_by_class_name("BpkLink_bpk-link__2Jqrw.BpkNavigationBarButtonLink_bpk-navigation-bar-button-link__14cZB.DetailsPanelHeader_backButtonLink__3BHkr.BpkNavigationBar_bpk-navigation-bar__leading-item__2WJLe")
        back.click()
        time.sleep(sleep_time)
        self.get_new_URL
        
    def get_tickets_list(self, nos_of_tickets = 3):

        while True:
            self.set_driver()
            self.flight_search()
            self.get_new_URL()
            self.close_login_popup()
            if self.check_for_no_flights():
                break
            self.set_to_cheap()
            tickets_list = []
            for ticket in range(nos_of_tickets):
                ticket_particulars = []
                ticket_info = self.get_ticket_info(ticket)
                ticket_particulars.append(ticket_info)
                ticket_URL = self.get_ticket_URL()
                ticket_particulars.append(ticket_URL)
                tickets_list.append(ticket_particulars)
                self.return_to_results()
            
            return tickets_list

my_parameters = Flight_Parameters()               
my_search = Sky_Scraper(my_parameters.where,my_parameters.oneway,my_parameters.depart_date,my_parameters.return_date,my_parameters.passengers)
tickets_list = my_search.get_tickets_list()           
