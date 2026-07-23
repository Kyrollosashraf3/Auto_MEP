from app.config import settings
import os 
import string
import random
import tempfile
class FileBase: 
    
    def __init__(self):
        
        self.settings = settings


        UPLOAD_DIR = os.path.join(tempfile.gettempdir(), settings.TEMP_FOLDER_NAME)

        #self.base_dir = settings.FILE_PATH
        self.base_dir = UPLOAD_DIR
        self.files_dir = os.path.join(
            self. base_dir,
            "assets/files"
        )
        

    def generate_random_string(self, length: int=5):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
