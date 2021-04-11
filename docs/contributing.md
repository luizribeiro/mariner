# Contributing

## Development Environment

If you're interested to help with development, these are rough
instructions on how to build and run everything locally.

The Pi Zero is a bit too slow for development, so I generally build things
on my desktop computer and `git push` them to a git repo the Pi to test.

```
$ poetry install --no-dev
$ cd frontend
$ yarn install
$ yarn build
$ cd ..
$ poetry run mariner
```

Running backend tests:

```
$ poetry green
```

Running frontend tests:

```
$ yarn --cwd frontend test
``
Hellow i need work in other models Like Anycubic Photon Mono, please
