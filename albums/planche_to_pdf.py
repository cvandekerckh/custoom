from fpdf import FPDF

DOCUMENT_SIZE = (286, 222)
SAFETY = 12.7 # mm
BLEED = 3.18 # mm
LIVE_WIDTH = 254 # mm
LIVE_HEIGHT = 191 # mm
TEXT_HEIGHT = 20 # mm
METRIC = 'mm'
FONT_NAME = 'Arial'
FONT_SIZE = 15
STORY_TEXT = 'Au coeur de la forêt de %(location)s, le cerf remercia %(nickname)s pour son aide'
TEMPLATE_IMG = "lulu_template.jpg"
PLANCHE_IMG = "planche_in.jpg"
ALBUMS_PATH = "albums"

def prepare_template():
    pdf = FPDF('P', METRIC, DOCUMENT_SIZE)
    pdf.add_page()
    pdf.set_font(FONT_NAME, size = FONT_SIZE)
    pdf.set_auto_page_break(False)
    return pdf

def add_planches(pdf, live_start):
    template_file = f"{ALBUMS_PATH}/{TEMPLATE_IMG}"
    planche_file  = f"{ALBUMS_PATH}/{PLANCHE_IMG}"
    pdf.image(
        template_file,
        x=0,
        y=0,
        w=DOCUMENT_SIZE[0],
    )
    pdf.image(
        planche_file,
        x=live_start,
        y=live_start,
        w=LIVE_WIDTH,
    )
    return pdf


def parse_text(variable_dict, story_text):
    return story_text % variable_dict


def add_text(pdf, text, live_start):
    start_text_y = live_start+LIVE_HEIGHT-TEXT_HEIGHT
    pdf.set_xy(live_start, start_text_y)
    pdf.cell(
        LIVE_WIDTH,
        TEXT_HEIGHT,
        text,
        1,
        1,
        'C'
    )
    return pdf


def create_album(variable_dict, album_filename):
    album_file = f"{ALBUMS_PATH}/{album_filename}.pdf"
    live_start = SAFETY+BLEED
    text = parse_text(variable_dict, STORY_TEXT)
    pdf = prepare_template()
    pdf = add_planches(pdf, live_start)
    pdf = add_text(pdf, text, live_start)
    pdf.output(album_file)

