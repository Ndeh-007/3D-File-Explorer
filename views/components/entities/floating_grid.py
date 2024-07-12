import numpy as np
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtCore import QObject
from PySide6.QtCore import QUrl
from PySide6.QtGui import (QMatrix4x4, QVector3D)


class LookAtTransform(Qt3DCore.QTransform):
    def __init__(self, camera: Qt3DRender.QCamera, parent: QObject = None):
        super().__init__(parent)
        self.camera = camera
        self.target = QVector3D(0, 0, 0)
        self.update_rotation()

        self.camera.positionChanged.connect(self.update_rotation)
        self.camera.viewCenterChanged.connect(self.update_rotation)

    def setCameraTransformTarget(self, target: QVector3D):
        self.target = target
        self.update_rotation()

    def update_rotation(self):
        rotation_matrix = self.rotation_matrix_to_normal(self.camera.position())
        self.setMatrix(rotation_matrix)

    @staticmethod
    def rotation_matrix_to_normal(v):
        # Ensure the target vector v is normalized
        v = np.array([v.x(), v.y(), v.z()])
        v = v / np.linalg.norm(v)

        # Original normal of the plane (0, 1, 0)
        n0 = np.array([0, 1, 0])

        # Cross product to get the rotation axis
        k = np.cross(n0, v)
        k_norm = np.linalg.norm(k)

        # If the cross product is zero, it means n0 and v are parallel
        if k_norm == 0:
            if np.dot(n0, v) > 0:
                # Already aligned
                return np.identity(3)
            else:
                # Aligned in opposite direction, rotate 180 degrees around any orthogonal axis
                return np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])

        # Normalize the rotation axis
        k = k / k_norm

        # Dot product to get the cosine of the angle
        cos_theta = np.dot(n0, v)

        # Sine of the angle
        sin_theta = np.sqrt(1 - cos_theta ** 2)

        # Skew-symmetric matrix K
        K = np.array([[0, -k[2], k[1]],
                      [k[2], 0, -k[0]],
                      [-k[1], k[0], 0]])

        # Rodrigues' rotation formula
        R = np.identity(3) + sin_theta * K + (1 - cos_theta) * np.dot(K, K)
        R_Matrix = QMatrix4x4(
            float(R[0][0]), float(R[0][1]), float(R[0][2]), 0.0,
            float(R[1][0]), float(R[1][1]), float(R[1][2]), 0.0,
            float(R[2][0]), float(R[2][1]), float(R[2][2]), 0.0,
            0.0, 0.0, 0.0, 1.0
        )
        return R_Matrix


class FloatingGrid:

    def __init__(self, parentEntity, camera: Qt3DRender.QCamera):
        super().__init__()

        self.parentEntity = parentEntity

        self.vertexData, self.indexData = self.create_triangular_mesh(20, 20)

        # vertex buffer
        self.vertexBuffer = Qt3DCore.QBuffer(self.parentEntity)
        self.vertexBuffer.setData(self.vertexData.tobytes())

        # index buffer
        self.indexBuffer = Qt3DCore.QBuffer(self.parentEntity)
        self.indexBuffer.setData(self.indexData.tobytes())

        # attributes
        self.positionAttribute = Qt3DCore.QAttribute(self.parentEntity)
        self.positionAttribute.setName(Qt3DCore.QAttribute.defaultPositionAttributeName())
        self.positionAttribute.setVertexBaseType(Qt3DCore.QAttribute.VertexBaseType.Float)
        self.positionAttribute.setVertexSize(3)
        self.positionAttribute.setAttributeType(Qt3DCore.QAttribute.AttributeType.VertexAttribute)
        self.positionAttribute.setBuffer(self.vertexBuffer)
        self.positionAttribute.setByteStride(3 * 4)
        self.positionAttribute.setCount(self.vertexData.shape[0])

        self.indexAttribute = Qt3DCore.QAttribute(self.parentEntity)
        self.indexAttribute.setVertexBaseType(Qt3DCore.QAttribute.VertexBaseType.UnsignedInt)
        self.indexAttribute.setAttributeType(Qt3DCore.QAttribute.AttributeType.IndexAttribute)
        self.indexAttribute.setBuffer(self.indexBuffer)
        self.indexAttribute.setCount(self.indexData.shape[0])

        # geometry
        self.geometry = Qt3DCore.QGeometry(self.parentEntity)
        self.geometry.addAttribute(self.positionAttribute)
        self.geometry.addAttribute(self.indexAttribute)

        # Mesh
        # self.mesh = Qt3DRender.QGeometryRenderer(self.parentEntity)
        # self.mesh.setGeometry(self.geometry)
        # self.mesh.setPrimitiveType(Qt3DRender.QGeometryRenderer.PrimitiveType.Triangles)

        # material
        self.material = Qt3DExtras.QPhongMaterial(self.parentEntity)
        # self.material.setDiffuse(Qt.GlobalColor.blue)

        self.mesh = Qt3DRender.QMesh(self.parentEntity)
        self.mesh.setSource(QUrl("qrc:/meshes/grid.obj"))

        # Transform
        self.transform = LookAtTransform(camera, self.parentEntity)

        # Entity
        self.entity = Qt3DCore.QEntity(self.parentEntity)
        self.entity.addComponent(self.mesh)
        self.entity.addComponent(self.material)
        self.entity.addComponent(self.transform)

    def moveTo(self, pos: QVector3D):
        """
        moves the whole grid to the target position
        :param pos:
        :return:
        """
        self.transform.setTranslation(pos)

    @staticmethod
    def create_triangular_mesh(m, n) -> tuple[np.ndarray, np.ndarray]:
        """
        Create a triangular mesh for a rectangle with a grid size of (m, n).

        :param m: Number of rows in the grid.
        :param n: Number of columns in the grid.
        :return: Tuple of vertices and indices.
        """
        # Create vertices
        vertices = []
        for i in range(m + 1):
            for j in range(n + 1):
                vertices.append([i, 0, j])

        # Convert vertices list to numpy array
        vertices = np.array(vertices, dtype=np.float32)
        vertices = vertices.flatten()

        # Create indices
        indices = []
        for i in range(m):
            for j in range(n):
                # Indices of the vertices of the current cell
                v0 = i * (n + 1) + j
                v1 = v0 + 1
                v2 = v0 + (n + 1)
                v3 = v2 + 1

                # Create two triangles for the current cell
                indices.append([v0, v1, v2])
                indices.append([v1, v3, v2])

        # Convert indices list to numpy array
        indices = np.array(indices, dtype=np.uint32)
        indices = indices.flatten()

        return vertices, indices
