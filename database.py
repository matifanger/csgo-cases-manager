from tinydb import TinyDB, Query

# save_data [-]
# get_data [X]
# update_data [X]
# search_data []
# GET TABLE [X]

class database:
    def __init__(self):
        self.casesDB = TinyDB(r'F:\PROYECTOS\PYTHON\STEAM-CASES\CASES-TEST\database\bp.json')
        self.User = Query()

    def create_db(self):
        pass

    def check_db(self):
        pass

    def save_data(self, table, data):
        self.get_table = self.casesDB.table(table)
        self.get_table.insert(data)

    def get_data(self, table, data):
        self.get_table = self.casesDB.table(table)
        self.tableresult = self.get_table.get(self.User.link)
        self.tableresult = self.tableresult.get(data)
        return self.tableresult

    def update_data(self, table, data):
        self.get_table = self.casesDB.table(table)
        self.get_table.update(data)

    def search_data(self, object):
        pass