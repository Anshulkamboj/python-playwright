from playwright.async_api import Page, expect
from pages.login_page import LoginPage

# Test Case 1: Successful Login
# Launch the browser.
# Navigate to the login page URL.
# Verify that the login page is displayed successfully.
# Enter Username: practice.
# Enter Password: SuperSecretPassword!.
# Click the Login button.
# Verify that the user is redirected to the /secure page.
# Confirm the success message "You logged into a secure area!" is visible.
# Verify that a Logout button is displayed.



async def test_Successfull_login(page: Page, logger):
    logger.info("Opening the Login Page")
    await page.goto("https://practice.expandtesting.com/login")

    username = page.locator("#username")
    password = page.locator("#password")
    login_button = page.locator("#submit-login")

    logger.info("Verifying the Username field is visible")
    await expect(username).to_be_visible()

    logger.info("Verifying the Password field is visible")
    await expect(password).to_be_visible()

    logger.info("Verifying the Login button is visible")
    await expect(login_button).to_be_visible()

    logger.info("Entering the Username")
    await username.fill("practice")

    logger.info("Entering the Password")
    await password.fill("SuperSecretPassword!")

    logger.info("Clicking the Login button")
    await login_button.click()

    logger.info("Verifying redirection to the Secure page")
    await expect(page).to_have_url(
        "https://practice.expandtesting.com/secure"
    )

    logger.info("Verifying the successful login message")
    await expect(page.locator("#flash")).to_contain_text(
        "You logged into a secure area!"
    )

    logger.info("Verifying the Logout button is visible")
    await expect(
        page.get_by_text("Logout", exact=True)
    ).to_be_visible()

    logger.info("Successful login test completed")



# Test Case 2: Invalid Username
# Launch the browser.
# Navigate to the login page URL.
# Verify that the login page is displayed successfully.
# Enter an incorrect Username (e.g., wrongUser).
# Enter Password: SuperSecretPassword!.
# Click the Login button.
# Verify that an error message "Invalid username." is displayed.
# Ensure the user remains on the login page.



async def test_Invalid_Username(page: Page, logger):
    login_page = LoginPage(page)

    logger.info("Opening the Login Page")
    await login_page.login_url()

    logger.info("Verifying the Username field is visible")
    await expect(login_page.username).to_be_visible()

    logger.info("Verifying the Password field is visible")
    await expect(login_page.password).to_be_visible()

    logger.info("Verifying the Login button is visible")
    await expect(login_page.login_button).to_be_visible()

    logger.info("Entering the invalid Username")
    await login_page.username.fill("wrongUser")

    logger.info("Entering the Password")
    await login_page.password.fill("SuperSecretPassword!")

    logger.info("Clicking the Login button")
    await login_page.login_button.click()

    logger.info("Verifying the invalid login error message")
    await expect(page.locator("#flash")).to_contain_text(
        "Your password is invalid!"
    )

    logger.info("Verifying the user remains on the Login Page")
    await expect(page).to_have_url(
        "https://practice.expandtesting.com/login"
    )

    logger.info("Invalid username test completed")

    