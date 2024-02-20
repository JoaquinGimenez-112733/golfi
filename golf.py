from lxml import html
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


url = "https://www.golfpass.com/travel-advisor/course-directory/1-world/"


country_dic = {}
url_arr = []
country_arr = []

# Configurar Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Para que no se abra una ventana del navegador
chrome_options.add_argument('log-level=3')
service = Service(ChromeDriverManager().install())

# Hacer la solicitud con Selenium
driver = webdriver.Chrome(service=service, options=chrome_options)

# world section
driver.get(url)

section = driver.find_elements(By.CLASS_NAME, 'LocationTagPage-sublocationsUnrolled')

country_title = section[0].find_elements(By.CLASS_NAME, 'LocationTagPromo-title')

for country in country_title:
    country_arr.append(country.find_element(By.TAG_NAME, 'a').text)
    url_arr.append(country.find_element(By.TAG_NAME, 'a').get_attribute("href"))

country_dic["Country"] = country_arr
country_dic["Url"] = url_arr


# country section
log_dic = {}
locations_dic = {}
message = []
country_c = []
url_sublocations = []
url_titles_sub = []
content_urls = []
location_names = []

for url_c in url_arr:
    
        driver.get(url_c)        
        html_content = driver.page_source
        tree = html.fromstring(html_content)    
        
        if "By Location" in html_content:
            sublocations = driver.find_element(By.CLASS_NAME, 'LocationTagPage-sublocations-content')        
            titles_sublocations = sublocations.find_elements(By.CLASS_NAME, 'LocationTagPromo-title')

            for tt in titles_sublocations:
                url_titles_sub.append(html.fromstring(tt.get_attribute("outerHTML")).xpath('//a')[0].get('href'))
            
                    
            for titles_s in url_titles_sub:
                
                    driver.get(titles_s)
                    
                    html_content = driver.page_source
                    tree = html.fromstring(html_content)
                    
                    if "By Location" in html_content:
                        sublocations = driver.find_element(By.CLASS_NAME, 'LocationTagPage-sublocations-content')
                        titles_sublocations = sublocations.find_elements(By.CLASS_NAME, 'LocationTagPromo-title')
                        
                        for t in titles_sublocations:
                            url_sublocations.append(html.fromstring(t.get_attribute("outerHTML")).xpath('//a')[0].get("href"))
                        
                        

                        for titles_sub in url_sublocations:
                            
                                driver.get(titles_sub)
                                
                                try:
                                    content = driver.find_element(By.CLASS_NAME, 'LocationTagPage-courses-content')
                                    titles_content = content.find_elements(By.CLASS_NAME,'StandardCoursePromo-title')
                                    for cont in titles_content:
                                        content_urls.append(cont.find_element(By.TAG_NAME,'a').get_attribute("href"))
                                        location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                                        locations_dic["location_name"] = location_names
                                        locations_dic["url"] = content_urls                            
                                        df = pd.DataFrame(locations_dic)
                                        df.to_csv("locations.csv", index=False)
                                except:
                                    content_urls.append("No tiene course")
                                    location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                                    locations_dic["location_name"] = location_names
                                    locations_dic["url"] = content_urls                            
                                    df = pd.DataFrame(locations_dic)
                                    df.to_csv("locations.csv", index=False)
                    else:
                        try:
                            content = driver.find_element(By.CLASS_NAME, 'LocationTagPage-courses-content')
                            titles_content = content.find_elements(By.CLASS_NAME,'StandardCoursePromo-title')
                            for cont in titles_content:
                                content_urls.append(cont.find_element(By.TAG_NAME,'a').get_attribute("href"))
                                location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                                locations_dic["location_name"] = location_names
                                locations_dic["url"] = content_urls                            
                                df = pd.DataFrame(locations_dic)
                                df.to_csv("locations.csv", index=False)
                        except:
                            content_urls.append("No tiene course")
                            location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                            locations_dic["location_name"] = location_names
                            locations_dic["url"] = content_urls                            
                            df = pd.DataFrame(locations_dic)
                            df.to_csv("locations.csv", index=False)

        else:
                try:
                    content = driver.find_element(By.CLASS_NAME, 'LocationTagPage-courses-content')
                    titles_content = content.find_elements(By.CLASS_NAME,'StandardCoursePromo-title')
                    for cont in titles_content:
                        content_urls.append(cont.find_element(By.TAG_NAME,'a').get_attribute("href"))
                        location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                        locations_dic["location_name"] = location_names
                        locations_dic["url"] = content_urls                            
                        df = pd.DataFrame(locations_dic)
                        df.to_csv("locations.csv", index=False)
                except:
                    content_urls.append("No tiene course")
                    location_names.append(driver.find_elements(By.TAG_NAME, 'h1')[0].text)
                    locations_dic["location_name"] = location_names
                    locations_dic["url"] = content_urls                            
                    df = pd.DataFrame(locations_dic)
                    df.to_csv("locations.csv", index=False)


locations_dic["location_name"] = location_names
locations_dic["url"] = content_urls
df = pd.DataFrame(locations_dic)
df.to_csv("locations.csv", index=False)
