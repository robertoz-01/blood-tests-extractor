# Blood-Tests-Extractor

This tool extracts blood test results from PDF or image files.

It provides an HTTP service that accepts a PDF via a POST request and returns a JSON response containing detailed
information for each analysis result.

In addition to its HTTP service, it can be used locally for experimentation.
In this mode, the tool processes a PDF file and generates an HTML file displaying the extracted tables and debugging information.

The extraction of tables from PDFs or images is powered by the [img2table](https://github.com/xavctn/img2table)
library.

This service is used by [Blood-Tests-App](https://github.com/robertoz-01/blood-tests-app), a web
application for digitalizing, managing, and comparing collections of blood test results.

## Example

From a PDF containing

<kbd> ![Section of a PDF containing a blood test result](docs/input.png) </kbd>

with the HTTP request

```shell
    curl -F file=@examples/input/checkup-2025-01-15.pdf http://localhost:8000/blood-test-pdf | jq
```

you get the JSON response:

```json
[
  {
    "name": "GLOBULI BIANCHI",
    "value": 6.73,
    "unit": "x10^3/μl",
    "reference_lower": 4,
    "reference_upper": 9.5
  },
  {
    "name": "GLOBULI ROSSI",
    "value": 7.22,
    "unit": "x10^6/μl",
    "reference_lower": 4.7,
    "reference_upper": 5.82
  },
  {
    "name": "COLESTEROLO HDL",
    "value": 63,
    "unit": "mg/dl",
    "reference_lower": 40,
    "reference_upper": null
  }
]
```

From the command line, executing
```shell
python -m src.command_line examples/input/checkup-2025-01-15.pdf
```

it generates an HTML containing:

<kbd> ![Section of the output HTML file](docs/html_output.png) </kbd>

## Development

Install the dependencies with:

```shell
poetry install --with development
```

Run an extraction of the analysis tables from a PDF:

1. Copy a PDF with a blood test to `examples/input`
2. Run `source .venv/bin/activate` to use the poetry virtual environment
3. Run `python -m src.command_line examples/input/checkup-123.pdf` (There is an example pdf file in `tests/data/fake-blood-check.pdf`)
4. Look at the generated HTML file(s) in `examples/output` 

Run the tests and coverage with:

```shell
coverage run -m unittest
```

Generate the coverage HTML report with:

```shell
coverage html
```

Run the http server with:

```shell
uvicorn src.http_api.main:app --reload
```

The code is formatted using `black`. Either configure the IDE to use it or run `black src/ tests/`. 

## TODO list
* Recognise the language first. In this way analysis name, decimal numbers, unit measure can be recognized more accurately.
* Recognise the type of column through machine learning instead of using the fixed `AnalysisTable.CONFIDENCE_THRESHOLD` 