import json
import yaml
from kubernetes import client, config, watch
import os
import base64
import platform

DOMAIN = "estaleiro.io"


def play_music(crds, obj):
    metadata = obj.get("metadata")
    spec = obj.get("spec")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")    
        
    
    
    try:
       configMaps = client.CoreV1Api(api_client)
       musicConfig = spec.get('music')
       music = configMaps.read_namespaced_config_map(musicConfig, namespace)
       payload = music.binary_data['payload.mp3']
       f = open("temp.mp3", "w")
       f.write(base64.b64decode(payload))
       f.close()
       print("Tocando o mp3 %s" % name)
       obj["spec"]["status"] = "Sucesso"
       arch = platform.machine()
       if arch == "x86_64":
          os.system("/usr/bin/mpg123 temp.mp3")
       if arch == "armv7": 
           os.system("/usr/bin/omxplayer temp.mp3")
       os.remove("temp.mp3")
       

    except:
        print("Falha ao decodificar o Payload do CRD %s" % name)
        obj["spec"]["status"] = "Falha"
   
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "musics", name, obj)


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    configuration = client.Configuration()
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    crds = client.CustomObjectsApi(api_client)
    print("Esperando pra tocar musicas")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "musics", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            metadata = obj.get("metadata")
            name = metadata.get("name")
            if not spec:
                continue
            status = spec.get("status")
            if operation == "ADDED" and status is None:
                print("Obtendo %s" % name)
                play_music(crds, obj)
    
