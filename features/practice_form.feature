Feature: DemoQA Practice Form

  Scenario: Successfully fill out and submit the practice form
    Given I navigate to https://demoqa.com/
    When I click on the "Forms" card
    And I click on the "Practice Form" submenu item
    And I fill out the practice form with random data
    And I upload the sample text file
    And I submit the form
    Then a confirmation popup should appear
    And I close the confirmation popup

