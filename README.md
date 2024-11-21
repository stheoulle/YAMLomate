# YAML Parser Project

This project implements a custom YAML parser to validate and parse YAML syntax. Below are the steps to set up and run the project in a Python virtual environment.

The parser is very sensitive, and some copy and pastes don't add the right number of spaces for indentation, resulting in incorrect results. 
It is recommended to use the yaml provided in the project to test it.

yaml_input and yaml_input_2 are two valid yaml for the parser, whereas the wrong_indentation_yaml is the same as the yaml_input_2 with some indentations issues. 

---

## Prerequisites

Make sure you have the following installed:
- Python 3.7 or later
- `pip` (Python package installer)

---

## Setup Instructions

1. **Clone the Repository**

   Clone the project to your local machine:
   ```bash
   git clone git@github.com:stheoulle/YAMLomate.git
   cd YAMLomate
   ```

2. **Create a Virtual Environment**

   Create a virtual environment to isolate the project's dependencies:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On **Linux/MacOS**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

---

## How to Run the Parser

1. **Run the programm**

Run the command 
```bash
python3 parser.py
```
You can choose which snippet of code to execute in the parser.py file, changing the line 731 `if parser.parse(yaml_input6):` with another yaml_input discribed above it.


2. **Expected Output**

   - If the YAML is valid, the parser will return `Le YAML est conforme.`.
   - If the YAML is invalid, a `SyntaxError` will be raised with details about the unexpected character and position.

---``

1. **Deactivate Virtual Environment**

   When you are done working on the project, deactivate the virtual environment:
   ```bash
   deactivate
   ```

---

## Troubleshooting

- Ensure you are using the correct Python version.
- Check if the virtual environment is activated before running any Python commands.
- If you are missing a python dependency you can install it by running `pip install <dependency-name>`


For additional questions, feel free to contact the project maintainer.