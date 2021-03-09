
import pytesseract as pt
import pdf2image
import re
import json
import argparse
try:
    from PIL import Image
except ImportError:
    import Image
# Read a pdf file as image pages
# We do not want images to be too big, dpi=200
# All our images should have the same size (depends on dpi), width=1654 and height=2340

def extract_text(filename) :
    pages = pdf2image.convert_from_path(pdf_path=filename, dpi=200, size=(1654,2340))
    # Save all pages as images
    for i in range(len(pages)):
        pages[i].save('pdftoimg-' + str(i) + '.jpg')
    # Convert a page to a string (page 2)
    extracted_text = pt.image_to_string(Image.open('pdftoimg-0.jpg'))

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
    receipt_ocr['items_purchased'] =all_items
    receipt_ocr['Total_Due'] = total



    receipt_json = json.dumps(receipt_ocr,separators=(',',':'), indent=2)
    print(receipt_json)

    jsonFile = open("data.json", "w")
    jsonFile.write(receipt_json)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = vars(parser.parse_args())
    extract_text(args['filename'])
    