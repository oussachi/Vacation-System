from xml.dom.minidom import parse
import xml.dom.minidom

def openDocument(fileName):
    DOMTree = parse(fileName)
    collection = DOMTree.documentElement
    return collection

def getElementsByTag(fileName, tag):
    collection = openDocument(fileName)
    elements = collection.getElementsByTagName(tag)
    return elements