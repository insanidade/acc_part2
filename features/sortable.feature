Feature: Sortable List Interaction

  Scenario: Sort a list of items into ascending order
    Given I navigate to the DemoQA homepage at "https://demoqa.com/"
    When I click on the "Interactions" card
    And I select the "Sortable" submenu
    And I sort the list items into ascending order
    Then the list items should be in ascending order

