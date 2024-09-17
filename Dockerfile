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

# from gcp file credentials
ARG GCP_CREDENTIALS_SECRET_ENCODED
ENV GCP_CREDENTIALS_SECRET_ENCODED $GCP_CREDENTIALS_SECRET_ENCODED

ARG EMAIL_SENDER_ACCOUNT
ENV EMAIL_SENDER_ACCOUNT $EMAIL_SENDER_ACCOUNT

ARG EMAIL_PASSWORDS
ENV EMAIL_PASSWORDS $EMAIL_PASSWORDS

RUN pip install -U pip setuptools

COPY . ./
WORKDIR ./

RUN rm -rf notebooks

ENV GOOGLE_CREDENTIALS_FILEPATH "/tmp/gcloud-api.json"
RUN echo $GCP_CREDENTIALS_SECRET_ENCODED | base64 --decode > $GOOGLE_CREDENTIALS_FILEPATH
RUN pip install -r requirements.txt

RUN poetry config virtualenvs.create false && poetry install --no-root

ENTRYPOINT ["uvicorn", "src.innovation_api.api.main:fast_api", "--port", "8080", "--host", "0.0.0.0"]
