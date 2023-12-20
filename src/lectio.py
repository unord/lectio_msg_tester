import sys
import time
import traceback
from playwright.sync_api import sync_playwright, expect
from applitools.playwright import Eyes, Target


class LectioBot:
    def __init__(self,
                 school_id,
                 lectio_user,
                 lectio_password,
                 browser_headless=True,
                 applitools_is_active=False,
                 applitools_api_key=None,
                 applitools_app_name=None,
                 applitools_test_name=None):
        self.school_id = school_id
        self.lectio_user = lectio_user
        self.lectio_password = lectio_password
        self.browser_headless = browser_headless
        self.applitools_is_active = applitools_is_active
        self.applitools_api_key = applitools_api_key
        self.applitools_app_name = applitools_app_name
        self.applitools_test_name = applitools_test_name
        self.playwright = None
        self.browser = None
        self.page = None
        self.eyes = None


    def start_playwright(self):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.browser_headless)
            self.page = self.browser.new_page()
            if self.applitools_is_active:
                self.eyes = Eyes()
                self.eyes.api_key = self.applitools_api_key
                self.eyes.open(self.page, self.applitools_app_name, self.applitools_test_name)
        except Exception as e:
            print(f"Error starting Playwright: {e}")
            print(traceback.format_exc())
            sys.exit(1)

    def stop_playwright(self):
        try:
            if self.browser:
                if self.applitools_is_active:
                    self.eyes.close()
                    self.eyes.abort_if_not_closed()
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error stopping Playwright: {e}")
            print(traceback.format_exc())

    def login_to_lectio(self):
        try:
            self.page.goto(f"https://www.lectio.dk/lectio/{self.school_id}/login.aspx")
            if self.applitools_is_active:
                self.eyes.check_window("Lectio Login page")
            locator = self.page.locator('.maintitle')
            expect(locator).to_contain_text("Lectio Log ind")
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            sys.exit(1)
            return False

        try:
            self.page.fill("#username", self.lectio_user)
            self.page.fill("#password", self.lectio_password)
            self.page.click("#m_Content_submitbtn2")

            if self.applitools_is_active:
                self.eyes.check_window("Check to see if Lectio logins to home page")
            locator = self.page.locator('.ls-user-name')
            expect(locator).to_contain_text(self.lectio_user)
        except Exception as e:
            print("Error logging in")
            print(e)
            return False
        return True

    def navigate_to_messages(self):
        self.page.goto(f"https://www.lectio.dk/lectio/234/beskeder2.aspx")
        if self.applitools_is_active:
            self.eyes.check_window("Go to 'Lectio Beskeder' page")
        locator = self.page.locator("#s_m_Content_Content_NewMessageLnk")
        expect(locator, 'Ny besked')
        self.page.click("#s_m_Content_Content_NewMessageLnk")
        return True

    def send_message(self, send_to: str, subject: str, msg: str, this_msg_can_be_replied: bool):
        locator = self.page.locator("#s_m_Content_Content_MessageThreadCtrl_addRecipientDD_inp")
        if self.applitools_is_active:
            self.eyes.check_window("Check to see if 'Ny besked' page is loaded")
        expect(locator, 'end')

        to_field_locator = self.page.locator("#s_m_Content_Content_MessageThreadCtrl_addRecipientDD_inp")
        to_field_locator.fill(send_to)
        time.sleep(5)
        self.page.click(f"text={send_to}")

        subject_field_locator = self.page.locator(
            "#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeHeaderTitleTB_tb")
        subject_field_locator.fill(subject)

        if not this_msg_can_be_replied:
            self.page.click("#s_m_Content_Content_MessageThreadCtrl_RepliesNotAllowedChkBox")

        message_field_locator = self.page.locator(
            "#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeContentBBTB_TbxNAME_tb")
        message_field_locator.fill(msg)

        if self.applitools_is_active:
            self.eyes.check_window("Check to see if message is filled out correctly")
        self.page.click("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_SendMessageBtn")
        self.page.wait_for_timeout(2000)

        locator = self.page.locator("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_ctl03_innerBtn")
        expect(locator, 'more_vert')
        if self.applitools_is_active:
            self.eyes.check_window("Check to see if message after it is sent")

        return True


def main():
    pass


if __name__ == '__main__':
    main()
