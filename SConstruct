import os

env = Environment()

def add(in_name, out_name):
    env.Command(out_name, in_name, [
        'openscad -o %s %s' % (out_name, in_name)
    ])


for name in os.listdir('scad'):
    if not name.endswith('.scad'):
        continue
    base = name[:-5]

    add(f'scad/{name}', f'stls/{base}.stl')


