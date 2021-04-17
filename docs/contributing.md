# Contributing

## Development Environment

If you're interested to help with development, these are rough
instructions on how to build and run everything locally.

The Pi Zero is a bit too slow for development, so I generally build things
on my desktop computer and `git push` them to a git repo the Pi to test.

```bash
$ poetry install --no-dev
$ cd frontend
$ yarn install
$ yarn build
$ cd ..
$ poetry run mariner
```

Running backend tests:

```bash
$ poetry green
```

Running frontend tests:

```bash
$ yarn --cwd frontend test
```
