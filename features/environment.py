#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Manage the Selenium WebDriver lifecycle for Behave scenarios.

"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def before_scenario(context, scenario):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()


def after_step(context, step):
    time.sleep(1)

