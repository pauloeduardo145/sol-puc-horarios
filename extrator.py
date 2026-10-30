from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#import requests

soup = BeautifulSoup(open("horario_sol.html", encoding="utf-8"), 'html.parser')
#linhas = soup.find("tbody").find_all("tr")
aulas = []
DIAS = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]


# for linha in linhas:
#     dia = linha.find("th").get_text(strip=True)
#     celulas = linha.find_all("td",class_="aula")

#     for celula in celulas:

#         materiaL = celula.find("span", class_= "materia")
#         horarios = celula.find_all("span", class_="horario")

#         salaL = celula.find("span", class_="sala")

#         if not materiaL or not horarios or not salaL:
#             continue

#         materia = materiaL.get_text(strip=True)
#         sala = celula.find("span", class_="sala").get_text(strip=True)

#         for h in horarios:
#             horario = h.get_text(strip=True)
#             partes = horario.split("–")
#             aula = {"dia": dia, "materia": materia, "inicio": partes[0], "fim": partes[1], "sala": sala}
#             aulas.append(aula)

def pegar_inicio(aula):
    return aula["inicio"]

def aulas_do_dia(aulas, data):

    hoje = DIAS[data.weekday()]
    aulas_hoje = []

    for aula in aulas:
        if aula["dia"] == hoje:
            aulas_hoje.append(aula)

    aulas_hoje.sort(key=pegar_inicio)

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

disciplinas = soup.find_all("div", class_="disciplina")

for disciplina in disciplinas:
    nome = disciplina.find("h1").get_text(strip=True)
    horarios = disciplina.find_all("div", class_="horario")

    for horario in horarios:

        dia = horario.find("h1").get_text(strip=True)
        has4 = horario.find_all("h4")
        sala = has4[0].get_text(strip=True).replace("Local: ", "")
        tipo = has4[1].get_text(strip=True)

        hora = horario.find("h3").get_text(strip=True)
        partes = hora.split(" às ")
        inicio = partes[0]
        fim = partes[1]


        aula = {"dia": dia, "materia": nome, "inicio": inicio, "fim": fim, "sala": sala, "tipo": tipo}
        aulas.append(aula)
        
print(proxima_aula(aulas, datetime(2026, 10, 21, 16, 0)))   # quarta 16:00
print(proxima_aula(aulas, datetime(2026, 10, 21, 18, 0)))   # quarta 18:00
print(proxima_aula(aulas, datetime(2026, 10, 23, 21, 0)))   # sexta 21:00