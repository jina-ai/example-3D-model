import re
import tempfile
import numpy as np
import inflect
import trimesh

p = inflect.engine()

num_true = 0
num_all = 0

blacklist_prefix = ['sm_', 'mesh_', 'kbd_', 'mod_', 'model_', 'env_']


def get_class(filename):
    filename = filename.replace('%20', ' ')
    norm_file = filename.split('/')[-1].lower().strip().replace('.fbx', '')
    norm_file2 = re.sub(r'\d+', '', norm_file)
    if norm_file2:
        norm_file = norm_file2
    for b in blacklist_prefix:
        norm_file = norm_file.replace(b, '')
    norm_file = norm_file.replace('-', '_').rstrip('_').lstrip('-').lstrip('_')
    norm_file = re.sub(r'_+', '_', norm_file)
    tags = norm_file.split('_')
    final_tags = set()
    for t in tags:
        if len(t) < 3:
            continue
        final_tags.add(t.lower())
    return {p.singular_noun(t) if p.singular_noun(t) else t for t in final_tags}


def get_tags(
        content: bytes,
        uri: str
):
    print(f'in get_tags, getting tags from uri: {uri}')
    mesh = get_mesh(content)
    assert isinstance(mesh, trimesh.Scene)
    k, v = list(mesh.geometry.items())[0]
    v: trimesh.Trimesh

    return {
        'geometry_name': k,
        'mesh_class': list(get_class(uri)),
        'faces': len(v.faces),
        'vertices': len(v.vertices),
        'edges': len(v.edges),
        'triangles': len(v.triangles),
        'glb_path': uri
    }


def get_mesh(content: bytes):
    with tempfile.NamedTemporaryFile(
            suffix='.glb', delete=True
    ) as glb_file:
        glb_file.write(content)
        glb_file.flush()
        mesh = trimesh.load_mesh(glb_file.name)
    #mesh = mesh.deduplicated()
    return mesh
