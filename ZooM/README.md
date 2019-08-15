# Flows:
 - define by a yaml file:
    - args: []
    - kwargs: {}
    - out: []
    - modules: []
    - flow: [
      {
        - f: load_yaml
        - loop: []
        - args: []
        - kwargs: {}
        - out: []
      },
      .
      .
      .
    ]


 - contains a DAG of Ops and a list of module import
 - should be saved everytime with the last git version of the import
 - integrated with MLflow

# Dataset
 - define by a yaml:
    - root: "path/to/dataset"
    - inputs: ["file", "file", ...]
    - labels: [0, 1, ...]
    - classes: [...]
 - config files should be saved when a Flow runs it

# Ops
 - work with the conventions:
    - img: (row, col, 3) float(0,1)
    - mask: (row, col, 1) float(0,1)
    - batch: (N, )
    - bbox: (top, left, bottom, right)
    - point: (top, left)

 - well documented
