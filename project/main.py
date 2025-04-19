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
final_results = {}

for DB, neighborhoods in areas.items():
    for neighborhood in neighborhoods:
        b, MAE = run_simulation(DB, neighborhood)
        final_results[f"{DB}-{neighborhood}"] = [b, MAE]
        print(f"beta for {DB} {neighborhood} is: {b}")
        print(f"MAE for {DB} {neighborhood} is: {MAE}")

with open("beta_values.org", "w") as f:
    f.write("#+LATEX: \\begin{table}[htbp]\n")
    f.write("#+LATEX: \\centering\n")
    f.write("#+CAPTION: Empirical estimates for $\\beta$, for the selected areas.\n")
    f.write("#+LABEL: tab:results\n")
    f.write("| Province      | Neighborhood         | Beta      | MAE      |\n")
    f.write("|---------------+----------------------+-----------+----------|\n")

    for key, values in final_results.items():
        db, neighborhood = key.split("-", 1)
        neighborhood = neighborhood.replace("_", " ")
        db = db.replace("_", " ")
        f.write(
            f"| {db:<13} | {neighborhood:<20} | {values[0]:.4f} | {values[1]:.4f} |\n"
        )
