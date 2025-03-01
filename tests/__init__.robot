*** Settings ***
Library    Browser
Library    ../utils/perf_utils/performance_keywords.py

Suite Setup    Initialize Performance Monitoring    ${SUITE_NAME}    True
Suite Teardown    Close Browser Driver And Generate Report

*** Keywords ***
Initialize Performance Monitoring
    [Arguments]    ${suite_name}    ${performance_monitoring_flag}
    Enable Performance Monitoring    ${performance_monitoring_flag}
    Start Performance Monitoring    ${suite_name}

Close Browser Driver And Generate Report
    Close Browser
    Close Context
    Save Performance Metrics
    # Generate Performance Report    ${SUITE_NAME}
    # Generate HTML Performance Report    ${SUITE_NAME}
    End Performance Monitoring    ${SUITE_NAME}
