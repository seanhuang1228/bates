"""
Credit: gpt and https://github.com/cpknight/pdfbates/blob/master/pdfbates.py
"""

import os
from pypdf import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from optparse import OptionParser


def create_bates_canvas(page_number, bates_number, tmp_pdf, text):
    # TODO: custom size and position
    c = canvas.Canvas(tmp_pdf, pagesize=letter)
    c.drawString(0.5 * inch, 0.5 * inch,
                 f"{text}{bates_number + page_number}")
    c.save()


def add_bates_number(input_pdf, start_number, output_cnt=1, text="", batch=1):
    input_reader = PdfReader(open(input_pdf, "rb"))
    x, y = input_reader.pages[0].mediabox.upper_right
    num_pages = len(input_reader.pages)

    for i in range(0, output_cnt, batch):
        output_writer = PdfWriter()

        for j in range(i, min(i + batch, output_cnt)):

            tmp_pdf = f"tmp_page_{j}.pdf"
            create_bates_canvas(j, start_number, tmp_pdf, text)

            with open(tmp_pdf, "rb") as tmp_f:
                tmp_reader = PdfReader(tmp_f)
                overlay_page = tmp_reader.pages[0]

                for k in range(num_pages):
                    page = input_reader.pages[k]

                    new_page = PageObject.create_blank_page(
                        width=page.mediabox.width, height=page.mediabox.height)
                    new_page.merge_page(page)
                    new_page.merge_page(overlay_page)

                    output_writer.add_page(new_page)

            os.remove(tmp_pdf)

        fname = input_pdf[:-4]
        output_pdf = f"{fname}_{i}.pdf"
        with open(output_pdf, "wb") as out_f:
            output_writer.write(out_f)


if __name__ == "__main__":
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start", dest="start_number",
                      help="the bates number will start from START",
                      type="int", metavar="START")
    parser.add_option("-n", dest="copies_count",
                      help="make NUMBER of copies",
                      type="int", metavar="NUMBER")
    parser.add_option("-p", "--prefix", dest="prefix",
                      help="put PREFIX before the bates number",
                      metavar="PREFIX")
    parser.add_option("-b", "--batch", dest="batch",
                      help="put BATCH copies in each file",
                      type="int", metavar="BATCH")
    parser.set_defaults(start_number=1000, copies_count=1, prefix="", batch=1)

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        quit()

    input_pdf = args[0]
    start_number = options.start_number
    output_cnt = options.copies_count
    suffix = options.prefix
    batch = options.batch
    add_bates_number(input_pdf, start_number, output_cnt, suffix, batch)
