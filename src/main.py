import os
import shutil

def move_files(src, dist):
    files = os.listdir(src)

    if not files:
        return

    for file in files:
        if os.path.isfile(os.path.join(src, file)):
            shutil.copy(os.path.join(src, file), os.path.join(dist, file))
        else:
            os.mkdir(os.path.join(dist, file))
            move_files(os.path.join(src, file), os.path.join(dist, file))

def main():
    # static -> public
    this_file = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.abspath(os.path.join(this_file, ".."))

    src_path = os.path.join(root_path, "static") # Static is our 'source'
    dist_path = os.path.join(root_path, "public") # And public is the 'destination'

    if not os.path.exists(src_path):
        os.makedirs(src_path)

    # Delete the destination tree
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)

    os.mkdir(dist_path)
    move_files(src_path, dist_path)

if __name__ == "__main__":
    main()