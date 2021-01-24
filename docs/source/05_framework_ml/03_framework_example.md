# Framework example

## Introduction

### Pre-requisite

This assumes the user is familiar with Kedro. We will refer to a `kedro>=0.16.5, <0.17.0` project template files (e.g. `catalog.yml`, `pipeline.py` and `hooks.py`).

### Disclaimer

**This is NOT a Kaggle competition. I will not try to create the best model (nor even a _good_ model)** to solve this problem. The goal of this tutorial is to demonstrate how the `pipeline_ml_factory` can help to maintain consistency between training and inference and prepare deployment.

The associated code can be found on github, under [kedro-mlflow-imdb](https://github.com/Galileo-Galilei/kedro-mlflow-imdb) repo.

### Introducing the task and dataset

We will use the [IMDB movie review](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) dataset as an example. This dataset contains 50k movie reviews with associated "positive" or "negative" value manually labelled by a human.

We will train a classifier for binary classification to predict the sentiment associated to a movie review.

You can find [many notebooks on Kaggle](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews/notebooks) to learn more about this dataset.

## Building the project

To understand the division in *etl_app*, *ml_app* and *user_app*, you can refer to ["The components of a machine learning application"](./02_ml_project_components.md).

### The etl_app

We create a very basic `etl_app` for this example. It can be really complex in real life. What matters is that it is composed of two pipelines which produce `instances` and `labels` datasets.

The DAG looks like this:

![etl_app](../imgs/etl_app.png)

Where the "huggingface_split" parameter is just here to define if we should produce "training" or "test" data. We persist the `instances` and `labels` in the DataCatalog for further reuse:

```yaml
# catalog.yml
#### ETL
instances:
  type: pickle.PickleDataSet
  filepath: data/01_raw/instances_${huggingface_split}.pkl

labels:
  type: pickle.PickleDataSet
  filepath: data/01_raw/labels_${huggingface_split}.pkl
```


### The ml_app

Once the instances and labels have been created with the *etl_app*, we can create and launch the machine learning training and inference pipelines. The inference pipeline is the one you will deploy for your end users.

#### A vanilla example: training a machine learning model

The most basic project we can imagine is the following: the business object "instances" is a numeric matrix, and we can directely train a model on it.

The entire pipeline is:

```python
# pipeline.py
def create_ml_pipeline_vanilla(**kwargs):
    """This pipeline is just an example to generate a kedro viz.
    It is NOT intended to be used directly.
    """

    return Pipeline(
        [
            node(
                func=train_model,
                inputs=dict(
                    data="instances", hyperparameters="params:xgb_hyperparameters",
                ),
                outputs="model",
                tags=["training"],
            ),
            node(
                func=predict_with_model,
                inputs=dict(model="model", data="instances"),
                outputs="predictions",
                tags=["inference"],
            ),
        ]
    )
```

with the associated graph:

![ml_pipeline_vanilla](../imgs/ml_pipeline_vanilla.png)

You can **filter the pipeline to separate it between training and inference with efficient node reuse**.

| `pipeline.only_nodes_with_tags("training")`      | `pipeline.only_nodes_with_tags("inference")` |
| ----------- | ----------- |
| ![ml_pipeline_vanilla_training](../imgs/ml_pipeline/vanilla/training.png)| ![ml_pipeline_vanilla_inference](../imgs/ml_pipeline/vanilla/inference.png)|

Running the `training` pipeline will create the model, and if it is persisted in the `catalog.yml` file, youwill be able to run the infrence pipeline.

> This example is nice, but not realistic. It is extremely rare to train a model directly on raw data. It would be convenient to be able to add a preprocessing node, wouldn't it ? This is the purpose of the next session.

#### Sharing preprocessing: text cleaning example

Asssume you want to add an extra preprocessing node before training the model. The previous entire DAG would look like this:

![ml_pipeline_with_preprocessing](../imgs/ml_pipeline/preprocessing/all.png)|


You can once again filter this huge pipeline to separate it between `training` and `inference`. **Since you do not duplicate nodes, this ensure consistency because you are absolutely sure you call the exact same functions** in the two pipelines.

| `pipeline.only_nodes_with_tags("training")`      | `pipeline.only_nodes_with_tags("inference")` |
| ----------- | ----------- |
| ![ml_pipeline_preprocessing_training](../imgs/ml_pipeline/preprocessing/training.png)| ![ml_pipeline_preprocessing_inference](../imgs/ml_pipeline/preprocessing/inference.png)|

You want to serve the entire inference pipleine (extra preprocessing included) to your end users, and this is exactly what we are going to do here!

> Wait! In real life, it is often more complex: preproessing is often not declared manually through a function but also fitted on data
#### Reusing data objects: the example of OneHotEncoder

#### Reusing shared inputs: the example of stopwords

#### Adding some metrics and monitoring

### The user_app

Use `MlflowModelLoggerDataset` to force reading from a given run_id.
