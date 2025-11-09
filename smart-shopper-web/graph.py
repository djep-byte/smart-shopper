import math

# Grid coordinates (unit = ~1 meter logical) - tuned agar total jarak realistis
coordinates = {
    "Pintu Masuk": (0, 0),
    "Keranjang Belanja": (2, 0),
    "Koridor Depan": (5, 0),
    "Buah & Sayur": (4, 4),
    "Daging & Ikan": (4, 7),
    "Produk Susu": (7, 3),
    "Makanan Ringan": (7, 5),
    "Minuman": (7, 7),
    "Perlengkapan Rumah": (9, 5),
    "Koridor Belakang": (6, 9),
    "Gudang": (2, 9),
    "Kasir": (10, 0)
}

# Fungsi jarak Euclidean berdasarkan grid. Nilai sudah "masuk akal" untuk supermarket kecil.
def dist(a, b):
    x1, y1 = coordinates[a]
    x2, y2 = coordinates[b]
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2), 1)

supermarket_graph = {
    "Pintu Masuk": [("Keranjang Belanja", dist("Pintu Masuk", "Keranjang Belanja"))],
    "Keranjang Belanja": [("Koridor Depan", dist("Keranjang Belanja", "Koridor Depan")), ("Pintu Masuk", dist("Keranjang Belanja", "Pintu Masuk"))],
    "Koridor Depan": [
        ("Buah & Sayur", dist("Koridor Depan", "Buah & Sayur")),
        ("Produk Susu", dist("Koridor Depan", "Produk Susu")),
        ("Perlengkapan Rumah", dist("Koridor Depan", "Perlengkapan Rumah")),
        ("Kasir", dist("Koridor Depan", "Kasir")),
    ],
    "Buah & Sayur": [("Koridor Depan", dist("Buah & Sayur", "Koridor Depan")), ("Daging & Ikan", dist("Buah & Sayur", "Daging & Ikan"))],
    "Daging & Ikan": [("Buah & Sayur", dist("Daging & Ikan", "Buah & Sayur")), ("Koridor Belakang", dist("Daging & Ikan", "Koridor Belakang"))],
    "Produk Susu": [("Koridor Depan", dist("Produk Susu", "Koridor Depan")), ("Makanan Ringan", dist("Produk Susu", "Makanan Ringan"))],
    "Makanan Ringan": [("Produk Susu", dist("Makanan Ringan", "Produk Susu")), ("Minuman", dist("Makanan Ringan", "Minuman")), ("Koridor Belakang", dist("Makanan Ringan", "Koridor Belakang"))],
    "Minuman": [("Makanan Ringan", dist("Minuman", "Makanan Ringan")), ("Koridor Belakang", dist("Minuman", "Koridor Belakang"))],
    "Perlengkapan Rumah": [("Koridor Depan", dist("Perlengkapan Rumah", "Koridor Depan")), ("Koridor Belakang", dist("Perlengkapan Rumah", "Koridor Belakang"))],
    "Koridor Belakang": [
        ("Daging & Ikan", dist("Koridor Belakang", "Daging & Ikan")),
        ("Makanan Ringan", dist("Koridor Belakang", "Makanan Ringan")),
        ("Minuman", dist("Koridor Belakang", "Minuman")),
        ("Perlengkapan Rumah", dist("Koridor Belakang", "Perlengkapan Rumah")),
        ("Gudang", dist("Koridor Belakang", "Gudang")),
        ("Kasir", dist("Koridor Belakang", "Kasir"))
    ],
    "Gudang": [("Koridor Belakang", dist("Gudang", "Koridor Belakang"))],
    "Kasir": [("Koridor Depan", dist("Kasir", "Koridor Depan")), ("Koridor Belakang", dist("Kasir", "Koridor Belakang"))]
}

categories = ["Buah & Sayur","Daging & Ikan","Produk Susu","Makanan Ringan","Minuman","Perlengkapan Rumah"]

def get_coordinates(node):
    return coordinates.get(node, (0, 0))
