# Tworzenie na początku słownika firma - nie moge umiejscowić,
# żeby nie robić osobnej strony
# historia - start koniec - błąd


from flask import Flask, render_template, request
import json
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def welcome():

    with open('db.json') as f:
        firma = json.load(f)
    if request.method == "POST":
        typ_forma = request.form.get('typ_forma')
        if typ_forma == 'saldo':
            newsaldo = request.form.get('newsaldo')
            firma['saldo'] = float(newsaldo)
            firma['historia'].append('Zmiana salda: ',[firma['saldo'], newsaldo])
            with open('db.json', 'w') as f:
                json.dump(firma, f)

        elif typ_forma == 'kupno' or typ_forma == 'sprzedaz':
            przedmiot = request.form.get('nazwa')
            sztuk = request.form.get('sztuk')
            cena = request.form.get('cena')

            if not przedmiot:
                return {'sukces': True, 'msg': f'dodano {przedmiot}, {sztuk} sztuk'}

            try:
                sztuk = float(sztuk)
                cena = float(cena)
            except ValueError:
                return {'sukces': True, 'msg': f'Liczb sztuk i cena muszą być liczbami rzeczywistymi'}

            if typ_forma == 'kupno':
                firma['saldo'] -= sztuk * cena
                if przedmiot not in firma['stan_magazynu']:
                    firma['stan_magazynu'][przedmiot] = 0
                firma['stan_magazynu'][przedmiot] += sztuk
                firma['historia'].append(["kupno", przedmiot, sztuk, cena])

            elif typ_forma == 'sprzedaz':
                if przedmiot not in firma['stan_magazynu']:
                    return {'sukces': False, 'msg': f'Nie ma przedmiotu {przedmiot} w magazynie'}
                elif firma['stan_magazynu'][przedmiot] < sztuk:
                    return {'sukces': False, 'msg': f'Nie ma wystarczającej ilości przedmiotu {przedmiot} w magazynie'}
                else:
                    firma['saldo'] += sztuk * cena
                    firma['stan_magazynu'][przedmiot] -= sztuk
                    firma['historia'].append(["Sprzedaż", przedmiot, sztuk, cena])

            with open('db.json', 'w') as f:
                json.dump(firma, f)

    return render_template('index.html', saldo=firma['saldo'], firma=firma)

@app.route('/historia/')
def historia():
    with open('db.json') as f:
        firma = json.load(f)
        historia = firma['historia']
        return render_template('historia.html', historia=historia)

@app.route('/historia/<start>/<koniec>')
def wyswietl_historie(start, koniec):
    with open('db.json') as f:
        firma = json.load(f)

    start = int(request.args.get('start'))
    koniec = int(request.args.get('koniec'))

    historia = firma['historia'][start:koniec]
    if not historia:
        return 'Brak historii firmy'
    if start > koniec:
        return 'Błędny zakres'
    return render_template("historia.html", historia=historia)

# def create_db():
#     firma = {
#         'salata':5,
#         'kapusta':3,
#         'piwo':4,
#         'jajko':10,
#         'miesko':2,
#     }
#
#     with open('db.json', 'w') as f:
#         json.dump(firma, f)
#     return firma

if __name__ == '__main__':
    app.run(debug=True)

