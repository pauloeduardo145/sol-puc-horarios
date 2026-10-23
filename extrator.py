from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#import requests

soup = BeautifulSoup(open("horario_falso.html", encoding="utf-8"), 'html.parser')
linhas = soup.find("tbody").find_all("tr")

aulas = []
DIAS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

for linha in linhas:
    dia = linha.find("th").get_text(strip=True)
    celulas = linha.find_all("td",class_="aula")

    for celula in celulas:

        materiaL = celula.find("span", class_= "materia")
        horarios = celula.find_all("span", class_="horario")

        salaL = celula.find("span", class_="sala")

        if not materiaL or not horarios or not salaL:
            continue

        materia = materiaL.get_text(strip=True)
        sala = celula.find("span", class_="sala").get_text(strip=True)

        for h in horarios:
            horario = h.get_text(strip=True)
            partes = horario.split("–")
            aula = {"dia": dia, "materia": materia, "inicio": partes[0], "fim": partes[1], "sala": sala}
            aulas.append(aula)



def aulas_do_dia(aulas, data):

    hoje = DIAS[data.weekday()]
    aulas_hoje = []

    for aula in aulas:
        if aula["dia"] == hoje:
            aulas_hoje.append(aula)

    return aulas_hoje

def proxima_aula(aulas, agora):

    aulas_hoje = aulas_do_dia(aulas, agora)

    hora_atual = agora.strftime("%H:%M")
    faltam = []

    for aula in aulas_hoje:
        if aula["inicio"] > hora_atual:
            faltam.append(aula)

    if not faltam:
        n = 1

        do_dia = []

        while not do_dia and n <= 7:
            data = agora + timedelta(days=n)

            do_dia = aulas_do_dia(aulas, data)

            n = n + 1
        

        if not do_dia:
            return None

        return do_dia[0]
        
    return faltam[0]
