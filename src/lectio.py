import time
from playwright.sync_api import sync_playwright, expect


class LectioBot:
    def __init__(self, school_id, lectio_user, lectio_password, browser_headless=True):
        self.school_id = school_id
        self.lectio_user = lectio_user
        self.lectio_password = lectio_password
        self.browser_headless = browser_headless
        self.browser, self.page = self.launch_browser()

    def launch_browser(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.browser_headless)
            page = browser.new_page()
            return browser, page

    def login_to_lectio(self):
        self.page.goto(f"https://www.lectio.dk/lectio/{self.school_id}/login.aspx")
        locator = self.page.locator('.maintitle')
        expect(locator).to_contain_text("Lectio Log ind")

        self.page.fill("#username", self.lectio_user)
        self.page.fill("#password", self.lectio_password)
        self.page.click("#m_Content_submitbtn2")

        locator = self.page.locator('.ls-user-name')
        expect(locator).to_contain_text(self.lectio_user)
        return True

    def navigate_to_messages(self):
        locator = self.page.locator("#s_m_Content_Content_NewMessageLnk")
        expect(locator, 'Ny besked')
        self.page.click("#s_m_Content_Content_NewMessageLnk")
        return True

    def send_message(self, send_to: str, subject: str, msg: str, this_msg_can_be_replied: bool):
        locator = self.page.locator("#s_m_Content_Content_MessageThreadCtrl_addRecipientDD_inp")
        expect(locator, 'end')  # Replace 'end' with actual text you expect

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

        self.page.click("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_SendMessageBtn")
        self.page.wait_for_timeout(2000)

        locator = self.page.locator("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_ctl03_innerBtn")
        expect(locator, 'more_vert')  # Replace 'more_vert' with actual text you expect

        return True


def main():
    pass


if __name__ == '__main__':
    main()
