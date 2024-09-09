import trimesh
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import random
import os

scene = trimesh.load('sketchuphouse.glb')
mesh = scene.geometry[list(scene.geometry.keys())[0]]
vertices = mesh.vertices
base_points = tf.constant(vertices, dtype=tf.float32)

points = []

for i in range(100):
    try:
        file_txt = open(f"sparse/{i}/points3D.txt", "r").readlines()
        count = 0

        for line in file_txt:
            if count > 2:
                line_list = line.split()
                points.append([float(i) for i in line_list[1:4]])
            else:
                count += 1
    except:
        break

target_points = tf.constant(points, dtype=tf.float32)

def apply_transformations(points, rotation, scale, translation):
    rotation_matrix = tf.stack([
        [tf.cos(rotation[0]) * tf.cos(rotation[1]), tf.cos(rotation[0]) * tf.sin(rotation[1]) * tf.sin(rotation[2]) - tf.sin(rotation[0]) * tf.cos(rotation[2]), tf.cos(rotation[0]) * tf.sin(rotation[1]) * tf.cos(rotation[2]) + tf.sin(rotation[0]) * tf.sin(rotation[2])],
        [tf.sin(rotation[0]) * tf.cos(rotation[1]), tf.sin(rotation[0]) * tf.sin(rotation[1]) * tf.sin(rotation[2]) + tf.cos(rotation[0]) * tf.cos(rotation[2]), tf.sin(rotation[0]) * tf.sin(rotation[1]) * tf.cos(rotation[2]) - tf.cos(rotation[0]) * tf.sin(rotation[2])],
        [-tf.sin(rotation[1]), tf.cos(rotation[1]) * tf.sin(rotation[2]), tf.cos(rotation[1]) * tf.cos(rotation[2])]
    ])
    rotated_points = tf.matmul(points, rotation_matrix)
    scaled_points = rotated_points * scale
    translated_points = scaled_points + translation
    return translated_points

def point_to_line_distance_vectorized(points, line_start, line_end):
    x0, y0, z0 = points[:, 0], points[:, 1], points[:, 2]
    x1, y1, z1 = line_start[0], line_start[1], line_start[2]
    x2, y2, z2 = line_end[0], line_end[1], line_end[2]
    
    line_direction = tf.stack([x2 - x1, y2 - y1, z2 - z1], axis=0)
    point_direction = tf.stack([x0 - x1, y0 - y1, z0 - z1], axis=1)
    projection_length = tf.reduce_sum(point_direction * line_direction, axis=1) / tf.reduce_sum(line_direction ** 2)
    projection_length = tf.clip_by_value(projection_length, 0, 1)
    
    closest_point_x = x1 + projection_length * (x2 - x1)
    closest_point_y = y1 + projection_length * (y2 - y1)
    closest_point_z = z1 + projection_length * (z2 - z1)
    closest_point = tf.stack([closest_point_x, closest_point_y, closest_point_z], axis=1)
    
    distance = tf.norm(points - closest_point, axis=1)
    return distance

def loss_function(transformed_points, target_points):
    distances = []
    for i in range(8):
        line_start = transformed_points[i]
        line_end = transformed_points[(i + 1) % 8]
        distance = point_to_line_distance_vectorized(target_points, line_start, line_end)
        distances.append(distance)
    min_distances = tf.reduce_min(tf.stack(distances, axis=1), axis=1)
    loss = tf.reduce_mean(min_distances)
    return loss

rotation = tf.Variable([0.0, 0.0, 0.0], dtype=tf.float32)
scale = tf.Variable(1.0, dtype=tf.float32)
translation = tf.Variable([0.0, 0.0, 0.0], dtype=tf.float32)

optimizer = tf.optimizers.Adam(learning_rate=0.1)

for step in range(250):
    with tf.GradientTape() as tape:
        transformed_points = apply_transformations(base_points, rotation, scale, translation)
        loss = loss_function(transformed_points, target_points)
    gradients = tape.gradient(loss, [rotation, scale, translation])
    optimizer.apply_gradients(zip(gradients, [rotation, scale, translation]))
    if step % 50 == 0:
        print(f"Step {step}, Loss: {loss.numpy()}")

final_transformed_points = apply_transformations(base_points, rotation, scale, translation)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(base_points[:, 0], base_points[:, 1], base_points[:, 2], c='blue', label='Base Points')
# ax.scatter(target_points[:, 0], target_points[:, 1], target_points[:, 2], c='red', label='Target Points')
ax.scatter(final_transformed_points[:, 0], final_transformed_points[:, 1], final_transformed_points[:, 2], c='green', label='Transformed Points')

for i in range(8):
    ax.plot([final_transformed_points[i, 0], final_transformed_points[(i + 1) % 8, 0]],
            [final_transformed_points[i, 1], final_transformed_points[(i + 1) % 8, 1]],
            [final_transformed_points[i, 2], final_transformed_points[(i + 1) % 8, 2]], c='green')

ax.legend()
ax.set_title('Shape Fitting')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()