Feature: DemoQA Progress Bar

  Scenario: Start, stop, and reset the progress bar
    Given I navigate to the DemoQA homepage at "https://demoqa.com/"
    When I click on the "Widgets" card
    And I select the "Progress Bar" submenu
    And I click the "Start" button to begin the progress
    And I stop the progress before the bar reaches 25 percent
    Then the progress bar value should be less than or equal to 25
    When I click the "Start" button again
    And I wait for the progress to reach 100 percent
    And I click the "Reset" button
    Then the progress bar should be reset to 0 percent

