from typing import Optional

from jina import Document, DocumentArray, Executor, requests
from jina.logging.logger import JinaLogger
import trimesh
import copy
import numpy as np

from executors.glb_crafter.utils import get_tags, get_mesh


class GlbCrafter(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = JinaLogger('glb_crafter')

    def sample(self, content, doc_id):
        mesh = get_mesh(content)
        if not isinstance(mesh, trimesh.Scene):
            raise TypeError('mesh is of unsupported type')
        geo = list(mesh.geometry.values())
        if not geo:
            raise ValueError(f'Doc id: {doc_id}''s mesh does not have any geometry objects')
        if len(geo) > 1:
            self.logger.info(f'Doc id: {doc_id} mesh has {len(geo)} geometry object; get the first one in the '
                             'glb file')
        return geo[0].sample(2048)

    @requests(on=['/index', '/search'])
    def craft(self, docs: Optional[DocumentArray] = None, **kwargs):
        if not docs:
            return

        for d in docs:
            d: Document
            assert d.uri != '' or d.blob is not None, f'uri and blob are both empty, doc: {d}'
            if d.blob is not None:
                self.logger.info(f'query already has blob, obtained from path: {d.tags["glb_path"]}')
                continue
            uri = d.uri
            self.logger.info(f'retrieving doc from uri: {uri}')
            d.convert_uri_to_buffer()  # convert to buffer because if uri is remote we need to download
            d.tags = get_tags(d.content, uri)
            d.blob = self.sample(d.content, d.id)
            self.logger.info(f'd.blob length: {len(d.blob)}')
        self.logger.info('done')
