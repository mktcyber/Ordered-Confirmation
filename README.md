# Order Confirmation
A document (mainly invoice) reader that maps generated fields to JSON, or XML Format.

## How
This program accepts files in PDF Format, only, which is then converted to an image file for the embedded OCR Reader to read the text therefrom.
Data fields are generated using strictly "rule-based" approach.
The generated data is then translated into JSON, or XML Format as required.

## Use / Run
Firstly, install all requirements, as in the requirements.txt file, by using the command: ```pip install -r requirements.txt```

Then run: ```python3 main.py -i {input_file.pdf} -o {output_format=[JSON/XML]}```
Where {input_file.pdf} is the absolute path of the PDF file; and {output_format} is the format of the generated output - either in JSON or XML.

Either invoice.json, or invoice.xml will be generated containing the data-fields in JSON, or XML Format.

## Drawbacks
1. Uses strictly rule-based approach for data-mapping
2. May fail with documents that uses format other than the given sample.pdf file