import rerun as rr

rr.init("point_cloud", spawn=True)

points = []

for i in range(100):
    try:
        file_txt = open(f"sparse/{i}/points3D.txt", "r").readlines()
        count = 0

        for line in file_txt:
            if count > 2:
                line_list = line.split()
                points.append(line_list[1:7])
            else:
                count += 1
    except:
        break

rr.log(
    'point_cloud',
    rr.Points3D([sublist[:3] for sublist in points], colors=[sublist[3:] for sublist in points], radii=0.1)
)

rr.spawn()