# coding: utf-8
require "json"
require 'fileutils'

desc "build, backup and dowload things"
task :init do
  ["build:station", "build:configure", "dropbox:download:configuration","dropbox:download:audios","download:youtube", "dropbox:upload:all", "pd:init"].each{|task| Rake::Task[task].invoke}
end

namespace :build do

  desc "build station folder"
  task :station do
    if not File.directory?(ENV['STATION'])
      station = ENV['STATION']
      FileUtils.mkdir("#{station}/")
      FileUtils.touch("#{station}/station.log")
    else
      puts "=> Skipping build"
    end
  end

  desc "configure login and list files"
  task :configure do
    if not File.directory?(ENV['STATION'])
      stationname= ENV['STATION'].split("/")
      stationname= stationname[stationname.length-1]
      s = ENV['STATION'].gsub(".","\.")
      hash = Hash.new
      hash["host"] = ENV['ICECAST_HOST']
      hash["port"] = '8000'
      hash["listen"] = "#{stationname}.ogg"
      hash["music-path"] = "#{s}/Musics"
      parse hash["music-path"]
      hash["password"] = "mypass"
      puts "=> creating #{ENV['STATION']}/station.json"
      File.open("#{ENV['STATION']}/station.json", "w").open do |file|
        file.write(JSON.pretty_generate(hash).force_encoding("utf-8"))
      end
       
      sh "dropbox_uploader download /list.json #{ENV['STATION']}/list.json"
      puts "=> please change your password at #{ENV['STATION']}/station.json"
      puts "=> please change your playlist at #{ENV['STATION']}/list.json"
    end   
  end
end

namespace :download do

  desc "download from youtube"
  task :youtube do
    
    file = File.read("#{ENV['STATION']}/list.json")
    json = JSON.parse(file).each_pair do |k, v|
      # Check the date to download
      # new musics
      time = Time.now.strftime("%d-%m-%y")
      if k == time
        
        # Check if backup was already done
        if not File.file?("#{ENV['STATION']}/Musics/#{time}.tar.gz")
          # If not, them download
          options = [
            #'--dump-pages',
            #'--no-playlist',
            #"--write-thumbnail #{ENV['STATION']}/Thumbnails/%(title)s.%(ext)s",
            "--extract-audio",
            "--audio-format vorbis",
            "--audio-quality 4",
            "--output '#{ENV['STATION']}/Musics/%(title)s.%(ext)s'"
          ]
          options
          v.each do |link|
            sh "youtube-dl #{options.join(" ")} #{link}"
          end
        else
          puts "=> Skipping due to already downloaded files"
        end
      else
        puts "Nenhuma lista encontrada para #{time}"
      end
    end
    sh "echo '=> DONE'"
  end  
end

def parse(file)
  array = [
   ["\ ","\\ "],
   ["(", "\\("],
   [")", "\\)"],
   ["'", "\\\\'"],
   ["\"", "\\\""],
   [",","\\,"],
   ["á","a"],
   ["é","e"],
   ["í","i"],
   ["ó","o"],
   ["ú", "u"]
  ].each{|e| file.gsub!(e[0],e[1])}
end

namespace :dropbox do
  namespace :upload do

    desc "upload configurations"
    task :all do
      station = ENV['STATION'].split("/") 
      
      path= ENV['STATION']
      time = Time.now.strftime("%d-%m-%y")
      tar = "tar -cf #{time}.tar #{file}"
      Dir.glob("#{path}/Musics/*.ogg") do |file|
        parse file
        tar << " #{file}"
      end
            
      sh "#{tar}"
      sh "bzip2 -zvs9 #{time}.tar"
      sh "dropbox_uploader -f #{ENV['DROPBOX_CONF']} upload #{time}.tar.bz2 /Old/"
      rm "#{time}.tar*"
      puts "=> DONE"
    end
  end
  
  namespace :download do
    
    desc "download configurations"
    task :configuration do
      sh "dropbox_uploader -f #{ENV['DROPBOX_CONF']} download /list.json #{ENV['STATION']}/list.json"
    end
    
    desc "download audio from dropbox"
    task :audios do
      sh "rm -f #{ENV['STATION']}/Musics/*.ogg"
      sh "dropbox_uploader -s -f #{ENV['DROPBOX_CONF']} -s download Musics/ #{ENV['STATION']}"
      
      Dir.glob("#{ENV['STATION']}/Musics/*.wav") do |file|
        parse file
        name = file.split("/")
        name = name[name.size-1].split(".wav")[0]
        
        puts "=> Converting some .wav files"
        sh "ffmpeg -i #{file} -acodec libvorbis #{ENV['STATION']}/Musics/#{name}.ogg"
        sh "rm #{file}"
      end
    end
  end
end


namespace :pd do

  desc "Start PureData scheduller, loaded by a json configuration file."
  task :start do
    webcast = "webcast"
    begin
      JSON.parse("#{ENV['STATION']}/station.json").each_pair {|k, v|
        if k == "password" and v == "mystring"
          puts "=> WARN: You need set your password in #{ENV['STATION']}/station.json. But you can add here (INSECURE):"
          v = gets.chomp
        end
        string << " --#{k} #{v}"
      }
      sh webcast
    rescue Exception=>e
      puts e
      exit
    end
  end

end
