import base64
import logging
import re
from binascii import crc_hqx
from io import BytesIO
from unicodedata import normalize

from pix_app.core.qrgen import (
    Generator,
    add_center_gif
)

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def validate_cpf(numbers):
    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False
    for i in range(9, 11):
        value = sum(cpf[num] * ((i + 1) - num) for num in range(0, i))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def validate_phone(value):
    rule = re.compile(r"^\+?[1-9]\d{1,14}$")
    return bool(rule.match(value))


def get_value(identify, value):
    return f"{identify}{str(len(value)).zfill(2)}{value}"


def formatted_text(value):
    return re.sub(
        r"[^A-Za-z0-9$@%*+\-./:_ ]",
        "",
        normalize("NFD", value).encode("ascii", "ignore").decode("ascii"),
    )


def crc_compute(hex_string):
    msg = bytes(hex_string, "utf-8")
    crc = crc_hqx(msg, 0xFFFF)
    return f"{crc & 0xffff:04X}"


def get_qrcode():
    qr_generator = Generator()
    return qr_generator


def base64_qrcode(img, output, frames=None, duration=None):
    img_buffer = BytesIO()
    extension = "png"

    if frames:
        extension = "gif"
        for mode in [img_buffer, output]:
            frames[0].save(
                mode,
                save_all=True,
                format=extension.upper(),
                append_images=frames[1:],
                duration=duration,
                loop=0
            )
    else:
        img.save(img_buffer, format=extension.upper())
        img.save(output, format=extension.upper())

    img_buffer.seek(0)
    res = img_buffer.read()
    img_buffer.close()

    data_string = base64.b64encode(res).decode()
    return f"data:image/{extension};base64,{data_string}"


class Pix:

    def __init__(self):
        self.single_transaction = False
        self.key = None
        self.name_receiver = None
        self.city_receiver = None
        self.amount = 0.0
        self.zipcode_receiver = None
        self.identification = None
        self.description = None
        self.default_url_pix = None
        self.qr = None

    def set_default_url_pix(self, default_url_pix=None):
        self.default_url_pix = (
            default_url_pix.replace("https://", "") if default_url_pix else None
        )

    def set_key(self, key=None):
        self.key = key

    def set_zipcode_receiver(self, zipcode=None):
        self.zipcode_receiver = zipcode

    def set_name_receiver(self, name=None):
        if len(name) > 25:
            raise ValueError(
                "The maximum number of characters for the receiver name is 25."
            )
        self.name_receiver = name

    def set_identification(self, identification=None):
        self.identification = identification

    def set_description(self, description=None):
        self.description = description

    def set_city_receiver(self, city=None):
        if len(city) > 15:
            raise ValueError(
                "The maximum number of characters for the receiver city is 15."
            )
        self.city_receiver = city

    def set_amount(self, value=None):
        if len(str(f"{value:.2f}")) > 13:
            raise ValueError("The maximum number of characters for the value is 13.")
        self.amount = f"{value:.2f}"

    def is_single_transaction(self, single_transaction=None):
        self.single_transaction = single_transaction

    def get_br_code(self):
        result_string = (
            f"{get_value('00', '01')}"
            f"{get_value('01', '12' if self.single_transaction else '11')}"
            f"{self.get_account_information()}"
            f"{get_value('52', '0000')}"
            f"{get_value('53', '986')}"
            f"{get_value('54', str(self.amount)) if self.key else ''}"
            f"{get_value('58', 'BR')}"
            f"{get_value('59', formatted_text(self.name_receiver))}"
            f"{get_value('60', formatted_text(self.city_receiver))}"
            f"{get_value('61', formatted_text(self.zipcode_receiver)) if self.zipcode_receiver else ''}"
            f"{self.get_additional_data_field()}"
            f"6304"
        )
        return result_string + crc_compute(result_string)

    def get_account_information(self):
        base_pix = get_value("00", "br.gov.bcb.pix")
        info_string = ""
        if self.key:
            if len(self.key) == 11 and validate_cpf(self.key):
                self.key = self.key
            elif validate_phone(self.key):
                self.key = (
                    f"+55{self.key}" if not self.key.startswith("+55") else self.key
                )
            info_string += get_value("01", self.key)
        elif self.default_url_pix:
            info_string += get_value("25", self.default_url_pix)
        else:
            raise ValueError("You must enter a URL or a pix key.")
        if self.description:
            info_string += get_value("02", formatted_text(self.description))
        return get_value("26", f"{base_pix}{info_string}")

    def get_additional_data_field(self):
        if self.identification:
            return get_value("62", get_value("05", formatted_text(self.identification)))
        return get_value("62", get_value("05", "***"))

    def save_qrcode(
            self,
            output="./qrcode.png",
            box_size=7,
            border=1,
            custom_logo=None,
            **kwargs
    ):
        try:
            frames, duration, gif_logo = [], 100, None
            self.qr = get_qrcode()
            if custom_logo.endswith(".gif"):
                gif_logo = custom_logo
                custom_logo = None

            qr_img = self.qr.create_custom_qr(
                self.get_br_code(),
                size=box_size,
                border=border,
                center_image=custom_logo,
                **kwargs,
            )

            if gif_logo:
                output = output.replace(".png", ".gif")
                frames, duration = add_center_gif(
                    qr_img,
                    gif_logo,
                    gif_len_percent=1.15,
                    radius=2
                )

            return base64_qrcode(qr_img, output, frames=frames, duration=duration)
        except ValueError as e:
            logger.error(f"Error saving QR Code: {e}")
            return False

    def qr_ascii(self):
        return self.qr.print_ascii()
