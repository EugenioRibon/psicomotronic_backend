from users.models import CustomUser
from subastas.models import Category, Auction, Bid
from django.utils import timezone
from datetime import timedelta

# Crear usuarios (get_or_create evita duplicados)
usuarios = [
    {
        "username": "UsuarioNuevo1",
        "first_name": "Alberto",
        "last_name": "González",
        "email": "alberto.gonzalez@nuevodemo.com",
        "birth_date": "1992-05-14",
        "municipality": "Madrid",
        "locality": "Madrid",
        "password": "123"
    },
    {
        "username": "UsuarioNuevo2",
        "first_name": "Marina",
        "last_name": "Sánchez",
        "email": "marina.sanchez@nuevodemo.com",
        "birth_date": "1989-09-23",
        "municipality": "Cataluña",
        "locality": "Barcelona",
        "password": "123"
    },
    {
        "username": "UsuarioNuevo3",
        "first_name": "Javier",
        "last_name": "Domínguez",
        "email": "javier.dominguez@nuevodemo.com",
        "birth_date": "1985-02-10",
        "municipality": "Andalucía",
        "locality": "Córdoba",
        "password": "Sevilla"
    }
]

for u in usuarios:
    user, created = CustomUser.objects.get_or_create(username=u["username"], defaults=u)
    if not created:
        print(f"Usuario {u['username']} ya existe, no se creó de nuevo.")

# Crear categorías
category_luxury, _ = Category.objects.get_or_create(name='lujo')
category_sport, _ = Category.objects.get_or_create(name='deportivo')
category_smart, _ = Category.objects.get_or_create(name='inteligente')
category_vintage, _ = Category.objects.get_or_create(name='vintage')

# Crear o recuperar subastador
auctioneer, _ = CustomUser.objects.get_or_create(
    username="UsuarioDemo1",
    defaults={
        "first_name": "Demo",
        "last_name": "User",
        "email": "demo@nuevodemo.com",
        "birth_date": "1990-01-01",
        "municipality": "Madrid",
        "locality": "Madrid",
        "password": "demo123"
    }
)

# Crear subastas (sin rating)
subastas = [
    {
        "title": "Rolex Submariner",
        "description": "Icónico reloj de buceo con caja de acero inoxidable, bisel giratorio unidireccional y resistencia al agua de hasta 300 metros.",
        "price": 10500,
        "stock": 3,
        "brand": "Rolex",
        "category": category_luxury,
        "thumbnail": "https://media.gettyimages.com/id/1921982579/es/foto/leigh-on-sea-england-a-second-hand-rolex-oyster-perpetual-submariner-date-watch-is-displayed.jpg?s=612x612&w=0&k=20&c=rWa9NS1IN8fIihpt2ikPpLZ9yd9KZBhfmWfG4ioOAos="
    },
    {
        "title": "Omega Speedmaster Moonwatch",
        "description": "Reloj legendario que acompañó a los astronautas en la Luna. Cronógrafo de cuerda manual con cristal hesalite.",
        "price": 6500,
        "stock": 5,
        "brand": "Omega",
        "category": category_luxury,
        "thumbnail": "https://www.omegawatches.com/assets/moonwatch/assets/images/hero/background-m.jpg"
    },
    {
        "title": "Garmin Fenix 7X Pro",
        "description": "Reloj multideporte con GPS, mapas topográficos, sensor de pulso y linterna LED integrada. Ideal para deportes extremos.",
        "price": 899,
        "stock": 10,
        "brand": "Garmin",
        "category": category_sport,
        "thumbnail": "https://res.garmin.com/en/products/010-02778-11/v/cf-lg.jpg"
    },
    {
        "title": "Apple Watch Series 9",
        "description": "Pantalla Retina Always-On, chip S9, sensor de oxígeno en sangre, ECG, y compatibilidad con entrenamiento y salud.",
        "price": 529,
        "stock": 20,
        "brand": "Apple",
        "category": category_smart,
        "thumbnail": "https://es.etoren.com/upload/images/0.93516100_1695769835_apple-watch-series-9-gps-45mm-midnight-aluminium-case-with-midnight-sport-loop.jpg"
    },
    {
        "title": "Samsung Galaxy Watch6 Classic",
        "description": "Reloj inteligente con diseño clásico, pantalla Super AMOLED, sensor de frecuencia cardiaca y compatibilidad con Android.",
        "price": 419,
        "stock": 15,
        "brand": "Samsung",
        "category": category_smart,
        "thumbnail": "https://m.media-amazon.com/images/I/71klCnd2v3L._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Casio G-Shock GA-2100",
        "description": "Reloj analógico-digital ultra resistente, con diseño delgado y batería de larga duración. Resistente a impactos y agua.",
        "price": 129,
        "stock": 25,
        "brand": "Casio",
        "category": category_sport,
        "thumbnail": "https://cdn.laroyale.nl/B161lIZ0mxFGy5tDwT1T5X6BI-ZsVi0Mf7o9bK4OXd4/resize:fit:700:700/quality:90/aHR0cHM6Ly93d3cubGFyb3lhbGUubmwvbWVkaWEvY2F0YWxvZy9wcm9kdWN0Ly9nL2EvZ2EtMjEwMC0xYWVyX2Zyb250X3RpbHRlZF93ZWIuanBn.webp"
    },
    {
        "title": "Seiko 5 SNK809",
        "description": "Reloj automático con estilo militar, caja de acero inoxidable, correa de nylon y resistencia al agua hasta 30m.",
        "price": 99,
        "stock": 30,
        "brand": "Seiko",
        "category": category_vintage,
        "thumbnail": "https://preview.redd.it/seiko-snk809-switching-back-to-an-automatic-movement-field-v0-nq2kkwzw5urc1.jpg?width=640&crop=smart&auto=webp&s=7de51d0d4b7bceab1bf77f6238e0977ac0b84b31"
    }
]

for s in subastas:
    Auction.objects.get_or_create(
        title=s["title"],
        defaults={**s,
                  "closing_date": timezone.now() + timedelta(days=30),
                  "creation_date": timezone.now(),
                  "auctioneer": auctioneer}
    )

# Crear pujas solo si no existen
try:
    pruebas2 = CustomUser.objects.get(username="UsuarioNuevo1")
    pruebas3 = CustomUser.objects.get(username="UsuarioNuevo2")

    if not Bid.objects.filter(user=pruebas2).exists():
        Bid.objects.create(auction=Auction.objects.get(title="Rolex Submariner"), user=pruebas2, amount=500)
        Bid.objects.create(auction=Auction.objects.get(title="Omega Speedmaster Moonwatch"), user=pruebas2, amount=650)
        Bid.objects.create(auction=Auction.objects.get(title="Garmin Fenix 7X Pro"), user=pruebas2, amount=900)

    if not Bid.objects.filter(user=pruebas3).exists():
        Bid.objects.create(auction=Auction.objects.get(title="Omega Speedmaster Moonwatch"), user=pruebas3, amount=700)
        Bid.objects.create(auction=Auction.objects.get(title="Garmin Fenix 7X Pro"), user=pruebas3, amount=950)
        Bid.objects.create(auction=Auction.objects.get(title="Apple Watch Series 9"), user=pruebas3, amount=1200)

except CustomUser.DoesNotExist:
    print("Alguno de los usuarios de prueba no fue encontrado.")
