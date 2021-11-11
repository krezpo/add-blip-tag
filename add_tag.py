import glob
import yaml
import sys
import json

ENCODING = "UTF-8"

ACTION_TAG = {
    'ProcessHttp': {
        "background": "#7762E3",
        "label": "ProcessHttp",
        "id": "blip-tag-7df1e1a9-87d1-c1a1-fd37-37331fa8a21d",
        "canChangeBackground": False
    },
    'TrackEvent': {
        "background": "#61D36F",
        "label": "TrackEvent",
        "id": "blip-tag-bc58ce94-4e76-4f66-a2c4-efb9b8ebb738",
        "canChangeBackground": False
    },
    'MergeContact': {
        "background": "#FF1E90",
        "label": "MergeContact",
        "id": "blip-tag-3ff93695-d2ae-dfc7-7fe5-f4e4b7a547a8",
        "canChangeBackground": False
    },
    'Redirect': {
        "background": "#1EA1FF",
        "label": "Redirect",
        "id": "blip-tag-e6dead9d-5a52-3901-7aa5-9ad0e275ae67",
        "canChangeBackground": False
    },
    'ManageList': {
        "background": "#1EDEFF",
        "label": "ManageList",
        "id": "blip-tag-9f66207a-45bb-76a7-3816-ddd9c6289f94",
        "canChangeBackground": False
    },
    'ExecuteScript': {
        "background": "#FF961E",
        "label": "ExecuteScript",
        "id": "blip-tag-d2974ed4-d8d9-0d87-6153-fbed3205d146",
        "canChangeBackground": False
    },
    'SetVariable': {
        "background": "#FF4A1E",
        "label": "SetVariable",
        "id": "blip-tag-f56c273b-ba00-ca1c-9342-0d4c15d33ac3",
        "canChangeBackground": False
    },
    'ProcessCommand': {
        "background": "#FC91AE",
        "label": "ProcessCommand",
        "id": "blip-tag-a691d5d5-f3c4-ef6b-b9c5-614d5de16169",
        "canChangeBackground": False
    },
    'UserInput': {
        'background': '#232d11',
        'label': 'User Input',
        'id': 'blip-tag-ba80e21e-7e32-11e9-8f9e-2a86e4085a59',
        'canChangeBackground': False
    }
}

if __name__ == "__main__":

    with open("config.yml") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.SafeLoader)

    if config == None:
        sys.exit(-1)

    chatbots = glob.glob("{}*.json".format(config["source_folder"]))

    for chatbot in chatbots:
        print("Tagueando o {}".format(chatbot))

        with open(chatbot, 'r', encoding=ENCODING) as data:
            builder = json.load(data)

        for state in builder["flow"]:
            add_tags = []
            builder["flow"][state]['$tags'] = []

            for action in builder["flow"][state]['$enteringCustomActions'] + builder["flow"][state]['$leavingCustomActions']:
                if action['type'] not in add_tags:
                    try:
                        builder["flow"][state]['$tags'].append(ACTION_TAG[action['type']])
                        add_tags.append(action['type'])
                    except:
                        continue

            try:
                builder["flow"][state]['$contentActions'][-1]['input']['bypass']
            except:
                continue

            if not builder["flow"][state]['$contentActions'][-1]['input']['bypass']:
                builder["flow"][state]['$tags'].append(ACTION_TAG['UserInput'])

        chatbot_name = str(chatbot.split("/")[-1]).replace(".json", "")
        with open("{}{}.json".format(config["destination_folder"], chatbot_name), "w+", encoding=ENCODING) as output:
            print("Salvando em {}{}.json".format(config["destination_folder"], chatbot_name))
            json.dump(builder, output, indent=4, ensure_ascii=False)

    print("Fim de execução")