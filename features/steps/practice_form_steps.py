#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Step definitions for filling and submitting the DemoQA practice form.

"""

import random
from datetime import datetime
from pathlib import Path

from assertpy import assert_that
from behave import given, when, then
from faker import Faker
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


fake = Faker()
BASE_DIR = Path(__file__).resolve().parents[2]
RESOURCES_DIR = BASE_DIR / "resources"
SAMPLE_FILE = RESOURCES_DIR / "sample_file.txt"


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


@given("I navigate to the DemoQA homepage")
def step_navigate_homepage(context):
    context.driver.get("https://demoqa.com/")


@when('I click on the "Forms" card')
def step_click_forms_card(context):
    driver = context.driver
    forms_card = driver.find_element(By.XPATH, "//h5[text()='Forms']/ancestor::div[contains(@class, 'top-card')]")
    scroll_into_view(driver, forms_card)
    forms_card.click()


@when('I click on the "Practice Form" submenu item')
def step_click_practice_form(context):
    driver = context.driver
    practice_form = driver.find_element(By.XPATH, "//span[text()='Practice Form']")
    scroll_into_view(driver, practice_form)
    practice_form.click()


@when("I fill out the practice form with random data")
def step_fill_out_form(context):
    driver = context.driver

    first_name = driver.find_element(By.ID, "firstName")
    last_name = driver.find_element(By.ID, "lastName")
    email = driver.find_element(By.ID, "userEmail")
    mobile = driver.find_element(By.ID, "userNumber")
    address = driver.find_element(By.ID, "currentAddress")

    genders = driver.find_elements(By.XPATH, "//label[contains(@for, 'gender-radio')]")
    hobbies = driver.find_elements(By.XPATH, "//label[contains(@for, 'hobbies-checkbox')]")

    first_name.send_keys(fake.first_name())
    last_name.send_keys(fake.last_name())
    email.send_keys(fake.email())
    mobile.send_keys(fake.msisdn()[:10])
    address.send_keys(fake.street_address())

    gender_choice = random.choice(genders)
    scroll_into_view(driver, gender_choice)
    gender_choice.click()

    hobby_choice = random.choice(hobbies)
    scroll_into_view(driver, hobby_choice)
    hobby_choice.click()

    birth_date_input = driver.find_element(By.ID, "dateOfBirthInput")
    birth_date_input.click()

    # Set date to a fixed middle value for consistency
    target_date = datetime(fake.random_int(min=1990, max=2000), 6, 15)
    month_selector = driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")
    year_selector = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    month_selector.send_keys(target_date.strftime("%B"))
    year_selector.send_keys(str(target_date.year))

    day_selector = driver.find_element(
        By.XPATH,
        f"//div[contains(@class,'react-datepicker__day--0{target_date.day:02d}') and not(contains(@class,'--outside-month'))]",
    )
    day_selector.click()

    subjects_input = driver.find_element(By.ID, "subjectsInput")
    subjects_input.send_keys("Maths")
    ActionChains(driver).move_to_element(subjects_input).send_keys(Keys.RETURN).perform()

    state_city_pairs = [
        ("NCR", "Delhi"),
        ("Uttar Pradesh", "Lucknow"),
        ("Haryana", "Karnal"),
        ("Rajasthan", "Jaipur"),
    ]
    state_value, city_value = random.choice(state_city_pairs)

    state_container = driver.find_element(By.ID, "state")
    scroll_into_view(driver, state_container)
    state_container.click()
    state_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id,'react-select-3-option') and text()='{state_value}']"))
    )
    state_option.click()

    city_container = driver.find_element(By.ID, "city")
    scroll_into_view(driver, city_container)
    city_container.click()
    city_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id,'react-select-4-option') and text()='{city_value}']"))
    )
    city_option.click()


@when("I upload the sample text file")
def step_upload_file(context):
    driver = context.driver
    upload_input = driver.find_element(By.ID, "uploadPicture")
    upload_input.send_keys(str(SAMPLE_FILE))


@when("I submit the form")
def step_submit_form(context):
    driver = context.driver
    submit_button = driver.find_element(By.ID, "submit")
    scroll_into_view(driver, submit_button)
    submit_button.click()


@then("a confirmation popup should appear")
def step_verify_popup(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)
    modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
    assert_that(modal.is_displayed()).is_true()


@then("I close the confirmation popup")
def step_close_popup(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "closeLargeModal")))
    scroll_into_view(driver, close_button)
    driver.execute_script("arguments[0].click();", close_button)

