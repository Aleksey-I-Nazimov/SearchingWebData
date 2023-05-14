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

from random import randint as next_int
from random import uniform as next_float
import json

options = Options()
options.accept_insecure_certs = True
options.page_load_strategy = 'normal'
#options.add_argument("--headless")
options.add_argument('--ignore-certificate-errors')
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

#service = Service("chromedriver.exe")
#driver = webdriver.Chrome(service=service,chrome_options=chrome_options)
#driver.implicitly_wait(15)
#wait = WebDriverWait(driver,15)
#driver.get("https://numamo.org")



def move_mouse_relatively (mouse,step,step_range,timing,is_along_x):
    N = int(abs(step_range))
    for n in range(0,N):
        sleep(timing)
        if is_along_x:
            mouse.move(step,0)
        else:
            mouse.move(0,step)

def move_mouse (mouse,timing,target_x,target_y):
    current_x,current_y = mouse.position
    delta_x = target_x - current_x
    delta_y = target_y - current_y
    step_x = -1 if delta_x<0 else 1
    step_y = -1 if delta_y<0 else 1
    move_mouse_relatively(mouse=mouse,step=step_x,step_range=delta_x,timing=timing,is_along_x=True)
    move_mouse_relatively(mouse=mouse,step=step_y,step_range=delta_y,timing=timing,is_along_x=False)

def simulate_user_screen_click (target_x,target_y):
    n_actions = next_int (2,7)
    mouse = Controller()
    mouse.position = (0,0)
    for action in range(0,n_actions):
        move_mouse (mouse=mouse,timing=next_float(0,0.003),target_x=next_int (0,2*target_x),target_y=next_int (0,2*target_y))
    move_mouse (mouse=mouse,timing=next_float(0,0.001),target_x=target_x,target_y=target_y)
    mouse.click(Button.left, 1)
    print("Clicking on: {}x{}".format(target_x,target_y))
    
def get (driver,url,without_cookie=True,action=None):
    cookies = driver.get_cookies()
    print ("  --> GET: {}".format(url))
    print ("  --> Cookies: {}".format(cookies))
    if without_cookie:
        for cookie in cookies:
            driver.delete_cookie(cookie["name"])
    driver.get(url)
    sleep(1+next_int(1,3))
    if action!=None :
        action(driver)
    return driver
    
def open_chrome_driver (url,options,without_cookie=True):
    driver = webdriver.Chrome(chrome_options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}) 
    driver.maximize_window()
    return get(driver=driver,url=url,without_cookie=without_cookie)

def get_item_location (item,html_y_shift_px=0):
    print("  --> Item location: {} {}".format(item.location,item.size))
    browser_shift = 50
    x = item.location['x'] + item.size['width']/2
    y = item.location['y'] + item.size['height']/2+browser_shift+html_y_shift_px
    return (x,y)

def change_browser_tab_window (driver,awaited_tabs,awaited_title_content):
    WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(num_windows=awaited_tabs))
    current_wh = driver.current_window_handle
    for wh in driver.window_handles:
        print ("  --> Selected tab {}".format(wh))
        if current_wh!=wh:
            driver.switch_to.window(wh)
            print ("  --> Switched tab {}".format(wh))
            break
    WebDriverWait(driver, 30).until(EC.title_contains(title=awaited_title_content))
    print("  --> New window title: {} {}".format(driver.title,driver.current_url))
    return driver

def try_to_find_and_click (driver,xpath,js_click=False,html_y_shift_px=0):
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        el = driver.find_element(By.XPATH,xpath)
        if js_click:
            print ("  --> Making JS click: {}".format(xpath));
            el.click()
        else:
            print("  --> Simulating user movements: {}".format(xpath))
            x,y = get_item_location(item=el,html_y_shift_px=html_y_shift_px)
            simulate_user_screen_click(target_x=x,target_y=y)
    except Exception as e:
        print ("  --> Error: Xpath not found {}\n{}".format(xpath,e))
    return driver

def try_to_find_text(driver,xpath):
    try:
        return driver.find_element(By.XPATH,xpath).text
    except Exception as e:
        print ("  --> Error: The text was not found by{}".format(xpath))
        return None;

def try_to_find_element(driver,xpath):
    try:
        return driver.find_element(By.XPATH,xpath)
    except Exception as e:
        print ("  --> Error: The element was not found by{}".format(xpath))
        return None;
    
