FROM 3.13-alpine3.21

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

COPY . /app/

EXPOSE 8000

RUN groupadd -g 1000 turinabolum && useradd -u 1000 -g turinabolum -m turinabolum

RUN chown -R turinabolum:turinabolum /home/app/web

USER turinabolum

ENTRYPOINT ["sh", "./entrypoint.sh"]
