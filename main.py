#-*- coding: utf-8 -*-
from kivy.app import App
from ipaddress import IPv4Address

import routeros_api
from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty

class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message

class ScreenApp(App):

    def addALL(self):
        global ip
        def getipAddress(server):
            connection = routeros_api.RouterOsApiPool(server, username='admin', password='pwd.farm')
            api = connection.get_api()
            list_address = api.get_resource('/ip/firewall/address-list')
            address = list_address.get()[-1]['address']
            ip = IPv4Address(str(address)) + 1
            return str(ip)

        @mainthread
        def addListAddress(server):

            connection = routeros_api.RouterOsApiPool(server, username='admin', password='pwd.farm')
            try:
                api = connection.get_api()
                list_address = api.get_resource('/ip/firewall/address-list')
                try:
                    print(ip)
                    list_address.add(address=ip, comment=self.root.ids.desc_address.text, list="Liberados")
                    connection.disconnect()
                except routeros_api.exceptions.RouterOsApiCommunicationError:
                    self.root.ids.status_send.text = "O IP já existe na lista!\n"
            except routeros_api.exceptions.RouterOsApiConnectionError:
                self.root.ids.status_send.text = "Não está online ou dados incorretos!\n"

        @mainthread
        def addDHCP(server):
            connection = routeros_api.RouterOsApiPool(server, username='admin', password='pwd.farm', port=8727)
            try:
                api = connection.get_api()
                add_dhcp = api.get_resource('/ip/dhcp-server/lease')
                try:
                    print(ip)
                    add_dhcp.add(address=ip, comment=self.root.ids.desc_address.text,
                                 mac_address=self.root.ids.mac_address.text, server='server1')
                    connection.disconnect()
                except routeros_api.exceptions.RouterOsApiCommunicationError:
                    self.root.ids.status_send.text = "Mac já existente na lista!\n"
            except routeros_api.exceptions.RouterOsApiConnectionError:
                self.root.ids.status_send.text = "Não está online ou dados incorretos!\n"

        @mainthread
        def addAcessList(server):
            connection = routeros_api.RouterOsApiPool(server, username='admin', password='pwd.farm', port=8727)
            try:
                api = connection.get_api()
                add_acesslist = api.get_resource('interface/wireless/access-list')
                try:
                    add_acesslist.add(comment=self.root.ids.desc_address.text, interface='wlan2-WIFI-CAMPO',
                                      mac_address=self.root.ids.mac_address.text)
                    connection.disconnect()
                except routeros_api.exceptions.RouterOsApiCommunicationError:
                    self.root.ids.status_send.text = "Mac já existente na lista!\n"
            except routeros_api.exceptions.RouterOsApiConnectionError:
                self.root.ids.status_send.text = "Não está online ou dados incorretos!\n"

        hosts = ['170.82.116.10', '170.82.116.110', '170.82.116.2', '170.82.116.130']
        for host in hosts:
            try:
                ip = getipAddress(host)
                print(ip)
                break
            except:
                pass

        if self.root.ids.address_server.text == "TODOS":
            addListAddress('170.82.116.10')
            addListAddress('170.82.116.110')
            addListAddress('170.82.116.2')
            addListAddress('170.82.116.130')
            addDHCP('170.82.116.10')
            addDHCP('170.82.116.110')
            addDHCP('170.82.116.2')
            addDHCP('170.82.116.130')
            addAcessList('170.82.116.10')
            addAcessList('170.82.116.110')
            addAcessList('170.82.116.2')
            addAcessList('170.82.116.130')
        elif self.root.ids.address_server.text == "Frente 1A":
            addListAddress('170.82.116.10')
            addDHCP('170.82.116.10')
            addAcessList('170.82.116.10')
        elif self.root.ids.address_server.text == "Frente 1B":
            addListAddress('170.82.116.110')
            addDHCP('170.82.116.110')
            addAcessList('170.82.116.110')
        elif self.root.ids.address_server.text == "Frente 3":
            addListAddress('170.82.116.2')
            addDHCP('170.82.116.2')
            addAcessList('170.82.116.2')
        else:
            addListAddress('170.82.116.130')
            addDHCP('170.82.116.130')
            addAcessList('170.82.116.130')

if __name__ == '__main__':
    ScreenApp().run()