from parse_story import parse_story
from planche_to_pdf import create_album

MALE = "male"
FEMALE = "female"


output_filename = "albums/test"
albums_path = "albums/planches"
custom_dict = {
    "location": "Jambes",
    "nickname": "Léa",
    "friend": "Alexandre",
    "dog": "Eva",
    "cake": "mousse au chocolat",
    "nickname_gender": FEMALE,
    "friend_gender": MALE,
    "cake_gender": FEMALE,
}

parsed_list = parse_story(custom_dict)
create_album(parsed_list, output_filename, albums_path)
