# tap-trustrace

`tap-trustrace` is a Singer tap for trustrace.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install tap-trustrace
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-trustrace --about
```

### Source Authentication and Authorization

You have to provide your own api-key in the settings/config.

## Usage

You can easily run `tap-trustrace` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-trustrace --version
tap-trustrace --help
tap-trustrace --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_trustrace/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-trustrace` CLI interface directly using `poetry run`:

```bash
poetry run tap-trustrace --help
poetry run tap-trustrace --config config.json > out.jsonl
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-trustrace
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-trustrace --version
# OR run a test `elt` pipeline:
meltano elt tap-trustrace target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
