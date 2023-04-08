import os, magic
#from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import PyMuPDFLoader


class pdfLoader:
    pdfFilePaths = []
    dataIndex = []

    def __init__(self, path=None, recurse=False, symlinks=True):
        self.path       = path
        self.recurse    = recurse    # if path is a directory, whether or not to recurse into subdirectories
        self.symlinks   = symlinks   # changes whether or not we resolve symlinks

        print("pdfLoader_init(): successfully initialized pdfLoader class")

    def queueFile(self, filePath=None):
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

    def processDirectory(self, dirPath=None):
        for file in os.listdir(dirPath):
            filePath = os.path.join((dirPath), file)

            if os.path.isfile(filePath):
                self.queueFile(filePath)

            if os.path.isdir(filePath):
                if self.recurse:
                    self.processDirectory(filePath)
                else:
                    print("pdfLoader_processDirectory: skipping directory " + filePath)

        return True

    def process(self, processPath=None):
        ret = False

        if processPath is None:
            print("pdfLoader_process(): invalid path or path not set - unable to continue")
            return False

        if os.path.isfile(processPath):
            ret = self.queueFile(processPath)

        if os.path.isdir(processPath):
            ret = self.processDirectory(processPath)

        return ret

    def processQueue(self):
        if self.pdfFilePaths is []:
            print("pdfLoader_processQueue: empty queue - call process() first")
            return False

        for file in self.pdfFilePaths:
            try:
                loader = PyMuPDFLoader(file)
                data = loader.load()

                self.dataIndex.extend(data)
                
            except Exception as error:
                print("pdfLoader_processQueue: " + file + ":" + str(error))
                pass

        return True


