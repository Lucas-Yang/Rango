FROM python:3.7
RUN apt-get update

RUN useradd -u 7788 work --create-home --no-log-init --shell /bin/bash

USER root
WORKDIR /home/work/my_app
RUN chown -R work:work /home/work/my_app
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
USER work
COPY --chown=work:work . .
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN export C_FORCE_ROOT="true"
RUN export COLUMNS=80
EXPOSE 8000

CMD ["/bin/bash", "begin.sh"]
