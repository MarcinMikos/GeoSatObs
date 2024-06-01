# Project Overview

The project offers satellite data analysis.

## Project Structure

- **.idea/**: This directory contains configuration files used by IntelliJ IDEA and other JetBrains-based IDEs like PyCharm.
- **.venv/**: This directory is associated with Python virtual environments. A virtual environment is a tool that allows you to maintain isolated installations of packages and dependencies for different Python projects. This is particularly useful when different projects require different versions of the same packages or libraries.
- **src/**: This directory contains almost all the scripts present in this project, including the data storage directory.
- **app1/** and **website/**: These directories are used to deploy the site on a local development server provided by Django.
- **db.sqlite3**: This is the default database file used by Django when the project uses the SQLite database management system. SQLite is a built-in database system that does not require a separate database server, making it ideal for rapid prototyping and development.
- **manage.py**: This is a key script in every Django project. It is a command-line utility that allows you to interact with the Django project in various ways.
- **requirements.txt**: This file contains a list of dependencies (libraries and their versions) that are required to run the project.

## Getting Started

When running scripts, remember to start with:
- .\.venv\Scripts\activate 
- pip install -r requirements.txt

### Prerequisites

Make sure you have the following installed:

﻿numpy == 1.26.4
pandas == 2.2.1
matplotlib == 3.8.3
hatanaka == 2.8.1
django == 3.2.12
scikit-learn == 1.5.0

### Installation

Clone the repository:

   git clone https://github.com/MarcinMikos/GeoSatObs

### License

This project is licensed under the MIT License
