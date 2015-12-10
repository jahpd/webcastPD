require "json"

namespace :download do

  desc "download from youtube"
  task :youtube do
    file = File.read("/home/pi/.radio/list.json")
    JSON.parse(file).each_pair do |k, v|
      time = Time.now.strftime("%d-%m-%y")
      puts k
      puts time
      if k == time
        v.each do |link|
          sh "youtube-dl --verbose --abort-on-error --extract-audio --audio-format vorbis --audio-quality 0 --output '/home/pi/.radio/Musics/%(uploader)s-%(title)s.%(ext)s' #{link}"
        end
      else
        puts "Nenhuma lista encontrada para #{time}"
      end
    end
  end

end

namespace :convert do

  desc "convert any files to ogg"
  task :ogg do
    Dir.glob("#{ENV['FOLDER']}/*.#{ENV['EXT']}") do |file|
      name = file.split(".#{ENV['EXT']}")[0]
      sh "ffmpeg -i #{file} #{name}.ogg"
    end
  end
end

namespace :dropbox do

  desc "upload files (with specific extensions) in a folder to dropbox"
  task :upload do
    json = {"Musics/*.ogg" => "Musics/",
            "*.log" => "var/local/log/",
            "*.json" => "usr/local/etc/",
            "Rakefile" => "usr/local/bin/"}
    json.each_pair do |k, v|
      Dir.glob("/home/pi/.radio/#{k}") do |file|
        if v=="Musics/" then file.gsub!("\ ","\\ ") end
        sh "/home/pi/Github/Dropbox-Uploader/dropbox_uploader.sh upload #{file} #{v}"
      end
    end
  end
end

namespace :clean do
  
  desc "clean some audio files"
  task :audio do
    sh "rm -f .radio/Musics/*.ogg"
    sh "rm -f .radio/Musics/*.m4a"
    sh "rm -f .radio/Musics/*.part"
  end
end
