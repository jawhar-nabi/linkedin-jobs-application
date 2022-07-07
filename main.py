from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def execute(page):
	global successfulApps
	global parcoured
	global errorFound 
	global doNotApplyList 

	driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&f_TPR=r86400&geoId=91000000&keywords=angular&location=France&sortBy=DD&start="+str(page))

	WebDriverWait(driver,7).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".jobs-search-results__list.list-style-none")))

	html_list = driver.find_elements_by_css_selector(".jobs-search-results__list-item.occludable-update.p0.relative.ember-view")

	print("STARTED")
	html_list = driver.find_elements_by_css_selector(".jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
	while(len(html_list)==7):
		html_list = driver.find_elements_by_css_selector(".jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
    		
	for item in html_list:
		if(html_list.index(item)>5):
			driver.execute_script("arguments[0].scrollIntoView();", item )
		parcoured += 1
		errorFound = False
		print("processing...")
		time.sleep(0.5)
		WebDriverWait(driver,7).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".disabled.ember-view.job-card-container__link.job-card-list__title")))
		time.sleep(2.5)
		print(len(html_list))

		try:
			inside_element = item.find_element(By.CSS_SELECTOR,".disabled.ember-view.job-card-container__link.job-card-list__title")
		except Exception as e:
			print(e)
			time.sleep(2)
			inside_element = item.find_element(By.CSS_SELECTOR,".disabled.ember-view.job-card-container__link.job-card-list__title")
		print(inside_element.get_attribute("innerHTML"))
		if(any(n in inside_element.get_attribute("innerHTML") for n in doNotApplyList)):
			print("skipping because title is in blacklist")
			continue
		
		try:
			inside_element.click()
		except Exception as e:
			closeBtn = driver.find_element(By.CSS_SELECTOR,".artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
			closeBtn.click()
			item.find_element(By.CSS_SELECTOR,".disabled.ember-view.job-card-container__link.job-card-list__title").click()


		time.sleep(2)
		try:
			driver.find_element(By.CSS_SELECTOR,".jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view").click()
			time.sleep(0.5)
		except Exception as e:
			print("skipping because already applied or can't apply")
			continue
		print("job popup opened...")

		while(driver.find_element(By.CSS_SELECTOR,".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")):
			try:
				driver.find_element(By.CSS_SELECTOR,".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view").click()
			except Exception:
				break
			time.sleep(0.5)
			try:
				driver.find_element(By.CSS_SELECTOR,".fb-form-element__error-text.t-12:not(.visually-hidden)")
				errorFound = True
			except Exception as e:
				errorFound = False
			if(errorFound):
				print("error is found, gonna close the popup now !")
				closeBtn = driver.find_element(By.CSS_SELECTOR,".artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
				closeBtn.click()
				time.sleep(0.5)
				discardBtn = driver.find_element(By.CSS_SELECTOR,".artdeco-modal__confirm-dialog-btn.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view")
				discardBtn.click()
			time.sleep(2)

			try:
				# WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH,"//*[contains(text(),'Your application was sent')]"   )))
				popupHeader = driver.find_element(By.ID,"post-apply-modal")
				print("Application sent successfully, closing the popup now!")
				
				#if popup is open, close it
				closeBtn = driver.find_element(By.CSS_SELECTOR,".artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
				closeBtn.click()
				successfulApps += 1
				break

			except Exception as e:
				pass

			time.sleep(0.5)
			print("successful applications till now: ",successfulApps)



	print("parcoured : ",parcoured)
	print("successful : ",successfulApps)


def login(driver):
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "global-nav")))
	except Exception as e:
		driver.get("http://www.linkedin.com")
		WebDriverWait(driver,7).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#session_key")))
		assert "ou" in driver.title
		elem = driver.find_element(By.ID, "session_key")
		elem.send_keys("yourEmail@gmain.com")
		elem2 = driver.find_element(By.ID, "session_password")
		elem2.send_keys("your_password")
		driver.find_element(By.CSS_SELECTOR,'button.sign-in-form__submit-button').click()
		WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "global-nav")))
		print("successful login")


successfulApps = 72
parcoured = 0
page = 175
errorFound = False
doNotApplyList = ["Technical","technical","Test","test","QA","Testeur","testeur","Alternance","alternance","Senior","SENIOR","senior" "C#","php","Net","net","NET","PHP","symfony","laravel","J2EE","JEE","scala","ruby","RUBY","Ruby","j2ee","android","ionic","mobile"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-notifications")
#get session from local chrome
chrome_options.add_argument("user-data-dir=C:/Users/USER/AppData/Local/Google/Chrome/User Data/") 

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options,executable_path="D:/Downloads/chromedriver.exe")
#login(driver)
time.sleep(2)
driver.maximize_window();
print(successfulApps)
while(successfulApps < 100):
	execute(page)
	page += 25

