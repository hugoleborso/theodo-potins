FROM python:3.11-slim-buster
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git curl

# Install Prisma CLI
RUN pip3 install prisma

COPY schema.prisma schema.prisma
COPY ./migrations migrations

# Generate Prisma client
RUN prisma generate

# Start Prisma Studio
CMD ["prisma", "migrate", "deploy"]
