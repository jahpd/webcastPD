# webcastPD

Uma ferramenta de abstractions de PD e script python, para automatização de streaming no Raspberry Pi;

## Instalação

Este programa supõe que tens o [pd-extended](http://puredata.info/downloads/pd-extended), python e rake instalado no seu raspberry pi (até agora, conseguimos rodar em um debian [_Jessie_](https://www.raspberrypi.org/downloads/raspbian/)):

    $ sudo apt-get install pd-extended python

Provavelmente seu raspberry já vem com Ruby. Portanto execute o comando:

    $ sudo gem install rake
    
### Clone o projeto

No seu raspberry, execute:

    $ cd ~
    $ mkir ~/Github
    $ cd ~/Github
    $ git clone https://www.github.com/jahpd/webcastPD

### Crie uma pasta em /home/pi

    $ mkdir /home/pi/.radio

### Copie alguns arquivos para um local apropriado:

    $ cp ~/Github/webcastPD/radio-* /usr/local/bin/
    $ cp ~/Github/webcastPD/Rakefile ~/.radio/
    
# Execução

Esses são alguns comandos para

  - Inicialização de uma estação, backup e downloads de áudios para uma estação
  - Execução de uma estação
  - Verificação de uma estação
  - Playlist de uma estação
  
## Inicialização

A inicialização requer que já tenha um servidor [Icecast2](http://icecast.org/), no caso de um `localhost`. Uma opção é usar um já configurado, como o [Giss.tv](http://giss.tv/):

    $ radio-init minharadio localhost senha
    $ radio-init minharadio giss.tv senha
    
Após a inicialização, edite os arquivos ~/.radio/minhaestacao/station.conf. Modifique o parâmetro `-x` para a senha do seu servidor icecast.

## Execução

    $ radio-play minharadio

Muitas coisas irão aparecer, portanto talvez seja melhor:
    
    $ nohup radio-play minharadio > /home/pi/.radio/minharadio/station.log 2>&1&

# Verificação

Verifique se sua rádio está transmitindo:

    $ radio-check minharadio

# Playlist

Olhe as músicas da sua estação

    $ radio-playlist minharadio
    
# TODO

- Automatizar todos os passos anteriores, ou criar um pacote `.deb`?
- Verificar problemas de segurnaça nos arquivos supracitados ?  