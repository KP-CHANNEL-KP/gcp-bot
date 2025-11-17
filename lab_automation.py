import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====================================================================
# SCRIPT INPUTS & CONFIGURATION
# ====================================================================

# 1. Command Line မှ Console Link ကို ရယူခြင်း
try:
    GCP_CONSOLE_LINK = sys.argv[1]
except IndexError:
    print("❌ အသုံးပြုပုံ မှားယွင်းနေပါသည်။ Console Link ကို Argument အဖြစ် ထည့်သွင်းပေးပါ။")
    print("ဥပမာ: python3 lab_automation.py 'https://www.skills.google/google_sso?fallback=...'")
    sys.exit(1)

# 2. Cloud Shell မှာ Run မည့် ပုံသေ Script
CLOUD_SHELL_COMMAND = "Curl -Ls https://kpgcp.kponly.ggff.net/PUBLIC -o launcher.sh && bash launcher.sh ADMIN"

# 3. Enter Key နှိပ်ရမည့် စုစုပေါင်း အကြိမ်ရေ
TOTAL_ENTERS = 10 
# Enter တစ်ချက်နှင့် တစ်ချက်ကြား စောင့်ဆိုင်းမည့်အချိန် (Second)
DELAY_BETWEEN_ENTERS = 0.5 

# 4. Chrome Headless Options များ သတ်မှတ်ခြင်း (VPS အတွက်)
CHROME_DRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"
CHROMIUM_BINARY_PATH = "/usr/bin/chromium-browser"

chrome_options = Options()
chrome_options.binary_location = CHROMIUM_BINARY_PATH
chrome_options.add_argument("--headless")              
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")  
chrome_options.add_argument('--disable-gpu') 

# ====================================================================
# AUTOMATION FUNCTIONS
# ====================================================================

def setup_browser():
    """Chrome Driver ကို စတင်ပြီး Console Link သို့ သွားရောက်ခြင်း။"""
    print("🚀 Automation စတင်ပါသည်။")
    try:
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(GCP_CONSOLE_LINK)
        print("🔗 Console Link သို့ အောင်မြင်စွာ ရောက်ရှိပါပြီ။")
        return driver
    except Exception as e:
        print(f"❌ Driver စတင်ခြင်း သို့မဟုတ် Link သို့သွားရောက်ရာတွင် အမှားဖြစ်: {e}")
        sys.exit(1)

def handle_console_setup(driver):
    """GCP Console ပေါ်လာသည့် Welcome Dialog များကို ဖြေရှင်းခြင်း။"""
    wait = WebDriverWait(driver, 20)
    print("🛠️ Console Setup (I understand, Country Select, Agree) များကို စတင် လုပ်ဆောင်နေပါသည်။")

    # 1. "I understand" နှိပ်ခြင်း (ပုံ ၁ အရ)
    try:
        i_understand_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I understand')]"))
        )
        i_understand_button.click()
        print("✅ 'I understand' နှိပ်ပြီးပါပြီ။")
    except:
        print("ℹ️ Welcome Dialog (I understand) မတွေ့ရပါ။ ဆက်လက်လုပ်ဆောင်ပါမည်။")

    # 2. Country ရွေးခြင်း နှင့် Terms of Service သဘောတူခြင်း (ပုံ ၂ အရ)
    try:
        # Terms of Service Dialog ပေါ်လာသည်အထိ စောင့်ဆိုင်းခြင်း
        agree_and_continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'AGREE AND CONTINUE')]"))
        )
        
        # Country Select (Singapore)
        # XPath ကို သုံးထားသည်
        country_select = driver.find_element(By.TAG_NAME, "md-select")
        country_select.click()
        time.sleep(1) 
        
        # Singapore ကို ရွေးရန်
        singapore_option = driver.find_element(By.XPATH, "//md-option[contains(., 'Singapore')]")
        singapore_option.click()
        print("✅ Country ကို Singapore ရွေးချယ်ပြီးပါပြီ။")
        
        # 'I agree' Checkbox ကို နှိပ်ခြင်း
        i_agree_checkbox = driver.find_element(By.XPATH, "//md-checkbox[contains(., 'I agree')]")
        i_agree_checkbox.click()
        print("✅ Terms of Service ကို အမှန်ခြစ် ပြီးပါပြီ။")

        # AGREE AND CONTINUE နှိပ်ခြင်း
        agree_and_continue_button.click()
        print("✅ 'AGREE AND CONTINUE' နှိပ်ပြီး Dashboard သို့ သွားနေပါသည်။")
        
    except Exception as e:
        # ဒီ Dialog မပေါ်လာရင် ဆက်သွားပါ
        print(f"ℹ️ Console Setup Dialog များ ပြီးစီးသွားပါပြီ။")
        pass

