import copy
import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        if self._view._txtInDurata.value is None:
            self._view.create_alert("Inserire una durata")
            return

        try:
            dTot = int(self._view._txtInDurata.value) * 60 * 1000
        except ValueError:
            self._view.create_alert("Inserire un intero")
            return

        self._model.buildGraph(dTot)
        nN, nE = self._model.getGraphSize()

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))

        album = self._model.nodes
        for a in album:
            self._view._ddAlbum.options.append(ft.dropdown.Option(data=a, text=a.Title, on_click=self.getSelectedAlbum))

        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._choicheAlbum = None
        else:
            self._choicheAlbum = e.control.data

    def handleAnalisiComp(self, e):
        if self._choicheAlbum is None:
            self._view.create_alert("Scegliere un album")
            return
        dimensione, durata = self._model.getConnessa(self._choicheAlbum)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Dimensione componente connessa: {dimensione}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata componente: {durata/60000}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        if self._choicheAlbum is None:
            self._view.create_alert("Scegliere un album")
            return


        try:
            dTot = int(self._view._txtInSoglia.value)*60000
        except ValueError:
            self._view.create_alert("Inserire una durata intera")
            return

        bestSet = self._model.getBestSet(self._choicheAlbum, dTot)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Set migliore formato da {len(bestSet)} brani"))
        for i in bestSet:
            self._view.txt_result.controls.append(ft.Text(f"{i.Title}"))

        self._view.update_page()

