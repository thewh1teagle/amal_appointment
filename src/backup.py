from dataclasses import dataclass


@dataclass
class Location:
    name: str
    id: str


locations = [
    Location("om_alfaham", "9"),
    Location("ofakim", "18"),
    Location('eilat', '20'),
    Location('ashdod', '15'),
    Location('ashkelon', '30'),
    Location('gat', '10'),
    Location('dimona', '19'),
    Location('haifa', '7'),
    Location('tiberias', '5'),
    Location('jerusalem_beit_hanina', '11'),
    Location('jerusalem_new_city', '24'),  # nayot?
    Location('karmiel', '3'),
    Location('naharia', '1'),
    Location('the_galilee', '28'),
    Location('afula', '8'),
    Location('kiryat_hayim', '6'),
    Location('kiryat_shmona', '2')
]

months = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
]
