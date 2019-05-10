# models

# weights

# datasets
  - a hdf5 file for trainset and a hdf5 file for testset
  - hdf5 file with no `group` and two `datasets` inside : 'inputs' and 'outputs'
  - good practise to add 'title', 'date', 'comment' as attributes

# augmentation
  - yaml format
  - list of operators for augmentation
  ```yaml
    - name: AddGaussianNoise
      sometimes: 0.5
      kwargs:
        sigma: 0.5

    - name: AddWhiteNoise
      sometimes: 0.5
      kwargs:
        range: (0, 10)
  ```

# preprocessing
- yaml format
- list of operators for preprocessing
```yaml
  - name: BlackAndWhite
    kwargs:
      centered: True
```

# target_transform
- yaml format
- list of operators for target_transform
```yaml
  - name: OneHot
    kwargs:
      nb_class: 50
```
