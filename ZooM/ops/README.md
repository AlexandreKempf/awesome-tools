# TLDR

## LOADERS:
  - load_yaml(path, dirname='')
  - load_json(path, dirname='')
  - load_image(path, dirname='')
  - load_text(path, dirname='')

## SAVERS:
  - save_yaml(data, path, dirname='')
  - save_json(data, path, dirname='')
  - save_image(image, mask, path, dirname='')
  - save_text(data, path, dirname='', mode='w')

## IMG_OPS:
  - image_scale(img, low=0, high=1)
  - image_smooth(img, sigma=None)
  - image_pool(img, binsize, binstep=None, fun='mean')

## BATCH_OPS:
