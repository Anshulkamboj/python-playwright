import pytest
from playwright.async_api import Page

class Registration_Page:
    def __init__(self, page:Page):
        self.page = page
        self.username = page.locator('#username')
        self.password = page.locator('#password')
        self.confirmPassword = page.locator('#confirmPassword')
        self.registor_button = page.get_by_role('button', name='Register', exact=True)

    async def registration_url(self):
        await self.page.goto('/register')

    async def registration_page(self, username:str, password:str, confirmPassword:str):
        self.username.fill(username)
        self.password.fill(password)
        self.confirmPassword.fill(confirmPassword)
        self.registor_button.click()
        
    