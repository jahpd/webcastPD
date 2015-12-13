require "json"
require 'fileutils'

desc "build, backup and dowload things"
task :init do
  Rake::Task["build:station"].invoke
  Rake::Task["build:configure"].invoke
  Rake::Task["dropbox:upload"].invoke
  Rake::Task["download:youtube"].invoke
end

def generate_json(station)
  File.open("#{station}/list.json", "w") do |file|
    url = ""        
    json = """//Generated at #{Time.now}
{
  \"#{Time.now.strftime("%d-%m-%y")}\":[
    \"https:\/\/www.youtube.com\/watch?v=CG05gJ6uqP4\",
    \"https:\/\/www.youtube.com\/watch?v=aKq-LRYv1Q4\",
    \"https:\/\/www.youtube.com\/watch?v=3Z42ZR2mPdY\",
    \"https:\/\/www.youtube.com\/watch?v=vfNT20L2mSo\",
    \"https:\/\/www.youtube.com\/watch?v=w2sDV6Ylf48\",
    \"https:\/\/www.youtube.com\/watch?v=sX-xhjEcWZk\",
    \"https:\/\/www.youtube.com\/watch?v=PMWonO8jsdU\",
    \"https:\/\/www.youtube.com\/watch?v=RsH0lCPYANA\",
    \"https:\/\/www.youtube.com\/watch?v=SSOMWwr0s9M\",
    \"https:\/\/www.youtube.com\/watch?v=gn8B-L2CMso\",
    \"https:\/\/www.youtube.com\/watch?v=_qWPCoayhjY\",
    \"https:\/\/www.youtube.com\/watch?v=AHORp418B6s\",
    \"https:\/\/www.youtube.com\/watch?v=CD_61GzSvi4\",
    \"https:\/\/www.youtube.com\/watch?v=TjDBhmVqn4E\",
    \"https:\/\/www.youtube.com\/watch?v=v48o30LOJ2M\"
]
}"""
    file.write(json)
  end
end

namespace :build do

  desc "build station folder"
  task :station do
    dir = File.directory?(ENV['STATION'])
    if not dir
      station = ENV['STATION']
      ["", "Musics"].each{|e| FileUtils.mkdir("#{station << s}"); puts "=>    created #{station << s}"}
      FileUtils.touch("#{station}/station.log")
      puts "=>    created #{station}/station.log"   
    elsif
      puts "=> Skipping due to existing configuration"
    end
  end

  desc "configure login and list files"
  task :configure do
    stationname= ENV['STATION'].split("/")
    stationname= stationname[stationname.length-1]
    
    # Create configuration file
    puts "=> Creating #{ENV['STATION']}/station.conf"
    File.open("#{ENV['STATION']}/station.conf", "w") do |file|
      file.write("""-H #{ENV['ICECAST_HOST']} -p 8000 -l #{stationname}.ogg -m #{ENV['STATION']}/Musics -x stationpsk""")
    end
      
    # Create a list of musics
    puts "=> Creating  #{ENV['STATION']}/list.json"
    generate_json(ENV['STATION'])
    puts "=> please change your password at #{ENV['STATION']}/station.conf"
    puts "=> please change your playlist at #{ENV['STATION']}/list.json" 
  end
end


namespace :download do

  desc "download from youtube"
  task :youtube do
!    # Read from json a playlist
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
 
namespace :dropbox do

  desc "upload files (with specific extensions) in a folder to dropbox"
  task :upload do
    station = ENV['STATION'].split("/")
    station = station[station.size-1]
    json = {"#{ENV['STATION']}Musics/*.ogg" => "#{station}/Musics/",
            "*.log" => "#{station}/",
            "*.json" => "#{station}/",
            "Rakefile" => "/"}
   
    json.each_pair do |k, v|
      if v=="Musics/"
        if not Dir.glob("#{ENV['STATION']}/#{v}*.ogg").empty?
          time = Time.now.strftime("%d-%m-%y")
          oldmusics = "#{ENV['STATION']}/OldMusics"
          tar = "tar -cf #{oldmusics}/#{time}.tar"
          Dir.glob("#{ENV['STATION']}/#{k}/*.ogg") do |file|
            file.gsub!("\ ","\\ ")
            file.gsub!("(", "\\(")
            file.gsub!(")", "\\)")
            file.gsub!("'", "\\\\'")
            file.gsub!("\"", "\\\"")
            tar << " #{file}"
          end
        
          sh "#{tar}"
          sh "bzip2 -zvs9 #{oldmusics}.tar"
          sh "dropbox_uploader -s -f #{ENV['DROPBOX_CONF']} upload #{oldmusics}.tar.bz2 #{station}/Musics/"
          sh "rm #{oldmusics}.tar"
          sh "rm #{oldmusics}.tar.bz2"
        else
          puts "=> Skipping upload due to empty files"
        end
        puts "=> DONE'"
      end
    end
  end
end

namespace :pd do

  desc "Start PureData scheduller"
  task :start do
    sh "webcast $(cat #{ENV['STATION']}/station.conf)"
  end
end
