#!/usr/bin/env bash
# script prepares an ubuntu server for deployment of a static website

# install nginx
apt-get -y update && apt-get -y install nginx

# list of directories to make if they do  not exist
dir_list=('/data/' '/data/web_static/' '/data/web_static/releases/'
	  '/data/web_static/shared/' '/data/web_static/releases/test/')

# loop that creates the directories if they do not exit
for dir in "${dir_list[@]}"; do
	if [ -d "$dir" ]; then
		echo "$dir already exists"
	else
		mkdir "$dir"
	fi
done

# create a fake html file and add some content
html_file='/data/web_static/releases/test/index.html'

if [ -f "$html_file" ]; then
	echo "$html_file already exists"
else
	touch "$html_file"
fi

# add some content to the html file made
data="<html>\n <head>\n	 <title>test_script</title>\n </head>\n <body>\n  Holberton School is cool\n </body>\n</html>"
echo -e "$data" > "$html_file"

# link /data/web_static/current to the /data/web_static/releases/test/ folder
link_file='/data/web_static/current'

if [ -h "$link_file" ]; then
	rm "$link_file"
fi
ln -sf "${dir_list[4]}" "$link_file"

# changing ownership of /data/ file
chown -R ubuntu:ubuntu "${dir_list[0]}"

# add a new location to the server with an alias to another
nginx_path='/etc/nginx/sites-available/default'
check=$(grep '/hbnb_static' "$nginx_path")
if [ -n "$check" ]; then
	echo "already configured"
else
	sed -i.bak 's/^[^#]*server {/server {\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}/g' "$nginx_path"
fi

# restart the nginx server
service nginx restart
