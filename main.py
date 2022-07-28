# This is a sample Python script.
from xml.etree import ElementTree
from dict2xml import dict2xml
from xml.dom.minidom import parseString
from xmltodict import unparse

import html.parser
import xmltodict
import pprint
import json


def load_json(path: str) -> dict:
    if path.endswith(".json"):
        print(f"> Loading JSON from '{path}'")
        with open(path, mode="r") as open_file:
            content = open_file.read()

        return json.loads(content)
    elif path.endswith(".xml"):
        print(f"> Loading XML as JSON from '{path}'")
        xml = ElementTree.tostring(ElementTree.parse(path).getroot())
        return xmltodict.parse(xml, cdata_key="#text", dict_constructor=dict)

    print(f"> Loading failed for '{path}'")
    return {}


def unload_to_xml(dicc):
    xml = unparse(dicc, pretty=True, indent="  ")
  #  xml = dict2xml(dicc, wrap="all")
    #print(xml)
    save_path_file = "test.xml"
    h = html
    fin = h.unescape(xml)
    print(fin)
    fin = replace_smt(fin)
    with open(save_path_file, "w", encoding="utf-8") as f:
        f.write(fin)


def replace_smt(dicc):
    my_str = dicc.replace('<DateTime>', ' DateTime')
    my_str = my_str.replace('<T>', ' T')
    my_str = my_str.replace('<typeparam>', ' typeparam')
    my_str = my_str.replace('<summary>', ' summary')
    my_str = my_str.replace('<content>', ' content')
    my_str = my_str.replace('<value>', ' value')
    my_str = my_str.replace('<param>', ' param')
    my_str = my_str.replace('<returns>', ' returns')
    my_str = my_str.replace('<inheritdoc>', ' inheritdoc')
    my_str = my_str.replace('<placeholder>', ' placeholder')
    my_str = my_str.replace('<description>', '<description><![CDATA[')
    my_str = my_str.replace('</description>', '\n]]></description>')

    return my_str

def searchKey(key):
    try:
        res = next(item for item in mas if item['id'] == key)
        return {'id': res['id'], 'type': res['type'], 'severity': res['severity']}
    except:
     #   print('key ' + key + ' does not exist in final rule')
        return 'none'


def enrichWithSeverity(exp):
    match exp:
        case "Error":
            return 'BLOCKER'
        case "Warning":
            return 'MAJOR'
        case "Info":
            return 'INFO'
        case "Hidden":
            return 'INFO'
        case "None":
            return 'INFO'
        case _:
            print("wtf")


def enrichWithType(exp):
    match exp:
        case "Error":
            return 'BUG'
        case "Warning":
            return 'VULNERABILITY'
        case "Info":
            return 'CODE_SMELL'
        case "Hidden":
            return 'CODE_SMELL'
        case "None":
            return 'CODE_SMELL'
        case _:
            print("wtf")


path = "styleset.xml"
data = load_json(path)
# print(json.dumps(data, indent=2))

mas = []
theDict = {}
index = 0
while index < len(data['RuleSet']['Rules']):
    for d in data['RuleSet']['Rules'][index]['Rule']:
        #   print(d['@Id'] + " " + d['@Action'])
        theDict = {'id': d['@Id'], 'action': d['@Action'], 'severity': enrichWithSeverity(d['@Action']),
                   'type': enrichWithType(d['@Action'])}
        mas.append(theDict)
    index += 1

path2 = "Microsoft.VisualStudio.Threading.Analyzers.16.6.13.rules.template.xml"
data2 = load_json(path2)
mas2 = []
theDict2 = {}
index2 = 0

while index2 < len(data2['rules']['rule']):
    theDict2 = {'key': data2['rules']['rule'][index2]['key'], 'type': data2['rules']['rule'][index2]['type'],
                'severity': data2['rules']['rule'][index2]['severity']}
    # print('test ' + data2['rules']['rule'][index2]['key'])

    res = searchKey(data2['rules']['rule'][index2]['key'])

    if res != 'none':
        data2['rules']['rule'][index2]['key'] = res['id']
        data2['rules']['rule'][index2]['type'] = res['type']
        data2['rules']['rule'][index2]['severity'] = res['severity']
        print('found ' + json.dumps(res))
        print('fixed ' + json.dumps(data2['rules']['rule'][index2]))
    else:
        print(data2['rules']['rule'][index2]['key'] + ' not found')

    mas2.append(theDict2)
    index2 += 1

print("################## initial rules are")
print(mas)
print(len(mas))

print("################## xml rules are")
print(mas2)
print(len(mas2))

print('>>>>>>>>>>> UNLOADING')
print(data2)

unload_to_xml(data2)

#searchKey('SA1001')
# enrichMas(mas2)
