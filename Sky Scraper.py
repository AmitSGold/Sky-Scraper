#import requests
import bs4
from selenium import webdriver
import time


def popup():
    try:
        driver.find_element_by_class_name("LoginPrompt_LoginPrompt__sKBi6")
        close = driver.find_element_by_class_name("BpkCloseButton_bpk-close-button__1GhbM.BpkModalDialog_bpk-modal__close-button__3hxI0.BpkNavigationBar_bpk-navigation-bar__trailing-item__3MCMV")  
        close.click()
        time.sleep(1)
    except:
        pass
        
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.skyscanner.co.il/')
soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

to = driver.find_element_by_id("fsc-destination-search")

where = input("Where to? ")
to.send_keys(" " + where.title())
time.sleep(1)

trip = input("One Way? (Y/N) ")
if trip.lower() == 'y':
    oneway = driver.find_elements_by_class_name("BpkRadio_bpk-radio__input__1OAwe")[1]
    oneway.click()
    time.sleep(2)
    
departure = driver.find_element_by_id("depart-fsc-datepicker-button")
departure.click()
time.sleep(1)
dep_dates = driver.find_elements_by_class_name("BpkCalendarDate_bpk-calendar-date__MuPBz")
dep_input = int(input("Depart "))
dep_date = dep_dates[dep_input+5]
dep_date.click()
time.sleep(1)
if trip.lower() != 'y':
    ret = driver.find_element_by_id("return-fsc-datepicker-button")
    ret.click()
    time.sleep(1)
    ret_dates = driver.find_elements_by_class_name("BpkCalendarDate_bpk-calendar-date__MuPBz")
    ret_input = int(input("Return "))
    ret_date = ret_dates[ret_input+5]
    ret_date.click()
    time.sleep(1)
    
nos = int(input("Nos. of passengers "))
if nos > 1:
    pas = driver.find_element_by_class_name("CabinClassTravellersSelector_CabinClassTravellersSelector__triggertext__2uAq3")    
    pas.click()
    time.sleep(1)
    more = driver.find_elements_by_class_name("BpkButtonBase_bpk-button__1pnhi.BpkButtonBase_bpk-button--icon-only__3J3rW.BpkButtonSecondary_bpk-button--secondary__1-kNc.BpkNudger_bpk-nudger__button__YOZET")[1]
    for passenger in range(nos-1):
        more.click()
        time.sleep(1)
    done = driver.find_element_by_xpath('//*[@id="cabin-class-travellers-popover"]/footer/button')
    done.click()
    time.sleep(2)
    
go = driver.find_element_by_xpath('//*[@id="flights-search-controls-root"]/div/div/form/div[3]/button')
go.click()

newURl = driver.window_handles[0]
driver.switch_to_window(newURl)
soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
time.sleep(5)

popup()
time.sleep(5)

if 'Sorry, we found no results on these dates' in soup.text:
    print("No flights found for this destination on these dates")
    cont = input("Try other dates for same destination?" )
    if cont.lower() == 'y':
       driver.get('https://www.skyscanner.co.il/')
       to.send_keys(" " + where)
       time.sleep(1)
       if trip.lower() == 'y':
           oneway = driver.find_elements_by_class_name("BpkRadio_bpk-radio__input__1OAwe")[1]
           oneway.click()
elif "Want non-stop flights" or "Want a non-stop flight" in soup.text:
    go = driver.find_element_by_class_name("BpkText_bpk-text__2NHsO.BpkText_bpk-text--lg__3vAKN.BpkText_bpk-text--bold__4yauk")
    go.click()
    time.sleep(5)
    newURl = driver.window_handles[0]
    driver.switch_to_window(newURl)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')           
    popup()
    time.sleep(5)


buttons = driver.find_elements_by_class_name("DangerouslyUnstyledButton_container__xKSmg.DangerouslyUnstyledButton_enabled__2yl7j.FqsTabs_fqsTabWithSparkle__1PIoz")
cheap = buttons[1]
cheap.click()
time.sleep(5)

ticket = driver.find_element_by_class_name("EcoTicketWrapper_itineraryContainer__1VGlu")
print(ticket.text)

okay = input("Is this ticket fine? ")
if okay.lower() == 'y':
    go = driver.find_elements_by_class_name("BpkTicket_bpk-ticket__paper__2gPSe")[1]
    go.click()
    time.sleep(5)

    newURl = driver.window_handles[0]
    driver.switch_to_window(newURl)

    popup()
    
    links = driver.find_elements_by_tag_name("a")
    urls= [link.get_attribute('href') for link in links]
    flights = [url for url in urls if isinstance(url,str) and ('transport_deeplink' in url or 'checkliveprice' in url)]
    flight = flights[0]
    print(flight)

#driver.execute_script("window.history.go(-1)")


class Sky_Scraper:
    
    def __init__(self, where = '', one_way = False, dep = 0, ret = 0, pax = 1):
        self.where = where
        self.one_way = one_way
        self.dep = dep
        self.ret = ret
        self.pax = pax
    
    def flight_search(self):
        to = driver.find_element_by_id("fsc-destination-search")
        to.send_keys(" " + where.title())
        time.sleep(1)
        
        if self.one_way:
           oneway = driver.find_elements_by_class_name("BpkRadio_bpk-radio__input__1OAwe")[1]
           oneway.click()
           time.sleep(2) 
           
        departure = driver.find_element_by_id("depart-fsc-datepicker-button")
        departure.click()
        time.sleep(1)
        dep_dates = driver.find_elements_by_class_name("BpkCalendarDate_bpk-calendar-date__MuPBz")
        dep_date = dep_dates[self.dept+5]
        dep_date.click()
        time.sleep(1)
        
        if not self.one_way:
            ret = driver.find_element_by_id("return-fsc-datepicker-button")
            ret.click()
            time.sleep(1)
            ret_dates = driver.find_elements_by_class_name("BpkCalendarDate_bpk-calendar-date__MuPBz")
            ret_date = ret_dates[ret_input+5]
            ret_date.click()
            time.sleep(1)
        
        if self.pax > 1:
            pas = driver.find_element_by_class_name("CabinClassTravellersSelector_CabinClassTravellersSelector__triggertext__2uAq3")    
            pas.click()
            time.sleep(1)
            more = driver.find_elements_by_class_name("BpkButtonBase_bpk-button__1pnhi.BpkButtonBase_bpk-button--icon-only__3J3rW.BpkButtonSecondary_bpk-button--secondary__1-kNc.BpkNudger_bpk-nudger__button__YOZET")[1]
            for passenger in range(self.pax-1):
                more.click()
                time.sleep(1)
            done = driver.find_element_by_xpath('//*[@id="cabin-class-travellers-popover"]/footer/button')
            done.click()
            time.sleep(2)
        
    def popup():
    try:
        driver.find_element_by_class_name("LoginPrompt_LoginPrompt__sKBi6")
        close = driver.find_element_by_class_name("BpkCloseButton_bpk-close-button__1GhbM.BpkModalDialog_bpk-modal__close-button__3hxI0.BpkNavigationBar_bpk-navigation-bar__trailing-item__3MCMV")  
        close.click()
        time.sleep(1)
    except:
        pass