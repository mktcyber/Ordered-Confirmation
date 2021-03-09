import pytesseract as pt
import pdf2image
import re
try:
    from PIL import Image
except ImportError:
    import Image


def extract_text_as_dict(file_name):
    pages = pdf2image.convert_from_path(pdf_path=file_name, dpi=200, size=(1654,2340))
    assert len(pages) == 1
    pages[0].save('sample.jpg')
    extracted_text = pt.image_to_string(Image.open('sample.jpg'))

    receipt_ocr = {}
    splits = extracted_text.splitlines()
    #getting the company name
    company_name = splits[0]  
    receipt_ocr['company_name'] =company_name

    #getting the invoice number
    invoice_number = splits[16]
    y = invoice_number.split(' #')
    receipt_ocr['invoice_number'] = y[-1]

    # regex for date. The pattern in the receipt is in 30.07.2007 in DD:MM:YYYY
    date_pattern = r'20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])'
    date = re.search(date_pattern, extracted_text).group()
    receipt_ocr['invoice_date'] = date
    # print(date)

    # get lines with chf
    lines_with_chf = []
    for line in splits:
        if re.search(r'CHF',line):
            lines_with_chf.append(line)

    items = []
    for line in lines_with_chf:
        if re.search(r'SUBTOTAL',line):
            continue
        if re.search(r'SALES',line):
            continue
        if re.search(r'TOTAL DUE',line):
            continue
        else:
            items.append(line)

    # Get Name, quantity and ucost utotal cost 
    all_items = {}
    for item in items:
        details = item.split()
        quantity = details[0]
        quantity_description = details[1]
        unit_price = details[-3]
        UTotal = details[-1]
        all_items[quantity_description] = {'quantity':quantity, 'ucost':unit_price, 'UTotal':UTotal}
    #getting the total
    last_line = lines_with_chf[-1].split(' ')
    total = last_line[-1]
    # Store the results in the dict
    receipt_ocr['items_purchased'] = all_items
    receipt_ocr['Total_Due'] = total

    return receipt_ocr