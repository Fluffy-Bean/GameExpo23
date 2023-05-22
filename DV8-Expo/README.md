# Game Expo 2023
The all new and upgraded website that runs on the Flask macro-framework


## Developing
### Prerequisites
Clone the latest branch, and create a venv environment. Then, install the requirements.txt file.

To create the required database run:
```bash
$ flask --app website init-db
```

### Running
To run the website, run the following command:
```bash
$ flask --app website run
```

## Running
While the docker-compose file runs the program for you, its possible to just run the file locally.
```bash
# gunicorn --bind="0.0.0.0:5000" --workers=4 website:app
```
