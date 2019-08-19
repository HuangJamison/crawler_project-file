import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element,SubElement,tostring
from xml.dom import minidom
def main():
	tree = ET.parse('example.xml')
	root = tree.getroot()
	print(root.attrib)
	print('共有%s 個結果'%root.attrib['totalResults'])
	movie = []
	for tag in root.findall('result'):
		print(tag.attrib)
		movie.append(tag.attrib['title'])
	print('\n'.join(movie))
if __name__ == '__main__':
	main()