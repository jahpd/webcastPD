# webcastPD

Uma ferramenta de abstractions de PD e script python, para automatização de streaming no Raspberry Pi;

## Instalação

Este programa supõe que tens o pd-extended, python e rake instalado no seu raspberry pi (até agora, conseguimos rodar em um debian _Jessie_)

    $ sudo apt-get install pd-extended python
    
### Clone o projeto

    $ git clone https://www.github.com/jahpd/webcastPD

### Crie uma pasta em /home/pi

    $ mkdir /home/pi/.radio

### Instale alguns arquivos em `/usr/local/bin`

Instalação dos executáveis:

    $ cd webcastPD/
    $ sudo cp radio* /usr/local/bin/
    $ sudo cp giss.tv /usr/local/bin/
    $ sudo cp webcast /usr/local/bin/
    
E arquivos de configuração (modifique-os de acordo com sua estação)

    $ sudo cp minharadio.conf ~/.radio/

Por exemplo, preferimos colocar a pasta de música dentro de .radio

    giss.tv 8000 minhaestacao.ogg /home/pi/.radio/Musics minhasenha

# Execução

Adicionamos a seguinte linha em `/etc/rc.local` para execução do programa, assim que o raspberry pi estiver no final do boot:

    $ sudo /usr/local/bin/radio-init

Ou simplismente:

    $ sudo giss.tv $(cat /home/pi/.radio/minharadio.conf)
    
## Verifique se está rodando:

    $ radio-check

# TODO

- Automatizar todos os passos anteriores, ou criar um pacote .deb?
- Verificar problemas de segurnaça nos arquivos supracitados ?  