import pytest
from unittest.mock import MagicMock, patch
from app.core.pix import (
    validate_cpf, validate_phone, get_value, formatted_text,
    crc_compute, base64_qrcode, Pix
)


def test_validate_cpf_valid():
    assert validate_cpf("52998224725") is True


def test_validate_cpf_invalid():
    assert validate_cpf("12345678900") is False


def test_validate_phone_valid():
    assert validate_phone("+5511999999999") is True


def test_validate_phone_invalid():
    assert validate_phone("abc123") is False


def test_get_value():
    assert get_value("01", "abc") == "0103abc"


def test_formatted_text():
    assert formatted_text("João É!") == "Joao E"


def test_crc_compute():
    result = crc_compute("000201")
    assert isinstance(result, str)
    assert len(result) == 4


@patch("app.core.pix.BytesIO")
@patch("app.core.pix.base64.b64encode")
def test_base64_qrcode(mock_b64encode, mock_bytesio):
    mock_img = MagicMock()
    mock_buffer = MagicMock()
    mock_bytesio.return_value = mock_buffer
    mock_buffer.getvalue.return_value = b'test'
    mock_b64encode.return_value.decode.return_value = "base64string"

    result = base64_qrcode(mock_img)
    assert result.startswith("data:image/png;base64,")


def test_set_name_receiver_valid():
    pix = Pix()
    pix.set_name_receiver("Cleiton")
    assert pix.name_receiver == "Cleiton"


def test_set_name_receiver_too_long():
    pix = Pix()
    with pytest.raises(ValueError):
        pix.set_name_receiver("A" * 26)


def test_set_city_receiver_valid():
    pix = Pix()
    pix.set_city_receiver("Cariacica")
    assert pix.city_receiver == "Cariacica"


def test_set_city_receiver_too_long():
    pix = Pix()
    with pytest.raises(ValueError):
        pix.set_city_receiver("A" * 16)


def test_set_amount_valid():
    pix = Pix()
    pix.set_amount(1234.56)
    assert pix.amount == "1234.56"


def test_set_amount_too_large():
    pix = Pix()
    with pytest.raises(ValueError):
        pix.set_amount(123456789012.34)


@patch("app.core.pix.validate_cpf", return_value=True)
def test_get_account_information_with_cpf(mock_validate_cpf):
    pix = Pix()
    pix.set_key("52998224725")
    pix.set_name_receiver("Cleiton")
    pix.set_city_receiver("Cariacica")
    info = pix.get_account_information()
    assert "br.gov.bcb.pix" in info
    assert "52998224725" in info


@patch("app.core.pix.validate_phone", return_value=True)
def test_get_account_information_with_phone(mock_validate_phone):
    pix = Pix()
    pix.set_key("11999999999")
    pix.set_name_receiver("Cleiton")
    pix.set_city_receiver("Cariacica")
    info = pix.get_account_information()
    assert "+55" in info


def test_get_account_information_with_url():
    pix = Pix()
    pix.set_default_url_pix("https://example.com")
    pix.set_name_receiver("Cleiton")
    pix.set_city_receiver("Cariacica")
    info = pix.get_account_information()
    assert "example.com" in info


def test_get_br_code():
    pix = Pix()
    pix.set_key("52998224725")
    pix.set_name_receiver("Cleiton")
    pix.set_city_receiver("Cariacica")
    pix.set_amount(100.0)
    br_code = pix.get_br_code()
    assert br_code.startswith("000201")


@patch("app.core.pix.get_qrcode")
@patch("app.core.pix.base64_qrcode")
def test_save_qrcode(mock_base64_qrcode, mock_get_qrcode):
    mock_qr = MagicMock()
    mock_img = MagicMock()
    mock_qr.create_custom_qr.return_value = mock_img
    mock_get_qrcode.return_value = mock_qr
    mock_base64_qrcode.return_value = "base64img"

    pix = Pix()
    pix.set_key("52998224725")
    pix.set_name_receiver("Cleiton")
    pix.set_city_receiver("Cariacica")
    pix.set_amount(100.0)

    result = pix.save_qrcode(output="/tmp/test.png")
    assert result == "base64img"


@patch("app.core.pix.get_qrcode")
def test_qr_ascii(mock_get_qrcode):
    mock_qr = MagicMock()
    mock_qr.print_ascii.return_value = "ASCII"
    mock_get_qrcode.return_value = mock_qr

    pix = Pix()
    pix.qr = mock_qr
    result = pix.qr_ascii()
    assert result == "ASCII"
