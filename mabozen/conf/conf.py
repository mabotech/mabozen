
"""
prepare config for app
"""
# pip install toml



import toml

def test():

    with open("conf.toml") as conffile:
        config = toml.loads(conffile.read())
        
        #print(config)
        print(config["app"]["name"])
    
    
"""
load config to etcd
"""


"""
get config from etcd
"""


if __name__ == "__main__":
    test()