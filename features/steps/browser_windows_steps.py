#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Step definitions for handling DemoQA browser window interactions.

"""

from assertpy import assert_that
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


@given("I navigate to https://demoqa.com/")
def step_navigate_homepage(context):
    context.driver.get("https://demoqa.com/")


@when('I click the "Alerts, Frame & Windows" card')
def step_click_alerts_card(context):
    driver = context.driver
    alerts_card = driver.find_element(
        By.XPATH,
        "//h5[text()='Alerts, Frame & Windows']/ancestor::div[contains(@class, 'top-card')]",
    )
    scroll_into_view(driver, alerts_card)
    alerts_card.click()


@when('I select the "Browser Windows" submenu')
def step_select_browser_windows(context):
    driver = context.driver
    submenu = driver.find_element(By.XPATH, "//span[text()='Browser Windows']")
    scroll_into_view(driver, submenu)
    submenu.click()


@when('I click the "New Window" button')
def step_click_new_window_button(context):
    driver = context.driver
    context.original_window = driver.current_window_handle
    new_window_button = driver.find_element(By.ID, "windowButton")
    scroll_into_view(driver, new_window_button)
    new_window_button.click()


@then("a new browser window should open")
def step_validate_new_window_opened(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)
    wait.until(EC.number_of_windows_to_be(2))

    for handle in driver.window_handles:
        if handle != context.original_window:
            context.new_window_handle = handle
            break
    assert_that(context.new_window_handle).is_not_none()
    driver.switch_to.window(context.new_window_handle)


@then('the new window should contain the text "This is a sample page"')
def step_validate_new_window_text(context):
    driver = context.driver
    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sampleHeading"))
    )
    assert_that(heading.text).contains("This is a sample page")


@when("I close the new browser window")
def step_close_new_window(context):
    context.driver.close()


@then("I should return to the original window")
def step_return_to_original_window(context):
    driver = context.driver
    driver.switch_to.window(context.original_window)
    assert_that(driver.current_window_handle).is_equal_to(context.original_window)

