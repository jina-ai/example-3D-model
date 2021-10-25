import numpy as np
from jina import Document, DocumentArray, Executor, requests
from jina.logging.logger import JinaLogger

from executors.pn_encoder.pn import get_bottleneck_model


class PNEncoder(Executor):
    def __init__(self, ckpt_path: str, **kwargs):
        super().__init__(**kwargs)
        self.embedding_model = get_bottleneck_model(ckpt_path=ckpt_path)
        self.logger = JinaLogger('pn-encoder')

    @requests(on=['/index', '/search'])
    def encode(self, docs: DocumentArray, **kwargs):
        embeds = self.embedding_model.predict(np.stack(docs.get_attributes('blob')))

        for layer_embeds in embeds:
            for d, b in zip(docs, layer_embeds):
                d.chunks.append(Document(embedding=b))

        # set content to uri to reduce document size
        for d in docs:
            d.uri = d.tags['glb_path']


