# Concepts and principles

## The philosophy behind machine learning frameworking

### An incomplete list of rising issues when it comes to machine learning deployment

We will focus on machine learning *development* lifecycle. Orchestration

#### The training process is poorly reproducible

Lots of moving part: code + parameters + data + environment (packages versions...) + infrastructure (build on Windows, deploy on linux)

- lots of randomness (seed for each model, separation train/test/validation, moving underlying data sources -> non immutable data...)

- process non linear : test, show result to stakeholder, remove one varibale, add another, retrain...

As a consequence, data scientists deploy models (trained) rather than pipelines, e.g. a zip and a very long & obfuscated script which do a lot of poorly related things (both data visualisation, training, inference, extra statistical analysis...)

This makes everything 1) very hard to modify 2) very hard to correct 3) very long to deploy beacause there are a lot of manual tests

#### The data scientist and stakeholders focus on training

- best example is Kaggle: you do not deploy an inference pipeline, but only the predictions, which means that you completely ignore the non reproducibility which arises from the preprocessing (encoding, code bugs...)

- schema: preprocess test and train simultaneously train, then analyze predictions on test, never form the beginning

=> many data scientists have poor CS abilities (because it is not what they were trained for)

#### Inference and training are entirely decoupled

- nobody cares about inference before deployment (cf previous paragraph)
- This is where difficulty arise for the data scientist

#### data scientists do not deliver pipelines, and consequently do not handle business objects

scenario: movie review
The data scientist imagine that someone will deliver a one hot encoded matrix with the dictionary he has defined!!

> Lots of recoding, hardly possible to modify, high operational risk, cannot update the model

#### Many other problems not addressed here

Latency, data underlying distribution over time, model decay, data access...

### Overcoming these problems: support an organisational solution with an efficient tool

-> auto tracking
-> data scientists must deliver training pipelines which takes business objects as inputs
-> training and inference pipelines must be developped at the same time and not one after another

-> declare a clear contrat of what the output of the data science project is: an inference pipeline. This defines a clear "definition of done" of the data science project: is it ready to deploy?

Downside? -> it increases data scientist's responsibilities ->
However, this adds rigidity to the data scientist work and this must not decreases the quality of the delivery: the data scientist should still benifts from the interactivy he needs to work => we want to leverage kedro which is very flexible and offers a convenient way to transition from notebooks to pipeline

> Enforcing these solutions with a tool: `kedro-mlflow` at the rescue
