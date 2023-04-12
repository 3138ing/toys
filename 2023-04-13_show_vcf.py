# %%
import quopri
import base64
import io
from PIL import Image as PIL_Image
from IPython.display import Image, display

# %%
class vcard:
    def __init__(self):
        self.dic = {}
        self.last_key = ''
    def append(self, line):
        if line[0] in ('=', ' '):
            last_list = self.dic[self.last_key] 
            last_list[len(last_list) - 1] += line[1:]
            return
        index = [line.find(':'), line.find(';')]
        index = [x for x in index if x != -1]
        if len(index) == 0:
            print('### ERROR', 'vcard.append.key:none', line[0], line[0] == ' ', line)
            return
        index = min(index)    
        key = line[:index]
        value = line[index + 1:]
        if key in self.dic:
            self.dic[key].append(line[len(key) + 1:])
        else:
            self.dic[key] = [line[len(key) + 1:]]
        self.last_key = key

# %%
def conv_1(dic):
    utf8_statement = 'CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:'
    base64_jpeg_statement = 'ENCODING=BASE64;JPEG:'
    new_dic = {}
    check_dic = dic.copy()
    key = 'VERSION' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv.version:many', len(value_list))
            return {}
        value = value_list[0]
        if value != '2.1':
            print('### ERROR', 'vcard.conv.version:unknown')
            return {}
        check_dic.pop(key)
    else:
        print('### ERROR', 'vcard.conv.version:none')
        return {}
    key = 'N' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(utf8_statement, '').strip(';')
        new_dic['이름1'] = quopri.decodestring(value).decode('utf-8').strip()
        check_dic.pop(key)
    key = 'FN' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(utf8_statement, '').strip(';')
        new_dic['이름2'] = quopri.decodestring(value).decode('utf-8').strip()
        check_dic.pop(key)
    key = 'NOTE' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(utf8_statement, '').strip(';')
        new_dic['메모'] = quopri.decodestring(value).decode('utf-8').strip()
        check_dic.pop(key)
    key = 'X-PHONETIC-LAST-NAME' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(utf8_statement, '').strip(';')
        new_dic['이름-포닉'] = quopri.decodestring(value).decode('utf-8').strip()
        check_dic.pop(key)
    key = 'ORG' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(utf8_statement, '').strip(';')
        new_dic['조직'] = quopri.decodestring(value).decode('utf-8').strip()
        if len(new_dic['조직']) == 0:
            new_dic.pop('조직')
        check_dic.pop(key)
    key = 'PHOTO' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        if len(value_list) > 1:
            print('### ERROR', 'vcard.conv:many', key)
            return {}
        value = value_list[0]
        value = value.replace(base64_jpeg_statement, '').strip(';').encode()
        z = value[value.find(b'/9'):]
        new_dic['사진'] = PIL_Image.open(io.BytesIO(base64.b64decode(z)))
        check_dic.pop(key)
    key = 'TEL' ### ### ###
    if key in check_dic:
        value_list = check_dic[key]
        for value in value_list:
            if value.startswith('CELL;PREF:'):
                new_dic['전화번호:모바일(pref)'] = value[len('CELL;PREF:'):]
            elif value.startswith('CELL:'):
                new_dic['전화번호:모바일'] = value[len('CELL:'):]
            elif value.startswith('VOICE:'):
                new_dic['전화번호:음성'] = value[len('VOICE:'):]
            else:
                print('### ERROR', 'vcard.conv.tel:unknown', value)
        check_dic.pop(key)
    # check N, FN
    if '이름1' in new_dic and '이름2' in new_dic and new_dic['이름1'] == new_dic['이름2']:
        new_dic.pop('이름2')
    # check
    if len(check_dic.keys()) > 0:
        print('### ERROR', 'vcard.conv.key:unknown')
        for k in check_dic:
            print('', f'key:"{k}"', f'value:"{check_dic[k]}"')
        return new_dic
    return new_dic

# %%
def test(filename):
    line_number = 0

    vcard_list = []
    new_vcard = None

    with open(filename, 'rb') as f:
        begin_vcard = False
        while True:
            line = f.readline()
            line_number += 1
            if not line:
                break
            line = line.decode().rstrip()
            if len(line) == 0:
                continue
            if line == ';;;':
                continue
            if line == 'BEGIN:VCARD':
                if new_vcard != None:
                    print('### DEBUG: BEGIN:VCARD\r\n', line, line_number)
                    vcard_list.append(new_vcard)
                    new_vcard = None
                new_vcard = vcard()
            elif line == 'END:VCARD':
                if new_vcard == None:
                    print('### DEBUG: END:VCARD\r\n', line, line_number)
                    continue
                vcard_list.append(new_vcard)
                new_vcard = None
            else:
                if new_vcard == None:
                    print('### DEBUG: LINE\r\n', line, line_number)
                    continue
                new_vcard.append(line)
    for v in vcard_list:
        print('---------------')
        dic = conv_1(v.dic)
        for k in dic:
            if k == '사진':
                display(dic[k])
            else:
                print(k, dic[k])
            
            

# %%
test(r'D:\연락처.vcf')
