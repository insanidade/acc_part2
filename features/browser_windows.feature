Feature: Browser Window Handling

  Scenario: Open and validate a new browser window
    Given I navigate to https://demoqa.com/
    When I click the "Alerts, Frame & Windows" card
    And I select the "Browser Windows" submenu
    And I click the "New Window" button
    Then a new browser window should open
    And the new window should contain the text "This is a sample page"
    When I close the new browser window
    Then I should return to the original window