def try_to_find_elements(driver,xpath):
    try:
        return driver.find_elements(By.XPATH,xpath)
    except Exception as e:
        print ("  --> Error: The elements was not found by{}".format(xpath))
        return [];



# Welcome to the merlin:-----------------------------------------------------------------
# Google is used to avoid internal commercial blocks
search = "leroymerlin"
url = "https://{}.ru/".format(search)
search_ref_xpath = "//a[@href='{}']".format(url)

driver = open_chrome_driver (url="https://google.ru",options=options,without_cookie=False)
print("  --> Start window title: {}" .format(driver.title))
driver.find_element(By.TAG_NAME,'textarea').send_keys(search+Keys.ENTER)
try_to_find_and_click(driver=driver, xpath=search_ref_xpath)
change_browser_tab_window (driver=driver,awaited_tabs=2,awaited_title_content="Леруа")
#----------------------------------------------------------------------------------------


# Clicking on main buttons and going to the CATALOGUE:-----------------------------------
try_to_find_and_click(driver=driver, xpath="//button[@data-qa-cookie-notification-accept='']",js_click=True)
try_to_find_and_click(driver=driver, xpath="//button[@data-qa-region-accept='']",html_y_shift_px=15)

try_to_find_and_click(driver=driver, xpath="//button[@data-qa-catalogue-button='']",js_click=True)
print("  --> Current window title: {} x {}".format(driver.title,driver.current_url))

try_to_find_and_click(driver=driver, xpath="//button[@data-qa='catalogue-item-name']/span[contains(text(), 'Сад')]",js_click=True)
print("  --> Current window title: {} x {}".format(driver.title,driver.current_url))

try_to_find_and_click(driver=driver, xpath="//button[@data-qa='catalogue-item-name']/span[contains(text(), 'Садовая техника')]",js_click=True)
print("  --> Current window title: {} x {}".format(driver.title,driver.current_url))

try_to_find_and_click(driver=driver, xpath="//a[@data-qa='catalogue-item-name']/span[contains(text(), 'Газонокосилки')]",js_click=True)
print("  --> Current window title: {} x {}".format(driver.title,driver.current_url))
#----------------------------------------------------------------------------------------



# Parsing the single page:---------------------------------------------------------------
product_list=[]

wait_element =  WebDriverWait(driver, 20);
product_divs = wait_element.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-qa-product='']")))
print ("  --> Searched products: {}".format(len(product_divs)));
for product_div in product_divs:
    articule = try_to_find_text(product_div,"div/span")
    name = try_to_find_text(product_div,"div[1]/a/span/span")
    price = try_to_find_text(product_div,"div[2]/div/div/p")
    img_list = try_to_find_elements(product_div, "a/span/picture/source")
    img_list = list(map(lambda img: img.get_attribute("srcset").split(" ")[0],img_list))
    parsed_product = {
        "articule":articule,
        "name":name,
        "price":price,
        "img_list":img_list
        }
    product_list.append(parsed_product)
    print (parsed_product)
#----------------------------------------------------------------------------------------


# Parsing all pages like the single one:-------------------------------------------------
next_template = "//a[contains(@href,'/?page={}')]"
next_cnt =2    
while True:
    next_page_xpath = next_template.format(next_cnt);
    next = try_to_find_element(driver, next_page_xpath)
    if next!=None:
        try_to_find_and_click(driver=driver, xpath=next_page_xpath,js_click=True)
        
        wait_element =  WebDriverWait(driver, 20);
        product_divs = wait_element.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-qa-product='']")))
        print ("  --> +++++++++++++++++++++++++ Searched products: {}".format(len(product_divs)));
        
        # TODO: lets make the separate method
        for product_div in product_divs:
            articule = try_to_find_text(product_div,"div/span")
            name = try_to_find_text(product_div,"div[1]/a/span/span")
            price = try_to_find_text(product_div,"div[2]/div/div/p")
            img_list = try_to_find_elements(product_div, "a/span/picture/source")
            img_list = list(map(lambda img: img.get_attribute("srcset").split(" ")[0],img_list))
            parsed_product = {
                "articule":articule,
                "name":name,
                "price":price,
                "img_list":img_list
            }
            product_list.append(parsed_product)
            print (parsed_product)
        next_cnt+=1;
    else:
        print ("  --> {} pages were parsed! The end!".format(next_cnt-1))
        break;
#----------------------------------------------------------------------------------------


with open("gazonokosilki.json", "w",encoding='utf-8') as text_file:
    text_file.write(json.dumps(product_list))

driver.close();



   


