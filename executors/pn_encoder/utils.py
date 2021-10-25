import tempfile

import trimesh


def get_mesh(content: bytes):
    with tempfile.NamedTemporaryFile(
            suffix='.glb', delete=False
    ) as glb_file:
        glb_file.write(content)
        glb_file.flush()
        mesh = trimesh.load_mesh(glb_file.name)
    mesh = mesh.deduplicated()
    return mesh
