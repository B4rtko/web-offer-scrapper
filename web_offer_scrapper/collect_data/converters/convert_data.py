import re
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, Union

from unidecode import unidecode

from web_offer_scrapper.collect_data.scrap_handlers.config import offer_fields_config

from ..database_utils import config as database_fields_config


def try_exception(arg: Union[Callable, int]) -> Callable:
    """
    Decorator or decorator factory function for returning desired number of None values in case of any exceptino

    :param arg: number of None values to return - default is 1
    :raises Exception: when the argument is not a callable nor integer
    :return: wrapped function that returns normal result if no exceptions occured or tuple with desired
    number of None values
    """
    if isinstance(arg, int):
        num_return_nans = arg
    elif callable(arg):
        num_return_nans = 1
    else:
        raise Exception(
            f"try_exception decorator is meant to be used without argument or with 1 int argument, not {arg}"
        )

    def decorator_func(foo):
        @wraps(foo)
        def wrapped_func(*args, **kwargs):
            try:
                return foo(*args, **kwargs)
            except Exception:
                if num_return_nans == 1:
                    return None
                else:
                    return tuple(None for _ in range(num_return_nans))

        return wrapped_func

    if callable(arg):
        return decorator_func(arg)
    else:
        return decorator_func


class Converter:
    dictionary: Dict[str, Any]

    def __init__(self, dictionary: Dict):
        self.dictionary: Dict[str, Any] = dictionary
        self._converted_dictionary: Dict[str, Any]
        self._converted = False

    @property
    def converted(self) -> bool:
        return self._converted

    @property
    def converted_dictionary(self) -> Dict[str, Any]:
        if not self._converted:
            self.convert_all()
        return self._converted_dictionary.copy()

    def convert_all(self) -> Dict:
        price_converted = self.convert_price(offer_fields_config.price.data_name)
        address_street, address_estate, address_district, address_city, address_province = self.convert_address()
        surface_converted = self.convert_surface()
        building_ownership_converted = self.replace_polish_char_and_whitespaces(
            offer_fields_config.building_ownership.data_name
        )
        rooms_converted = self.convert_str_to_number(offer_fields_config.rooms.data_name)
        construction_status_converted = self.replace_polish_char_and_whitespaces(
            offer_fields_config.construction_status.data_name
        )
        floor, floors_in_building = self.convert_floor_attribute()
        outdoor_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.outdoor.data_name)
        rent_converted = self.convert_price(offer_fields_config.rent.data_name)
        parking_space_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.parking_space.data_name)
        heating_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.heating.data_name)
        market_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.market.data_name)
        advertiser_type_converted = self.replace_polish_char_and_whitespaces(
            offer_fields_config.advertiser_type.data_name
        )
        free_from_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.free_from.data_name)
        build_year_converted = self.convert_str_to_number(offer_fields_config.build_year.data_name)
        building_type_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.building_type.data_name)
        windows_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.windows.data_name)
        lift_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.lift.data_name)
        media_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.media.data_name)
        securities_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.securities.data_name)
        equipment_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.equipment.data_name)
        extra_info_converted = self.replace_polish_char_and_whitespaces(offer_fields_config.extra_info.data_name)
        building_material_converted = self.replace_polish_char_and_whitespaces(
            offer_fields_config.building_material.data_name
        )

        self._converted_dictionary = {
            database_fields_config.price.db_name: price_converted,
            database_fields_config.address_street.db_name: address_street,
            database_fields_config.address_estate.db_name: address_estate,
            database_fields_config.address_district.db_name: address_district,
            database_fields_config.address_city.db_name: address_city,
            database_fields_config.address_province.db_name: address_province,
            database_fields_config.surface.db_name: surface_converted,
            database_fields_config.building_ownership.db_name: building_ownership_converted,
            database_fields_config.rooms.db_name: rooms_converted,
            database_fields_config.construction_status.db_name: construction_status_converted,
            database_fields_config.floor.db_name: floor,
            database_fields_config.floors_in_building.db_name: floors_in_building,
            database_fields_config.outdoor.db_name: outdoor_converted,
            database_fields_config.rent.db_name: rent_converted,
            database_fields_config.parking_space.db_name: parking_space_converted,
            database_fields_config.heating.db_name: heating_converted,
            database_fields_config.market.db_name: market_converted,
            database_fields_config.advertiser_type.db_name: advertiser_type_converted,
            database_fields_config.free_from.db_name: free_from_converted,
            database_fields_config.build_year.db_name: build_year_converted,
            database_fields_config.building_type.db_name: building_type_converted,
            database_fields_config.windows.db_name: windows_converted,
            database_fields_config.lift.db_name: lift_converted,
            database_fields_config.media.db_name: media_converted,
            database_fields_config.securities.db_name: securities_converted,
            database_fields_config.equipment.db_name: equipment_converted,
            database_fields_config.extra_info.db_name: extra_info_converted,
            database_fields_config.building_material.db_name: building_material_converted,
            database_fields_config.link_id.db_name: self.dictionary.get(offer_fields_config.link_id.data_name),
            database_fields_config.description.db_name: self.dictionary.get(offer_fields_config.description.data_name),
        }
        self._converted = True
        return self.converted_dictionary

    @try_exception
    def replace_polish_char_and_whitespaces(self, text: str) -> Optional[str]:
        text_from_directory = self.dictionary.get(text)
        ascii_text = unidecode(text_from_directory)

        result_text: Optional[str]
        # Remove all whitespaces
        result_text = re.sub(r"\s+", "_", ascii_text)
        # replace slash with underscore
        result_text = re.sub(r"_{2,}", "_", result_text.replace("/", "_"))
        if result_text == "brak_informacji":
            result_text = None
        return result_text

    @try_exception
    def convert_price(self, feature: str) -> Optional[int]:
        #  Remove spaces and the currency symbol
        price = self.dictionary.get(feature)
        assert isinstance(price, str)

        return int(re.sub(r"[^0-9]", "", price))

    @try_exception(5)
    def convert_address(self) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
        # Divide into separate parts that creates address from the link
        address = self.dictionary.get(offer_fields_config.address.data_name)
        list_of_address_elements = unidecode(address).split(", ")
        if len(list_of_address_elements) != 5:
            address_street = None
        else:
            address_street = list_of_address_elements[0]
            list_of_address_elements.pop(0)

        address_estate, address_district, address_city, address_province = list_of_address_elements

        return address_street, address_estate, address_district, address_city, address_province

    @try_exception
    def convert_surface(self) -> Optional[float]:
        # Remove unit and convert number to float value
        surface = self.dictionary.get(offer_fields_config.surface.data_name)
        assert isinstance(surface, str)

        numeric_text = re.sub(r"[^\d,]", "", surface)
        return float(numeric_text.replace(",", "."))

    @try_exception
    def convert_str_to_number(self, feature: str) -> Optional[int]:
        dict_result = self.dictionary.get(feature)
        assert isinstance(dict_result, str)

        return int(dict_result)

    @try_exception(2)
    def convert_floor_attribute(self) -> Tuple[Optional[int], Optional[int]]:
        floor = self.dictionary.get(offer_fields_config.floor.data_name)
        assert isinstance(floor, str)

        apartment_floor, floors = floor.split("/")
        return int(apartment_floor), int(floors)


findings = {
    "cena": "480 000 zł",
    "adres": "ul. Królewiecka, Maślice, Fabryczna, Wrocław, dolnośląskie",
    # 'adres' : 'Stare Miasto, Stare Miasto, Wrocław, dolnośląskie',
    "powierzchnia": "36,77 m²",
    "forma_wlasnosci": "pełna własność",
    "liczba_pokoi": "2 ",
    "stan_wykonczenia": "do wykończenia",
    "pietro": "1/3",
    "balkon_ogrod_taras": "balkon",
    "czynsz": None,
    "miejsce_parkingowe": "garaż/miejsce parkingowe",
    "ogrzewanie": None,
    "rynek": "pierwotny",
    "typ_ogloszeniodawcy": "prywatny",
    "dostepne_od": "brak informacji",
    "rok_budowy": "2024",
    "rodzaj_zabudowy": "blok",
    "okna": "plastikowe",
    "winda": "tak",
    "media": "brak informacji",
    "zabezpieczenia": "domofon / wideofon",
    "wyposazenie": "brak informacji",
    "informacje_dodatkowe": "brak informacji",
    "material_budynku": "silikat",
    "link_id": "2998347",
}
