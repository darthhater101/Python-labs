import single
import gevent_var
import xml.etree.ElementTree as ET


def main():
    conf = ET.parse("res/conf.xml")
    option = conf.findtext("option")
    if(option == '0'):
        single.main()
    elif(option == '1'):
        gevent_var.main()
    else:
        print("Wrong option, must be 0 or 1")


if __name__ == "__main__":
    main()
