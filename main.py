from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional
import zipfile

def checker(email: str, proxy: str) -> Optional[bool]:

    host_port, credentials = proxy_string.split('@', 1)
    host, port = host_port.split(':', 1)
    username, password = credentials.split(':', 1)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % ((host, port, username, password))



    try:
        chrome_options = webdriver.ChromeOptions()

        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        chrome_options.add_extension(pluginfile)

        service = Service('....') #path to chrome_driver.exe
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://accounts.firefox.com')

        element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.NAME, 'email')))

        email_input = driver.find_element(By.NAME, 'email')
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 120).until(
            lambda driver: 'signin?' in driver.execute_script("return window.location.href;") or 
                        'signup?' in driver.execute_script("return window.location.href;")
        )
        current_url=driver.execute_script("return window.location.href;")

        driver.quit()

        if 'signin' in current_url:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


print(checker('...', '...')) #email, proxy - host:port@login:password