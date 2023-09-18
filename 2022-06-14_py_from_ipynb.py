# -*- coding: utf-8 -*-

import glob
import os
import re
import shutil
import json

__dir_abs__ = os.path.dirname(os.path.abspath(__file__))

header_comment = '# %%\n'
header_comment_markdown = '#\n'
header_comment_code = '#\n'

def nb2py(notebook):
    result = []
    cells = notebook['cells']

    for cell in cells:
        cell_type = cell['cell_type']
        source = ''.join(cell['source']).strip()
        if cell_type == 'markdown':
            nlines = source.count('\n')
            if nlines == 0:
                result.append('%s# %s'%
                              (header_comment_markdown, source))
            else:
                result.append('%s"""\n%s\n"""'%
                              (header_comment_markdown, source))

        if cell_type == 'code':
            result.append("%s%s" % (header_comment_code, source))

    return '\n\n'.join(result)


def py2nb(py_str):
    # remove leading header comment
    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment):]

    cells = []
    chunks = py_str.split('\n\n%s' % header_comment)

    for chunk in chunks:
        cell_type = 'code'
        if chunk.startswith("'''"):
            chunk = chunk.strip("'\n")
            cell_type = 'markdown'
        elif chunk.startswith('"""'):
            chunk = chunk.strip('"\n')
            cell_type = 'markdown'

        cell = {
            'cell_type': cell_type,
            'metadata': {},
            'source': chunk.splitlines(True),
        }

        if cell_type == 'code':
            cell.update({'outputs': [], 'execution_count': None})

        cells.append(cell)

    notebook = {
        'cells': cells,
        'metadata': {
            'anaconda-cloud': {},
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'},
            'language_info': {
                'codemirror_mode': {'name': 'ipython', 'version': 3},
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.6.1'}},
        'nbformat': 4,
        'nbformat_minor': 4
    }

    return notebook

def convert(in_file, out_file):
    _, in_ext = os.path.splitext(in_file)
    _, out_ext = os.path.splitext(out_file)

    if in_ext == '.ipynb' and out_ext == '.py':
        with open(in_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        py_str = nb2py(notebook)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(py_str)

    elif in_ext == '.py' and out_ext == '.ipynb':
        with open(in_file, 'r', encoding='utf-8') as f:
            py_str = f.read()
        notebook = py2nb(py_str)
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)

    else:
        raise(Exception('Extensions must be .ipynb and .py or vice versa'))

def get_ipynblist(parent):
    ipynblist = []
    target = os.path.join(parent, '*')
    target = target.replace('[', '<').replace(']', '>').replace('<', '[[]').replace('>', '[]]')
    for filepath in glob.glob(target):
        if not os.path.isdir(filepath):
            if filepath.split('.')[-1] == 'ipynb':
                ipynblist.append(filepath)
            continue
        ipynblist += get_ipynblist(filepath)
    return ipynblist

if __name__ == '__main__':
    
    #import Day12_01 as test
    #import Day12_02 as test
    #import Day12_03 as test

    #test.test()

    # 결과 dir 만들기
    basedir = __dir_abs__
    exportdir = os.path.join(basedir,  'pyexport')
    if not os.path.exists(exportdir):
        os.mkdir(exportdir)

    # 작업
    day_pattern2 = re.compile('.*(Day[0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9])')
    day_pattern1 = re.compile('.*(Day[0-9]_[0-9][0-9][0-9][0-9][0-9][0-9])')
    filename_pattern = re.compile('.*\\\\(.*\.ipynb)')
    ipynblist = []
    ipynblist += get_ipynblist(basedir)
    count = 0
    for ipynbpath in ipynblist:
        try:
            # 파일이름만들기:날짜따오기
            day = ''
            match = day_pattern2.match(ipynbpath)
            if match is not None:
                day = match.groups()[0]
            else:
                match = day_pattern1.match(ipynbpath)
                if match is not None:
                    day = match.groups()[0].replace('Day', 'Day0')
            # 파일이름만들기
            match = filename_pattern.match(ipynbpath)
            if match is None:
                continue
            filename_ipynb = day + "_" + match.groups()[0]
            filename_txt = filename_ipynb.replace('.ipynb', '.txt')
            filename_py = filename_ipynb.replace('.ipynb', '.py')
            # 파일복사
            src = ipynbpath
            dst = os.path.join(exportdir, filename_ipynb)
            #print("src", src)
            #print("dst", dst)
            shutil.copy2(src, dst)
            # 파일변환
            os.chdir(dst[:dst.rfind("\\")])
            #command = "jupyter nbconvert --to markdown *.ipynb"
            #command = f"ipynb-py-convert \"{filename_ipynb}\" \"{filename_py}\""
            #print("command", command)
            convert(filename_ipynb, filename_py)
            count += 1
            #os.system(command)
            os.remove(dst)
            
            # 파일 확장자 변환
            #src = os.path.join(exportdir, filename_txt)
            #dst = os.path.join(exportdir, filename_py)   
            #print("src", src)
            #print("dst", dst)     
            #if os.path.exists(src):
            #    os.rename(src, dst)
            
            
            # 파일생성되었는지 확인
            if not os.path.exists(filename_py):
                print(">>> "+filename_ipynb)
        except Exception as e:
            print(e)
    print(f"{count} files done.\r\n")
    input()
