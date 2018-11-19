from functools import wraps

from blinker import NamedSignal


class Signal(NamedSignal):

    def __init__(self, name, providing_args, doc=None):
        self.providing_args = providing_args
        self.signal_name = name
        super(Signal, self).__init__(name, doc)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            ret = func(*args, **kwargs)
            func_args = self._get_providing_args(*args, **kwargs)
            self.send(self.signal_name, **func_args)
            return ret
        return wrapped

    def _get_providing_args(self, *args, **kwargs):
        pos_args = args[1:] if args else []
        func_args = {}
        for arg, name in zip(pos_args, self.providing_args):
            func_args[name] = arg
        func_args.update(kwargs)
        print func_args
        return func_args

# - Experiment
create_experiment_signal = Signal(
    name='create-experiment',
    providing_args=('name', 'artifact_location'),
    doc="Post run signal for MlflowClient.create_experiment")

delete_experiment_signal = Signal(
    name='delete-experiment',
    providing_args=('experiment_id'),
    doc="Post run signal for MlflowClient.delete_experiment")

restore_experiment_signal = Signal(
    name='restore-experiment',
    providing_args=('experiment_id'),
    doc="Post run signal for MlflowClient.restore_experiment")

rename_experiment_signal = Signal(
    name='rename-experiment',
    providing_args=('experiment_id', 'new_name'),
    doc="Post run signal for MlflowClient.rename_experiment")

# - Run
create_run_signal = Signal(
    name='create-run',
    providing_args=('experiment_id', 'user_id', 'run_name', 'source_type',
                   'source_name', 'entry_point_name', 'start_time',
                   'source_version', 'tags', 'parent_run_id'),
    doc="Post run signal for MlflowClient.create_run")

set_terminated_signal = Signal(
    name='set-terminated',
    providing_args=('run_id', 'status', 'end_time'),
    doc="Post run signal for MlflowClient.set_terminated")

delete_run_signal = Signal(
    name='delete-run',
    providing_args=('run_id'),
    doc="Post run signal for MlflowClient.delete_run")

restore_run_signal = Signal(
    name='restore-run',
    providing_args=('run_id'),
    doc="Post run signal for MlflowClient.restore_run")

# - Run Logging
log_metric_signal = Signal(
    name='log-metric',
    providing_args=('run_id', 'key', 'value', 'timestamp'),
    doc="Post run signal for MlflowClient.log_metric")

log_param_signal = Signal(
    name='log-param',
    providing_args=('run_id', 'key', 'value'),
    doc="Post run signal for MlflowClient.log_param")

set_tag_signal = Signal(
    name='set-tag',
    providing_args=('run_id', 'key', 'value'),
    doc="Post run signal for MlflowClient.set_tag")

log_artifact_signal = Signal(
    name='log-artifact',
    providing_args=('run_id', 'local_path', 'artifact_path'),
    doc="Post run signal for MlflowClient.log_artifact")

log_artifacts_signal = Signal(
    name='log-artifacts',
    providing_args=('run_id', 'local_dir', 'artifact_path'),
    doc="Post run signal for MlflowClient.log_artifacts")
