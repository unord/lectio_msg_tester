import time

from playwright.sync_api import sync_playwright, expect


def lectio_send_msg(school_id: str,
                    lectio_user: str,
                    lectio_password: str,
                    send_to: str,
                    subject: str,
                    msg: str,
                    this_msg_can_be_replied: bool = False,
                    browser_headless: bool = True
                    ) -> dict:

    print(f'Logging in to school id: {school_id}')
    this_url = f"https://www.lectio.dk/lectio/{school_id}/login.aspx"
    main_page_url = f"https://www.lectio.dk/lectio/{school_id}/forside.aspx"

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=browser_headless)
            page = browser.new_page()

            # Go to login page and expect the username field to be present
            page.goto(this_url)
            locator = page.locator('.maintitle')
            expect(locator).to_contain_text("Lectio Log ind")


            # fill username and password fields
            page.fill("#username", lectio_user)
            page.fill("#password", lectio_password)

            # click the login button and expect to navigate to the home page
            page.click("#m_Content_submitbtn2")
            locator = page.locator('.ls-user-name')
            expect(locator).to_contain_text(lectio_user)  # replace with an actual selector that indicates successful login

            # If the above line didn't throw, it means login was successful
            current_user = page.inner_text(".ls-user-name")
            print(f'Logged in as: {current_user}')

            page.goto(main_page_url)
            print('Main page loaded')
            page.click("#s_m_HeaderContent_subnavigator_ctl12")

            # Expect the new message button to be visible and click it
            locator = page.locator('#s_m_Content_Content_NewMessageLnk')
            expect(locator).to_contain_text('Ny besked')
            print('Link: "Beskeder" clicked')
            page.click("#s_m_Content_Content_NewMessageLnk")
            print('Link: New message clicked')

            # Fill the 'to field'
            locator = page.locator("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_SendMessageBtn")
            expect(locator).to_contain_text('end')
            print('New message page loaded')
            to_field_locator = page.locator("#s_m_Content_Content_MessageThreadCtrl_addRecipientDD_inp")
            to_field_locator.fill(send_to)
            time.sleep(1)
            page.click(f"text={send_to}")

            # Fill the subject field
            subject_field_locator = page.locator(
                "#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeHeaderTitleTB_tb")
            subject_field_locator.fill(subject)

            # Handle the 'may reply' checkbox
            if not this_msg_can_be_replied:
                page.click("#s_m_Content_Content_MessageThreadCtrl_RepliesNotAllowedChkBox")

            # Fill the message field
            message_field_locator = page.locator(
                "#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeContentBBTB_TbxNAME_tb")
            message_field_locator.fill(msg)

            # Click the send button
            page.click("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_SendMessageBtn")

            # Wait for 2 seconds (2000 milliseconds)
            page.wait_for_timeout(2000)

            # check if the message was sent
            locator = page.locator("#s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_ctl03_innerBtn")
            expect(locator).to_contain_text('more_vert')

            browser.close()
            return {'msg': f'message sent successful to: {send_to}', 'success': True}
        except Exception as e:
            if browser:
                browser.close()
            print(f'Error in lectio_send_msg: {e}')
            return {'msg': f'Login failed. Exception: {e}', 'success': False}


def main():
    pass


if __name__ == '__main__':
    main()
