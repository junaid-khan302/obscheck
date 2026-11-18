# ObsCheck

A command-line tool that validates raw classroom observation text files,
labels every line as Valid, Warning or Error, stores the results in SQLite
and exports a CSV report.

Personal learning project, inspired by a classroom-observation use case.

## Features

- Detects the file encoding automatically
- Validates each line (time, student ID, activity, observer)
- Three result levels: Valid, Warning, Error
- Keeps the original raw line unchanged in the database
- Exports a CSV report
- Unit tests with pytest

## Input format

Each line has four fields separated by semicolons:

    timestamp;student_id;activity;observer
    09:00:05;S01;Passive;Obs1

Allowed activities: Passive, Active, Constructive, Interactive.

## Validation rules

| Result | Examples |
|---|---|
| Valid | all four fields correct |
| Warning | wrong capitalisation, extra spaces, missing observer |
| Error | wrong number of fields, impossible time, unknown activity, empty student ID |

## Setup

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

## Usage

    python src/validator.py

## Run the tests

    pytest

## Tech

Python, pandas, SQLite, charset-normalizer, pytest

## What I learned

(Write 3-4 sentences here in your own words.)