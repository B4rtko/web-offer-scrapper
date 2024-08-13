from dataclasses import dataclass
from typing import Optional


@dataclass
class FieldConfig:
    data_name: str
    html_name: Optional[str] = None


class OfferTabularFieldsConfig:
    price: FieldConfig = FieldConfig(data_name="cena")
    address: FieldConfig = FieldConfig(data_name="adres")
    description: FieldConfig = FieldConfig(data_name="opis")
    surface: FieldConfig = FieldConfig(data_name="powierzchnia", html_name="table-value-area")
    building_ownership: FieldConfig = FieldConfig(
        data_name="forma_wlasnosci", html_name="table-value-building_ownership"
    )
    rooms: FieldConfig = FieldConfig(data_name="liczba_pokoi", html_name="table-value-rooms_num")
    floor: FieldConfig = FieldConfig(data_name="pietro", html_name="table-value-floor")
    construction_status: FieldConfig = FieldConfig(
        data_name="stan_wykonczenia", html_name="table-value-construction_status"
    )
    outdoor: FieldConfig = FieldConfig(data_name="balkon_ogrod_taras", html_name="table-value-outdoor")
    rent: FieldConfig = FieldConfig(data_name="czynsz", html_name="table-value-rent")
    parking_space: FieldConfig = FieldConfig(data_name="miejsce_parkingowe", html_name="table-value-car")
    heating: FieldConfig = FieldConfig(data_name="ogrzewanie", html_name="table-value-heating")
    market: FieldConfig = FieldConfig(data_name="rynek", html_name="table-value-market")
    advertiser_type: FieldConfig = FieldConfig(data_name="typ_ogloszeniodawcy", html_name="table-value-advertiser_type")
    free_from: FieldConfig = FieldConfig(data_name="dostepne_od", html_name="table-value-free_from")
    build_year: FieldConfig = FieldConfig(data_name="rok_budowy", html_name="table-value-build_year")
    building_type: FieldConfig = FieldConfig(data_name="rodzaj_zabudowy", html_name="table-value-building_type")
    windows: FieldConfig = FieldConfig(data_name="okna", html_name="table-value-windows_type")
    lift: FieldConfig = FieldConfig(data_name="winda", html_name="table-value-lift")
    media: FieldConfig = FieldConfig(data_name="media", html_name="table-value-media_types")
    securities: FieldConfig = FieldConfig(data_name="zabezpieczenia", html_name="table-value-security_types")
    equipment: FieldConfig = FieldConfig(data_name="wyposazenie", html_name="table-value-equipment_types")
    extra_info: FieldConfig = FieldConfig(data_name="informacje_dodatkowe", html_name="table-value-extras_types")
    building_material: FieldConfig = FieldConfig(
        data_name="material_budynku", html_name="table-value-building_material"
    )
    link_id: FieldConfig = FieldConfig(data_name="link_id")

    @property
    def fields_with_html_name(self) -> list[FieldConfig]:
        fields = [getattr(self, i) for i in dir(self) if not i.startswith("_") and i != "fields_with_html_name"]
        fields = [field for field in fields if isinstance(field, FieldConfig) and field.html_name is not None]
        return fields


offer_fields_config = OfferTabularFieldsConfig()
