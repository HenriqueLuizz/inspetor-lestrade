import json
import common
import ipoci



class Cloud:


    def __init__(self):
        pass


    def identifyCloud(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)
            for cloud in ['oci','aws','azure','gcp']:
                if cloud in data:
                    return [cloud]

    def enable_instance(self):
        clouds = self.identifyCloud()

        for c in clouds:
            if c == 'oci':
                self.oci('START')
            else:
                print(f'Sorry, {c.upper()} not yet supported!')



    def disable_instance(self):
        clouds = self.identifyCloud()

        for c in clouds:
            if c == 'oci':
                self.oci('STOP')
            else:
                print(f'Sorry, {c.upper()} not yet supported!')



    def get_oci(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)
            if 'oci' in data:
                return data['oci']
            else:
                return []


    def oci(self, action):
        ipoci.instancie_oci(self.get_oci(), action)


    def set_oci(self, iids):
        conf = {}

        with open('settings.json') as json_file:
            conf = json.load(json_file)
            
            for iid in iids:
                conf['oci'].append(iid)

        with open('settings.json', 'w') as json_read:
            json.dump(conf, json_read,indent=4)

        return conf


   

    # def getTotvs(self):
    #     with open('settings.json') as json_file:
    #         data = json.load(json_file)
    #         if 'totvs' in data:
    #             return data['totvs']
    #         else:
    #             return []


    # def getAWS(self):
    #     with open('settings.json') as json_file:
    #         data = json.load(json_file)
    #         if 'aws' in data:
    #             return data['aws']
    #         else:
    #             return []


    # def getAzure(self):
    #     with open('settings.json') as json_file:
    #         data = json.load(json_file)
    #         if 'azure' in data:
    #             return data['azure']
    #         else:
    #             return []

    # def getGcp(self):
    #     with open('settings.json') as json_file:
    #         data = json.load(json_file)
    #         if 'gcp' in data:
    #             return data['gcp']
    #         else:
    #             return []



