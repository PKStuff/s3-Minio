import json
from api.upload import upload_file
from api.getObject import Pull_Objects 


def main():
    with open('input.json', 'r') as fp:
        body = json.loads(fp.read())

    print("1.Upload Package.\n2.Get Single Package\n3.Get Latest Package\n4.List All Packages\n5.Delete Package.")

    inp = input('Enter your choice:')
    obj = Pull_Objects()

    if inp == '1':
        print(upload_file(body['remote'][0]))
    
    elif inp == '2':
        print(obj.single_object(body['remote'][1]))
    
    elif inp == '3':
        print(obj.latest_object())
    
    elif inp == '4':
        all_data = obj.get_All_objects()
        print(all_data['code'])
        for obj,url in all_data['url'].items():
            print("object:{}".format(obj))
            print("url:{}".format(url))
    
    elif inp == '5':
        print(obj.delete_object(body['remote'][1]))
    else:
        print("Invalid choice..")

if __name__ == '__main__':
    main()