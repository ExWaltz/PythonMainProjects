import json


class Todo:
    """ Number 2 of my: Let's make 9 python apps
        All projects are at https://github.com/ExWaltz/PythonMainProjects

        title = Title of todo
        *do = The things you need to do

        # Future Improvement:
            * Improve names
    """
    __slots__ = ['title', 'items', 'data']  # to improve perfromance

    def __init__(self, title, *do):
        self.title = title
        self.items = {}
        for e in do:
            e = str(e).lower()
            self.items[e] = False
        self.data = {self.title: self.items}

    def new(self, *do):
        """ Make a new Todo
            *do must be str
        """
        for e in do:
            e = e.lower()
            self.items[e] = False
        self.data = {self.title: self.items}

    def _switchdo(self, do, status=False):
        """Set todo items to True or False"""
        doarg = [str(e).lower() for e in do]    # tuple to list
        for doA in doarg:
            if doA in self.items:
                self.items[doA] = status    # Update do items
        self.data = {self.title: self.items}    # Update data

    def done(self, *do):
        """Set todo items to True"""
        self._switchdo(do, status=True)     # Set do items to Done(True)

    def notdone(self, *do):
        """Set todo items to False"""
        self._switchdo(do, status=False)    # Set do items to Unfinished(False)

    def delete(self, *do):
        """Delete todo items"""
        doarg = [str(e).lower() for e in do]    # tuple to list
        for doA in doarg:
            if doA in self.items:
                del self.items[doA]     # Delete do item(s)
        self.data = {self.title: self.items}    # Update data

    def save(self, filedir):
        """Save Todo items"""
        filedir = self._fileFormat(filedir)     # Check if filename has .todo extension
        sFile = open(filedir, "w", encoding="utf-8")
        dJsn = json.dumps(self.data)
        jsn = json.loads(dJsn)
        json.dump(jsn, sFile, indent=2)     # Save data into json format
        sFile.close()

    @staticmethod
    def open(filedir):
        """Open an existing Todo file"""
        filedir = Todo._fileFormat(filedir)
        sFile = open(filedir, "r", encoding="utf-8")
        jsn = json.loads(sFile.read())
        title = list(jsn.keys())[0]
        dos = jsn[title]
        key = list(dos.values())
        values = list(dos.keys())
        # Recreate Todo list
        td = Todo(title, values[0])
        td._switchdo((values[0],), key[0])
        for k, v in zip(key[1:], values[1:]):
            td.new(v)
            td._switchdo((v,), k)
        return td

    @ staticmethod
    def _fileFormat(fname):
        """Check if file ends with .todo extension"""
        lowFname = str(fname).lower()
        if str(lowFname).endswith(".todo"):
            return fname
        return f"{fname}.todo"

    def __str__(self):
        """String version of Todo"""
        compileInfo = f"{self.title}: \n"
        for k, v in self.items.items():
            fv = str(v).replace("True", "X").replace("False", " ")
            compileInfo = compileInfo + f"\t[{fv}] : "
            compileInfo = compileInfo + str(k) + "\n"
        return compileInfo

if name ==
