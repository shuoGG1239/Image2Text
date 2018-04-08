if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['main.py','-D','-w','--icon=./asset/myicon.ico']
    run(opts)
