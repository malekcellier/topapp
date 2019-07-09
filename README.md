# topapp
Topology App to try out Qt related ideas

The app is made of a backend called Topology located in app/ and a TopologyGui located in gui/

The purpose is to use the dummy Topology model to create an Qt based gui that allows to edit and interact with the model.


Run the gui by issuing the command:

``
python gui/gui.py
``

## Coding style

### Pre-Commit
The Docker container comes with [pre-commit](https://pre-commit.com/) installed.
pre-commit is a pre-commit framework which can be attached as git hook. It
runs code-formatting and other checks automatically before committing any code.
You just need to install with:

```bash
pre-commit install
pre-commit autoupdate
```

### Python

For Python we can use [black](https://github.com/ambv/black):

```bash
black -S .
```

**NOTE:** The `-S` parameter prevents black from changing quotes.
