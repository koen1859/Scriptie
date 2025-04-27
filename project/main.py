from run_simulation import run_simulation, write_tsps
from areas import areas


for DB, neighborhoods in areas.items():
    for neighborhood in neighborhoods:
        print(f"Generating TSPS for {DB} {neighborhood}")
        write_tsps(DB, neighborhood)

# final_results = {}
#
# for DB, neighborhoods in areas.items():
#     for neighborhood in neighborhoods:
#         b, MAE = run_simulation(DB, neighborhood)
#         final_results[f"{DB}-{neighborhood}"] = [b, MAE]
#         print(f"beta for {DB} {neighborhood} is: {b}")
#         print(f"MAE for {DB} {neighborhood} is: {MAE}")
#
# with open("beta_values.tex", "w") as f:
#     f.write("\\begin{longtable}{llcc}\n")
#     f.write(
#         "\\caption{Empirical estimates for $\\beta$ in selected neighborhoods.} \\label{tab:results}\\\\\n"
#     )
#     f.write("\\hline\n")
#     f.write("Province & Neighborhood & $\\beta$ & MAE \\\\\n")
#     f.write("\\hline\n")
#     f.write("\\endfirsthead\n")
#     f.write("\\hline\n")
#     f.write("Province & Neighborhood & $\\beta$ & MAE \\\\\n")
#     f.write("\\hline\n")
#     f.write("\\endhead\n")
#
#     for key, values in final_results.items():
#         db, neighborhood = key.split("-", 1)
#         neighborhood = neighborhood.replace("_", " ")
#         db = db.replace("_", " ")
#         f.write(f"{db} & {neighborhood} & {values[0]:.4f} & {values[1]:.4f} \\\\\n")
#
#     f.write("\\hline\n")
#     f.write("\\end{longtable}\n")
