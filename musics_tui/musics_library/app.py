from typing import Callable, Any

import pwinput
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from musics_library.domain import Username, Password, Name, Artist, RecordCompany, Genre, EANCode, Price, CD, \
    ID
from musics_library.exceptions import AppException
from musics_library.menu import Menu, Entry, Description
from musics_library.services import AuthenticationService, CDLibrary
from dotenv import load_dotenv
import os
load_dotenv()

music_website= os.getenv('MUSIC_WEBSITE')


class App:
    def __init__(self):
        self.login_service = AuthenticationService()
        self.authenticated_user = None
        self.music_library = CDLibrary()
        self.menu = self.__create_menu()
        self.console = Console()

    def __create_menu(self):
        menu_builder = Menu.Builder(
            Description("Music Library"), auto_select=lambda: self.__invite_to_register_to_anonymous_user()) \
            .with_entry(
                Entry.create('1', 'Add CD', on_selected=lambda: self.__add_cd())) \
            .with_entry(
                Entry.create('2', 'Remove CD', on_selected=lambda: self.__remove_cd())) \
            .with_entry(
                Entry.create('3', 'Update a CD', on_selected=lambda: self.__update_cd())) \
            .with_entry(
                Entry.create('4', 'Get all CDs by Publisher', on_selected=lambda: self.__print_cds_by_published_by())) \
            .with_entry(
                Entry.create('5', 'Get all CDs by CD Name', on_selected=lambda: self.__print_cds_by_cd_name())) \
            .with_entry(
                Entry.create('6', 'Get all CDs by Artist', on_selected=lambda: self.__print_cds_by_artist())) \
            .with_entry(
                Entry.create('7', 'Get all CDs', on_selected=lambda: self.__print_all_cds()))

        if self.authenticated_user:
            menu_builder.with_entry(
                Entry.create('8', 'Logout', on_selected=lambda: self.__logout()))
        else:
            menu_builder.with_entry(
                Entry.create('8', 'Login', on_selected=lambda: self.__login()))

        menu_builder.with_entry(
            Entry.create('0', 'Exit', on_selected=lambda:self.__exit(), is_exit=True))
        return menu_builder.build()

    def __exit(self):
        y_or_n = Confirm.ask("Are you sure?")
        if y_or_n:
            self.console.print(Text().append("Music Library says you Goodbye!", style="bold cyan"))
            self.authenticated_user = None

    def __invite_to_register_to_anonymous_user(self):
        if self.authenticated_user is None:
            self.console.print(f"If you want to register an account into Music Library you can go here, {music_website}")

    def __print_welcome(self) -> None:
        self.console.print("*** Welcome to ***")

    def __add_cd(self):
        if self.authenticated_user == None:
            raise AppException("You must be logged.")
        if not self.authenticated_user.is_authorized:
            raise AppException(f"You must be publisher, register as publisher on {music_website}.")
        cd = CD(*self.__read_cd_for_add())
        y_or_n = Confirm.ask("Are you sure?")
        if y_or_n:
            self.music_library.add_cd(cd, self.authenticated_user)
        else:
            self.console.print("Music not added")

    def __update_cd(self):
        if self.authenticated_user == None:
            raise AppException("You must be logged.")
        if not self.authenticated_user.is_authorized:
            raise AppException(f"You must be publisher, register on {music_website}.")
        cd_id = self.__read('ID', ID.parse)
        cd = self.music_library.cd(cd_id)
        self.__create_and_print_table_with_single_cd(cd)
        print("*** Leave the field blank if you don't want update an attribute. ***")
        cd_fields = self.__read_cd_for_update(cd)
        y_or_n = Confirm.ask("Are you sure?")
        if y_or_n:
            cd_updated = CD(id=cd_id, name=cd_fields[0], artist=cd_fields[1], record_company=cd_fields[2],
                       genre=cd_fields[3], ean_code=cd_fields[4], price=cd_fields[5])
            self.music_library.update_cd(cd_updated, self.authenticated_user)
        else:
            self.console.print("Record will not be updated.")

    def __remove_cd(self):
        if self.authenticated_user == None:
            raise AppException("You must be logged.")
        if not self.authenticated_user.is_authorized:
            raise AppException(f"You must be publisher, register on {music_website}.")
        cd_id = self.__read('ID', ID.parse)
        cd = self.music_library.cd(cd_id)

        self.__create_and_print_table_with_single_cd(cd)

        y_or_n = Confirm.ask("Are you sure that you want delete this record?")
        if y_or_n:
            self.music_library.remove_cd(cd_id, self.authenticated_user)
        else:
            self.console.print("Record will not be deleted.")

    def __create_and_print_table_with_single_cd(self, cd):
        table = Table(title="CD " + str(cd.id))
        columns = ['#', 'NAME', 'ARTIST', 'RECORD COMPANY', 'GENRE', 'EANCODE', 'PRICE', 'PUBLISHED BY',
                   'CREATED AT', 'UPDATED AT']
        for col in columns:
            table.add_column(col, justify="center", style="cyan")

        table.add_row(str(cd.id.value), cd.name.value, cd.artist.value, cd.record_company.value, cd.genre.value,
                      cd.ean_code.value, str(cd.price), cd.published_by.value, cd.createdat, cd.updatedat)

        self.console.print(table)

    def __create_and_print_table_with_list_of_cd(self, cds):
        table = Table(title="CDs")
        columns = ['#', 'NAME', 'ARTIST', 'RECORD COMPANY', 'GENRE', 'EANCODE', 'PRICE', 'PUBLISHED BY',
                   'CREATED AT', 'UPDATED AT']
        for col in columns:
            table.add_column(col, justify="center", style="cyan")

        for cd in cds:
            table.add_row(str(cd.id.value), cd.name.value, cd.artist.value, cd.record_company.value, cd.genre.value,
                          cd.ean_code.value, str(cd.price),
                          cd.published_by.value, cd.createdat, cd.updatedat)
        self.console.print(table)

    def __print_cds_by_artist(self):
        artist = self.__read('Artist', Artist)
        cds = self.music_library.cds_by_artist(artist)
        self.__create_and_print_table_with_list_of_cd(cds)

    def __print_cds_by_published_by(self):
        published_by = self.__read('Username', Username)
        cds = self.music_library.cds_by_published_by(published_by)
        self.__create_and_print_table_with_list_of_cd(cds)

    def __print_cds_by_cd_name(self):
        cd_name = self.__read('CD Name', Name)
        cds = self.music_library.cds_by_cd_name(cd_name)
        self.__create_and_print_table_with_list_of_cd(cds)

    def __print_all_cds(self) -> None:
        cds = self.music_library.cds()
        self.__create_and_print_table_with_list_of_cd(cds)

    def __read_cd_for_update(self, cd: CD):
        name = self.__read_for_update("Name", cd.name.value, Name)
        artist = self.__read_for_update("Artist", cd.artist.value, Artist)
        record_company = self.__read_for_update("Record Company", cd.record_company.value, RecordCompany)
        genre = self.__read_for_update("Genre", cd.genre.value, Genre)
        ean_code = self.__read_for_update("EANCode", cd.ean_code.value, EANCode)
        price = self.__read_for_update("Price", str(cd.price), Price.parse)
        return name, artist, record_company, genre, ean_code, price

    def __read_cd_for_add(self):
        name = self.__read("Name", Name)
        artist = self.__read("Artist", Artist)
        record_company = self.__read("Record Company", RecordCompany)
        genre = self.__read("Genre", Genre)
        ean_code = self.__read("EANCode", EANCode)
        price = self.__read("Price", Price.parse)
        return name, artist, record_company, genre, ean_code, price

    def __read_user(self):
        user = self.__read('Username', Username)
        password = self.__read_password(Password)
        return user, password

    def __login(self):
        username, password = self.__read_user()
        self.authenticated_user = self.login_service.login(username, password)
        print_sep = lambda: self.console.print("*" * len("Welcome ") + "*" * len(self.authenticated_user.username.value))
        print_sep()
        self.console.print(Text().append("Welcome " + self.authenticated_user.username.value, style="bold cyan"))
        print_sep()
        self.__rerun_menu()

    def __logout(self):
        y_or_n = Confirm.ask("Are you sure that you want to logout?")
        if y_or_n:
            self.login_service.logout(self.authenticated_user)
            self.authenticated_user = None
            self.__rerun_menu()

    def __rerun_menu(self):
        self.menu.stop()
        self.menu = self.__create_menu()
        self.menu.run()

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = Prompt.ask(f'{prompt} ')
                res = builder(line.strip())
                return res
            except:
                print("Error")

    @staticmethod
    def __read_password(builder):
        while True:
            try:
                line = pwinput.pwinput(prompt='Password : ', mask='*')
                res = builder(line.strip())
                return res
            except:
                print("Error")

    @staticmethod
    def __read_for_update(prompt: str, default: str, builder: Callable) -> Any:
        while True:
            try:
                line = Prompt.ask(f'{prompt} ', default=default)
                res = builder(line.strip())
                return res
            except:
                print("Error")

    def __run(self) -> None:
        try:
            self.__print_welcome()
        except:
            print('App Error')
        self.menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except(Exception) as a:
            print('Panic error!')


