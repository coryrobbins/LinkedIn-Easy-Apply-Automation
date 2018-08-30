import time
import traceback
import JobData
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import ReportingModule as Report
import datetime as dt
'''
Reference: https://stackoverflow.com/questions/37088589/selenium-wont-open-a-new-url-in-a-new-tab-python-chrome
https://stackoverflow.com/questions/28431765/open-web-in-new-tab-selenium-python
https://stackoverflow.com/questions/39281806/python-opening-multiple-tabs-using-selenium
'''
calijobslink = "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&keywords=Software%20Developer&location=95112%20San%20Jose%2C%20CA&locationId=POSTAL.us.95112"#Action link for sanjose alerts
usualjobslink = "https://www.linkedin.com/jobs"
username = "" # your email here
password = "" # your password here
jobTitle = "Software Engineer -senior -Senior" # your desired job title
jobLocation = "Austin, Texas" # your desired job location
resumeLocation = "" # your resume location on local machine

currentPageJobsList = []
allEasyApplyJobsList = []
failedEasyApplyJobsList = []
appliedEasyApplyJobsList = []


def click(driver, x, y):
    el = driver.find_elements_by_xpath("//button[contains(string(), 'Lucky')]")[0]
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(el, x, y)
    action.click()
    action.perform()
    # win32api.SetCursorPos((x,y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def init_driver():
    #driver = webdriver.Chrome(executable_path = "./chromedriver.exe")
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef


def login(driver, username, password):
    driver.get("https://www.linkedin.com/")
    try:
        user_field = driver.find_element_by_class_name("login-email")
        pw_field = driver.find_element_by_class_name("login-password")
        login_button = driver.find_element_by_id("login-submit")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef


def searchJobs(driver):
    driver.get(usualjobslink)
    time.sleep(5)

    jobDescField = driver.find_element_by_css_selector("[id^=jobs-search-box-keyword-id-ember]")
    print('jobDescField id', jobDescField.get_attribute("id"))
    locField = driver.find_element_by_css_selector("[id^=jobs-search-box-location-id-ember]")
    print('locField id', locField.get_attribute("id"))
    search_button = driver.find_element_by_class_name("jobs-search-box__submit-button")
    jobDescField.send_keys(jobTitle)
    time.sleep(1)
    locField.send_keys(jobLocation)
    time.sleep(1)
    search_button.click()
    time.sleep(2)   

    while True:
        scheight = .1
        while scheight < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
            scheight += .01
        alljobsonpage = driver.find_elements_by_class_name("card-list__item")
        for i in alljobsonpage:

            try:
                # Easy apply button
                i.find_element_by_class_name("job-card-search__easy-apply")
                job = convertJobElement(driver, i)
                currentPageJobsList.append(job)
                allEasyApplyJobsList.append(job)
            except:
                traceback.print_exc()
                print("Not Easy Apply")
            print("____________________________")
        loopThroughJobs(driver,currentPageJobsList)
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            print("Next Button")
            
            nextButton = driver.find_element_by_class_name('next')
            nextButton.click()
            del currentPageJobsList[:]
        except:
            break
        
    print("____________________________")


def loopThroughJobs(driver,jobsList):
    #applyToJob(driver,jobsList[0])
    for i in jobsList:
        print('applying: ', i)
        #time.sleep(30)
        if(applyToJob(driver,i)):
            continue
    allwindows = driver.window_handles
    if(len(allwindows) == 2):
        driver.switch_to_window(allwindows[1])
        driver.close()
        driver.switch_to_window(allwindows[0])

