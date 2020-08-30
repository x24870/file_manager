import datetime, os, json
import py7zr
from send2trash import send2trash

TODAY = datetime.datetime.now().strftime('%Y_%m_%d')

class Extractor():
    def __init__(self, src_folder, des_folder):
        self.src_folder = src_folder
        self.des_folder = des_folder

    def extract_7z(self):
        count = 0
        targe_folder = os.path.join(self.des_folder, TODAY)
        while os.path.exists(targe_folder):
            count += 1
            targe_folder = os.path.join(self.des_folder, TODAY) + '_' + str(count)
        else:
            os.mkdir(targe_folder)

        print(f'Extract all .7z files in:\n    {self.src_folder}\nTo:\n    {targe_folder}\n-------------------------------------------------------------------\n', flush=True)

        extracted_files = []
        enum = list( enumerate(os.listdir(self.src_folder)) )
        for idx, f_name in enum:
            if f_name.endswith('.7z'):
                abs_f_name = os.path.join(self.src_folder, f_name)
                print(f'Extracing file {idx} of {enum[-1][0]}:', flush=True)
                try:
                    print(f'    {abs_f_name}\n', flush=True)
                    with py7zr.SevenZipFile(abs_f_name, mode='r', password='megamega') as z:
                        z.extractall(targe_folder)
                    extracted_files.append(abs_f_name)
                except:
                    print(f'ERROR: error occured when extracting:\n    {abs_f_name}', flush=True)

        for f_to_del in extracted_files:
            if os.path.exists(f_to_del):
                send2trash(f_to_del)
            else:
                print(f'WARNING: The file to be delete not exist:\n    {f_to_del}', flush=True)

        print('DONE')

def get_folder_and_check(folder_type='source'):
    if folder_type != 'source' and folder_type != 'destination':
        raise Exception('Invalid folder type')
    folder = input(f"Please enter the {folder_type} folder path:\n")
    if not os.path.isdir(folder):
        if folder_type == 'source':
            raise FileExistsError(f"This folder is not exist or valid")
        else:
            create_folder = input("Do you want create this folder?[y/n]")
            if create_folder == 'y':
                try:
                    os.mkdir(des_path)
                except Exception as e:
                    print(e)
            else:
                raise FileExistsError(f"This folder is not exist or valid")

    return folder


def get_src_and_des_path():
    src_path = ''
    des_path = ''

    # read last time record
    try:
        with open(os.path.join('.', '.record')) as record:
            data = json.load(record)
            if os.path.isdir(data['src']): src_path = data['src']
            if os.path.isdir(data['des']): des_path = data['des'] 
    except:
        pass

    # enqury src and des path
    if src_path != '':
        use_recorded_src = input(f"Found last time source folder record:\n{src_path}\nWould you like to use this folder as source?[y/n]\n")
        if use_recorded_src != 'y':
            src_path = get_folder_and_check(folder_type='source')
    else:
        src_path = get_folder_and_check(folder_type='source')

    if des_path != '':
        use_recorded_des = input(f"Found last time destination folder record:\n{src_path}\nWould you like to use this folder as destination?[y/n]\n")
        if use_recorded_des != 'y':
            des_path = get_folder_and_check(folder_type='destination')
    else:
        des_path = get_folder_and_check(folder_type='destination')

    # save current path
    with open(os.path.join('.', '.record'), 'w') as record:
        data = {}
        data['src'] = src_path
        data['des'] = des_path
        json.dump(data, record)

    return (src_path, des_path)

if __name__ == "__main__":
    src_path, des_path = get_src_and_des_path()
    extractor = Extractor(src_path, des_path)
    extractor.extract_7z()