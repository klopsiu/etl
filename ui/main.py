import tkinter as tk
import requests
import csv
import json
import ast
import json2table
import os

# api_get = 'https://michal-tests.cledar.pl/api/data'
# json_data = requests.get(api_get).json()

os.environ['NO_PROXY'] = '127.0.0.1'

def do_nothing():
    pass

def extract():
    print(requests.get('http://127.0.0.1:7676/api/extract').json())

def transform():
    print(requests.get('http://127.0.0.1:7676/api/transform').json())

def load():
    print(requests.get('http://127.0.0.1:7676/api/load').json())


def saveToFile():
    response = requests.get('http://127.0.0.1:7676/api/data').json()

    with open('output.json', 'w') as f:
        json.dump(response, f)

def data():
    print(requests.get('http://127.0.0.1:7676/api/data').json())

def etl():
    requests.get('http://127.0.0.1:7676/api/extract').json()
    requests.get('http://127.0.0.1:7676/api/transform').json()
    requests.get('http://127.0.0.1:7676/api/load').json()
    print(requests.get('http://127.0.0.1:7676/api/data').json())


def delete():
    print(requests.delete('http://127.0.0.1:7676/api/data').json())


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("LTS PROCESS")
        self.selected = tk.IntVar()
        self.selected.set(0)

        self.rad1 = tk.Radiobutton(self, text='EXTRACT', value=1, variable=self.selected)
        self.rad2 = tk.Radiobutton(self, text='TRANSFORM', value=2, variable=self.selected)
        self.rad3 = tk.Radiobutton(self, text='LOAD', value=3, variable=self.selected)
        self.rad4 = tk.Radiobutton(self, text='ETL', value=4, variable=self.selected)
        self.rad5 = tk.Radiobutton(self, text='DELETE', value=5, variable=self.selected)
        self.rad6 = tk.Radiobutton(self, text='DATA', value=6, variable=self.selected)
        self.rad7 = tk.Radiobutton(self, text='SAVE TO FILE', value=7, variable=self.selected)


        self.button1 = tk.Button(self, text="Select", command=self.clicked)
        self.button2 = tk.Button(self, text="Quit", command=self.destroy)

        self.rad1.grid(column=0, row=0)
        self.rad2.grid(column=0, row=1)
        self.rad3.grid(column=0, row=2)
        self.rad4.grid(column=0, row=3)
        self.rad5.grid(column=0, row=4)
        self.rad6.grid(column=0, row=5)
        self.rad7.grid(column=0, row=6)
        self.button1.grid(column=6, row=0)
        self.button2.grid(column=6, row=1)


        self.mainloop()

    def clicked(self):

        v = self.selected.get()
        if v == 0:
            do_nothing()
        elif v == 1:
            extract()
        elif v == 2:
            transform()
        elif v == 3:
            load()
        elif v == 4:
            etl()
        elif v == 5:
            delete()
        elif v == 6:
            data()
        elif v == 7:
            saveToFile()
        else:
            print('an error occurred, the wrong value was received')


GUI()
