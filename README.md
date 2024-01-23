# DevCompete

## How to setup this django project locally
<details>
    <summary>Using poetry (Recommended)</summary>
    Steps:
    <ol>
        <li>Install poetry from <a href="https://python-poetry.org/docs/#installation">here</a></li>
        <li>Clone this repository</li>
        <li>Run <code>poetry install</code> in the root directory of the project</li>
        <li>Run <code>poetry shell</code> to activate the virtual environment</li>
        <li>Run <code>python manage.py migrate</code> to apply migrations</li>
        <li>Run <code>python manage.py collectstatic</code> to collect static files</li>
        <li>Run <code>python manage.py createsuperuser</code> to create a superuser</li>
        <li>Run <code>python manage.py runserver</code> to run the server</li>
        <li>Go to <code>localhost:8000</code> to view the website</li>
    </ol>
</details>

<details>
    <summary>Using pip</summary>
    Steps:
    <ol>
        <li>Clone this repository</li>
        <li>Run <code>pip install -r requirements.txt</code> in the root directory of the project</li>
        <li>Run <code>python manage.py migrate</code> to apply migrations</li>
        <li>Run <code>python manage.py collectstatic</code> to collect static files</li>
        <li>Run <code>python manage.py createsuperuser</code> to create a superuser</li>
        <li>Run <code>python manage.py runserver</code> to run the server</li>
        <li>Go to <code>localhost:8000</code> to view the website</li>
    </ol>
</details>

## Features
### Practice Problems
You can pratice coding problems on our platform in a very user friendly & appealing user interface. You can also get help from AI and get subtle hints to improve your code to optimize it.

### Contests
You can participate in 1v1 coding contests on our platform. 
The contest modules allows users to see realtime progress of their opponenet to make the contest more interesting.

### AI Chat
You can chat with our AI to get help with learn and upskill yourself. You can also get help from AI and get subtle hints to improve your code to optimize it.

## Project Structure

The project is organized into several Django apps, each serving a different part of the application:

- `contest/`: This app handles the creation and management of coding contests.
- `practice/`: This app is responsible for managing practice problems.
- `devcompete/`: This is the main Django project directory. It contains settings, URL configurations, and utility functions.

## Code execution
The code is evaluated using the Judge0. You can use your own instance of judge0 by deploying it on your own cloud. 

We are currently using the Judge0 instance that we have deployed on our Azure VM. 

Judge0 API docs: https://ce.judge0.com/
Judge0 executes our code in an isolated environment. The code is executed in a docker container.

## API & Services used
- Private Judge0 Instance: For Code execution
- Google Gemini API: For AI help & Code analysis
- Azure VM: For hosting the Judge0 instance
- Azure App Service: For hosting the Django app
- Azure Database for MySQL: For storing the data
- Redis Cloud: For caching the data
- Azure OpenAI Service: For AI help & Code analysis based on gpt3.5 model