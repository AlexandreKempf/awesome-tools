# Organization of a dataset:
  - root:
    - path/to/dataset
  - inputs:
    - 'id1.png'
    - 'id3.png'
  - labels:
    - 'id1': 0
    - 'id2': 2
    - 'id3': 1
  - classes:
    - "tiger"
    - "cat"
    - "house"
  - pipeline:
    - {"f": "load_img"
       "args": inputs
       "kwargs": {}
       "out": inputs}
