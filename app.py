import os
import random

import click
from jina import Flow, Document, DocumentArray
from jina.logging.logger import JinaLogger
import requests

logger = JinaLogger('3d-showcase')


def config():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.join(cur_dir, 'workspace')
    os.environ['JINA_PORT'] = '45678'
    os.environ['WORKSPACE_MOUNT'] = f'{workspace_dir}:/workdir/workspace'


def get_docs(num_docs):
    file_url = 'https://storage.googleapis.com/showcase-3d-models/{0}'
    list_url = 'https://storage.googleapis.com/storage/v1/b/showcase-3d-models/o'
    data = requests.get(list_url).json()
    random.shuffle(data['items'])
    objects = data['items'][:num_docs]
    docs = DocumentArray(
        [Document(uri=file_url.format(obj['name'].replace(' ', '%20'))) for obj
         in objects])
    return docs


@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'query', 'query_restful']))
def main(task):
    config()
    num_docs = 1000
    flow = Flow.load_config('flow.yml')

    if task == 'index':
        with flow:
            flow.post(on='/index', inputs=get_docs(num_docs))


if __name__ == '__main__':
    main()
