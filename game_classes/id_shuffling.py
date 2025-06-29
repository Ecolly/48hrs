
import random
#initialize fakename to realname list for staffs and tomes
#the 'key' number represents local sprite index (aka the color)
#any items wit a definite sprite & name are excluded (e.g. #28 (white) & #24 (black) for tomes)
fakenames_staffs_key = [0, 1, 2, 3, 7, 8, 10, 13, 16, 17, 19, 22, 23, 26]
fakenames_tomes_key = [0, 1, 2, 3, 7, 8, 10, 13, 16, 17, 19, 22, 23, 26]

fakenames_staffs_realnames = ("Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence")
fakenames_tomes_realnames = ("Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Staffboost Tome", "Tome of Consolidation", "Tome of Dispersion", "Coloring Tome", "Summoning Tome", "Banishing Tome")


random.shuffle(fakenames_staffs_key)
random.shuffle(fakenames_tomes_key)
