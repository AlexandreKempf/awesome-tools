# Flows:
 - define by a yaml file
 - contains a DAG of Ops and a list of module import
 - should be saved everytime with the last git version of the import
 - integrated with MLflow
 - possibility of loops

# Dataset
 - define by a yaml, with a list of paths and labels
 - config files should be saved when a Flow runs it

# Ops
 - work with the conventions:
  - img:
  - mask:
  - index:
  - batch:
  - bbox:
  - point:
 - well documented
 -
