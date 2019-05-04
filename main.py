import pickle
import sqlite3
import re

from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from random import randint

class MenuScreen(Screen):
        pass

class SearchScreen(Screen):
        def suggest(self, reçu):
            if reçu:
                r = re.compile(r".*{}.*".format(reçu[1]))
                suggestion = list(filter(r.match, total_trajet))
                if len(suggestion)>5:
                    for i in range(5):
                        print(suggestion[i])
                elif len(suggestion)>0 and len(suggestion)<5:
                    for i in range(len(suggestion)):
                        print(suggestion[i])
           

        def status(self):
                allowed_bus = self.ids.allowed_bus
                allowed_bus.clear_widgets()
                self.depart = self.ids.txt1.text
                self.arrivee = self.ids.txt2.text
                if self.depart!="" or self.arrivee!="":
                    cur_tata.execute("select numero from tata where trajet regexp ? and trajet regexp ?",(self.depart, self.arrivee))
                    cur_ddd.execute("select numero from ddd where trajet regexp ? and trajet regexp ?",(self.depart, self.arrivee))
                    self.liste_tata = cur_tata.fetchall()
                    self.liste_ddd = cur_ddd.fetchall()
                    for bus in self.liste_tata:
                        self.chemin = Label(bold=True, text="TATA {}".format(bus[0]))
                        self.chemin.color = [0,255,0,1]
                        allowed_bus.add_widget(self.chemin)
                    for bus in self.liste_ddd:
                        self.chemin = Label(bold=True, text="DDD {}".format(bus[0]))
                        self.chemin.color = [0,255,0,1]
                        allowed_bus.add_widget(self.chemin)
                self.try_combinaison()



        def try_combinaison(self):
            self.popup = Popup(title="Combinaison De Bus", size_hint=(.6,.3))
            popBox = BoxLayout(orientation="vertical")
            popScroll = ScrollView(size_hint=(1,None))
            popGrid = GridLayout(cols=1, row_default_height=30, size_hint_y=None)
            co1_tata = cur_tata.execute("""select numero,trajet from tata where trajet regexp ?\
             and trajet not regexp ?""",(self.depart,self.arrivee)).fetchall()
            co2_tata = cur_tata.execute("""select numero,trajet from tata where trajet regexp ?\
             and trajet not regexp ?""",(self.arrivee, self.depart)).fetchall()

            co1_ddd = cur_ddd.execute("""select numero,trajet from ddd where trajet regexp ?\
                and trajet not regexp ?""",(self.depart,self.arrivee)).fetchall()
            co2_ddd = cur_ddd.execute("""select numero,trajet from ddd where trajet regexp ?\
                and trajet not regexp ?""",(self.arrivee,self.depart)).fetchall()
            
            popGrid.add_widget(Label(text="TATA", font_size=10))
            for bus1 in co1_tata:
                for bus2 in co2_tata:
                    k = set(bus1[1]).intersection(set(bus2[1]))
                    if k:
                        popGrid.add_widget(Label(text='{}'.format(str(bus1[0])+" <> "+str(bus2[0]))))

            popGrid.add_widget(Label(text="DDD", font_size=10))
            for bus1 in co1_ddd:
                for bus2 in co2_ddd:
                    k = set(bus1[1]).intersection(set(bus2[1]))
                    if k:
                        popGrid.add_widget(Label(text='{}'.format(str(bus1[0])+" <> "+str(bus2[0]))))

            if popGrid.cols>=1:
                self.ids.combine.opacity=1
                popScroll.add_widget(popGrid)
                popBox.add_widget(popScroll)
                self.popup.content = popBox
            else:
                self.ids.combine.opacity=0

        def show_popup(self):
            self.popup.open()

class TrajectoryScreen(Screen):
    # def on_pre_enter(self):
    #     self.y_pos = self.height*.17
    #     self.font_size = self.width*.01
    #     test = total_tata[4]
    #     for chemin in test[1].split("==>"):
    #         mylab = CLabel(font_size=self.font_size, text="{}".format(chemin))
    #         mylab.y = self.y_pos
    #         self.ids.lay.add_widget(mylab)
    #         self.y_pos-=30
    #         self.font_size += 3
    pass



class ReseauScreen(Screen):
    def on_pre_enter(self):
        for bus in total_tata:
            bouton = CButton(text="{}".format("TATA N° "+str(bus[0])))
            self.ids.grid1.add_widget(bouton)

        for bus in total_ddd:
            bouton = CButton(text="{}".format("DDD N° "+str(bus[0])))
            self.ids.grid2.add_widget(bouton)


class CButton(Button):
    pass

class CLabel(Label):
    pass


class ScreenManagement(ScreenManager):
        pass


presentation = ScreenManager()
class MainApp(App):
        def buid(self):
            print(presentation.screens)
            return presentation


def load_data():
        def regexp(pat, data):
                reg = re.compile(pat, re.IGNORECASE)
                return reg.search(data) is not None

        tata = sqlite3.connect("Tata.db")
        cur1 = tata.cursor()
        ddd = sqlite3.connect("Ddd.db")
        cur2 = ddd.cursor()

        tata.create_function("regexp", 2, regexp)
        ddd.create_function("regexp", 2, regexp)

        return cur1, cur2


if __name__ == "__main__":
        with open("total_trajet.txt", "rb") as file1:
            total_trajet = pickle.load(file1)
        try:
            cur_tata, cur_ddd = load_data()
            print("Database Connected!")
        except:
            print("Connection with database failed")

        total_tata = cur_tata.execute("select numero, trajet from tata").fetchall()
        total_ddd = cur_ddd.execute("select numero, trajet from ddd").fetchall()
        MainApp().run()