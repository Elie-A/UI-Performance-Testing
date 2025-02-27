# UI Automation and Performance Test PoC

## Introduction

This Proof of Concept (PoC) project aims to evaluate the feasibility and effectiveness of using Python, Robot Framework, and the Browser library _(Playwright)_ for UI automation leveraging the _Page Object Model (POM)_ design pattern, along with integrating performance testing. The goal is to establish a robust and scalable automation framework that can be used for comprehensive testing of web applications.

## Objectives

- UI Automation: Implement automated UI tests using the Robot Framework and the Browser library to validate the functionality of web applications.
- Performance Testing: Integrate performance testing tools to assess the application's responsiveness and stability under various load conditions.
- Framework Evaluation: Assess the ease of use, flexibility, and scalability of the chosen tools and technologies.

## How To Install

### Prerequisites

- Install [git](https://git-scm.com/downloads)
- Install python
  - [v3.10](https://www.python.org/downloads/release/python-3100/)
  - [v3.11](https://www.python.org/downloads/release/python-3110/)
  - You can install any version in between preferably [v3.10.7](https://www.python.org/downloads/release/python-3107/)
- Make sure to add git and python to your system PATH variables, if not added after intallation
- Download [VSCode](https://code.visualstudio.com/download)

### Repository

**Note: The provided link serves merely as a foundational template to facilitate the initial setup of your project.**

- Create your own fork of this repository, then clone it

### Setup environment

- Validate that python is installed on your system: `python --version` else install it - refer to Prerequisites section
- Open VSCode and configure the following extensions (5th icon in vertical menu)
  - Install Python extension
  - Install RobotCode extension
  - Even Better Toml
  - Install Workspace explorer extension
  - Install open in browser extension
  - Install Docker extension
  - Install HTML Preview extension
  - _(Optiona) Markdown Preview Enhanced_
- Restart VSCode
- Open your cloned forked repository in VSCode
- Save your workspace
- Configure workspace Explorer settings
  - Open VSCode settings and search for: `@ext:tomsaunders-code.workspace-explorer`
  - Set both user and workspace paths
- Create your virtual environment:
  - Open a terminal, type: `python -m venv .venv`
  - Activate your venv:
    - macOS/Linux: `source .venv/bin/activate`
    - Windows: `.\.venv\Scripts\activate`
    - If you encounter an error, type this command: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, then recreate your virtual environment
- Install requirements, whilst in the virtual environment, enter this command: `pip install -r ./requirements.txt`
- Install playwright wrapper using this command: `rfbrowser init`
- Create your **launch.json** file:
  - If _.vscode_ directory does not exist, you can create it under the project root directory
- Create your launch.json file, as a sample you may use the below sample:

```json
{
  "configurations": [
    {
      "type": "robotcode",
      "name": "Robot Framework: Launch template",
      "request": "launch",
      "target": "${workspaceFolder}/tests/",
      "args": [
        "--outputdir",
        "logs",
        "--suite",
        "*",
        "--exclude",
        "TAGS_TO_EXCLUDE",
        "--variable",
        "ENV:${input:env}"
      ]
    }
  ],
  "inputs": [
    {
      "id": "env",
      "type": "pickString",
      "description": "Choose your target environment",
      "options": ["dev", "uat", "pdt", "prd"],
      "default": "dev"
    }
  ]
}
```

## Execution

- You can execute your tests by:

  - Through the `launch.json` file configuration
  - Individual test suites (play button)
  - RobotCode command: `robotcode -p PROFILE_NAME robot ${TEST_PATH}` (must have profiles defined in **_robot.toml_** file) check below for a sample of toml file

    ```toml
    [profiles.dev]
    variables = { ENV = "dev", VAR1 = "VAR1_VALUE", USERNAME = "DEV_USERNAME", PASSWORD = "DEV_PASSWORD" }
    args = [
        "--exclude", "do-not-run"
    ]

    [profiles.uat]
    variables = { ENV = "uat", VAR1 = "VAR1_VALUE", USERNAME = "UAT_USERNAME", PASSWORD = "UAT_PASSWORD" }
    exclude = ["do-not-run"]
    ```

## Project Structure

imperative that we meticulously delineate its structure, encompassing all critical phases and deliverables.

To ensure our documentation is thorough and user-friendly, we should incorporate the following elements:

- Updated Directory Structure
- Guidelines for Adding Components

### Updated Directory Structure

- This section provides a clear and organized layout of our project’s directories. It includes detailed descriptions of each folder and subfolder, ensuring easy navigation and management. This structure helps maintain consistency and improves the overall maintainability of the project.
  - tests: The `tests` folder ensures our code’s reliability by containing all necessary tests.
  - utils: The `utils` folder is organized into these subfolders:
    - `keywords`: For managing pages' dedicated keywords
    - `perf_utils`: For managing classes, functions and performance keywords
    - `browser_manager`: Python file to manage browser instance
    - `misc_utils`: Python file to manage miscellaneous functionalities (i.e. sorting, get_screen_resolution, etc.)
  - pages: For managing `base_base` (common web elements functionalities), and pages functionalities
  - templates: Contains performance test html template

## Guidelines For Adding Tests

- This section provides clear instructions on how to integrate new elements into the project. It covers best practices for adding tests, utilities, configurations, and test data, ensuring consistency and maintainability across the codebase

### Adding Keywords

- Ascertain whether the action is a common one that can be utilized across multiple pages.
  - If affirmative, it should be integrated into the `base_page.py` file.
  - If negative, it should be incorporated into its respective page within the pages directory.
- Identify the web element locators, ensuring adherence to best practices.
  - The integration of new functions can either be an update of existing page functions or a new implementation
  - Once the page action function(s) is/are added, you must create or update their respective keywords within the keywords folder. - For guidance on the `Browser` library, which can be utilized either in Python or directly in Robot Framework, refer to [Browser Lib](https://marketsquare.github.io/robotframework-browser/Browser.html)
    **_Note: Make sure to name your keywords as a functional action i.e. user sorts products_**

### Adding The Test Scripts

- Once everything is finalized, you must write your tests. The current practice is to utilize [Gherkin](https://cucumber.io/docs/gherkin/) syntax
- All tests must be added to the `tests` folder. Ensure you **create a new file** when working on a **new feature**, or **update an existing file** if you are **modifying an existing feature**.
  _\_\_Note that the supported Gherkin version in Robot is below 6, so you won't be able to use the `_`nor`Rule` Gherkin keywords\_\_\*

## Performance Tests

In the current
