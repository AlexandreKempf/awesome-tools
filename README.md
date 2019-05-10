# 🔧 Tools

## Reveal-md ([git](https://github.com/webpro/reveal-md) - [doc](https://github.com/webpro/reveal-md) - [demo](./reveal-md/demo.md))

Build the slides and open it in the default browser:
```bash
reveal-md demo.md --css style.css
```

Build the HTML out of the file:

```bash
reveal-md demo.md --css style.css --static _slides
```
Continue with `decktape` to export to PDF
```bash
cd _slides && decktape reveal main.html test.PDF
```

⚠️ The images on the background are not copied on the `_slides` folder so they need to be add manually ! 
