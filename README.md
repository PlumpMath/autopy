Python packaging without the boilerplate

`autopy` is a layer on top of setuptools that infers as much as possible
from the directory layout, avoiding boilerplate. No need for a
`setup.py`, `long_description` is pulled from the README automatically,
and some other nice things.

# Invocation

Just call `autopy` with the arguments you would normally pass to
setup.py:

    autopy build
    autopy install
    ...

You can use autopy to manage itself, without having already installed
it:

    python autopy.py build
    python autopy.py install
    ...

# License

MIT.

# Roadmap

This is still very WIP. Documentation about exactly what is inferred and
how will be forthcoming.
