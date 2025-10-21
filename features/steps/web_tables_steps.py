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
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


fake = Faker()


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def set_rows_per_page(driver, size=20):
    try:
        select_element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[aria-label='rows per page']"))
        )
        Select(select_element).select_by_value(str(size))
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "select[aria-label='rows per page']"), str(size))
        )
    except TimeoutException:
        pass


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
    set_rows_per_page(driver, 20)


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
    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, f"//div[text()='{context.user_email}']"))
    )


def build_random_record():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "age": str(fake.random_int(min=18, max=65)),
        "salary": str(fake.random_int(min=30000, max=150000)),
        "department": fake.job(),
    }


def submit_registration_form(driver, data):
    form = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "userForm")))
    form.find_element(By.ID, "firstName").clear()
    form.find_element(By.ID, "firstName").send_keys(data["first_name"])
    form.find_element(By.ID, "lastName").clear()
    form.find_element(By.ID, "lastName").send_keys(data["last_name"])
    form.find_element(By.ID, "userEmail").clear()
    form.find_element(By.ID, "userEmail").send_keys(data["email"])
    form.find_element(By.ID, "age").clear()
    form.find_element(By.ID, "age").send_keys(data["age"])
    form.find_element(By.ID, "salary").clear()
    form.find_element(By.ID, "salary").send_keys(data["salary"])
    form.find_element(By.ID, "department").clear()
    form.find_element(By.ID, "department").send_keys(data["department"])
    form.find_element(By.ID, "submit").click()


@when("I create 12 new records dynamically using random data")
def step_create_bulk_records(context):
    driver = context.driver
    context.bulk_user_emails = []
    for _ in range(12):
        add_button = driver.find_element(By.ID, "addNewRecordButton")
        scroll_into_view(driver, add_button)
        add_button.click()

        record = build_random_record()
        submit_registration_form(driver, record)

        context.bulk_user_emails.append(record["email"])
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[@role='rowgroup']/div[@role='row'][.//div[text()='{record['email']}']]")
            )
        )


@when("I delete all newly created records")
def step_delete_bulk_records(context):
    driver = context.driver
    for email in getattr(context, "bulk_user_emails", []):
        try:
            row = find_row_by_email(driver, email)
        except TimeoutException:
            continue

        delete_button = row.find_element(By.CSS_SELECTOR, "span[title='Delete']")
        scroll_into_view(driver, delete_button)
        delete_button.click()
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, f"//div[text()='{email}']"))
        )


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

    assert_that(found).described_as("Primary record should be deleted").is_false()

    for email in getattr(context, "bulk_user_emails", []):
        try:
            driver.find_element(By.XPATH, f"//div[text()='{email}']")
            bulk_found = True
        except NoSuchElementException:
            bulk_found = False

        assert_that(bulk_found).described_as(f"Bulk record with email {email} should be deleted").is_false()