def applyToJob(driver,job):
    
    window_before = driver.window_handles[0]
    if job:
        execScript = "window.open('"+job.link+"', 'CurrJob');"
    else:
        return False
    driver.execute_script(execScript)
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    time.sleep(3)
    # Dont Change This setting
    scheight = 4
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += 4

    driver.execute_script("window.scrollTo(0, 0);")

    # Unlock this section for applying jobs
    try:
        div = driver.find_element_by_class_name("jobs-details-top-card__actions")
        applyButton = div.find_element_by_class_name("jobs-s-apply__button")
        applyButton.click()
        print("clicked on easyapply")
        time.sleep(5)
    except:
        print("Found None")

    try:
        upload_element = driver.find_elements_by_css_selector('input[type="file"]')
        upload_element.sendKeys(resumeLocation)

        # ember709-phone-number-question
        # for all input type=radio, click first child

        # upload_button = driver.find_element_by_xpath("//button[contains(.,'Upload resume')]")
        # print(upload_button)
        # upload_button.click()
        #driver.find_element_by_css_selector('input[type="file"]').clear()
        #driver.find_element_by_css_selector('input[type="file"]').send_keys(resumeLocation)
        # click(driver, 610,505)
        # time.sleep(1)
        # keyboard.write("resume.pdf")
        # time.sleep(1)
        # keyboard.press_and_release('Enter')
        # time.sleep(3)
        # click(driver, 410,440)
        # time.sleep(1)
        # keyboard.write("(757)439-0083")
        # time.sleep(3)
        submitButton = driver.find_element_by_class_name('jobs-apply-form__submit-button')
        submitButton.click()
        time.sleep(1)
        appliedEasyApplyJobsList.append(job)
        time.sleep(3)
        return True
        
    except:
        traceback.print_exc()
        failedEasyApplyJobsList.append(job)
        allwindows = driver.window_handles
        if(len(allwindows) == 3):
            currWindow  = allwindows[2]
            driver.switch_to_window(currWindow)
            driver.close()
            driver.switch_to_window(window_after)
            
        return False

    # driver.close()
    return False
    

def convertJobElement(driver, i):
    curr = None
    base_url = driver.current_url
    try:
        html = i.get_attribute("innerHTML")
        job_div = i.find_element_by_css_selector('[data-control-name="A_jobssearch_job_result_click"]')
        job_id = job_div.get_attribute('data-job-id')
        print('job_id', job_id)
        link = '{}&currentJobId={}'.format(base_url, job_id)
        print('link', link)
        #title = soup.find("h3", {"class" : "job-card__title"}).getText().strip()
        title = ""
		#print("Job Title:" + title)
        #company = soup.find("h4", {"class" : "job-card__company-name"}).getText().strip()
        company = ""
        #print("Company:" + company)
        # link = i.find_element_by_class_name("job-card-search__link-wrapper").get_attribute('href')
        # link = soup.find("a", {"class" : "job-card-search__link-wrapper"})['href']
        #print("Link:" + link)
        city = ""
        #city = soup.find("h5", {"class" : "job-card__location"}).getText().strip().replace("Job Location","")
        #print("City:" + city.strip())
        curr = JobData.JobData(title,company,link,city.strip(),html)
        print(curr)
    except:
        traceback.print_exc()
        print("Howdy !!! Unable to convert JobElement")

    return curr


def sendReportToEmail():
    try:
        appliedjobs = "\n".join(str(i) for i in appliedEasyApplyJobsList)
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Applied Jobs',appliedjobs)
        failedjobs = "\n".join(str(i) for i in failedEasyApplyJobsList)
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Need your attention to complete applications',failedjobs)
    except:
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Warning Email',"Failed to Generate Report")

def writeToFile(filename,data,filemode):
    f= open(filename,filemode)
    f.write(data)
    f.close()  

def saveReportAsCSV():
    appliedjobs = "\n".join(str(i) for i in appliedEasyApplyJobsList)
    failedjobs = "\n".join(str(i) for i in failedEasyApplyJobsList)
    filename = dt.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    f1 = '{0}-{1}.{2}'.format('applied',filename,'csv')
    f2 = '{0}-{1}.{2}'.format('failed',filename,'csv')
    writeToFile(f1,appliedjobs,"w+")
    writeToFile(f2,failedjobs,"w+")


def main():
    driver = init_driver()
    time.sleep(3)
    print ("Logging into Linkedin account ...")
    login(driver, username, password)
    time.sleep(1)
    searchJobs(driver)
    sendReportToEmail()
    saveReportAsCSV()


if __name__ == "__main__":
    main()
