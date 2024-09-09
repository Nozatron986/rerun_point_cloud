import trimesh
import matplotlib.pyplot as plt

obj = trimesh.load('sketchuphouse1.glb', force='mesh', process=False)

vertices = obj.vertices

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='b', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()