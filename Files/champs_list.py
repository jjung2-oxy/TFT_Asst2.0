import Levenshtein


set10_champs = [
    "Annie", "Corki", "Evelynn", "Jinx", "Kennen", "K'Sante", "Lillia", "Nami", "Olaf", "Tahm Kench", "Taric", "Vi", "Yasuo",
    "Aphelios", "Bard", "Garen", "Gnar", "Gragas", "Jax", "Kai'Sa", "Katarina", "Kayle", "Pantheon", "Senna", "Seraphine", "Twitch",
    "Amumu", "Ekko", "Lulu", "Lux", "Miss Fortune", "Mordekaiser", "Neeko", "Riven", "Samira", "Sett", "Urgot", "Vex", "Yone",
    "Ahri", "Akali K/DA", "Akali True-DMG", "Blitzcrank", "Caitlyn", "Ezreal", "Karthus", "Poppy", "Thresh", "Twisted Fate", "Viego", "Zac", "Zed",
    "Illaoi", "Jhin", "Kayn", "Lucian", "Qiyana", "Sona", "Yorick", "Ziggs"
]

set9_champs = [
    "Cassiopeia", "Cho'Gath", "Graves", "Illaoi", "Irelia", "Jhin", "Kayle", "Malzahar", "Milio", "Orianna", "Poppy", "Renekton", "Samira",
    "Ashe", "Galio", "Jinx", "Kassadin", "Naafiri", "Qiyana", "Sett", "Soraka", "Swain", "Taliyah", "Twisted Fate", "Vi", "Warwick",
    "Darius", "Ekko", "Jayce", "Karma", "Katarina", "Miss Fortune", "Nautilus", "Neeko", "Quinn", "Rek'Sai", "Sona", "Taric", "Vel'Koz",
    "Aphelios", "Azir", "Fiora", "Jarvan IV", "Kai'Sa", "Mordekaiser", "Nasus", "Nilah", "Sejuani", "Shen", "Silco", "Xayah",
    "Aatrox", "Ahri", "Bel'Veth", "Gangplank", "Heimerdinger", "K'Sante", "Ryze", "Sion"
]

def find_closest(target, string_list):
    closest_string = None
    min_distance = float('inf')

    for s in string_list:
        distance = Levenshtein.distance(target, s)
        if distance < min_distance:
            min_distance = distance
            closest_string = s

    return closest_string