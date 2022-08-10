# Selection UI window for importing CSV files
import carb
from omni.kit.window.file_importer import get_file_importer
import os.path
from pathlib import Path
# external python lib
import csv
import itertools


#This class is designed to import data from 3 input files 
#This file acts like a data provider for the data_manager

class OfflineDataManager():
    def __init__(self):

        # limit the number of rows read
        self.max_elements = 5000

        self._sub_csv_file_path = ""
        self._rg_csv_file_path = ""
        self._rs_csv_file_path = ""

        #datasets
        self._subscriptions = {}
        self._groups = {}
        self._resources = {}            

    #Load all the data
    def loadFiles(self):
        self.load_rg_file(self)
        self.load_res_file(self)
        self.load_sub_file(self)

    #Resource Groups File Import
    #NAME,SUBSCRIPTION,LOCATION
    def load_rg_file(self):
        if os.path.exists(self._rg_csv_file_path):
            # Read CSV file
            with open(self._rg_csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    name = row["NAME"]
                    subs = row["SUBSCRIPTION"]
                    location = row["LOCATION"]


    #Resources File Import
    #NAME,TYPE,RESOURCE GROUP,LOCATION,SUBSCRIPTION
    def load_res_file(self):
         # check that CSV exists
        if os.path.exists(self._rs_csv_file_path):
            # Read CSV file
            with open(self._rs_csv_file_path) as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    name = row["NAME"]
                    type = row["TYPE"]
                    group = row["RESOURCE GROUP"]
                    location = row["LOCATION"]
                    subscription = row["SUBSCRIPTION"]

    #Subscription / AAD Info File Import (need a file)
    def load_sub_file(self):
        print("Load")
        #todo


    # Handles the click of the Load button
    def select_file(self, fileType: str):
        self.file_importer = get_file_importer()

        if fileType == "sub":
            self.file_importer.show_window(
                title="Select a CSV File",
                import_button_label="Select",
                import_handler=self._on_click_sub_open,
                file_extension_types=[(".csv", "CSV Files (*.csv)")],
                file_filter_handler=self._on_filter_item
                )

        if fileType == "rg":
            self.file_importer.show_window(
                title="Select a CSV File",
                import_button_label="Select",
                import_handler=self._on_click_rg_open,
                file_extension_types=[(".csv", "CSV Files (*.csv)")],
                file_filter_handler=self._on_filter_item
                )

        if fileType == "res":
            self.file_importer.show_window(
                title="Select a CSV File",
                import_button_label="Select",
                import_handler=self._on_click_res_open,
                file_extension_types=[(".csv", "CSV Files (*.csv)")],
                file_filter_handler=self._on_filter_item
                )                

    # Handles the click of the open button within the file importer dialog
    def _on_click_rg_open(self, filename: str, dirname: str, selections):
        
        # File name should not be empty.
        filename = filename.strip()
        if not filename:
            carb.log_warn(f"Filename must be provided.")
            return

        # create the full path to csv file
        if dirname:
            fullpath = f"{dirname}{filename}"
        else:
            fullpath = filename

        self.rg_csv_file_path = fullpath
        self.rg_csv_field_model.set_value(str(fullpath))

    # Handles the click of the open button within the file importer dialog
    def _on_click_res_open(self, filename: str, dirname: str, selections):
        
        # File name should not be empty.
        filename = filename.strip()
        if not filename:
            carb.log_warn(f"Filename must be provided.")
            return

        # create the full path to csv file
        if dirname:
            fullpath = f"{dirname}{filename}"
        else:
            fullpath = filename

        self.rs_csv_file_path = fullpath
        self.rs_csv_field_model.set_value(str(fullpath))

    # Handles the click of the open button within the file importer dialog
    def _on_click_sub_open(self, filename: str, dirname: str, selections):
        
        # File name should not be empty.
        filename = filename.strip()
        if not filename:
            carb.log_warn(f"Filename must be provided.")
            return

        # create the full path to csv file
        if dirname:
            fullpath = f"{dirname}{filename}"
        else:
            fullpath = filename

        self._sub_csv_file_path = fullpath
        self.sub_csv_field_model.set_value(str(fullpath))


    # Handles the filtering of files within the file importer dialog
    def _on_filter_item(self, filename: str, filter_postfix: str, filter_ext: str) -> bool:
        if not filename:
            return True
        # Show only .csv files
        _, ext = os.path.splitext(filename)
        if ext == filter_ext:
            return True
        else:
            return False