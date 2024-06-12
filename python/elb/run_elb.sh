docker image build -t elb-nginx:latest .

docker run -d \
   --name nginx \
   --restart always \
   --net pyservernetbridge \
   -p 80:80 \
   elb-nginx
