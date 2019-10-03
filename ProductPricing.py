import time
from datetime import datetime
import MySQLdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
'''driver setup'''
driver = webdriver.Chrome(executable_path= r"E:\Wellmonk\chromedriver.exe")
driver.maximize_window()
driver.get("https://www.flipkart.com/grocery-supermart-store?marketplace=GROCERY")
assert "Flipkart" in driver.title #title name
driver.implicitly_wait(5)
searchBar = driver.find_element_by_name("q")
searchBar.clear()
searchBar.send_keys('Cashews')
searchBar.send_keys(Keys.RETURN)
time.sleep(10)

product_item_names = []
titles = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='container']/div/div[3]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div")))
for title in titles:
    product_item_names.append(title.text)
try:
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    titles = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='productDescriptionAndPrice']//h4/a")))
    for title in titles:
        product_item_names.append(title.text)

except:
    pass
    # print(product_item_names)

'''connet to database '''
db = MySQLdb.connect(host = "localhost", user = "root",password = "password",database = "MySQL")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
# print ("Database version : %s " % data)
current_time = datetime.now()
value = product_item_names[0].split('\n')
replace_list = []
for item in value:
    x = item.replace('₹', '') #remove the ₹ symbol
    replace_list.append(x)
print(replace_list)
pname = replace_list[0]
pprice = replace_list[1]
pweight = replace_list[4]
print({'product_name':pname, 'product_price':pprice, 'product_weight': pweight, 'product_addedDate':current_time})
query = "INSERT INTO wellmonk.product_pricings(product_name,product_weight,product_price,product_addedDate) \
        VALUES ('%s', '%s', '%s','%s')" %(pname, pweight, pprice,current_time) #Insert into data
cursor.execute(query)
db.commit()
cursor.close()
db.close()