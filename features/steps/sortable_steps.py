#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
- Step definitions for sorting the DemoQA sortable list widget.

"""

from assertpy import assert_that
from behave import when, then
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def capture_list_texts(elements):
    return [el.text.strip() for el in elements]


@when('I click on the "Interactions" card')
def step_click_interactions_card(context):
    driver = context.driver
    card = driver.find_element(By.XPATH, "//h5[text()='Interactions']/ancestor::div[contains(@class, 'top-card')]")
    scroll_into_view(driver, card)
    card.click()


@when('I select the "Sortable" submenu')
def step_select_sortable_submenu(context):
    driver = context.driver
    submenu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sortable']"))
    )
    scroll_into_view(driver, submenu)
    submenu.click()


@when('I sort the list items into ascending order')
def step_sort_list_items(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)
    list_container = wait.until(EC.visibility_of_element_located((By.ID, "demo-tab-list")))
    items_locator = (By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item.list-group-item-action")
    original_elements = wait.until(EC.presence_of_all_elements_located(items_locator))

    original_texts = capture_list_texts(original_elements)
    context.original_sorted_texts = sorted(original_texts)

    action = ActionChains(driver)

    for index, target_text in enumerate(context.original_sorted_texts):
        wait.until(EC.presence_of_all_elements_located(items_locator))
        current_elements = driver.find_elements(*items_locator)
        source_element = next(el for el in current_elements if el.text.strip() == target_text)
        target_element = current_elements[index]
        if source_element == target_element:
            continue
        scroll_into_view(driver, source_element)
        scroll_into_view(driver, target_element)
        action.click_and_hold(source_element).move_to_element(target_element).release().perform()
        action.reset_actions()


@then('the list items should be in ascending order')
def step_verify_sorted_order(context):
    driver = context.driver
    items_locator = (By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item.list-group-item-action")
    current_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(items_locator)
    )
    current_texts = capture_list_texts(current_elements)
    expected_texts = context.original_sorted_texts
    assert_that(current_texts).is_equal_to(expected_texts)

