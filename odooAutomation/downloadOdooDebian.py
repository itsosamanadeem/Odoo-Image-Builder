from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import os

class DownloadOdooSetup:
    async def downloadOdoo(self, i, time):
        browser = None
        download_dir = f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{i}"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chrome_options.add_argument("--no-sandbox")

        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.get('https://www.odoo.com/page/download')
            download_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@class, 'btn') and contains(@class, 'btn-outline-primary') and contains(@class, 'w-100') and contains(@data-platform-version,'deb_{i}e')]"))
            )
            download_button.click()
            
            key_input = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'form-control') and contains(@class, 'oe_download_code')]"))
            )
            key_input.send_keys('M22042639039621')
            
            confirm_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'oe_download_button')]"))
            )
            confirm_button.click()
            
            WebDriverWait(browser, time).until(
                lambda driver: any([file.endswith(".deb") for file in os.listdir(download_dir)])
            )
            print(f"Downloaded Odoo setup {i}.0 to {download_dir}")

        except Exception as e:
            print(f"An error occurred: {e}")
            for file in os.listdir(download_dir):
                if file.endswith('.crdownload'):
                    await self.retry_download(i, download_dir, time)
        finally:
            print(f"odoo setup {i}.0 downloaded")
            if browser:
                browser.quit()


    async def retry_download(self, i, download_dir, time):
        print(f"Retrying download for version {i}")
        shutil.rmtree(download_dir)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)  
        
        time += 100
        await self.downloadOdoo(i, time)
