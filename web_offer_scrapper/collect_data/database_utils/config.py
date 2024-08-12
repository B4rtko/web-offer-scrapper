from dataclasses import dataclass


@dataclass
class DBColumn:
    db_name: str
    sql_datatype: str


price = DBColumn(db_name="price", sql_datatype="INTEGER")

address = DBColumn(db_name="address", sql_datatype="VARCHAR")
address_street = DBColumn(db_name="address_street", sql_datatype="VARCHAR")
address_estate = DBColumn(db_name="address_estate", sql_datatype="VARCHAR")
address_district = DBColumn(db_name="address_district", sql_datatype="VARCHAR")
address_city = DBColumn(db_name="address_city", sql_datatype="VARCHAR")
address_province = DBColumn(db_name="address_province", sql_datatype="VARCHAR")

surface = DBColumn(db_name="surface", sql_datatype="NUMERIC")
building_ownership = DBColumn(db_name="building_ownership", sql_datatype="VARCHAR")
rooms = DBColumn(db_name="rooms_num", sql_datatype="INTEGER")
construction_status = DBColumn(db_name="construction_status", sql_datatype="VARCHAR")
floor = DBColumn(db_name="floor", sql_datatype="VARCHAR")
floors_in_building = DBColumn(db_name="floors_in_building", sql_datatype="VARCHAR")
outdoor = DBColumn(db_name="outdoor", sql_datatype="VARCHAR")
rent = DBColumn(db_name="rent", sql_datatype="NUMERIC")
parking_space = DBColumn(db_name="parking_space", sql_datatype="VARCHAR")
heating = DBColumn(db_name="heating", sql_datatype="VARCHAR")
market = DBColumn(db_name="market", sql_datatype="VARCHAR")
advertiser_type = DBColumn(db_name="advertiser_type", sql_datatype="VARCHAR")
free_from = DBColumn(db_name="free_from", sql_datatype="VARCHAR")
build_year = DBColumn(db_name="build_year", sql_datatype="NUMERIC")
building_type = DBColumn(db_name="building_type", sql_datatype="VARCHAR")
windows = DBColumn(db_name="windows", sql_datatype="VARCHAR")
lift = DBColumn(db_name="lift", sql_datatype="VARCHAR")
media = DBColumn(db_name="media", sql_datatype="VARCHAR")
securities = DBColumn(db_name="securities", sql_datatype="VARCHAR")
equipment = DBColumn(db_name="equipment", sql_datatype="VARCHAR")
extra_info = DBColumn(db_name="extra_info", sql_datatype="VARCHAR")
building_material = DBColumn(db_name="building_material", sql_datatype="VARCHAR")
link_id = DBColumn(db_name="link_id", sql_datatype="VARCHAR")
description = DBColumn(db_name="description", sql_datatype="VARCHAR")
