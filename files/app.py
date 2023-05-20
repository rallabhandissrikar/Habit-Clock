from flask import *
from DatabaseConnection import *
import datetime

app = Flask(__name__)


@app.route('/athUser')
def athUser():
    name_args = request.args.get('name')
    passw_args = request.args.get('passw')
    usr_is_there = ath_user(name_args, passw_args)
    if usr_is_there == True:
        return 'user exists'
    else:
        return 'no user exists'


@app.route('/createUser')
def createUser():
    name_args = request.args.get('name')
    passw_args = request.args.get('passw')
    load_status = create_user(name_args, passw_args)
    if load_status:
        return 'new user created'
    else:
        return 'user exists'


@app.route('/addTodo')
def addTodo():
    name_arg = request.args.get('name')
    todo_title_args = request.args.get('title')
    ed_args = request.args.get('ed')

    def checkTimeStamps(ed: str):
        if ed[:4].strip().isdigit() and ed[5:7].strip().isdigit() and ed[8:].strip().isdigit():
            return True
        else:
            return False
    if checkTimeStamps(ed_args):
        data_add_status = add_todo_new(
            name_arg, title=todo_title_args, ed=ed_args)
        if data_add_status:
            return 'data added'
        else:
            return 'data not added'
    else:
        return 'data not added'


@app.route('/getUserTodoList')
def getUserTodoList():
    name_args = request.args.get('name')
    dat = get_todo_from_user(name_args)
    return dat


@app.route('/updateTodo')
def updateTodo():
    name_args = request.args.get('name')
    id_args = int(request.args.get('id'))
    update_status = update_todo(name_args, id_args)
    if update_status:
        return 'update done'
    else:
        return 'update not done'


@app.route('/addHabit')
def addHabit():
    title_args = request.args.get('title')
    name_args = request.args.get('name')
    sd_args = request.args.get('sd')

    def checkTimeStamps(sd: str):
        if sd[:4].strip().isdigit() and sd[5:7].strip().isdigit() and sd[8:].strip().isdigit():
            return True
        else:
            return False
    if checkTimeStamps(sd_args):
        add_status = add_habit_new(name_args, title_args, sd_args)
        if add_status :
            return 'data added'
        else :
            return 'data not added'
    else:
        return 'data not added'

@app.route('/updateHabit')
def updateHabit():
    name_args = request.args.get('name')
    id_args = int(request.args.get('id'))
    update_status = update_habit(name_args, id_args)
    if update_status :
        return 'update done'
    else :
        return 'update not done'

@app.route('/restartHabit')
def restartHabit():
    name_args = request.args.get('name')
    id_args = int(request.args.get('id'))
    sd_args = request.args.get('sd')
    def checkTimeStamps(sd: str):
        if sd[:4].strip().isdigit() and sd[5:7].strip().isdigit() and sd[8:].strip().isdigit():
            return True
        else:
            return False
        
    if checkTimeStamps(sd_args):
        update_status = restart_habit(name_args, id_args, sd_args)
        if update_status :
            return 'reset done'
        else :
            return 'reset not done'
    else :
        return 'reset not done'

@app.route('/getUserHabitList')
def getUserHabitList() :
    name_args = request.args.get('name')
    get_status = get_habits_from_user(name_args)
    return get_status

@app.route('/removeHabit')
def removeHabit():
    name_args = request.args.get('name')
    id_args = int(request.args.get('id'))
    remove_status = remove_habit(name_args, id_args)
    if remove_status :
        return 'deletion done'
    else :
        return 'deletion now done'


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
