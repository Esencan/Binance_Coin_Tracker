from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from UI_Templates.main_python import Ui_MainWindow
from apps.get_graph import getGraph
from apps.getPredict import getPredict
from apps.findCoins import Find_Coin
from binance.client import Client

class Main(QMainWindow):
	def __init__(self)->None:
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Buttons
		self.ui.pushButton_getgraph.clicked.connect(self.getgraph)
		self.ui.pushButton_addCheckList.clicked.connect(self.addToCheckList)
		self.ui.pushButton_clearList.clicked.connect(self.clearToFile)
		self.ui.pushButton_addFromBinance.clicked.connect(self.addFromBinance)
		self.ui.pushButton_addFromFile.clicked.connect(self.addFromFile)
		self.ui.pushButton_predict.clicked.connect(self.getPredict)
		self.ui.pushButton_recommendCoins.clicked.connect(self.findCoins)
		self.ui.pushButton_clearRecommendCoins.clicked.connect(self.clearRecommendCoins)

		# PyQt Models
		self.model = QStringListModel()
		self.model_result = QStringListModel()

		#Scripts
		self.get_graph = getGraph()
		self.getPredict = getPredict()
		self.findCoins = Find_Coin()

		#Binance Connection
		self.client = Client()


	def getgraph(self):
		# Collect param
		symbol = self.ui.lineEdit_coinsymbol.text()
		period = self.ui.comboBox_period.currentText()
		time_interval_start = self.ui.dateEdit_timeinterval_start.date()
		time_interval_stop = self.ui.dateEdit_timeinterval_stop.date()
		# Control
		if not symbol or not period or not time_interval_start or not time_interval_stop:
			QMessageBox.warning(self, 'Warning...!', 'Please make sure to fill in the Symbol Name, Period and Time Interval fields.')
		else:
			# Convert time format
			time_interval_start = str(time_interval_start.toPyDate().strftime('%d %b, %Y'))
			time_interval_stop = str(time_interval_stop.toPyDate().strftime('%d %b, %Y'))
			# Control selected checkbox
			indicators = self.indicators()

			# Run to function
			self.get_graph.run(symbol, period, time_interval_start, time_interval_stop, "Graph", indicators)

	def addToCheckList(self):
		# Read lineEdit
		text = self.ui.lineEdit_coinsymbol.text()
		# Control
		if not text:
			QMessageBox.warning(self, 'Warning...!', 'Please make sure to fill in the Symbol Name field')
		else:
			# Save to file
			self.saveToFile(text)


	def indicators(self):
		bb = self.ui.checkBox_bb.isChecked()
		sma = self.ui.checkBox_sma.isChecked()
		trends = self.ui.checkBox_trends_lines.isChecked()
		result = [trends, bb, sma]
		return result

	def saveToFile(self, text):
		"""

		:param text: Coming symbol name
		:return:
		"""
		if text:
			# Write to file
			with open('coins.txt', 'a') as file:
				file.write(text + '\n')
		# Update list
		self.updateListView()

	def clearToFile(self):
		dosya_yolu = 'coins.txt'
		# Clear to file
		with open(dosya_yolu, 'w') as dosya:
			pass
		# Update list
		self.updateListView()

	def clearRecommendCoins(self):
		# Clear to listview
		self.model_result.setStringList([])

	def addFromFile(self):
		self.updateListView()

	def addFromBinance(self):

		exchange_info = self.client.get_exchange_info()

		if not exchange_info:
			QMessageBox.warning(self, 'Warning...!', 'An error occurred while retrieving data from Binance.')
		else:
			# Filter
			usdt_symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['symbol'].endswith('USDT') 
					and symbol['status'] == 'TRADING']

			# Symbol sort
			usdt_symbols_sorted = sorted(usdt_symbols)
			# Selection changed to symbol name (lineEdit)
			self.ui.listView_checkCoin.setModel(self.model)
			self.model.setStringList([line.strip() for line in usdt_symbols_sorted])
			self.ui.listView_checkCoin.selectionModel().selectionChanged.connect(self.selection_changed)


	def updateListView(self):
		
		self.ui.listView_checkCoin.setModel(self.model)
		# Read file
		with open('coins.txt', 'r') as file:
			lines = file.readlines()
		# Selection changed to symbol name (lineEdit)
		self.model.setStringList([line.strip() for line in lines])
		self.ui.listView_checkCoin.selectionModel().selectionChanged.connect(self.selection_changed)

	def selection_changed(self, selected, deselected):
		# get index from selected item
		indexes = self.ui.listView_checkCoin.selectedIndexes()
		if indexes:
			# Seçili elemanın değerini al
			selected_value = self.model.data(indexes[0], 0)
			self.ui.lineEdit_coinsymbol.setText(selected_value)

	def selection_changed1(self, selected, deselected):
		# get index from selected item
		indexes1 = self.ui.listView_recommendResult.selectedIndexes()
		if indexes1:
			# Seçili elemanın değerini al
			selected_value = self.model_result.data(indexes1[0], 0)
			self.ui.lineEdit_coinsymbol.setText(selected_value)

	def getPredict(self):
		# Collect param
		symbol = self.ui.lineEdit_coinsymbol.text()
		period = self.ui.comboBox_period.currentText()
		time_interval_start = self.ui.dateEdit_timeinterval_start.date()
		time_interval_stop = self.ui.dateEdit_timeinterval_stop.date()

		# Control
		if not symbol or not period or not time_interval_start or not time_interval_stop:
			QMessageBox.warning(self, 'Warning...!', 'Please make sure to fill in the Symbol Name, Period and Time Interval fields.')
		else:
			time_interval_start = str(time_interval_start.toPyDate().strftime('%d %b, %Y'))
			time_interval_stop = str(time_interval_stop.toPyDate().strftime('%d %b, %Y'))
			predict, ticker = self.getPredict.get_data(symbol, period, time_interval_start, time_interval_stop)
			predict = round(float(predict), 6)
			ticker = round(float(ticker), 6)
			self.ui.lineEdit_lastValue.setText(str(ticker))
			self.ui.lineEdit_predictValue.setText(str(predict))

	def findCoins(self):
		#Collect Param
		symbol_list = self.model.stringList()
		period = self.ui.comboBox_period.currentText()
		daysLength = self.ui.lineEdit_daysLength.text()

		# Control
		if not symbol_list or not period or not daysLength:
			QMessageBox.warning(self, 'Warning...!', 'Please make sure to fill in the Symbol List, Period and Data Length fields.')
		else:
			strong_buy = []
			for name in symbol_list:
				optimum, direnc, destek, value = self.findCoins.run(name, period, daysLength+" "+"day ago UTC")
				print(name, destek, value)
				if value < destek:
					strong_buy.append(name)
					self.ui.listView_recommendResult.setModel(self.model_result)
			self.model_result.setStringList([line.strip() for line in strong_buy])
			if strong_buy:
				self.ui.listView_recommendResult.selectionModel().selectionChanged.connect(self.selection_changed1)

		
		

app = QApplication([])
frame = Main()
frame.show()
app.exec_()
