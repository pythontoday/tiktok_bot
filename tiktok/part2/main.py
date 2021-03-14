import os
import pickle
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from tiktok.config import vk_phone, vk_password


class TikTokBot:
    def __init__(self, vk_phone, vk_password):
        self.vk_phone = vk_phone
        self.vk_password = vk_password
        options = webdriver.FirefoxOptions()
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
        )
        options.set_preference("dom.webdriver.enabled", False)
        self.driver = webdriver.Firefox(
            executable_path="/absolute_path/geckodriver",
            options=options
        )

    def xpath_exists(self, xpath):
        """Checks element by xpath"""

        try:
            self.driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def class_exists(self, class_name):
        """Checks element by class"""

        try:
            self.driver.find_element_by_class_name(class_name)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def closes_driver(self):
        """Closes driver"""

        self.driver.close()
        self.driver.quit()

    def get_cookies(self):
        """Gets cookies"""

        if os.path.exists(f"/absolute_path/{vk_phone}_cookies"):
            print("Cookies exist! You can log in!")
            self.closes_driver()
        else:
            print("No cookies! Trying to log in...")
            self.driver.get("https://tiktok.com/")
            time.sleep(5)

            if self.class_exists("login-button"):
                try:
                    self.driver.find_element_by_class_name("login-button").click()
                    time.sleep(5)

                    # switch to iframe
                    iframe = self.driver.find_element_by_xpath("//iframe[@class='jsx-2873455137']")
                    self.driver.switch_to.frame(iframe)
                    time.sleep(5)

                    if self.xpath_exists("//div[contains(text(), 'VK')]"):
                        self.driver.find_element_by_xpath("//div[contains(text(), 'VK')]").click()
                        time.sleep(5)
                    elif self.xpath_exists("//div[contains(text(), 'Log in with VK')]"):
                        self.driver.find_element_by_xpath("//div[contains(text(), 'Log in with VK')]").click()
                        time.sleep(5)

                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(3)

                    email_input = self.driver.find_element_by_name("email")
                    email_input.clear()
                    email_input.send_keys(vk_phone)
                    time.sleep(3)

                    password_input = self.driver.find_element_by_name("pass")
                    password_input.clear()
                    password_input.send_keys(vk_password, Keys.ENTER)
                    time.sleep(15)

                    self.driver.switch_to.window(self.driver.window_handles[0])

                    # cookies
                    pickle.dump(
                        self.driver.get_cookies(),
                        open(f"/absolute_path/{vk_phone}_cookies", "wb")
                    )
                    print("You're in! Good job! Cookies saved!")
                    self.closes_driver()
                except Exception as ex:
                    print(ex)
                    self.closes_driver()
            else:
                print("Ups... Something was wrong...")
                self.closes_driver()

    def set_like(self, post_url):
        """Sets a like on a post by link"""

        try:
            self.driver.get("https://tiktok.com/")
            time.sleep(4)
            for cookie in pickle.load(
                open(f"/absolute_path/{vk_phone}_cookies", "rb")
            ):
                self.driver.add_cookie(cookie)
            time.sleep(2)
            self.driver.refresh()
            time.sleep(3)

            if not self.class_exists("login-button"):
                print("Log in successfully!")

                self.driver.get(url=post_url)
                time.sleep(random.randrange(3, 7))
                item_video_container = self.driver.find_element_by_class_name("item-video-container").click()
                time.sleep(random.randrange(3, 7))

                like_span = self.driver.find_element_by_class_name(
                    "action-wrapper-v2"
                ).find_element_by_class_name("icons")

                # checking whether it was liked before
                if "liked" in like_span.get_attribute("class").split():
                    print("Sorry, You already liked this post!")
                else:
                    like_button = self.driver.find_element_by_class_name("like").click()
                    time.sleep(random.randrange(3, 7))
                    close_button = self.driver.find_element_by_class_name("close").click()
                    time.sleep(random.randrange(3, 7))
                    print("Yeah! You liked the post!")

                self.closes_driver()
            else:
                print("Bad log in, try again!")
                self.closes_driver()
        except Exception as ex:
            print(ex)
            print("Check the URL please!")
            self.closes_driver()


def main():
    tiktok_bot = TikTokBot(vk_phone=vk_phone, vk_password=vk_password)
    # tiktok_bot.get_cookies()
    tiktok_bot.set_like(post_url="post_url")


if __name__ == '__main__':
    main()
