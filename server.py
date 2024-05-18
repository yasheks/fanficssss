from flask import Flask, render_template, redirect, abort, request

app = Flask(__name__)


categories = [
    {
        "name": "Фанфики про Лунтика",
        "fanfics": [
            {
                "faname": "велеколепное кольцо лунтика",
                "text": "Измотанный лунтик уже год нес кольцо в мордор, и лембас был на исходе. Он велел мне быстро собраться и выйти во двор, чтобы немного отдышаться. У меня возникло нехорошее предчувствие. Я подумал, что с моим приятелем случилось что-то неладное. Этот лунтик был одним из моих наиболее уважаемых клиентов, и никогда раньше мы с ним не расставались.",
                "likes": 84,
                "like": False
            },
            {
                "faname": "матрица 104928129401",
                "likes": 104928129401,
                "text": "Лунтик подключился к матрице и тут же направился на поиски Тринити. Вместе с ним побрел в зал тот самый павиан, у которого товарищ во время первого опыта подал сигнал тревоги. Вместе с павианом тоже отправился рядышком работник ларингологического центра, который своими глазами видел условного контактного попугая вживую. Так сказать, семейный характер опыта.",
                "like": False
            },
            {
                "faname": "невероятное приключение лунтика",
                "likes": 93,
                "text": "Вот наконец за окнами поезда появился Бобруйск. Он встретил Лунтика неприветливым дождем. Под мокрыми тентами там и сям стояли разноцветные машины, будто все они были машинами времени. Когда Лунтик прошел внутрь вокзала, лица у встречавших вытянулись. Даже оживление, с которым он шел, показалось им странно театральным.",
                "like": False
            },
            {
                "faname": "лунтик в космосе",
                "likes": 404,
                "text": "Звездолет капитана Лунтика дрейфовал где-то в районе Венеры. Топливо заканчивалось, но сила духа неиссякала. Было время, когда капитан Лунтик надеялся попасть на Землю и даже послал на разведку какой-то металлический корабль, который описал в своем рапорте около десятка кругов вокруг планеты. Наверно, на обратном пути он дал сам себе слово «не возвращаться».",
                "like": False
            }
        ]
    },
    {
        "name": "Фанфики про Вупсеня",
        "fanfics": [
            {
                "faname": "вупсень в баре",
                "likes": 237,
                "text": "Заходит Вупсень в бар. На него бабы и мужики смотрят, млеют. Тут один мент спрашивает: А кто это такой у вас? А Вупсень, не будь дурак, подходит к менту, приставил ему пистолет ко лбу и говорит: Я — Вупсень, убийца ментов! И прямо-таки вот этой самой ножкой тычет в лоб менту. Все аж замерли. Только один мент еле слышно хихикнул. Ну Вупсень сам и говорит: «Ты мент или нет?» Мент еще громче захихикал. И тут, естественно, вокруг паника. Одна баба кричит: «Я Барыню видела!» И тут же — бах! бах! трах! трах! и прочие террористические акты. Потом Вупсень как раз работал официантом в ресторане. Барыня его и запомнила.",
                "like": False
            },
            {
                "faname": "интересная шляпа",
                "likes": 99,
                "text": "Купил Вупсень шляпу, и пошел с ней прямо в лес, и стал ходить по лесу, и наконец подошел к большой луже. Глядит – а там лягушка сидит и еще один такой же. А первый кричит: «Ты чего сюда забрел? Иди отсюда!» – «Я, говорит, пришел на лягушку посмотреть, какая она».",
                "like": False
            }
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/category/<int:category_id>')
def category_page(category_id):
    if category_id >= 0 and category_id < len(categories):
        category = categories[category_id]
        return render_template('category.html', category=category, category_id=category_id)
    else:
        return abort(404)

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/like')
def add_like(category_id, fanfic_id):
    if category_id < 0 or category_id >= len(categories) or fanfic_id < 0 or fanfic_id >= len(categories[category_id]['fanfics']):
        abort(404)


    categories[category_id]['fanfics'][fanfic_id]["likes"] += 1
    # Поскольку у нас уже есть страница с отображением списка задач, можем просто перенаправить туда пользователя
    return redirect(f'/category/{category_id}')

@app.route('/category/add', methods=['post'])
def add_category():
    category_name = request.form.get('category_name')

    if category_name:
        categories.append({
            "name": category_name,
        })

    return redirect('/')


@app.route('/category/<int:id>/delete')
def delete_category(id):
    if id < 0 or id >= len(categories):
        abort(404)

    del categories[id]

    return redirect('/')

@app.route('/category/<int:id>/edit')
def edit_category_page(id):
    if id < 0 or id >= len(categories):
        abort(404)
    # Передаем в шаблон текущие параметры категории
    return render_template('edit.html', categories=categories, id=id)

@app.route('/category/<int:id>/edit', methods=['POST'])
def edit_category(id):
    if id < 0 or id >= len(categories):
        abort(404)

    category_name = request.form.get('category_name')

    if category_name:
        categories[id]['name'] = category_name

    return redirect('/')

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/edit')
def edit_fanfic_page(category_id, fanfic_id):
    if category_id < 0 or category_id >= len(categories) or fanfic_id < 0 or fanfic_id >= len(categories[category_id]['fanfics']):
        abort(404)

    return render_template('edit_fanfic.html', categories=categories, category_id=category_id, fanfic_id=fanfic_id)

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/edit', methods=['POST'])
def edit_fanfic(category_id, fanfic_id):
    if category_id < 0 or category_id >= len(categories) or fanfic_id < 0 or fanfic_id >= len(categories[category_id]['fanfics']):
        abort(404)

    fanfic_name = request.form.get('fanfic_name')
    fanfic_text = request.form.get('fanfic_text')

    if fanfic_name:
        categories[category_id]['fanfics'][fanfic_id]["faname"] = fanfic_name
        categories[category_id]['fanfics'][fanfic_id]["text"] = fanfic_text

    return redirect(f"/category/{category_id}")


@app.route('/category/<int:category_id>/fanfic/add', methods=['POST'])
def add_fanfic(category_id):
    fanfic_name = request.form.get('fanfic_name')
    fanfic_text = request.form.get('fanfic_text')

    categories[category_id]['fanfics'].append({
        "faname": fanfic_name,
        "text": fanfic_text,
        "likes": 0,
        "like": False
    })

    return redirect(f"/category/{category_id}")


@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/delete')
def delete_fanfic(category_id, fanfic_id):
    if category_id < 0 or category_id >= len(categories) or fanfic_id < 0 or fanfic_id >= len(
            categories[category_id]['fanfics']):
        abort(404)

    del categories[category_id]['fanfics'][fanfic_id]
    # Поскольку у нас уже есть страница с отображением списка задач, можем просто перенаправить туда пользователя
    return redirect(f'/category/{category_id}')


app.run(debug=True)