def execute_cloud_shell(driver):
    """Cloud Shell ဖွင့်ခြင်း၊ Script Run ခြင်းနှင့် Enter Key များ ပို့လွှတ်ခြင်း။"""
    # စောင့်ဆိုင်းချိန် 90s သို့ တိုးမြှင့်ထားသည်
    wait = WebDriverWait(driver, 90)
    
    # 1. Cloud Shell Button ကို နှိပ်ခြင်း
    print("☁️ Cloud Shell ကို စတင် ဖွင့်နေပါသည်။")
    cloud_shell_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Activate Cloud Shell"]'))
    )
    cloud_shell_button.click()

    # 2. **"CONTINUE"** ခလုတ်ကို စစ်ဆေးပြီး နှိပ်ခြင်း (ပုံ ၃ အရ - Main Page တွင် တိုက်ရိုက် ရှာဖွေ)
    try:
        dialog_wait = WebDriverWait(driver, 45) 
        continue_button = dialog_wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'CONTINUE')]"))
        )
        continue_button.click()
        print("✅ Cloud Shell ၏ 'CONTINUE' ခလုတ်ကို နှိပ်ပြီးပါပြီ။")
    except:
        print("ℹ️ 'CONTINUE' Dialog မတွေ့ရပါ။ ဆက်လက်လုပ်ဆောင်ပါမည်။")
        
    # 3. **"AUTHORIZE"** ခလုတ်ကို စစ်ဆေးပြီး နှိပ်ခြင်း (ပုံ ၄ အရ - Main Page တွင် တိုက်ရိုက် ရှာဖွေ)
    try:
        dialog_wait = WebDriverWait(driver, 45)
        authorize_button = dialog_wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'AUTHORIZE')]"))
        )
        authorize_button.click()
        print("✅ Cloud Shell ၏ 'AUTHORIZE' ခလုတ်ကို နှိပ်ပြီးပါပြီ။")
    except:
        print("ℹ️ 'AUTHORIZE' Dialog မတွေ့ရပါ။ ဆက်လက်လုပ်ဆောင်ပါမည်။")
        pass
        
    # 4. Cloud Shell Terminal ပေါ်လာသည်အထိ စောင့်ဆိုင်းခြင်း
    print("⏳ Terminal ပေါ်လာသည်အထိ စောင့်ဆိုင်းနေပါသည်။...")
    
    # Terminal input field သည် iframe အတွင်း၌ရှိသည်၊ ထို iframe ကို စောင့်ဆိုင်းပြီး switch လုပ်ရန်လိုအပ်သည်
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='Google Cloud Console Terminal']")))

    # 5. Terminal ၏ input field ကို Iframe အတွင်းမှ ရှာဖွေခြင်း
    cloud_shell_input_selector = 'span[role="textbox"][aria-label="Cloud Shell Terminal"]'
    
    cloud_shell_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cloud_shell_input_selector))
    )
    
    # Terminal Ready ဖြစ်ဖို့ သေချာအောင် ခဏစောင့်
    time.sleep(5) 
    
    # 6. Script ကို ရိုက်ထည့်ပြီး Enter နှိပ်ခြင်း
    global CLOUD_SHELL_COMMAND
    print(f"Executing: {CLOUD_SHELL_COMMAND}")
    cloud_shell_input.send_keys(CLOUD_SHELL_COMMAND)
    cloud_shell_input.send_keys(Keys.ENTER)
    
    # 7. Enter Key (၁၀) ကြိမ် ပို့လွှတ်ခြင်း
    global TOTAL_ENTERS
    print(f"Sending {TOTAL_ENTERS} Enter Keys to handle prompts...")
    time.sleep(5) 
    
    for i in range(TOTAL_ENTERS):
        cloud_shell_input.send_keys(Keys.ENTER)
        time.sleep(DELAY_BETWEEN_ENTERS) 
        
    print("✅ Automation လုပ်ငန်းစဉ် ပြီးစီးပါပြီ။")


# ====================================================================
# MAIN EXECUTION
# ====================================================================

if __name__ == "__main__":
    driver = setup_browser()
    try:
        handle_console_setup(driver)
        execute_cloud_shell(driver)
    except Exception as e:
        print(f"❌ အဓိက လုပ်ငန်းစဉ်တွင် အမှားဖြစ်: {e}")
    finally:
        driver.quit()
