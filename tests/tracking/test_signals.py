import random

import mlflow
from mlflow import signals
from mlflow.tracking.client import MlflowClient


def listen_create_experiment(sender, **kwargs):
    exp_id = kwargs.get('experiment_id')
    exp_name = kwargs.get('name')

    exp = MlflowClient().get_experiment(exp_id)
    assert exp.experiment_id == exp_id
    exp = MlflowClient().get_experiment_by_name(exp_name)
    assert exp.experiment_id == exp_id

def test_signal_experiment():
    signals.create_experiment_signal.connect(listen_create_experiment)
    mlflow.create_experiment(
        "Some random experiment name %d" % random.randint(1, 1e6))
    signals.create_experiment_signal.disconnect(listen_create_experiment)