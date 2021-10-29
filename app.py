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
    data_dir = os.path.join(cur_dir, 'toy_data')
    os.environ['JINA_PORT'] = '45678'
    os.environ['WORKSPACE_MOUNT'] = f'{workspace_dir}:/workdir/workspace'
    os.environ['DATA_MOUNT'] = f'{data_dir}:/workspace/toy_data'


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
@click.option('--num_data', '-n', type=int, default=1000)
def main(task, num_data):
    config()
    flow = Flow.load_config('flow.yml')

    if task == 'index':
        with flow:
            flow.post(on='/index', inputs=get_docs(num_data))
    elif task == 'query':
        input_doc = Document(uri='toy_data/laptop_laptop_computer_17.glb')
        with flow:
            results = flow.post(on='/search', return_results=True, inputs=input_doc)
            for index, match in enumerate(results[0].docs[0].matches):
                print(f'Match {index:02d}: {match.uri}')

    elif task == 'query_restful':
        with flow:
            flow.block()


if __name__ == '__main__':
    main()
