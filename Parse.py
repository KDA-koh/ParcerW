import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

cities = ['city']
names = ['name']
emails = ['email']
jobs = ['job']
d = {}


def name_swap(name1, name2):
    name1Idx = names.index(name1)
    name2Idx = names.index(name2)
    names[name1Idx], names[name2Idx] = name2, name1


# для работника в центре
def central(el):
    for i in el:
        value = i.text.split('\n')
        cities.append('')
        names.append(value[0])
        jobs.append(value[1])
        emails.append(value[3])


def parse(url):
    # настройки селениума
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    elems = driver.find_elements(By.XPATH, '// *[contains(@style, "line-height")]')
    el = driver.find_elements(By.XPATH, '//*[@id="rec339883716"]/div[2]/div/div[2]/div/div')
    central(el)
    # парсинг
    for i in elems:
        value = i.text
        lineHeight = int(i.get_attribute("style").split(" ")[1][:2])

        if lineHeight == 56 and value != '':
            cities.append(value)

        if lineHeight == 29 and value != '':
            if value == "Оксана Маклакова":
                names.insert(2, value)
            else:
                names.append(value)

        if lineHeight == 28 and value != '':
            jobsAndEmails = value.split('\n')
            jobs.append(jobsAndEmails[0])
            emails.append(jobsAndEmails[1].strip())

    names.append('')
    name_swap('Эллина Юсупова', 'Татьяна Плотникова')
    name_swap('Екатерина Шайтанова', 'Зоя Кузнецова')
    name_swap('Карина Миллер', '')

    # добавление в csv
    with open("parse1.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(zip(cities, names, jobs, emails))
    print(list(map(len, [cities, names, jobs, emails])))
    names.sort()

    # добавление кол-ва фамилий сотрудников начинаются на каждую из букв русского алфавита
    df_0 = pd.read_csv("parse1.csv", usecols=['name'], encoding='cp1251')
    govno = pd.read_csv("parse1.csv", encoding='cp1251')
    df = df_0.fillna(' ')
    new = df["name"].str.split(" ", n=1, expand=True)
    dp = pd.DataFrame()
    letterCount = []
    letter = []

    letters = [lname[0] for lname in set(new[1].values) if len(lname) > 0]
    # df["Last Name"] = new[1]
    # df.drop(columns=["name"], inplace=True)
    for lname in letters:
        if lname in d:
            d[lname] = d[lname] + 1
        else:
            d[lname] = 1
    for key in list(d.keys()):
        letterCount.append(d[key])
        letter.append(key)
    dp["Letters"] = letter
    dp["LettersCount"] = letterCount
    govno = pd.concat([govno, dp], axis=1)
    govno.to_csv("parse1.csv", encoding='cp1251')


def main():
    parse("https://mediakit.iportal.ru/our-team")


if __name__ == "__main__":
    main()
