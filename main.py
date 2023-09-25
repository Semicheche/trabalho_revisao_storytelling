import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from flask import render_template



import sqlite3

def database_conect():
    return sqlite3.connect('database.sqlite')

con = database_conect()

from flask import Flask

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello_world():
    res = []
    con = database_conect()
    result = con.execute("""
                         SELECT
                            substr( o.data, 7, 10 ) ano,
                            o.tipoOcorrencias,
                            SUM(o.Qtde) qtde
                        FROM ocorrencias as o
                        WHERE o.tipoOcorrencias IN ('roubo_rua', 'estelionato') Group By 1, 2  """).fetchall()
    est_ameaca = con.execute("""
                             SELECT  o.cisp,
                                      (SELECT
                                        SUM(o1.Qtde) qtde
                                      FROM ocorrencias as o1
                                      WHERE o1.tipoOcorrencias IN ('ameaca') and o1.cisp = o.cisp) ameaca,
                                      (SELECT
                                        SUM(o1.Qtde) qtde
                                      FROM ocorrencias as o1
                                      WHERE o1.tipoOcorrencias IN ('estelionato') and o1.cisp = o.cisp) estelionato
                                      FROM ocorrencias as o GROUP BY o.cisp
                                      """).fetchall()
    
    
    for val in  est_ameaca:
        res.append({
            'batalhao': val[0],
            'ameaca': val[1],
            'estelionato': val[2]
        })

    ano =  [res[0] for res in result]
    ocor = [res[1] for res in result]
    qtde = [res[2] for res in result]

    return render_template("home.html", ano=ano, ocorencia=ocor, qtde=qtde, resultado=res)



# dados = pd.groupby(['regiao']).sum('Qtde').sort_values('Qtde', ascending=False)
# print("leu os daados")
# dados = dados.sort_values('Qtde')

# plt.bar(dados.index, dados['Qtde'])
# plt.show()
# dados01 = pd[pd['TipoOcorrencias'] == 'roubo_transeunte']

# dados01['ano'] = [ val.split('m')[0] for val in dados01['mes_ano'].to_numpy()]
# dados01 = dados01.groupby(['ano']).sum('Qtde').sort_values('Qtde', ascending=False)

# print(dados01)
# plt.bar(dados01.index, dados01['Qtde'])
# plt.show()

