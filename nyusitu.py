import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import configparser

import os
import errno
config_ini = configparser.ConfigParser()
config_ini_path = 'config.ini'


def check_initfile_exist():
    # 指定したiniファイルが存在しない場合、エラー発生
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(
            errno.ENOENT), config_ini_path)


def kenkatsukun_check(nyushitsu, url, email, password):
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element_by_id('i0116').send_keys(email)
    driver.find_element_by_id('idSIButton9').click()
    time.sleep(1.0)

    driver.find_element_by_id('i0118').send_keys(password)
    driver.find_element_by_id('idSIButton9').click()
    time.sleep(1.0)

    driver.find_element_by_id('idBtn_Back').click()
    time.sleep(1.0)

    ans = []
    for q_num in nyushitsu:
        yes_or_no = read_nyushitsu.get(q_num)
        if yes_or_no == 'はい':
            ans.append('1')
        else:
            ans.append('2')
    if not len(ans)==6:
        raise Exception("回答の数が合ってません")

    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div['+ans[0]+']/div/label/input').click()
    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div['+ans[1]+']/div/label/input').click()
    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/div['+ans[2]+']/div/label/input').click()
    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/div['+ans[3]+']/div/label/input').click()
    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/div['+ans[4]+']/div/label/input').click()
    driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/div/div['+ans[5]+']/div/label/input').click()
    button_elements = driver.find_elements_by_class_name('button-content')
    for button in button_elements:
        if button.text == "送信":
            button.click()


if __name__ == "__main__":
    check_initfile_exist()
    config_ini.read(config_ini_path, encoding='utf-8')

    read_user = config_ini['CONFIG']
    Email = read_user.get('Email')
    Password = read_user.get('Password')
    url = read_user.get('ENTERURL')

    read_nyushitsu = config_ini['NYUSHITSU']
    kenkatsukun_check(read_nyushitsu, url, Email, Password)
