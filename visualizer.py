import warnings
import trimesh
import tempfile
from jina import Document
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class GlbVisualizer:
    def __init__(self, search_doc, matches=None, plot_matches=True):
        self.search_doc = search_doc
        self.matches = matches
        self.fig = plt.figure()
        self.plot_matches = plot_matches

    def visualize(self):
        try:
            subplot = 221 if self.plot_matches else 111
            self.visualize_3d_object(self.search_doc.uri, subplot, 'Search')
            if self.plot_matches:
                self.visualize_3d_object(self.matches[0].uri, 222, '1st Match')
                self.visualize_3d_object(self.matches[1].uri, 223, '2nd Match')
                self.visualize_3d_object(self.matches[2].uri, 224, '3rd Match')
        except Exception as e:
            warnings.warn(f'Error in visualization: {e}')
        plt.show()

    def visualize_3d_object(self, uri, ax, title):
        doc = Document(uri=uri)
        doc.convert_uri_to_buffer()
        with tempfile.NamedTemporaryFile(
                suffix='.glb', delete=True
        ) as glb_file:
            glb_file.write(doc.content)
            glb_file.flush()
            mesh = trimesh.load(glb_file.name)
            geo = list(mesh.geometry.values())
            mesh = geo[0]
            ax = self.fig.add_subplot(ax, projection='3d')
            ax.plot_trisurf(mesh.vertices[:, 0], mesh.vertices[:, 1],
                            triangles=mesh.faces, Z=mesh.vertices[:, 2])
            ax.set_title(title)