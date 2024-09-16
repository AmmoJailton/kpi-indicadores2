FROM python:3.10.14

EXPOSE 8080

#SSH
# RUN eval $(ssh-agent)

# ARG SSH_PRIVATE_KEY
# ENV SSH_PRIVATE_KEY $SSH_PRIVATE_KEY

# # creating the private key file
# RUN mkdir /root/.ssh/
# RUN echo $SSH_PRIVATE_KEY | base64 --decode --ignore-garbage > /root/.ssh/id_rsa

# # changing permissions for the private key file
# RUN chmod 600 /root/.ssh/id_rsa

# # make sure your domain is accepted
# RUN touch /root/.ssh/known_hosts
# RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN pip install poetry

COPY . ./
WORKDIR ./

# RUN ./set_env.sh

RUN poetry install
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "src.innovation_api.api.main:fast_api", "--port", "8080", "--host", "0.0.0.0"]
