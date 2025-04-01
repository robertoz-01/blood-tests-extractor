# Blood-Tests-Extractor

It extracts tables containing blood test results from PDF or image files.

It can be used as an HTTP service. For example:

```shell
curl ...
```

## Usage

Run the HTTP service with: ...

## Development

Install the dependencies with:

```shell
poetry install --with experiments
```

Run an extraction of the analysis tables from a PDF:

1. Copy a PDF with a blood test to `examples/input`
2. Run `source .venv/bin/activate` to use the poetry virtual environment
3. Run `python -m src.extract_table`
4. Look at the generated HTML file(s) in `examples/output` 


## TODO
* Recognise the language first. In this way analysis name, decimal numbers, unit measure can be recognized more accurately.
* Recognise the type of column through machine learning instead of using the fixed `AnalysisTable.CONFIDENCE_THRESHOLD` 