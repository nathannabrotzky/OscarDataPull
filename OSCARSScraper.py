###########################################################################################################################################################################################
print("\n\tIMPORTING LIBRARIES\n")
from selenium import webdriver #Imported to create instances of the webdriver class
from selenium.webdriver.chrome.options import Options #Imported to set the browser to headless, incognito, and disable the gpu
from selenium.common.exceptions import NoSuchElementException #Imported to handle exceptions when not able to find elements while gathering data
import pandas as pd #Imported to read and create data sets
from IPython.display import display
import itertools
###########################################################################################################################################################################################

URL = "https://awardsdatabase.oscars.org/"
CHROMEDRIVER = "C:\\Users\\natha\\AppData\\Local\\Programs\\Python\\Python39\\chromedriver.exe"
RECENT_ANNUM = 94

def Set_Chrome_Options(): #This function sets the chrome driver settings
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options
def util_Find_Data(nom): #This function finds data on nominee given the nominee element 'nom'
    data = []
    try:
        data.append(nom.find_element_by_css_selector("div[class=\"awards-result-nominationstatement\"").text)
    except NoSuchElementException:
        data.append("")
    try:
        films = []
        [films.append(x.text.replace(";","")) for x in nom.find_elements_by_css_selector("div[class=\"awards-result-film-title\"")]
        data.append(", ".join(films))
    except NoSuchElementException:
        data.append("")
    try:
        characters = []
        [characters.append(x.text.replace("{","").replace("}","").replace("\"","").replace(";","")) for x in nom.find_elements_by_css_selector("div[class=\"awards-result-character-name\"")]
        data.append(", ".join(characters))
    except NoSuchElementException:
        data.append("")
    try:
        nom.find_element_by_css_selector("span[title=\"Winner\"]")
        data.append(True)
    except NoSuchElementException:
        data.append(False)
    try:
        data.append(nom.find_element_by_css_selector("div[class=\"awards-result-placement\"").text)
    except NoSuchElementException:
        data.append("")
    try:
        data.append(nom.find_element_by_css_selector("div[class=\"awards-result-songtitle\"").text)
    except NoSuchElementException:
        data.append("")
    try:
        data.append(nom.find_element_by_css_selector("div[class=\"awards-result-publicnote\"").text)
    except NoSuchElementException:
        data.append("")
    return data

return_data = []
with webdriver.Chrome(executable_path = CHROMEDRIVER, options=Set_Chrome_Options()) as driver: #using with so that the driver always closes regardless of errors
    driver.get(URL)
    driver.find_element_by_css_selector("button[title=\"--Select--\"]").click()
    driver.find_element_by_css_selector("a[href=\"javascript:void(0);\"]").click()
    driver.find_element_by_id("btnbasicsearch").click()
    start = -1
    end = 10
    while start <= RECENT_ANNUM: #included this loop so that the driver could refresh, since the web page would time-out
        year_groups = enumerate(driver.find_elements_by_css_selector("div[class=\"awards-result-chron result-group group-awardcategory-chron\"]"))
        for count, group in year_groups: #loops through each year
            if count > start:
                year_title = group.find_element_by_css_selector("div[class=\"result-group-title\"]").text
                year = year_title[:4]
                annum = year_title[year_title.find("(") + 1: -3]
                for entry in group.find_elements_by_css_selector("div[class=\"result-subgroup subgroup-awardcategory-chron\"]"): #loops through each award
                    award = entry.find_element_by_css_selector("div[class=\"result-subgroup-title\"]").text
                    return_val = [year,annum,award]
                    #the following list comprhensions loops through the data on each nominee
                    [return_data.append(return_val + util_Find_Data(x)) for x in entry.find_elements_by_css_selector("div[class=\"result-details awards-result-actingorsimilar\"]")]
                    [return_data.append(return_val + util_Find_Data(x)) for x in entry.find_elements_by_css_selector("div[class=\"result-details awards-result-other\"]")]
                    [return_data.append(return_val + util_Find_Data(x)) for x in entry.find_elements_by_css_selector("div[class=\"result-details awards-result-song\"]")]
                print(f"\tCompleted Annum {annum}.")
                if count >= end:
                    break
            else:
                pass
        start = end
        end += 10
        print("\n\tRefreshing Driver.\n")
        driver.refresh()
#Sorts data, removes duplicates, formats it into a Data Frame, and exports it to csv
return_data.sort()
return_data = pd.DataFrame(data=list(return_data for return_data,_ in itertools.groupby(return_data)),columns=["Year","Annum","Award","Nomination","Film","Character","Win","Placement","Song","Note"])
return_data.to_csv("C:\\Users\\natha\\Desktop\\YouTube Content\\Data\\Oscars\\Award_Data.csv",index=False)


'''
'''