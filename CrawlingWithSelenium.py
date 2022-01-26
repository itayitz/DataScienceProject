import time
from selenium import webdriver
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def main():
    flag = True
    service =Service(executable_path="C:\\Users\\itayi\\Desktop\\chromedriver.exe")
    service.start()
    driver=webdriver.Remote(service.service_url)
    page = 1
    driver.get("https://www.yad2.co.il/realestate/forsale?topArea=41&area=21&city=0070&page={}".format(page))
    driver.maximize_window()
    time.sleep(25)
    print("start Crawling")
    print("Page: ")
    print(page)


    topCategories = ["חדרים", "קומה", 'מ"ר']
    mainBoxCategories= ['מיזוג', 'סורגים','מעלית','מטבח כשר','דוד שמש','גישה לנכים','ממ"ד','משופצת','מחסן','מזגן תדירן','ריהוט','גמיש','נכס בבלעדיות']
    topMainBoxCategories = ['חניות', 'מרפסות', 'קומות בבנין', 'מצב הנכס']

    while (page<54):

        try:
            feetItemTable = driver.find_elements(By.CLASS_NAME, "feeditem")
        except:
            try:
                feetItemTable = driver.find_elements(By.CLASS_NAME, "feeditem.table")
            except Exception as e:
                print(e, "\nwhile(True):")
                continue
        try:
            for feedItem in feetItemTable:

                DataSet = {"מטבח כשר": None, "משופצת": None, 'ממ"ד': None, "מזגן תדיראן": None,
                     "ריהוט": None,
                     "גישה לנכים": None, "מיזוג": None, "מעלית": None, "מחסן": None, "סורגים": None, 'חניות': None,
                     'מרפסות': None, 'קומות בבנין': None, 'מצב הנכס': None, "סוג נכס": None, "עיר": None, "שכונה": None}
                time.sleep(1)
                try:
                    feedItem.click()
                except Exception as e:
                    print(e)
                    try:
                        feedItem.click()
                    except:
                        print(e)
                        continue
                try:
                    time.sleep(1)
                    missingValue = feedItem.find_elements(By.CLASS_NAME, "info_feature.delete")
                    time.sleep(1)
                except:
                    pass

                try:
                    temp1 = []
                    for value in missingValue:
                        if str(value.text) in mainBoxCategories:
                            DataSet[str(value.text)] = 0
                            temp1.append(value.text)

                    infoFeature = feedItem.find_elements(By.CLASS_NAME, "info_feature")
                    time.sleep(1)

                    for info in infoFeature:
                        if str(info.text) in mainBoxCategories and DataSet.get(str(info.text)) != 0 and str(info.text) not in temp1:
                            DataSet[str(info.text)] = 1
                except:
                    pass

                try:
                    feedItem.find_elements(By.CLASS_NAME, "y2i_exclusive")
                    time.sleep(1)
                    DataSet["תיווך"] = 1
                except:
                    DataSet["תיווך"] = 0
                    pass

                try:
                    infoItems = feedItem.find_elements(By.CLASS_NAME, "info_item")

                    for info in infoItems:
                        string = str(info.text).split("\n")
                        if string[0] in topMainBoxCategories:
                            DataSet[string[0]] = string[1]
                except:
                    pass

                time.sleep(1)

                try:
                    subtitle = feedItem.find_element(By.CLASS_NAME, "subtitle")
                    string_subtitle = str(subtitle.text)
                    string_subtitle = string_subtitle.split(",")
                    DataSet["סוג נכס"] = string_subtitle[0]
                    DataSet["שכונה"] = string_subtitle[1:-1]
                    DataSet["עיר"] = string_subtitle[-1]

                except:
                    pass

                try:
                    time.sleep(1)
                    y = feedItem.find_elements(By.CLASS_NAME, "data")
                    time.sleep(1)

                    for g in y:
                        g = str(g.text)
                        g = g.split("\n")
                        if g[1] in topCategories:
                            DataSet[g[1]] = g[0]
                except:
                    pass

                time.sleep(1)
                try:
                    y = feedItem.find_element(By.CLASS_NAME, "price")
                    DataSet["מחיר"] = str(y.text)
                except:
                    DataSet["מחיר"] = None

                time.sleep(1)

                l = ['מטבח כשר', 'משופצת', 'ממ"ד', 'מזגן תדיראן', 'ריהוט', 'גישה לנכים', 'מיזוג',
                     'מעלית', 'מחסן', 'סורגים', 'חניות', 'מרפסות', 'קומות בבנין', 'מצב הנכס', 'סוג נכס', 'עיר', 'שכונה',
                     'תיווך', 'חדרים', 'קומה', 'מ"ר', 'מחיר']
                O = []


                for i in l:
                    if i not in DataSet.keys():
                        O.append(i)

                if len(O) > 0:
                    print("Missing categories: ", O)
                    for i in O:
                        DataSet[i] = None

                if flag:
                    with open('DataSetAshdod.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(DataSet.keys())

                    flag = False

                with open('DataSetAshdod.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(DataSet.values())

        except Exception as e:
            print("Erorr in -> for")
            print(e)


        page += 1
        print("page: {}".format(page))
        time.sleep(30)
        driver.get("https://www.yad2.co.il/realestate/forsale?topArea=41&area=21&city=0070&page={}".format(page))
        time.sleep(30)

    driver.close()


if __name__ == "__main__":
    main()
