
from playwright.async_api import Page, expect
from pages.register_page import Registration_Page


async def test_valid_registration(page: Page, logger):
    registration_page = Registration_Page(page)

    logger.info("Opening the Registration Page")
    await registration_page.registration_url()

    logger.info("Verifying the Username Element is visible")
    await expect(registration_page.username).to_be_visible()

    logger.info("Verifying the Password Element is visible")
    await expect(registration_page.password).to_be_visible()

    logger.info("Verifying the Confirm Password Element is visible")
    await expect(registration_page.confirmPassword).to_be_visible()

    logger.info("Verifying the Register Button is visible")
    await expect(registration_page.registor_button).to_be_visible()

    logger.info("Entering the Username")
    await registration_page.username.fill("Anshul")

    logger.info("Entering the Password")
    await registration_page.password.fill("Testing@123")

    logger.info("Entering the Confirm Password")
    await registration_page.confirmPassword.fill("Testing@123")

    logger.info("Clicking the Register Button")
    await registration_page.registor_button.click()

    logger.info("Verifying the registration error message")
    await expect(page.locator("#flash")).to_contain_text(
        "An error occurred during registration. Please try again."
    )

    logger.info("Registration error message verified successfully")
