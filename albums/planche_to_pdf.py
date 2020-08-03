from fpdf import FPDF

DOCUMENT_SIZE = (286, 222)
SAFETY = 12.7 # mm
BLEED = 3.18 # mm

LIVE_WIDTH = 254 # mm
LIVE_HEIGHT = 191 # mm

PAGE_NUMBER_OFF_X = 10
PAGE_NUMBER_OFF_Y = 15
PAGE_NUMBER_WIDTH = 20

PLANCHE_EPS = 0.2  # security in bleeding
PLANCHE_SHIFT_Y = 10  # starting from bleed

TEXT_EPS = 5  # security in safe marging
TEXT_SHIFT_Y = 30  # starting from bleed

TEXT_HEIGHT = 15 # mm
METRIC = 'mm'
FONT_NAME = 'lilly'
FONT_LOCATION = "albums/fonts/lilly/Lilly__.ttf"
FONT_SIZE = 15
TEMPLATE_FILE = "albums/lulu_black.png"
IMG_EXT = "jpg"


def prepare_template():
    pdf = FPDF('P', METRIC, DOCUMENT_SIZE)
    pdf.add_page()  # add blank page at start
    return pdf


def prepare_text_page(pdf):
    pdf.add_font(FONT_NAME, '', FONT_LOCATION,  uni=True)
    pdf.set_font(FONT_NAME, size = FONT_SIZE)
    pdf.set_auto_page_break(False)
    return pdf


def prepare_image_page(pdf, image_file):
    with open(image_file) as f:
        pass
    return pdf


def parse_text(variable_dict, story_text):
    return story_text % variable_dict


def insert_page_number(pdf, page_number):
    page_number_y = DOCUMENT_SIZE[1] - (BLEED + SAFETY + PAGE_NUMBER_OFF_Y)
    page_number_x = BLEED + SAFETY + PAGE_NUMBER_OFF_X
    if (page_number % 2)==1:
        page_number_x = DOCUMENT_SIZE[0] - page_number_x - PAGE_NUMBER_WIDTH
        align = 'R'
    else:
        align = 'L'

    pdf.set_xy(page_number_x, page_number_y)
    pdf.cell(
        PAGE_NUMBER_WIDTH,
        TEXT_HEIGHT,
        f'{page_number}',
        1,
        1,
        align,
    )
    return pdf


def get_centered_start_y(text_width, text):
    test_pdf = FPDF('P', METRIC, DOCUMENT_SIZE)
    test_pdf.add_font(FONT_NAME, '', FONT_LOCATION,  uni=True)
    test_pdf.set_font(FONT_NAME, size = FONT_SIZE)
    test_pdf.set_auto_page_break(False)
    test_pdf.add_page()
    initial_y = test_pdf.get_y()
    test_pdf.multi_cell(
        text_width,
        TEXT_HEIGHT,
        text,
        0,
        'C',
    )
    multi_cell_height = test_pdf.get_y() - initial_y
    start_y = int(round(0.5*(DOCUMENT_SIZE[1] - multi_cell_height)))
    return int(round(0.5*(DOCUMENT_SIZE[1] - multi_cell_height)))


def insert_text(text, pdf, page_number):
    text_width = LIVE_WIDTH - 2*TEXT_EPS
    text_start_x = BLEED + SAFETY + TEXT_EPS
    text_start_y = BLEED + TEXT_SHIFT_Y
    text_start_y = get_centered_start_y(text_width, text)
    pdf.add_page()
    pdf.set_xy(text_start_x, text_start_y)
    pdf.multi_cell(
        text_width,
        TEXT_HEIGHT,
        text,
        0,
        'C',
    )
    #pdf = insert_page_number(pdf, page_number)
    return pdf


def insert_planche(planche_file, pdf, page_number):
    planche_start_x = BLEED - PLANCHE_EPS
    planche_start_y = BLEED + PLANCHE_SHIFT_Y
    image_width = 2*SAFETY + LIVE_WIDTH + 2*PLANCHE_EPS

    pdf.add_page()
    pdf.image(
        TEMPLATE_FILE,
        x=0,
        y=0,
        w=DOCUMENT_SIZE[0],
    )
    pdf.image(
        planche_file,
        x=planche_start_x,
        y=planche_start_y,
        w=image_width,
    )
    #pdf = insert_page_number(pdf, page_number)
    return pdf


def assemble_pdf(parsed_list, albums_path):
    pdf = prepare_template()
    for i, parsed_part in enumerate(parsed_list):
        album_file = f"{albums_path}/{parsed_part[0]}.{IMG_EXT}"
        try:
            pdf = prepare_image_page(pdf, album_file)
            pdf = prepare_text_page(pdf)
            pdf = insert_text(parsed_part[1], pdf, 2*i+2)
            pdf = insert_planche(album_file, pdf, 2*i+3)
        except IOError:
            print(f"File {album_file} not accessible")
    return pdf



def create_album(parsed_list, output_filename, albums_path):
    assert abs(2*BLEED+2*SAFETY+LIVE_WIDTH-DOCUMENT_SIZE[0]) < 1
    assert abs(2*BLEED+2*SAFETY+LIVE_HEIGHT-DOCUMENT_SIZE[1]) < 1
    pdf = assemble_pdf(parsed_list, albums_path)
    pdf.output(f"{output_filename}.pdf")



custom_dict = {
    "location": "Enghien",
    "nickname": "Corentin",
    "friend": "Charlotte",
    "dog": "Sultan",
    "cake": "glace",
    "nickname_gender": "male",
    "friend_gender": "female",
    "cake_gender": "female"
}

