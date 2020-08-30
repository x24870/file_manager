import datetime, os
import py7zr
from send2trash import send2trash

TODAY = datetime.datetime.now().strftime('%Y_%m_%d')

class Extractor():
    def __init__(self):
        cur_folder = os.path.abspath('.')
        self.src_folder = os.path.dirname(cur_folder)
        self.des_folder = os.path.join(cur_folder, TODAY)

    def extract_7z():
        count = 0
        while os.path.exists(des_folder):
            count += 1
            des_folder = os.path.join(cur_folder, TODAY) + '_' + str(count)
        else:
            os.mkdir(des_folder)

        print(f'Extract all .7z files in:\n    {source_folder}\nTo:\n    {des_folder}\n-------------------------------------------------------------------\n', flush=True)

        extracted_files = []
        enum = list( enumerate(os.listdir(source_folder)) )
        for idx, f_name in enum:
            if f_name.endswith('.7z'):
                abs_f_name = os.path.join(source_folder, f_name)
                print(f'Extracing file {idx} of {enum[-1][0]}:', flush=True)
                try:
                    print(f'    {abs_f_name}\n', flush=True)
                    with py7zr.SevenZipFile(abs_f_name, mode='r', password='megamega') as z:
                        z.extractall(des_folder)
                    extracted_files.append(abs_f_name)
                except:
                    print(f'ERROR: error occured when extracting:\n    {abs_f_name}', flush=True)

        for f_to_del in extracted_files:
            if os.path.exists(f_to_del):
                send2trash(f_to_del)
            else:
                print(f'WARNING: The file to be delete not exist:\n    {f_to_del}', flush=True)

        print('DONE')



if __name__ == "__main__":
    pass
    # extract_7z()