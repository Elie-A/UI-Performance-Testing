*** Settings ***
Library    ../utils/keywords/login_keywords.py
Library    ../utils/keywords/products_keywords.py

*** Variables ***
@{SORT_OPTIONS}    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)

*** Test Cases ***
Login
    Given user navigates to application    headless_mode=False
    When user logs in    standard_user    secret_sauce
    Then user is on products page

Sort Products
    Given user is on products page
    FOR  ${option}  IN  @{SORT_OPTIONS}
        When user sorts products    attribute=text    option_text=${option}
        Then products are sorted    option_text=${option}
    END
