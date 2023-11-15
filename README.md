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