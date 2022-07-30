FROM node:latest AS build
USER root
# 换系统源
ADD ../sources.list /etc/apt/
# 设置环境变量
ENV TZ=Asia/Shanghai
RUN set -eux; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone
ENV LANG en_US.utf8
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
# 安装/更新系统依赖
RUN apt-get -y update && apt-get install -y vim && apt-get clean all
# 更新pip
RUN python -m pip install --upgrade pip
WORKDIR /test_platform
ADD ../frontend .
RUN npm install -g pnpm
# pnpm换源
RUN pnpm config set registry https://registry.npm.taobao.org
# 安装/更新前端依赖
WORKDIR /frontend
RUN pnpm install

FROM build AS development
EXPOSE 3100
ENTRYPOINT ["pnpm", "serve"]

