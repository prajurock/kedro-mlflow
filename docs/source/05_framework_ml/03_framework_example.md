# Framework example

This assumes the user is familiar with Kedro. We will refer to a Kedro project template files (e.g. `catalog.yml`, `pipeline.py` and `hooks.py`).

## Introducing the task and dataset

IMDB movie review dataset, sentiment analysis task

Warning: not a kaggle, I do not try to produce a good model, just a comprehensive example.

*Link to the github example*

## Building the project

### The etl_app

Very basic for the example, but can be really complex in real life. What matters is that it produces "instances" and "labels".

### The ml_app

#### A vanilla example: training a machine learning model

The most basic project we can imagine is the following: the business object is a numeric matrix, and we want to train our model on it.

#### Sharing preprocessing: text cleaning example

#### Reusing data objects: the example of OneHotEncoder

#### Reusing shared inputs: the example of stopwords

#### Adding some metrics and monitoring

### The user_app

Use `MlflowModelLoggerDataset` to force reading from a given run_id.
