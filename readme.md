# Edukační aplikace pro gramatické jevy v českém jazyce

## Setup Instructions

### Step 1: Set up a Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to the project directory:
    ```sh
    cd /path/to/your/project
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

### Step 2: Install Required Packages

1. Ensure the virtual environment is activated.
2. Install the required packages with the specified versions:
    ```sh
    pip install stanza==1.10.1 fastapi==0.115.8 uvicorn==0.34.0
    ```

### Step 3: Run the Installation Script

1. Ensure the virtual environment is activated.
2. Run the  script:
    ```sh
    python install.py
    ```

You are now ready to use the application.