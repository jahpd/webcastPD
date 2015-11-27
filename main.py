from optparse import OptionParser
from subprocess import call


#import inspect

# PROGRAMA PRINCIPAL
PROG = "RadioLabicRuntime"
VERSION = "0.0.1"
description = "Script python para inicializar todos os programas necessarios"
parser = OptionParser(usage='usage: %prog [OPTIONS, [ARGS]]',
                      version='%s %s' % (PROG, VERSION),
                      description=description)

# Opcoes do programa
opt =  [("p", "path", None, "caminho da pasta contendo uma lista de musicas"),
        ("P", "password", None, "senha do servidor giss.tv")]

# Create a list of tuples
# to create a list of options
for word in opt:
    v = "_".join(word[1].split("-"))
    a = "-%s" % word[0]
    b = "--%s" % word[1]
    if word[2] != None:
        parser.add_option(a, b, action=word[2], help=word[3], dest=v, default=False)
        #elif word[1] == "measures":
        #    parser.add_option(a, b, action=word[2], help=word[3], dest=v, default=False, nargs=2)
    else:
        parser.add_option(a, b, help=word[3], dest=v, default=False)

# Capturar os argumentos passados pelo 
(options, args) = parser.parse_args()

main = ("#N canvas 1 50 638 359 10;",
        "#X text 0 0 ITS A GENERATED PATCH. DO NOT MODIFY!;", 
        "#X obj 1 77 cast.player~ "+options.path+" ;", # /home/guilherme/Github/labic_patchs/music
        "#X obj 1 37 tgl 15 0 empty empty empty 17 7 0 10 -262144 -1 -1 0 1;",
        "#X obj 1 107 gen_cast.server.simple~;", 
        "#X obj 0 131 cast.client.simple~ 5000;",
        "#X obj 1 18 loadbang;",
        "#X obj 1 56 t f f;",
        "#X obj 0 159 dac~;",
        "#X msg 42 43 \; pd dsp \$1;", 
        "#X connect 1 0 3 0;",
        "#X connect 1 1 3 1;", 
        "#X connect 2 0 6 0;",
        "#X connect 3 0 4 0;",
        "#X connect 4 0 7 0;",
        "#X connect 4 1 7 1;", 
        "#X connect 4 2 1 0;", 
        "#X connect 5 0 2 0;",
        "#X connect 6 0 3 2;", 
        "#X connect 6 1 8 0;")

cast_server= ("#N canvas 1 50 1278 358 10;",
              "#X obj 36 61 oggcast~ 2 512;",
              "#X obj 37 32 inlet~;",
              "#X obj 116 30 inlet~;",
              "#X msg 412 87 server 1;",
              "#X obj 36 126 print cast.server.simple~ :;",
              "#X obj 118 157 print cast.server.simple~ (frame):;",
              "#X obj 338 13 inlet;",
              "#X obj 338 37 sel 0 1;"
              "#X msg 257 32 disconnect;",
              "#X msg 367 143 vorbis 44100 2 133 128 96;",
              "#X msg 359 171 print;",
              "#X obj 339 60 t b b b b b;",
              "#X msg 392 114 passwd "+options.password+" ;",
              "#X msg 317 211 connect giss.tv radiolabic.ogg 8000;",
              "#X obj 36 188 outlet;",
              "#X connect 0 0 4 0;",
              "#X connect 0 0 14 0;",
              "#X connect 0 1 5 0;",
              "#X connect 1 0 0 0;",
              "#X connect 2 0 0 1;",
              "#X connect 3 0 0 0;",
              "#X connect 6 0 7 0;",
              "#X connect 7 0 8 0;",
              "#X connect 7 1 11 0;",
              "#X connect 8 0 0 0;",
              "#X connect 9 0 0 0;",
              "#X connect 10 0 0 0;",
              "#X connect 11 0 13 0;",
              "#X connect 11 1 10 0;",
              "#X connect 11 2 9 0;",
              "#X connect 11 3 12 0;",
              "#X connect 11 4 3 0;",
              "#X connect 12 0 0 0;",
              "#X connect 13 0 0 0;")


f = open("main.pd", "w")
g = open("gen_cast.server.simple~.pd", "w")
f.write("\n".join(main))
g.write("\n".join(cast_server))
f.close()
g.close()

#from subprocess import call
call(["pd-extended", "-nogui", "-noadc", "-alsa", "main.pd"])
