import pathlib
from rich.progress import track
from typing import List, Tuple

import subprocess
import os
import shutil

def get_swift_wget_commands(obsid: str, dtype: str, overwrite: bool) -> List[str]:

    if overwrite is False:
        overwrite_option = '-nc'
    else:
        overwrite_option = ''
    wget_command = 'wget ' + overwrite_option + f' -q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt*  http://www.swift.ac.uk/archive/reproc/{obsid}/{dtype}/'
    return wget_command

def swift_download_uncompressed(obsid: str, tname:str, dtype: str, dest_dir: pathlib.Path = None) -> None:
    
    # given a Swift target id and type of data, this function downloads the uncompressed
    # data to the directory dest_dir
    
    # get our download commands from the server
    wget_command = get_swift_wget_commands(obsid, dtype, overwrite=False)
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    if (os.path.isdir(f'{os.getcwd()}/{tname}/{obsid}/{dtype}') == True):
        return 
    presult = subprocess.run(wget_command.split())
    if presult.returncode != 0:
        return

    # change folders back
    os.chdir(old_cwd)

    if(os.path.isdir(f'{dest_dir}/{tname}/{obsid}')):
        shutil.move(f'{dest_dir}/{obsid}/{dtype}', f'{dest_dir}/{tname}/{obsid}', copy_function = shutil.copytree)
        shutil.rmtree(f'{dest_dir}/{obsid}/')
    else:
        shutil.move(f'{dest_dir}/{obsid}', f'{dest_dir}/{tname}', copy_function = shutil.copytree)
    
def download_files(tlist: str, dtype_list: str, dest_dir: str) -> None: 
    # iterates over each requested data type and observation collected from get_multi_tlists()
    for obsids_list, tname in tlist:
        for obsid in track(obsids_list, description=f"[cyan]Downloading target id[/] [magenta]{obsids_list[0][0:8]}[/][/][cyan]...[/]"):
            for dtype in dtype_list: 
                swift_download_uncompressed(obsid=obsid, tname=tname, dtype=dtype, dest_dir=dest_dir)
                