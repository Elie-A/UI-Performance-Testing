# *** Settings ***
# Library    ../utils/keywords/login_keywords.py
# Library    ../utils/keywords/products_keywords.py
# Library    ../utils/perf_utils/performance_keywords.py

# *** Variables ***
# @{SORT_OPTIONS}    Name (A to Z)    Name (Z to A)    Price (low to high)    Price (high to low)

# *** Keywords ***
# Login
#     user navigates to application    headless_mode=False
#     user logs in    standard_user    secret_sauce
#     user is on products page

# Sort Products
#     user is on products page
#     FOR  ${option}  IN  @{SORT_OPTIONS}
#         user sorts products    attribute=text    option_text=${option}
#         products are sorted    option_text=${option}
#     END

# *** Test Cases ***
# Login Test
#     Measure Keyword    Login
#     Measure Keyword    Sort Products