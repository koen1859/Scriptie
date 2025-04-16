from run_simulation import run_simulation


areas = {
    "groningen": [
        "Hortusbuurt",
        "Binnenstad",
        "Oosterpoort",
        "Rivierenbuurt",
        "De Wijert",
        "Oosterparkwijk",
        "De Hoogte",
        "Korrewegwijk",
        "Schildersbuurt",
        "Paddepoel",
        "Oranjewijk",
        "Tuinwijk",
        "Selwerd",
        "Vinkhuizen",
        "Hoogkerk-zuid",
        "Gravenburg",
        "De Held",
        "Reitdiep",
        "Hoornse Meer",
        "Corpus den Hoorn",
        "Eemspoort",
        "Euvelgunne",
        "Driebond",
        "Winschoterdiep",
        "Eemskanaal",
        "Helpman",
        "Lewenborg",
        "Beijum",
        "Maarsveld",
    ],
    "noord_holland": [
        "Schrijverswijk",
        "Stad van de Zon",
        "Stadshart",
        "Jordaan",
        "Slotervaart",
        "IJburg",
        "Oostelijke Eilanden",
        "Oostelijk Havengebied",
        "Frederik Hendrikbuurt",
        "Van Lennepbuurt",
        "Da Costabuurt",
        "Kinkerbuurt",
        "Kersenboogerd",
        "Pax",
        "Graan voor Visch",
        "Vrijschot-Noord",
        "Toolenburg",
        "Floriande",
        "Overbos",
        "Bornholm",
        "Beukenhorst-Oost",
        "De Hoek",
        "West",
        "Zuid",
        "Oost",
        "Noord",
        "De President",
        "Graan voor Visch-Zuid",
        "Zuidwijk",
        "Buitenveldert-West",
        "Buitenveldert",
        "Apollobuurt",
        "Stadionbuurt",
        "Prinses Irenebuurt e.o.",
        "Hoofddorppleinbuurt",
        "Willemspark",
        "Schinkelbuurt",
        "Vondelparkbuurt",
        "Helmersbuurt",
        "Overtoomse Sluis",
        "Museumkwartier",
        "Rivierenbuurt",
        "IJselbuurt",
        "Scheldebuurt",
        "Rijnbuurt",
        "De Baarsjes",
        "Landlust",
        "Staatsliedenbuurt",
        "Spaarndammerbuurt",
        "De Pijp",
        "Grachtengordel",
        "Oud-Zuid",
    ],
}
beta = {}

for DB, neighborhoods in areas.items():
    for neighborhood in neighborhoods:
        b = run_simulation(DB, neighborhood)
        beta[f"{DB}-{neighborhood}"] = b
        print(f"beta for {DB} {neighborhood} is: {b}")

with open("beta_values.org", "w") as f:
    f.write("| Province      | Neighborhood         | Beta      |\n")
    f.write("|---------------+----------------------+-----------|\n")

    for key, value in beta.items():
        db, neighborhood = key.split("-", 1)
        neighborhood = neighborhood.replace("_", " ")
        f.write(f"| {db:<13} | {neighborhood:<20} | {value:.4f} |\n")
