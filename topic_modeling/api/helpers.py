from unipath import FILES
from json import loads
from config import constants
from .lda import LDA


def load_lda_models(folder_path=constants.lda_models_path):
    """ Load all lda models in given directory """

    return {
        file.name[-8:-6]: LDA(filename=file)
        for file in folder_path.listdir(pattern='lda_??.model', filter=FILES)
    }


def load_ref_messages(filename=constants.ref_messages_path):
    """ Load reference messages from json """

    with open(filename, encoding=constants.load_encoding) as file:
        return loads(file.read())


lda_models = load_lda_models()
ref_messages = load_ref_messages()
