FROM nginx:alpine

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

# TODO: Add the extra files when landing is finalized
# ADD ./extras /extras

# Add the client files
WORKDIR client
ADD ./client /client
