# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
import api
import winUser
import controlTypes
from ui import message
from re import search
from os import path
from keyboardHandler import KeyboardInputGesture
from threading import Thread
from time import sleep
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):

	fg = ""
	escape = KeyboardInputGesture.fromName("escape")

	def event_NVDAObject_init(self, obj):
		self.fg = api.getForegroundObject()

	def event_gainFocus(self, obj, nextHandler):
		if obj.name == '' and obj.role == controlTypes.ROLE_DOCUMENT:
			obj.simplePrevious.doAction()
			nextHandler()
		else:
			nextHandler()

	@script(gestures=[f"kb:control+{i}" for i in range(0, 10)])
	def script_status(self, gesture):
		key = -(int(gesture.mainKeyName) + 1)
		try:
			statusObj = self.fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].name
			objName = search(r"Origen.+Destino", statusObj)
			fileName = path.basename(objName[0][8:][:-9])
			progress = search(r"Progreso\:\s\d+", statusObj)
			message("{}; {} porciento".format(fileName, progress[0][10:]))
		except (TypeError, IndexError):
			# Translators: Anuncia que no hay datos
			message(_('Sin datos'))

	@script(
		category="AirExplorer",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de cuentas'),
		gesture="kb:control+shift+c")
	def script_cuentas(self, gesture):
		obj = self.fg.children[0].children[3].children[3].children[3].children[0].children[3].children[5]
		message(obj.name)
		obj.doAction()

	@script(
		category="AirExplorer",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de opciones'),
		gesture="kb:control+shift+o")
	def script_opciones(self, gesture):
		obj = self.fg.children[0].children[3].children[3].children[3].children[0].children[3].children[6]
		message(obj.name)
		obj.doAction()

	@script(
		category="AirExplorer",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se desplaza a la lista de archivos de la carpeta con el foco'),
		gesture="kb:control+rightArrow")
	def script_listFocus(self, gesture):
		focus = api.getFocusObject()
		if focus.role != controlTypes.ROLE_TREEVIEWITEM: return
		ancestors = api.getFocusAncestors()
		for ancestor in reversed(ancestors):
			try:
				if ancestor.next.role == controlTypes.ROLE_WINDOW:
					obj = ancestor.next
					break
			except AttributeError:
				pass
		api.moveMouseToNVDAObject(obj)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)

	@script(
		category="AirExplorer",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se desplaza al árbol de carpetas'),
		gesture="kb:control+leftArrow")
	def script_treeFocus(self, gesture):
		focus = api.getFocusObject()
		if focus.role != controlTypes.ROLE_LISTITEM and focus.role != controlTypes.ROLE_LIST: return
		ancestors = api.getFocusAncestors()
		for ancestor in reversed(ancestors):
			try:
				if ancestor.previous.role == controlTypes.ROLE_WINDOW:
					obj = ancestor.previous
					break
			except AttributeError:
				pass
		api.moveMouseToNVDAObject(obj)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		Thread(target=self.closeEditableText).start()

	def closeEditableText(self):
		sleep(1)
		fc = api.getFocusObject()
		if fc.role == controlTypes.ROLE_EDITABLETEXT:
			self.escape.send()
