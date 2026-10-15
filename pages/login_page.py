import pytest

from playwright.async_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator('#username')
        self.password = page.locator('#password')
        self.login_button = page.locator('#submit-login')
    async def login_url(self):
        await self.page.goto('/login')
        
    async def login(self, username:str, password:str):
        await self.username.fill('username')
        await self.username.fill('password')
        await self.login_button.click()