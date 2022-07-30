FROM python:latest AS build
USER root
# 换系统源
ADD ../sources.list /etc/apt/
ADD ../pip.conf /root/.pip/
# 设置环境变量
ENV TZ=Asia/Shanghai
RUN set -eux; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone
ENV LANG en_US.utf8
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
# 安装/更新系统依赖
RUN apt-get -y update && apt-get install -y vim python-pip python-setuptools && apt-get clean all
# 更新pip
RUN python -m pip install --upgrade pip
WORKDIR /test_platform
ADD ../backend .
# python依赖
RUN pip install -r /test_platform/backend/requirements.txt

FROM build AS development
EXPOSE ["8800", "8801"]
ENTRYPOINT ["python", "main.py"]
