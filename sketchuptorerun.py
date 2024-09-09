import rerun as rr

def run(path):
    rr.init('Sketchup To Rerun', spawn=True)

    # rr.log_file_from_path(r"C:\Users\noahv\OneDrive\Documents\backintime\sketchuphouse.glb")
    rr.log("world", rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)
    rr.log("world/asset", rr.Asset3D(path=path))
    # rr.log_file_from_contents('Sketchup To Rerun', 'sketchuphouse.glb')

    rr.spawn()

run('sketchuphouse.glb')