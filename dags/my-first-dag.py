from datetime import datetime

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

namespace = conf.get('kubernetes', 'NAMESPACE')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

dag = DAG('my_sample_dag', default_args=default_args, schedule=None)

with dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="alayahamza/batch:1.0.0",
        env_vars={
            'greetings': "{{dag_run.conf['greetings']}}"
        },
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=False,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        kubernetes_conn_id="kubernetes-docker-desktop",
        is_delete_operator_pod=True,
        get_logs=True,
    )
