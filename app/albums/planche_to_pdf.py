from fpdf import FPDF

DOCUMENT_SIZE = (286, 222)
SAFETY = 12.7 # mm
BLEED = 3.18 # mm
LIVE_WIDTH = 254 # mm
LIVE_HEIGHT = 191 # mm
TEXT_HEIGHT = 20 # mm

# save FPDF() class into a
# variable pdf
pdf = FPDF('P', 'mm', DOCUMENT_SIZE)

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size = 15)
pdf.set_auto_page_break(False)

# add image
live_start = SAFETY+BLEED
pdf.image(
    "template.jpg",
    x=0,
    y=0,
    w=DOCUMENT_SIZE[0],
)
pdf.image(
    "planche_2.jpg",
    x=live_start,
    y=live_start,
    w=LIVE_WIDTH,
)

# add text
# Move to to the right
start_text_y = live_start+LIVE_HEIGHT-TEXT_HEIGHT
pdf.set_xy(live_start, start_text_y)
# Centered text in a framed 20*10 mm cell and line break
pdf.cell(LIVE_WIDTH, TEXT_HEIGHT, "C'est alors que le cerf les remercia pour leur aide. Il inclina la tête en guise de remerciement", 1, 1, 'C')

# save the pdf with name .pdf
pdf.output("planche_out.pdf")
