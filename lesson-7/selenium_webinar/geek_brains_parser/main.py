from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from pynput.mouse import Button, Controller




#from selenium.webdriver.support import 

options = Options()
options.accept_insecure_certs = True
options.page_load_strategy = 'normal'
#options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
#options.add_argument("cookie=_slid_server=; _ym_uid=164595051449003469; _slid_server=; ggr-widget-test=1; _ym_d=1683683759; _regionID=34; cookie_accepted=true; st_uid=debdb1d9e430bf8117df5694a2678fb7; _singleCheckout=true; _unifiedCheckout=true; _showSberPay=true; _clientTypeInBasket=true; _gaexp=GAX1.2.IUgFRjY7S7qnkK4uRsCZRw.19540.2; x-api-option=srch-2705-default; _ym_isad=2; ___dmpkit___=e463a62e-1851-4b08-be2d-fb8e70024898; iap.uid=6387fdc8fcff41a28c67d9c5ecf48d68; tmr_lvid=7b0003e32b9384637908fb66f3b526c2; tmr_lvidTS=1683683761853; aplaut_distinct_id=TlcUgZous3jm; uxs_uid=d1b94c60-eed5-11ed-9878-2f55b839328d; adrdel=1; adrcid=A2rJzc_V05H8yWxO5y85uZw; _gid=GA1.2.1524893129.1683683767; qrator_ssid=1683686186.566.vvM1lQSAPaxV035o-0mpq8n72ohcp78ncevgaltqoa7sa1rd6; qrator_jsid=1683686239.474.fofEyXOsguFhjRnk-t4tk50qh4gn104b9be5cmpcceaurr0s9; GACookieStorage=GA1.2.1698243876.1683683760; _ga=GA1.2.1698243876.1683683760; tmr_detect=0|1683686244411; _ga_Z72HLV7H6T=GS1.1.1683686238.2.1.1683686258.0.0.0")

# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_argument("disable-blink-features=AutomationControlled")

# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 

# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 

#driver = webdriver.Chrome(chrome_options=chrome_options)

#service = Service("chromedriver.exe")
#driver = webdriver.Chrome(service=service,chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}) 

#driver.implicitly_wait(15)




#wait = WebDriverWait(driver,15)

#driver.get("https://numamo.org")
driver.maximize_window()
driver.get("https://google.ru")
sleep(3)

print("Parent window title: " + driver.title)
driver.find_element(By.TAG_NAME,'textarea').send_keys("leroymerlin"+Keys.ENTER)
sleep(3)

merlin_item = driver.find_element(By.XPATH,"//a[@href='https://leroymerlin.ru/']")
print(merlin_item.location)
print(merlin_item.size)

x = merlin_item.location['x'] + merlin_item.size['width']/2
y = merlin_item.location['y'] + merlin_item.size['height']/2+50

mouse = Controller()
mouse.position = (0,0)

for xtr in range(0,int(x)):
    sleep(0.01)
    mouse.move(1,0)
    
for xtr in range(0,int(y)):
    sleep(0.01)
    mouse.move(0,1)

mouse.click(Button.left, 1)
print("Clicking on: {}x{}".format(x,y))



current_wh = driver.current_window_handle
all_wh = driver.window_handles

for wh in all_wh:
    if current_wh!=wh:
        driver.switch_to.window(wh)
        break

print("New window title: " + driver.title)

#di
sleep(1000)


#element = driver.find_element(By.XPATH,"//button[contains(@data-testid,'button')]")

# //button[@data-qa="catalogue-item-name"]
# //a[@data-qa="catalogue-item-name"]

# action = ActionChains(driver)
# action.move_to_element(merlin_item) 
# action.click()
# action.perform()

#driver.find_element(By.XPATH,"//a[@href='https://leroymerlin.ru/']").click()

html_string = driver.page_source
print(html_string)
driver.close();



   


