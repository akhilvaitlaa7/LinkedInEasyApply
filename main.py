from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re




class EasyApply:
    
    def __init__(self,data):
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        
    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        
        login_email = self.driver.find_element_by_name("session_key")
        login_email.clear()
        login_email.send_keys(self.email)
        
        login_password = self.driver.find_element_by_name("session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        
        login_password.send_keys(Keys.RETURN)
        
    def job_search(self):
        jobs_link = self.driver.find_element_by_link_text("Jobs")
        jobs_link.click()
        time.sleep(3)
        search_keyword = self.driver.find_element_by_xpath("//input[starts-with(@id,'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        time.sleep(2)
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id,'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(2)
        search_location.send_keys(Keys.RETURN)
        
    def job_search_filter(self):
        all_filters_button = self.driver.find_element_by_class_name("search-reusables__filter-binary-toggle")
        all_filters_button.click()
        
    def find_offers(self):
        total_results = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal.jobs-search-results-list__text")
        total_results_int = int(total_results.text.split(" ",1)[0].replace(",",""))
        print(total_results_int)
     
        time.sleep(2)
        #results of first page
        current_page = self.driver.current_url
        results = self.driver.find_elements_by_class_name("ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")
        
        for result in results:
            self.driver.implicitly_wait(10)
            ActionChains(self.driver).move_to_element(result).click(result).perform()
            # hover = ActionChains(self.driver).move_to_element(result)
            # hover.perform()
            titles = result.find_elements_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")
            for title in titles:
                self.submit_application(title)
                
        # if there are more than one page, find all pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)
            
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            print(last_page)
            total_jobs = int(last_page.split('start=',1)[1])
            print(total_jobs)
            #iterate through all pages and apply
            for page_number in range(25,total_jobs+25,25):
                print("In for loop")
                self.driver.get(current_page+"&start="+str(page_number))
                print("ok")
                time.sleep(2)
                results_ext = self.driver.find_elements_by_class_name("ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")
                for result_ext in results_ext:
                    # self.driver.implicitly_wait(10)
                    # ActionChains(self.driver).move_to_element(result_ext).click(result_ext).perform()
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")
                    for title_ext in titles_ext:
                        self.submit_application(title_ext)
        else:
            self.close_session()
               
            
    def submit_application(self,job_ad):
        print("You are applying to position:",job_ad.text)
        job_ad.click()
        #job_ad.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # try to click easy apply or skip if already applied
        try:
            in_apply = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            in_apply.click()
            #in_apply.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print("Already applied to this position")
            return
        
        time.sleep(1)
        #try if next step is available
        try:
            print("1st step")
            next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
            next.click()
            time.sleep(2)
        except NoSuchElementException:
            pass
        
        try:
            print("2st step")
            choose_resume = self.driver.find_element_by_xpath("//button[@aria-label='Choose Resume']")
            choose_resume.send_keys(Keys.RETURN)
            time.sleep(1)
            next_next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
            next_next.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            pass
        
        try:
            print("3st step")
            next_next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
            next_next.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            pass
        
        try:
            print("4st step")
            review = self.driver.find_element_by_xpath("//button[@aria-label='Review your application']")
            review.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            pass
        
        try:
            print("5st step")
            print("trying submit")
            submit = self.driver.find_element_by_xpath("//button[@aria-label='Submit application']")
            submit.send_keys(Keys.RETURN)
            time.sleep(2)
            print("Application submission done")
            close_confirm = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss']")
            close_confirm.send_keys(Keys.RETURN)
        #if submit is not available, discard the application
        except NoSuchElementException:
            print("6st step")
            print("Not a direct application")
            self.close_application() 
        
    def submit_application1(self, job_ad):
        print("You are applying to position:", job_ad.text)
        job_ad.click()
        time.sleep(2)

        try:
            in_apply = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            in_apply.click()
        except NoSuchElementException:
            print("Already applied to this position")
            return

        time.sleep(1)

        try:
            other_element = self.driver.find_element_by_xpath("//div[@class='ph5']")
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='ph5']")))

            next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
            next.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            try:
                choose_resume = self.driver.find_element_by_xpath("//button[@aria-label='Choose Resume']")
                choose_resume.send_keys(Keys.RETURN)
                time.sleep(1)
                next_next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
                next_next.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                try:
                    next_next = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
                    next_next.send_keys(Keys.RETURN)
                    time.sleep(1)
                except NoSuchElementException:
                    try:
                        review = self.driver.find_element_by_xpath("//button[@aria-label='Review your application']")
                        review.send_keys(Keys.RETURN)
                        time.sleep(1)
                    except NoSuchElementException:
                        try:
                            print("trying submit")
                            submit = self.driver.find_element_by_xpath("//button[@aria-label='Submit application']")
                            submit.send_keys(Keys.RETURN)
                            time.sleep(2)
                            print("Application submission done")
                            close_confirm = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss']")
                            close_confirm.send_keys(Keys.RETURN)
                        except NoSuchElementException:
                            print("Not a direct application")
                            self.close_application()
                            
            
    def close_application(self):
        try:
            discard = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss']")
            discard.send_keys(Keys.RETURN)
            time.sleep(1)
            discard_confirm = self.driver.find_element_by_xpath("//button[@data-control-name='discard_application_confirm_btn']")
            discard_confirm.send_keys(Keys.RETURN)                     
        except NoSuchElementException:
            pass
        time.sleep(1) 
        

    def close_session(self):
        print("end of session")
        self.driver.close()        
        
        
    def apply(self):
        # self.driver.maximize_window()
        self.login()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.job_search_filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()
                   
        
        
if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)
        
    bot = EasyApply(data)
    bot.apply()