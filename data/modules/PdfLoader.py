import os, magic

from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter

class pdfLoader:
    pdfFilePaths    = []
    documentIndex   = []

    def __init__(self, persistdb=None, path=None, recurse=True, symlinks=True):
        self.path       = path
        self.recurse    = recurse    # if path is a directory, whether or not to recurse into subdirectories
        self.symlinks   = symlinks   # changes whether or not we resolve symlinks
        self.persistdb  = persistdb  # persistent memory store, for now Chroma/DuckDB

        print("pdfLoader_init(): successfully initialized pdfLoader class")

    def queueFile(self, filePath=None):
        if filePath is None:
            filePath = self.path

        if self.symlinks:
            filePath = os.path.realpath(filePath)

        if filePath.endswith(".pdf"):
            # Check the application/mimetype of the provided file with the 'magic' library
            fileType = magic.from_file(filePath, mime=True)

            if fileType == "application/pdf":
                self.pdfFilePaths.append(filePath)
            else:
                print("pdfLoader_queueFile: " + filePath + ":" + fileType + " - skipping")
                return False

        return True

    def queueDirectory(self, dirPath=None):
        if dirPath is None:
            dirPath = self.path

        for file in os.listdir(dirPath):
            filePath = os.path.join((dirPath), file)

            if os.path.isfile(filePath):
                self.queueFile(filePath)

            if os.path.isdir(filePath):
                if self.recurse:
                    self.queueDirectory(filePath)
                else:
                    print("pdfLoader_queueDirectory: skipping directory " + filePath)

        return True

    def addPathToQueue(self, processPath=None):
        ret = False

        if processPath is None:
            print("pdfLoader_addToQueue(): invalid path or path not set - unable to continue")
            return False

        if os.path.isfile(processPath):
            ret = self.queueFile(processPath)

        if os.path.isdir(processPath):
            ret = self.queueDirectory(processPath)

        return ret

    def processQueue(self):
        if self.pdfFilePaths is []:
            print("pdfLoader_processQueue: empty queue - call process() first")
            return False

        for file in self.pdfFilePaths:
            print("pdfLoader_processQueue: processing " + file)
            try:
                loader = PyMuPDFLoader(file)
                data = loader.load()

                self.persistdb.add_documents(data)
                
            except Exception as error:
                print("  ~> " + file + ": " + str(error))
                continue

        return True

    def emptyQueue(self):
        self.dataIndex = []
        self.pdfFilePaths = []
        print("pdfLoader_emptyQueue: emptied queue")
        return

    def storeQueue(self):
        if self.documentIndex is []:
            print("pdfLoader_storeQueue: no documents loaded into index - run processQueue() first")
            return False
        self.persistdb.persist()

