#!/bin/bash
set -e
echo "clar docker cache"
docker buildx prune --all

echo "Get version"
export VERSION="v"`grep "__version__" src/innovation_api/__init__.py | sed 's/[ "]//g'| sed 's/\./-/g'|cut -d"="  -f2`
echo $VERSION

echo "export image name"
export DOCKER_IMAGE_NAME="$GCP_ARTIFACT_REGISTRY_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_APP_NAME-$ENV/$GCP_IMAGE_NAME:$VERSION"

echo "build image $DOCKER_IMAGE_NAME"
# docker buildx build --platform linux/amd64 --push -t $DOCKER_IMAGE_NAME ./
# docker buildx build --platform linux/amd64 --push -t $DOCKER_IMAGE_NAME --build-arg SSH_PRIVATE_KEY=$SSH_PRIVATE_KEY ./
docker buildx build --platform linux/amd64 --push -t $DOCKER_IMAGE_NAME --build-arg GCP_CREDENTIALS_SECRET=$GCP_CREDENTIALS_SECRET ./

echo "finish export image"
gcloud run services update $GCP_APP_NAME-$ENV --image $DOCKER_IMAGE_NAME --platform managed --region $GCLOUD_RUN_REGION --port 8080
echo "finish update service"
