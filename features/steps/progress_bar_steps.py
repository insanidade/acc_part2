#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Step definitions for interacting with the DemoQA progress bar widget.

"""

from assertpy import assert_that
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def get_progress_value(driver):
    progress_bar = driver.find_element(By.CSS_SELECTOR, "div[role='progressbar']")
    return int(progress_bar.get_attribute("aria-valuenow"))


@when('I click on the "Widgets" card')
def step_click_widgets_card(context):
    driver = context.driver
    widgets_card = driver.find_element(By.XPATH, "//h5[text()='Widgets']/ancestor::div[contains(@class, 'top-card')]")
    scroll_into_view(driver, widgets_card)
    widgets_card.click()


@when('I select the "Progress Bar" submenu')
def step_select_progress_bar(context):
    driver = context.driver
    submenu = driver.find_element(By.XPATH, "//span[text()='Progress Bar']")
    scroll_into_view(driver, submenu)
    submenu.click()


@when('I click the "Start" button to begin the progress')
def step_start_progress(context):
    driver = context.driver
    start_button = driver.find_element(By.ID, "startStopButton")
    scroll_into_view(driver, start_button)
    start_button.click()


@when('I stop the progress before the bar reaches 25 percent')
def step_stop_progress_before_25(context):
    driver = context.driver
    stop_button = driver.find_element(By.ID, "startStopButton")

    while True:
        value = get_progress_value(driver)
        if 15 < value < 25:
            stop_button.click()
            context.partial_progress_value = value
            break


@then('the progress bar value should be less than or equal to 25')
def step_validate_progress_value(context):
    driver = context.driver
    value = get_progress_value(driver)
    measured_value = getattr(context, "partial_progress_value", value)
    assert_that(measured_value).is_less_than_or_equal_to(25)
    assert_that(value).is_less_than_or_equal_to(25)


@when('I click the "Start" button again')
def step_restart_progress(context):
    driver = context.driver
    start_button = driver.find_element(By.ID, "startStopButton")
    scroll_into_view(driver, start_button)
    start_button.click()


@when('I wait for the progress to reach 100 percent')
def step_wait_for_completion(context):
    driver = context.driver
    WebDriverWait(driver, 30).until(
        EC.text_to_be_present_in_element_attribute(
            (By.CSS_SELECTOR, "div[role='progressbar']"), "aria-valuenow", "100"
        )
    )


@when('I click the "Reset" button')
def step_click_reset(context):
    driver = context.driver
    reset_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "resetButton"))
    )
    scroll_into_view(driver, reset_button)
    reset_button.click()


@then('the progress bar should be reset to 0 percent')
def step_verify_reset(context):
    driver = context.driver
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_attribute(
            (By.CSS_SELECTOR, "div[role='progressbar']"), "aria-valuenow", "0"
        )
    )
    value = get_progress_value(driver)
    assert_that(value).is_equal_to(0)

