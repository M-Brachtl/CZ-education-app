# Edukační aplikace pro gramatické jevy v českém jazyce

## Contents
* [Setup Instructions](#setup-instructions)
* [Frontend repository](https://github.com/Tucnuc/Czech-Education-App)
* [Usage](#usage)


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
2. Install the required packages with the specified versions using requirements.txt:
    ```sh
    pip install -r requirements.txt
    ```
   or you can list it directly:  
    ```sh
    pip install stanza==1.10.1 fastapi==0.115.8 uvicorn==0.34.0 mistralai==1.7.0
    ```

### Step 3: Run the Installation Script

1. Ensure the virtual environment is activated.
2. Run the  script:
    ```sh
    python install.py
    ```

### Step 4: Set up API Key as an Environment Variable

1. Obtain your API key from [Mistral AI](https://mistral.ai/products/la-plateforme).
2. Create a `.env` file in the root directory of your project.
3. Add the following line to the `.env` file, replacing `your_api_key_here` with your actual API key:
    ```
    MISTRAL_API_KEY=your_api_key_here
    ```

You are now ready to use the application.

## Usage
### Running the code
After you've set up your virtual environment, you can launch the code by running main.py file.
### Testing the code
The testing html is available on [localhost:8000/test/test.html](http://localhost:8000/test/test.html)
### Using the app
The full version of the app with frontend is availeble on [localhost:8000/Czech-Education-App](localhost:8000/Czech-Education-App)