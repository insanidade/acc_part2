#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Step definitions for CRUD operations on DemoQA Web Tables.

"""

from assertpy import assert_that
from behave import given, when, then
from faker import Faker
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


fake = Faker()


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


@given('I navigate to the DemoQA homepage at "{url}"')
def step_navigate_homepage(context, url):
    context.driver.get(url)


@when('I click on the "Elements" card')
def step_click_elements_card(context):
    driver = context.driver
    elements_card = driver.find_element(By.XPATH, "//h5[text()='Elements']/ancestor::div[contains(@class, 'top-card')]")
    scroll_into_view(driver, elements_card)
    elements_card.click()


@when('I click the "Web Tables" submenu item')
def step_click_web_tables_submenu(context):
    driver = context.driver
    submenu = driver.find_element(By.XPATH, "//span[text()='Web Tables']")
    scroll_into_view(driver, submenu)
    submenu.click()


@when('I add a new record to the table with random data')
def step_add_new_record(context):
    driver = context.driver
    add_button = driver.find_element(By.ID, "addNewRecordButton")
    scroll_into_view(driver, add_button)
    add_button.click()

    context.first_name = fake.first_name()
    context.last_name = fake.last_name()
    context.user_email = fake.unique.email()
    context.age = str(fake.random_int(min=18, max=65))
    context.salary = str(fake.random_int(min=30000, max=150000))
    context.department = fake.job()

    driver.find_element(By.ID, "firstName").send_keys(context.first_name)
    driver.find_element(By.ID, "lastName").send_keys(context.last_name)
    driver.find_element(By.ID, "userEmail").send_keys(context.user_email)
    driver.find_element(By.ID, "age").send_keys(context.age)
    driver.find_element(By.ID, "salary").send_keys(context.salary)
    driver.find_element(By.ID, "department").send_keys(context.department)
    driver.find_element(By.ID, "submit").click()


def find_row_by_email(driver, email):
    wait = WebDriverWait(driver, 5)
    return wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//div[@role='rowgroup']/div[@role='row'][.//div[text()='{email}']]",
            )
        )
    )


@when('I edit the first name of the newly created record')
def step_edit_record(context):
    driver = context.driver
    row = find_row_by_email(driver, context.user_email)
    edit_button = row.find_element(By.CSS_SELECTOR, "span[title='Edit']")
    scroll_into_view(driver, edit_button)
    edit_button.click()

    first_name_input = driver.find_element(By.ID, "firstName")
    first_name_input.clear()
    first_name_input.send_keys("EditedName")
    driver.find_element(By.ID, "submit").click()


@when('I delete the newly created record')
def step_delete_record(context):
    driver = context.driver
    row = find_row_by_email(driver, context.user_email)
    delete_button = row.find_element(By.CSS_SELECTOR, "span[title='Delete']")
    scroll_into_view(driver, delete_button)
    delete_button.click()


@then('the record should no longer be present in the table')
def step_verify_record_deleted(context):
    driver = context.driver
    wait = WebDriverWait(driver, 5)
    wait.until(EC.invisibility_of_element_located((By.XPATH, f"//div[text()='{context.user_email}']")))

    try:
        driver.find_element(By.XPATH, f"//div[text()='{context.user_email}']")
        found = True
    except NoSuchElementException:
        found = False

    assert_that(found).is_false()

