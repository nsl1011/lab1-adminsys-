from peewee import *
from sys import argv
import datetime
import random
import os.path
import pytest


db_name = 'database.db'
db = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = db


class Clients (BaseModel):
    name = CharField()
    city = CharField()
    address = CharField()


class Orders (BaseModel):
    clients = ForeignKeyField(Clients, backref='client')
    date = DateTimeField()
    amount = IntegerField()
    description = CharField()


def init_db():
    # ---Create or delete database---

    if os.path.exists(db_name) == True:
        os.remove(db_name)
        print('--- DataBase delete ---')
    db.create_tables([Clients, Orders], safe=True)
    print('--- DataBase create ---')

    # ---Over---


def fill_db():
    # ---Create table---
    people_number = 10
    print('--- Filling out database ---')
    clients_list = []
    name_arr = ["Максим", "Александра", "Павел", "Ярослава", "Антон", "Анатолий", "Даниил", "Ульяна", "Мария", "Богдан", "Артём", "Никита"]
    city_arr = ["Сосногорск", "Отрадный", "Кораблино", "Ладушкин", "Зеленогорск", "Азов", "Инза", "Киренск", "Шахты", "Москва", "Сургут"]
    address_arr = ["Майская 25", "Сосновая 12", "Звездная 1", "Каприловская 35", "Чудная 7", "Кариловская 9", "Петровская 24/1", "Самойловская 64/3"]

    for i in range(people_number):
        clients_list.append({'name': name_arr[random.randint(
            0, len(name_arr) - 1)], 'city': city_arr[random.randint(0, len(city_arr) - 1)], 'address': address_arr[random.randint(0, len(address_arr) - 1)]})

    orders_list = []
    orders_list_dis = ['Кольцо', 'Цепочка', 'Серьги', 'Браслет', 'Кактус']

    for i in range(len(clients_list)):
        orders_list.append({'clients': i+1, 'date': str(random.randint(2000, 2020))+'-'+str(random.randint(1, 12))+'-'+str(
            random.randint(1, 28)), 'amount': random.randint(1, 100), 'description': orders_list_dis[random.randint(0, 4)]})

    Clients.insert_many(clients_list).execute()
    Orders.insert_many(orders_list).execute()
    print('--- Database is full ---')
    # ---Over---


def show_db(names):
    if names == 'Clients':
        print('\nNAME\tSITY\tADDRESS')
        query = Clients.select().order_by(Clients.id)
        for row in query:
            print(row.name, row.city, row.address, sep='\t', end='\n')
    elif names == 'Orders':
        print('\nID CLIENTS\t\tDATE\t\t\tAMOUNT\t\tDESCRIPTION')
        query = Orders.select().order_by(Orders.id)
        for row in query:
            print(row.clients.name, row.date, row.amount,
                  row.description, sep='\t\t', end='\n')
    elif names == 'all':
        print('\n-----------TABLE CLIENTS-----------\n')
        print('\nNAME\tSITY\tADDRESS')
        query = Clients.select().order_by(Clients.id)
        for row in query:
            print(row.name, row.city, row.address, sep='\t', end='\n')
        print('\n-----------TABLE ORDERS-----------\n')
        print('\nID CLIENTS\t\tDATE\t\t\tAMOUNT\t\tDESCRIPTION')
        query = Orders.select().order_by(Orders.id)
        for row in query:
            print(row.clients.name, row.date, row.amount,
                  row.description, sep='\t\t', end='\n')


if __name__ == "__main__":
    if len(argv) <= 1:
        print(
            "for create db:\tinit\nfor fill:\tfill\nfor select db:\tshow\nfor start:\tstart")
    else:
        if argv[1] == 'init':
            init_db()
        if argv[1] == 'fill':
            fill_db()
        if argv[1] == 'show':
            if len(argv) <= 2:
                print("tables:\tClients, Orders")
            else:
                show_db(argv[2])
        if argv[1] == "start":
            init_db()
            fill_db()
            show_db(argv[2])
