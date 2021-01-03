# Why we need a mlops framework to manage machine learning development lifecycle

## Machine learning deployment is hard because it comes with a lot of constraints and no adequate tooling

### Identifying the challenges to address when deploying machine learning

It is a very common pattern to hear that "machine learning deployment is hard", and this is supposed to explain why so many firms do not achieve to insert ML models in their IT systems (and consequently, not make money despite consequent investments in ML).

On the other hand, you can find thousands of tutorial across the web to explain how to deploy a ML API in 5 mn, either locally or on the cloud. There is also a large amount of training sessions which can teach you "how to become a machine learning engineer in 3 months".

*Who is right then? Both!*

Actually, there is a confusion on what "deployment" means, especially in big enterprises that are not "tech native" or for newbies in ML world. Serving a model over an API pattern is a start, but you often need to ensure (at least) the following properties for your system:

- **scalability and cost control**: in many cases, you need to be able to deal with a lot of (possibly concurrent) requests (likely much more than during training phase). It may be hard to ensure that the app will be able to deal with such an important amount of data. Another issue is that ML oftens needs specific infrastrusture (e.g., GPU's) which are very expensive. Since the request against the model often vary wildly over time, it may be important to adapt the infrastructure in real time to avoid a lot of infrastructure costs
- **speed**: A lot of recent *state of the art* (SOTA) deep learning / ensemble models are computationally heavy and this may hurt inference speed, which is critical for some systems.
- **disponibility and resilience**: Machine learning systems are more complex than traditional softwares because they have more moving parts (i.e. data and parameters). This increases the risk of errors, and since ML systems are used for critical systems making both the infrastructure and the code robust is key.
- **portability / ease of integration with external components**: ML models are not intended to be directly used by the end users, but rather be consumed by another part of your system (e.g a call to an API). To speed up deployment, your model must be easy to be consumed, i.e. *as self contained as possible*. As a consequence, you must **deploy a ML pipeline which hanbles business objects instead of only a ML model**. If the other part which consumes your API needs to make a lot of data preprocessing *before* using your model, it makes it:
  - very risky to use, because preprocessing and model are decoupled: any change in your model must be reflected in this other data pipeline and there is a huge mismatch risk when redeploying
  - slow and costful to deploy because each deployment of your model needs some new development on the client side
  - poorly reusable beacuse each new app who wants to use the model needs some specific development on its own
- **reproducibility**: the ML development is very iterative by nature. You often try a simple baseline model and iterate (sometimes directly by discussing with the final user) to finally get the model that suits the most your needs ( wich is the balance between speed / accuracy / interpretability / maintenance costs / inference costs / data availability / labelling costs...). Looping through these iterations, it is very easy to forget what was the best model. You should not rely only on your memory to compare your experiments. Moreover, many countries have regulatory constraints to avoid discriminations (e.g. GDPR in the EU), and your must be able to justify how your model was built and to that extent reproducibility is key. It is also essential when you redeploy a model that turns out to be worse than the old one and you have to rollback fast.
- **monitoring and ease of redeployment**: It is well known that model quality decay over time (sometimes quickly!), and if you use ML for a critical activity, you will have to retrain your model periodically to maintain its performance. It is critical to be able to redeploy easily your model. This implies that retraining (or even redeployment of a new model) must be as **automated as possible** to ensure deployment speed and model quality.

An additional problem that happens in real world is that it is sometimes poorly understood by end users that the ML model is not standalone. It implies
**external developments** from the client side (at least to call the model, sometimes to adapt a data pipeline or to change the user interface to add the ML functionality) and they have hard times to understand the entire costs of a ML project as well as their responsibilities in the project. This is not really a problem of ML but rather on how to give a minimal culture on ML to business end users.

### A comparison between traditional software development and machine learning projects

#### ML and traditional software have different moving parts

A traditional software project contains several moving parts:

- code
- environment (packages versions...)
- infrastructure (build on Windows, deploy on linux)

Since it is a more mature industry, efficient tools exists to manage these items (Git, pip/conda, infra as code...). On the other hand, a ML project has additional moving parts:

- parameters
- data

As ML is much less mature field, efficient tooling to adress these items are very recent and not completely standardized yet (e.g. Mlflow to track parameters, DVC to version data, `great-expectations` to monitor data which go through your pipelines, `tensorboard` to monitor your model metrics...)

> **Mlflow is one of the most mature tool to manage these new moving parts.**

#### ML and traditional software have different development lifecycles

In traditional software, the development workflow is roughly the following:

- you create a git branch
- you develop your new feature
- you add tests and ensure there are no regression
- you merge the branch on the main branch to add your feature to the codebase

This is a **linear** development process based on **determinist** behaviour of the code.

However in ML development, the workflow is much more iterative and may looklike this:

- you create a notebook
- you make some exploration on the data with some descriptive analysis and a baseline model
- you switch to a git branch and python scripts once the model is quite stable
- you retrain the model, eventually do some parameter tuning
- you merge your code on the main branch to share your work

If you need to modify the model later (do a different preprocessing, change the model type...), you do not **add** code to the codebase, you **modify** the existing code. This makes unit testing much harder because the desired features changed over time.

The other difficulty when testing machine learning applications is it hard to test for regression, since the model depends on underlying data and the chosen metrics. If a new model performs slightly better or worse than the previous one ont the same dataset, it may be due to randomness and not to code quality. If the metric varies on a different dataset, it is even harder to know if it is due to code quality or to innate randomness.

This is a **cyclic** development process based on a **stochastic** behaviour of the code.

> **Kedro is a very new tool and cannot be called "mature" at this stage but tries to solve this development lifecyle with a very fluent API to create and modify machine learning pipelines.**

## Deployment issues addressed by `kedro-mlflow`

### Out of scope

We will focus on machine learning *development* lifecycle. As a consequence, these items are out of scope:

- Orchestration
- Issues related to infrastructure (the 3 first items of above list: scalability and cost control, speed, disponibility and resilience)

### Issue addressed 1: The training process is poorly reproducible

A ML project contains a lot of moving parts:

- code
- parameters
- data
- environment (packages versions...)
- infrastructure (build on Windows, deploy on linux)

Parameters and data are not moving parts of software traditional development, so the traditional tools to manage software development lifecycle tools are not sufficient to address these problems. The other difficulty is that standard

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
