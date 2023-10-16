import constants as c, datetime, json

class FIMPMessage:
    def __init__(self, serv:str, type:str, val_t:str = None, val = None, props:dict = None, tags:list = None, resp_to:str = None, corid:str = None, storage:dict = None, topic:str = None):
        self.serv = serv
        self.type = type
        self.val_t = val_t
        self.val = val
        self.props = props
        self.tags = tags
        self.resp_to = resp_to
        self.corid = corid
        self.storage = storage
        self.topic = topic
        self.ctime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        self.src = c.app_name
        self.uid = c.uid
        self.ver = "1"
        

    def to_json(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True)