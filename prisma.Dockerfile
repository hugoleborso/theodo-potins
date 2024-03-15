FROM python:3.11-slim-buster
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git curl

# Install Prisma CLI
RUN pip3 install prisma

COPY schema.prisma schema.prisma

# Generate Prisma client
RUN prisma generate


# Expose the port Prisma Studio uses
EXPOSE 5555

# Start Prisma Studio
CMD ["prisma", "studio", "--port", "5555","--schema", "schema.prisma"]
