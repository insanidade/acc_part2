Feature: Web Tables CRUD Operations

  Scenario: Create, edit, and delete a record in the web table
    Given I navigate to the DemoQA homepage at "https://demoqa.com/"
    When I click on the "Elements" card
    And I click the "Web Tables" submenu item
    And I add a new record to the table with random data
    And I edit the first name of the newly created record
    And I delete the newly created record
    Then the record should no longer be present in the table

