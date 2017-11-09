# coding: utf-8
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import os
import sys

from googletrans import Translator

translator = Translator()

url = 'http://redgate.linguaporta.jp/'
ID = ''
password = 'cocet2600'

useTranslation = False

# ------------------1~20---+------------2~21---+--3-#
pagenum = list(range(1, 21)) + list(range(2, 22)) + [3]  #


# --------------------------------------------------#

def compareJPwithJP(text, texts):
    """

    :param text:  Japanese of linguaporta
    :param texts: Japanese of gotten by api
    :return:      bool
    """
    pass


def EnglishToJapanese(text):
    """

    :param text: English of linguaporta
    :return:     string
    """
    string = translator.translate(text, dest='ja').text
    return string


def solver(browser, element):
    """

    :type browser: object
    """
    question = browser.find_element_by_id('qu02').text
    answers = browser.find_elements_by_name('answer[0]')
    for answer in answers:
        answer_text = answer.find_elementget_attribute('value')
        if (True):
            answer.click()


def solverByUserInput(browser):
    """

    :type browser: object
    """
    while (True):
        print('----------------------------------------')
        question = browser.find_element_by_id('qu02').text
        answers = browser.find_elements_by_name('answer[0]')
        # os.system("osascript -e 'display notification \"{}\"'".format(question))

        first_question = True
        while (True):
            if (first_question):
                print('{}の意味は?\n[1]{}\n[2]{}\n[3]{}\n[4]{}\n[5]{}\n'.format(
                    question,
                    answers[0].get_attribute('value'),
                    answers[1].get_attribute('value'),
                    answers[2].get_attribute('value'),
                    answers[3].get_attribute('value'),
                    answers[4].get_attribute('value'),
                ))
                if (useTranslation):
                    print('翻訳結果:{}'.format(EnglishToJapanese(question)))
                first_question = False
            num = input('回答>>')
            try:
                num = int(num)
            except:
                print('[-]numの入力が間違っています')
                continue
            if (int(num) in [1, 2, 3, 4, 5]):
                break
            else:
                print("[-]numの入力が間違っています。1~5の間で入力してください")
                continue
        # 正解を選択
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        answers[int(num) - 1].click()

        # 答えを送る
        browser.find_element_by_xpath('//*[@id="ans_submit"]').click()

        # 次の問題(正解)
        if (browser.find_elements_by_id('true_msg') != []):
            print('正解!')
            # os.system("osascript -e 'display notification \"正解!\"'")
            score = browser.find_element_by_xpath('//*[@id="content-study"]/table/tbody/tr[2]/td/div[5]').text
            if (score.startswith("25 点")):
                # 25点が最後なので抜ける
                break
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            nextButton = browser.find_element_by_xpath('//*[@id="under_area"]/form/input[1]')

        # 次の問題(不正解)
        elif (browser.find_elements_by_id('false_msg') != []):
            print('不正解><')
            # os.system("osascript -e 'display notification \"不正解><\"'")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            nextButton = browser.find_element_by_xpath('//*[@id="under_area"]/form[2]/input[1]')

        nextButton.click()
    # ループを抜けた後、学習ユニット一覧に戻る
    print('ユニット終了!')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.find_element_by_xpath('//*[@id="question_td"]/form[2]/input[2]').click()


def unitlist(browser):
    # 学習リストから単語の意味を選択
    """

    :type browser: object
    """
    first_question = True
    while (True):
        if (first_question):
            print("[*]何ページ目から開始しますか？")
            first_question = False
        i = input()
        try:
            i = int(i)
        except:
            print('[-]入力が間違っています')
            continue
        if (int(i) in list(range(42))):
            break
        else:
            print("[-]入力が間違っています。1~42の間で入力してください")
            continue
    r = re.compile("([^ ]+)単語の意味")
    for count in list(range(i, 42)):
        for element in browser.find_elements_by_class_name('table-resp-row'):
            element_element = element.find_element_by_class_name('col-unitname')
            text = element_element.text
            if (r.match(text) and not (text.endswith("終了"))):
                print("[*]{}のユニットを開始します".format(text))
                f = element.find_element_by_class_name('btn-study')
                location = f.location["y"] - 370
                browser.execute_script("window.scrollTo(0, %d);" % location)
                f.click()
                # solver(browser, element)
                solverByUserInput(browser)
                break
        time.sleep(1)
        if (count < 42):
            browser.find_element_by_xpath('//*[@id="content-study"]/div[2]/a[{}]'.format(pagenum[count])).click()
        else:
            break
        time.sleep(1)


def main():
    try:
        browser = webdriver.Chrome('./chromedriver')
        browser.get(url)
        browser.maximize_window()
        time.sleep(1)

        # リンガポルタ開く
        print("[*]リンガポルタを開いています")
        browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div[1]/div[2]/form/input').click()

        # 別ウインドウ遷移待機
        print("[*]別ウインドウに遷移するのを待機しています")
        WebDriverWait(browser, 3).until(lambda d: len(d.window_handles) > 1)
        browser.switch_to.window(browser.window_handles[1])

        # ID入力
        print("[*]IDを入力しています")
        browser.find_element_by_name('id').send_keys(ID)
        # PASSWORD入力
        print("[*]パスワードを入力しています。")
        browser.find_element_by_xpath('//*[@id="content-login"]/form/table/tbody/tr[2]/td/input').send_keys(password)
        # ログイン
        print("[*]ログインしています")
        browser.find_element_by_xpath('//*[@id="btn-login"]').click()

        time.sleep(1)

        # studyボタンを押す
        print("[*]studyボタンを押しています")
        browser.find_element_by_xpath('//*[@id="menu2"]/dl/dt[2]/form/a').click()

        # ユニットリストクリック
        print("[*]ユニットリストを開いています")
        browser.find_element_by_xpath('//*[@id="content-study"]/form/div/div[2]/div[3]/input').click()

        while (True): unitlist(browser)

        input('')

    finally:
        print('END')


if __name__ == '__main__':
    args = sys.argv
    if (not (len(args)) == 1):
        if (args[1] == '-t'):
            useTranslation = True
    if(ID==''):
        print('Please write your UserID')
        exit()
    main()
