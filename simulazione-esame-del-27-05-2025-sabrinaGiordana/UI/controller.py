import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = 0


    def fillDDYear(self):
        anni = self._model.getAnni()
        for anno in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(anno['year']))

        self._view.update_page()

    def handleCreaGrafo(self,e):
        self._anno = self._view._ddAnno.value
        self._model.builtGraph(self._anno)
        self._view.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi {self._model.numNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi {self._model.numArchi()}"))

        self._view.update_page()

        self._model.trovaMigliorPilota()
        self._view.txt_result.controls.append(ft.Text(f"Best Driver {self._model._bestPilota}, with score {self._model._bestDiff}"))
        self._view.update_page()


    def readDDAnno(self, e):
        if e.control.value is None:
            self._anno = None
        else:
            self._anno = e.control.data
        print(f"anno selezionato -- {self._anno}")

    def handleCerca(self, e):
        num = int(self._view._txtIntK.value)
        if num is None or num<=0 :
            self._view.txt_result.controls.append(ft.Text("Inserire un numero valido", color="red"))

        self._bestPath, self._bestScore = self._model.getDreamTeam(num)
        self._view.txt_result.controls.append(ft.Text(f"Il tuo dream team è composto da {num} piloti:"))

        for pil in self._bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{pil}"))

        self._view.txt_result.controls.append(ft.Text(f"Con tasso totale di sconfitta pari a {self._bestScore}"))

        self._view.update_page()