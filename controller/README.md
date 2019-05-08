 Para tocar musica:

* Criar o CRD musics: ``kubectl create -f music.yaml``

* Criar um Configmap de um arquivo mp3 (com o nome payload.mp3): ``kubectl create configmap musica --from-file=payload.mp3``

* Criar um objeto do tipo Music com a spec ``music`` apontando para o configmap criado. Exemplos no diretório ``crd``


