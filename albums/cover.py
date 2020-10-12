from fpdf import FPDF

DOCUMENT_SIZE = (568, 222)
METRIC = "mm"
BLEED = 3.18 # mm
SAFETY = 6.35
SPINE = 3.35

COVER_EPS = 0.2

TEMPLATE_FILE = "albums/cover/lulu_cover_template.png"

COVER_FILE = "albums/cover/cover_v4.png"
COVER_DIMENSION = (3678, 1264)

FONT_NAME = "alepo"
FONT_LOCATION = "albums/fonts/alepo/Alepo.otf"

TITLE = "Le Roi de la forêt"
TEXT_HEIGHT = 15 # mm
FONT_SIZE = 40
TITLE_SHIFT_X = 10
TITLE_SHIFT_Y = 15
NAME_FONT_SIZE = 60
AND_FONT_SIZE = 30
TITLE_FONT_SIZE = 40
TITLE_TEXT_COLOR = (0, 0 ,0)

RESUME_FONT_SIZE = 20
RESUME_EPS = 10
RESUME_SHIFT_X = 60
RESUME_SHIFT_Y = 40
RESUME_WIDTH_RATE = 0.75
RESUME_TEXT_COLOR = (255, 255, 255)

SPINE_FILE = "albums/cover/spine_background.png"


def prepare_cover():
    pdf = FPDF('P', METRIC, DOCUMENT_SIZE)
    pdf.add_font(FONT_NAME, '', FONT_LOCATION,  uni=True)
    pdf.set_font(FONT_NAME, size = FONT_SIZE)
    pdf.set_auto_page_break(False)
    return pdf


def insert_title(pdf, nickname, title):
    r, g, b = TITLE_TEXT_COLOR
    pdf.set_text_color(r, g, b)
    title_x = DOCUMENT_SIZE[0]/2 + BLEED + SAFETY + TITLE_SHIFT_X
    title_y = BLEED + SAFETY + TITLE_SHIFT_Y
    title_list = [nickname, "&", title]
    title_font_sizes = [NAME_FONT_SIZE, AND_FONT_SIZE, TITLE_FONT_SIZE]
    jump = 0
    for title_part, title_font_size in zip(title_list, title_font_sizes):
        pdf.set_font(FONT_NAME, size = title_font_size)
        pdf.set_xy(title_x, title_y + jump)
        pdf.cell(
            0,
            TEXT_HEIGHT,
            title_part,
            0,
            1,
            'C',
        )
        jump = jump + TEXT_HEIGHT
    return pdf



def insert_resume(pdf, parsed_list):
    r, g, b = RESUME_TEXT_COLOR
    pdf.set_text_color(r, g, b)
    text_width = int(RESUME_WIDTH_RATE*(0.5*DOCUMENT_SIZE[0] - 2*BLEED - 2*RESUME_EPS))
    resume_x = BLEED + SAFETY + RESUME_SHIFT_X
    resume_y = BLEED + SAFETY + RESUME_SHIFT_Y
    resume_content = parsed_list[0][1]
    pdf.set_font(FONT_NAME, size = RESUME_FONT_SIZE)
    pdf.set_xy(resume_x, resume_y)
    pdf.multi_cell(
        text_width,
        TEXT_HEIGHT,
        resume_content,
        0,
        'C',
    )
    return pdf


def add_spine(pdf):
    spine_start_x = 0.5*DOCUMENT_SIZE[0] - 0.5*SPINE
    spine_start_y = 0
    pdf.image(
        SPINE_FILE,
        x=spine_start_x,
        y=spine_start_y,
        h=2*DOCUMENT_SIZE[1],
        w=SPINE,
    )
    return pdf

def insert_cover_image(pdf):
    cover_start_y = BLEED-COVER_EPS
    image_height = DOCUMENT_SIZE[1] - 2*BLEED + 2*COVER_EPS
    cover_width = (COVER_DIMENSION[0]/COVER_DIMENSION[1])*image_height
    overlap = DOCUMENT_SIZE[0] - cover_width
    cover_start_x = overlap/2
    pdf.add_page()
    #pdf.image(
    #    TEMPLATE_FILE,
    #    x=0,
    #    y=0,
    #    w=DOCUMENT_SIZE[0],
    #)
    pdf.image(
        COVER_FILE,
        x=cover_start_x,
        y=cover_start_y,
        h=image_height,
    )
    #pdf = insert_page_number(pdf, page_number)
    return pdf


def assemble_cover(parsed_list, nickname):
    pdf = prepare_cover()
    pdf = insert_cover_image(pdf)
    pdf = insert_title(pdf, nickname, TITLE)
    pdf = insert_resume(pdf, parsed_list)
    # pdf = add_spine(pdf)
    return pdf


def create_cover(parsed_list, nickname, output_filename):
    pdf = assemble_cover(parsed_list, nickname)
    pdf.output(f"{output_filename}.pdf")


