from fpdf import FPDF
from parse_story import parse_story

DOCUMENT_SIZE = (286, 222)
SAFETY = 12.7 # mm
BLEED = 3.18 # mm
LIVE_WIDTH = 254 # mm
LIVE_HEIGHT = 191 # mm
TEXT_HEIGHT = 15 # mm
METRIC = 'mm'
FONT_NAME = 'Arial'
FONT_SIZE = 15
STORY_TEXT = 'Au coeur de la forêt de %(location)s, le cerf remercia %(nickname)s pour son aide'
TEMPLATE_FILE = "albums/lulu_template.jpg"
IMG_EXT = "jpg"


def prepare_template():
    pdf = FPDF('P', METRIC, DOCUMENT_SIZE)
    return pdf


def prepare_text_page(pdf):
    pdf.set_font(FONT_NAME, size = FONT_SIZE)
    pdf.set_auto_page_break(False)
    return pdf


def prepare_image_page(pdf, image_file):
    with open(image_file) as f:
        pass
    return pdf


def parse_text(variable_dict, story_text):
    return story_text % variable_dict


def insert_text(text, pdf, live_start):
    pdf.add_page()
    start_text_y = live_start+40
    pdf.set_xy(live_start, start_text_y)
    print(text)
    pdf.multi_cell(
        LIVE_WIDTH,
        TEXT_HEIGHT,
        text,
        0,
        'C',
    )
    return pdf


def insert_planche(planche_file, pdf, live_start):
    pdf.add_page()
    pdf.image(
        TEMPLATE_FILE,
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


def assemble_pdf(parsed_list, live_start, albums_path):
    pdf = prepare_template()
    for parsed_part in parsed_list:
        album_file = f"{albums_path}/{parsed_part[0]}.{IMG_EXT}"
        try:
            pdf = prepare_image_page(pdf, album_file)
            pdf = prepare_text_page(pdf)
            pdf = insert_text(parsed_part[1], pdf, live_start)
            pdf = insert_planche(album_file, pdf, live_start)
        except IOError:
            print(f"File {album_file} not accessible")
    return pdf



def create_album(parsed_list, output_file, albums_path):
    live_start = SAFETY+BLEED
    pdf = assemble_pdf(parsed_list, live_start, albums_path)
    pdf.output(output_file)



custom_dict = {
    "location": "Dinant",
    "nickname": "Léa",
    "friend": "Didier",
    "dog": "Patmolle",
    "cake": "glace"
    "nickname_gender": "male",
    "friend_gender": "male",
}

parsed_list = parse_story("albums/histoire.txt", custom_dict)
create_album(parsed_list, "albums/tmp.pdf", "albums/planches")
