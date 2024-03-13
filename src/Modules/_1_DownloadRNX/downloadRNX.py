# Libraries
from ftplib import FTP_TLS
import os
import hatanaka
from pathlib import Path

# A class that retrieves RNX files from a particular data service
class DownloadRNX:
    """
    The class uses a designated center that stores observations of Global Navigation Satellite Systems.
    It downloads the files in .gz format, which it then unpacks into .crx (hatanaka) format, and then releases
    the already available .rnx format.

    save_path - path to save data,
    host - link to data center,
    user - login to enable you to log in,
    passwd - password to enable you to log in,
    cwd_path - a specific place on the server with data,
    year - year / years for data,
    day - day / days for data,
    name_station_list - specyfic name for International GNSS Service (IGS),
                        he first four characters of the station designation,
    """
    def __init__(self, save_path:str, host:str, user:str, passwd:str,
                 cwd_path:str, year:list, day:list, name_station_list:list):
        self.save_path = save_path
        self.host = host
        self.user = user
        self.passwd = passwd
        self.cwd_path = cwd_path
        self.year = year
        self.day = day
        self.name_station_list = name_station_list
        self.ftps = None

    def connect_to_ftp(self):
        try:
            self.ftps = FTP_TLS(host=self.host)
            self.ftps.login(user=self.user, passwd=self.passwd)
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def download_rinex_files(self):
        try:
            os.chdir(self.save_path)
            self.connect_to_ftp()

            for y in self.year:
                for d in self.day:
                    self.ftps.cwd(self.cwd_path + str(y) + '/' + str(d) + '/' + str(y)[2:] + 'd' + '/')
                    self.ftps.prot_p()
                    file_list = self.ftps.nlst()
                    file_list.sort()

                    selected_list = [n_station for n_station in file_list if any(name[:4] == n_station[:4] for name in self.name_station_list)]

                    for o in selected_list:
                        if 'crx' in o:
                            with open(o, 'wb') as file:
                                self.ftps.retrbinary('RETR %s' % o, file.write)
                            rinex_data = hatanaka.decompress(Path(o).read_bytes())
                            hatanaka.decompress_on_disk(o)
                            os.remove(o)

                            # Additional part, unpacking the .gz format
                            # if o.endswith('.gz'):
                            #     gz_name = os.path.abspath(o)
                            #     file_name = (os.path.basename(gz_name)).rsplit('.', 1)[0]
                            #     with gzip.open(gz_name, 'rb') as f_in, open(file_name, 'wb') as f_out:
                            #         shutil.copyfileobj(f_in, f_out)
                            #     os.remove(gz_name)

        except Exception as e:
            print(f"Error downloading RINEX files: {e}")
        finally:
            if self.ftps:
                self.ftps.quit()

# The class takes the Day of Year (DoY) as a string
class ModifiedDay:
    """
    The class takes information about specific days in the DOY system
    and writes it to a string as a string of three characters.

    start_day - first day for analisys,
    end_day - last day for analisys,
    """
    def __init__(self, start_day:int, end_day:int) -> list:
        self.start_day = start_day
        self.end_day = end_day

    def generate_list(self) -> list:
        days = range(self.start_day, self.end_day + 1)
        modified_day = []
        for i in days:
            if i < 10:
                i = '00' + str(i)
            elif i < 100:
                i = '0' + str(i)
            else:
                i = str(i)
            modified_day.append(i)
        return modified_day