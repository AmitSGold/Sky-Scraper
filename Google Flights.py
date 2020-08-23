#import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.com/flights')
soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

time.sleep(1)
to = driver.find_elements_by_class_name("flt-input")[1]
to.click()
to = driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input')

where = input("Where to? ")
to.send_keys(where)
time.sleep(1)
to.send_keys(Keys.ENTER)

trip = input("One Way? ")
if trip.lower() == 'y':
    drop = driver.find_element_by_class_name("gws-flights-form__menu-label")
    drop.click()
    oneway = driver.find_elements_by_class_name("mSPnZKpnf91__menu-item")[1]
    oneway.click()
    time.sleep(1)

nos = int(input("Nos. of passengers "))
if nos > 1:
    pas = driver.find_element_by_xpath('//*[@id="flt-pax-button"]')    
    pas.click()
    time.sleep(1)
    more = driver.find_elements_by_class_name("gws-flights-widgets-numberpicker__flipper-shadow")[1]
    for passenger in range(nos-1):
        more.click()
        time.sleep(1)
    done = driver.find_element_by_class_name("gws-flights__dialog-button.gws-flights__dialog-primary-button")
    done.click()
    time.sleep(2)
    
departure = driver.find_element_by_class_name("flt-input.gws-flights__flex-box.gws-flights__flex-filler.gws-flights-form__departure-input")
departure.click()
time.sleep(1)
dates = driver.find_elements_by_class_name("gws-travel-calendar__day-label")
dep_input = int(input("Depart "))
dep_date = dates[dep_input-1]
dep_date.click()
time.sleep(1)
if trip.lower() != 'y':
    ret_input = int(input("Return "))
    ret_date = dates[ret_input-1]
    ret_date.click()
    time.sleep(1)
done = driver.find_element_by_class_name("eE8hUfzg9Na__button.eE8hUfzg9Na__legacy-button.eE8hUfzg9Na__blue")
done.click()
time.sleep(3)



#go = driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[4]/floating-action-button')
#go.click()
#time.sleep(5)

sort = driver.find_elements_by_class_name("mSPnZKpnf91__container")[1]
sort.click()
time.sleep(2)
cheap = driver.find_elements_by_class_name("gws-flights-results__sort-menu-option")[1]
cheap.click()
time.sleep(3)
drop = driver.find_element_by_class_name("gws-flights-results__more")
drop.click()
time.sleep(2)

ticket = driver.find_element_by_class_name("gws-flights-results__result-item")
print(ticket.text)
time.sleep(1)

okay = input("Is this ticket fine? ")
if okay.lower() == 'y':
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(1)
    go = driver.find_element_by_class_name("gws-flights-results__itinerary-details-heading.gws-flights__flex-box.gws-flights__flex-filler.gws-flights__align-center.flt-subhead1")
    go.click()
    time.sleep(2)

    #go = driver.find_element_by_class_name("gws-flights-results__itinerary-details-heading.gws-flights__flex-box.gws-flights__flex-filler.gws-flights__align-center.flt-subhead1")
    #go.click()
    #time.sleep(2)
    
    if trip.lower() != "y":
        second = driver.find_element_by_class_name("gws-flights-results__expand")
        second.click()
        time.sleep(1)
        return_ticket = driver.find_element_by_class_name("gws-flights-results__result-list")
        print(return_ticket.text)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(2)
        go = driver.find_element_by_class_name("gws-flights-results__select-button.CpMx2b.LZHEY.flt-subhead2.RQn3j")
        go.click()
        time.sleep(1)

        
    button = driver.find_element_by_class_name("gws-flights-book__book-button")
    button.click()
    
    driver.switch_to.window(driver.window_handles[-1])
    flight = driver.current_url
    print(flight)
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

#driver.find_element_by_class_name("gws-flights__flex-box gws-flights__flex-filler gws-flights-form__departure-input gws-flights-form__round-trip" data-flt-ve="departure_date" role="presentation" jsaction="jsl._;f_f:jsl._;ica_bc:jsl._;keydown:jsl._" jsan="7.flt-input,7.gws-flights__flex-box,7.gws-flights__flex-filler,7.gws-flights-form__departure-input,7.gws-flights-form__round-trip,0.data-flt-ve,0.role,22.jsaction" jstcache="579"><div jscontroller="pSNSIe" class="gws-flights-widgets-inputcapturearea__capture-area-wrapper" jsaction="rcuQ6b:npT2md" jstcache="580"><span jsname="bOjMyf" style="display:none" aria-live="polite" jsvs="'bOjMyf';" jsan="0.jsname,5.display,0.aria-live,t-Zq6YzLjb2h0" id="flt-ica-3" jstcache="492"> <jsl jstcache="588">Departure date</jsl> <span jstcache="589">Mon, 31 Aug</span> </span><textarea jsname="LlUqIb" class="gws-flights-widgets-inputcapturearea__capture-area" data-focus_id="date-0" role="textbox" tabindex="0" jsaction="keyup:dbqUTd;focus:h06R8;blur:zjh6rb" jsvs="'LlUqIb';'keyup:dbqUTd;focus:h06R8;blur:zjh6rb';" jsan="0.jsname,7.gws-flights-widgets-inputcapturearea__capture-area,0.data-focus_id,0.role,0.tabindex,22.jsaction" aria-labelledby="flt-ica-3" jstcache="493"></textarea></div><jsl jstcache="581"><span class="gws-flights-form__calendar-icon"><span class="z1asCe zKp81c"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"></path></svg></span></span></jsl><div class="gws-flights__flex-filler gws-flights__ellipsize gws-flights-form__input-target" aria-hidden="true" jstcache="0"><span class="gws-flights-form__date-content" jstcache="582">Mon, 31 Aug</span></div><div style="" jsan="7.gws-flights-form__flipper,t-wS2ukrFosTY" jstcache="583" class="gws-flights-form__flipper"><span jstcache="591" jsaction="jsl._" jsan="22.jsaction" class="gws-flights-form__prev" aria-hidden="true" role="presentation" tabindex="-1"><span class="z1asCe u3p1Tb"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"></path></svg></span></span><span jstcache="592" jsaction="jsl._" jsan="22.jsaction" class="gws-flights-form__next" aria-hidden="true" role="presentation" tabindex="-1"><span class="z1asCe LV6CSb"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"></path></svg></span></span></div></div>