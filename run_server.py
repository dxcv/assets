import os

def main():
    bokeh_cmd = 'bokeh.exe serve'
    assets = ['currency', 'interest', 'bond', 'commodity']

    os.system('%s %s --host * --port 5001'%(bokeh_cmd, ' '.join(assets)))

if __name__ == '__main__':
    main()
