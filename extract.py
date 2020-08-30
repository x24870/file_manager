import datetime, os
import py7zr
from send2trash import send2trash

TODAY = datetime.datetime.now().strftime('%Y_%m_%d')

class Extractor():
    def __init__(self, src_folder, des_folder):
        cur_folder = os.path.abspath('.')
        self.src_folder = src_folder
        self.des_folder = os.path.join(des_folder, TODAY)

    def extract_7z(self):
        count = 0
        while os.path.exists(self.des_folder):
            count += 1
            des_folder = os.path.join(self.des_folder, TODAY) + '_' + str(count)
        else:
            os.mkdir(self.des_folder)

        print(f'Extract all .7z files in:\n    {self.src_folder}\nTo:\n    {self.des_folder}\n-------------------------------------------------------------------\n', flush=True)

        extracted_files = []
        enum = list( enumerate(os.listdir(self.src_folder)) )
        for idx, f_name in enum:
            if f_name.endswith('.7z'):
                abs_f_name = os.path.join(self.src_folder, f_name)
                print(f'Extracing file {idx} of {enum[-1][0]}:', flush=True)
                try:
                    print(f'    {abs_f_name}\n', flush=True)
                    with py7zr.SevenZipFile(abs_f_name, mode='r', password='megamega') as z:
                        z.extractall(self.des_folder)
                    extracted_files.append(abs_f_name)
                except:
                    print(f'ERROR: error occured when extracting:\n    {abs_f_name}', flush=True)

        for f_to_del in extracted_files:
            if os.path.exists(f_to_del):
                send2trash(f_to_del)
            else:
                print(f'WARNING: The file to be delete not exist:\n    {f_to_del}', flush=True)

        print('DONE')

def get_src_and_des_path():
    src_path = input("Please enter the source folder path:\n")
    # assert os.path.isdir(src_path), f"Can not find the folder: {src_path}"
    if not os.path.isdir(src_path):
        print(f"Source folder is not exist or valid")
        return
    
    des_path = input("Please enter the destination folder path:\n")
    if not os.path.isdir(src_path):
        print(f"Destination folder is not exist or valid")
        create_folder = input("Do you want create this folder?[y/n]")
        if create_folder == 'y':
            try:
                os.mkdir(des_path)
            except Exception as e:
                print(e)
                print(f"Error occured when creating folder at:\n{des_path}")
        else:
            return

    return (src_path, des_path)

if __name__ == "__main__":
    src_path, des_path = get_src_and_des_path()
    extractor = Extractor(src_path, des_path)
    extractor.extract_7z()