# -*- coding: utf-8 -*-
from time import sleep
from random import randint
import scrapy
from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import pickle
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from scrapy_selenium import SeleniumRequest

k = 0


class LearningbarSpider(scrapy.Spider):
    name = 'learningbar'
    allowed_domains = ['learningbar.tw']
    start_urls = ['https://www.learningbar.tw/LBR_Login.asp']

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        chrome_path = which("chromedriver")

        self.driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options)
        self.driver.get('https://www.learningbar.tw/LBR_Login.asp')
        username = self.driver.find_element_by_css_selector("#User_E_Mail")
        password = self.driver.find_element_by_css_selector("#User_Password")

        username.send_keys("")
        password.send_keys("")

        self.driver.find_element_by_xpath('//*[@id="Submit"]').click()

# 進入分類

        self.driver.switch_to.default_content()
        main = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements_by_tag_name('frame[name^="LBR_Body"]'))  # 隱性等待
        self.driver.switch_to.frame(main[0])  # 切換frame進入網頁2
        WebDriverWait(self.driver, 10).until(lambda d: d.find_elements_by_css_selector(
            'div[class^="container"] > ul > li')[1]).click()

    def parse(self, response):
        self.driver.switch_to.default_content()
        main = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements_by_tag_name('frame[name^="LBR_Body"]'))  # 隱性等待
        self.driver.switch_to.frame(main[0])  # 切換frame進入網頁2
        WebDriverWait(self.driver, 10).until(lambda d: d.find_elements_by_xpath(
            "//option[contains(text(),'Select')]/following-sibling::option")[1])
        if self.driver.find_element_by_xpath("(//option[contains(text(),'Select')]/following-sibling::option)[1]"):

            # get the number of details to click

            self.driver.switch_to.default_content()
            main = WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements_by_tag_name('frame[name^="LBR_Body"]'))  # 隱性等待
            self.driver.switch_to.frame(main[0])  # 切換frame進入網頁2
            WebDriverWait(self.driver, 10).until(lambda d: d.find_elements_by_xpath(
                "//option[contains(text(),'Select')]/following-sibling::option"))
            opts = self.driver.find_elements_by_xpath(
                "(//option[contains(text(),'Select')]/following-sibling::option)")
            for i, opts[i] in enumerate(opts):
                self.driver.switch_to.default_content()
                main = WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_elements_by_tag_name('frame[name^="LBR_Body"]'))  # 隱性等待
                self.driver.switch_to.frame(main[0])  # 切換frame進入網頁2
                WebDriverWait(self.driver, 10).until(lambda d: d.find_elements_by_xpath(
                    "//option[contains(text(),'Select')]/following-sibling::option"))
                opts = self.driver.find_elements_by_xpath(
                    "(//option[contains(text(),'Select')]/following-sibling::option)")
                opts[i].click()

                self.driver.find_element_by_xpath(
                    "//input[@id='Submit']").click()

                self.driver.switch_to.default_content()
                main = WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_elements_by_tag_name('frame[name^="LBR_Body"]'))  # 隱性等待
                self.driver.switch_to.frame(main[0])  # 切換frame進入網頁2

                WebDriverWait(self.driver, 10).until(lambda d: d.find_elements_by_xpath(
                    "//font[contains(text(),'第')]/ancestor::div[@class='row']"))

                self.html = self.driver.page_source
                self.driver.refresh()

            # ==============================================================================================================
                resp = Selector(text=self.html)
                questions = resp.xpath(
                    '//*[@width="2.25%"]/ancestor::div[@class="col-md-12"]')
                for j, question in enumerate(questions):
                    title = question.xpath(
                        './/tbody/tr[1]/td[3]/span/text()').get(),
                    # choices = question.xpath(
                    #     ".//td[@valign='top']/div/div[@class='col-md-12']//table").getall()
                    # "//td[@valign='top']/div/div[@class='col-md-12']//td")
                    # for c in choices:
                    #     choices = c.text
                    #source = question.find_element_by_xpath('')
                    print(title)
                    details = resp.xpath(
                        "//font[contains(text(),'第')]/ancestor::div[@class='row']")
                    for k, detail in enumerate(details):
                        # source = detail.xpath(
                        #     ".//div[contains(@class,'col-md-7 text-left')]/font/font/text()")
                        # source = source.xpath('string(.)').extract()[0]
                        answer = detail.xpath(
                            ".//div[contains(@class,'col-md-1')]/font[2]/text()").get()
                        #source = question.find_element_by_xpath('')
                    # yield{
                    #     'title': title,
                    #     # 'choices':choices,
                    #     'source': source,
                    #     'answer': answer,
                    # }
                        print(answer)
                    # print(source)
                    k += 1
                    j += 1
                i += 1
            else:
                self.driver.close()
                # yield SeleniumRequest(
                #     wait_time=3,
                #     callback=self.parse
                # )
                # article = item.LearningbartwItem()
                # article['title'] = title
                # article['choices'] = choices
                # article['source'] = source
                # article['answer'] = answer
