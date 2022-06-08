const express = require("express");
const expressWs = require("express-ws");
const { until } = require("selenium-webdriver");
const { Builder, By, Capabilities } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const assert = require("node:assert/strict");
const pino = require("pino");
const expressPino = require("express-pino-logger");
const fs = require("fs");
const mineType = require("mime-types");


const server = express();
expressWs(server);
const file = `./logs/${new Date().getTime().toString()}.txt`
const transport = pino.transport({
  target: 'pino/file',
  options: {
    destination: file,
    level: 'info',
  }
})
const logger = pino(transport);
server.use(expressPino({ logger }));

server.use((req, res, next) => {
  if (req.path !== "/" && !req.path.includes(".")) {
    res.set({
      // 由于vue启动时会自己占用一个端口，所以我们在服务端进行配置解决跨域问题
      "Access-Control-Allow-Credentials": true,
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers":
        "X-Requested-With,Content-Type,access-token",
      "Access-Control-Allow-Methods": "PUT,POST,GET,DELETE,OPTIONS",
      "Content-Type": "application/json; charset=utf-8",
    });
  }
  req.method === "OPTIONS" ? res.status(204).end() : next();
});

let port = 10099;
var host = "localhost";
server.listen(port, host, () => {
  logger.info(`server running @ http://${host}:${port}`);
});

server.ws("/localTest", async (ws, req) => {
  var path = "";
  var steps = {};
  var result = {};
  var broswer = null;
  ws.on("message", async (message) => {
    if (message != "ping") {
      var data = JSON.parse(message);
      path = data["path"];
      steps = data["steps"];
      broswer = init_browser(path);
      await broswer.manage().window().maximize();
      for (const step in steps) {
        res = await exectureTest(steps[step], broswer);
        result[step] = res;
        tmp = {}
        tmp[step] = res;
        if (res == "success") {
          ws.send(JSON.stringify(tmp));
        } else {     
          break;
        }
      }
      // 发送全部结果
      // ws.send(JSON.stringify(result));
      // 将本地log文件上传到服务器
      // let log = fs.readFileSync(file, "utf-8");
      // var log_buffer = Buffer.from(log).toString("base64");
      // var log_base64 = 'data:' + mineType.lookup(file) + ';base64,' + log_buffer;
      // ws.send(JSON.stringify({"log": log_base64}));
      ws.close();
      }
    });

  ws.on("close", async () => {
    await broswer.quit();
  });
});

function init_browser(path) {
  try {
    var options = new chrome.Options();
    var prefs = {
      "profile.managed_default_content_settings.images": 2,
      credentials_enable_service: false,
      "profile.password_manager_enabled": false,
      useAutomationExtension: false, // 去掉提示浏览器受控制
    };
    options.setUserPreferences(prefs);
    options.addArguments("window-size=1920x1080"); // 指定浏览器分辨率
    options.addArguments("--disable-gpu"); // 谷歌文档提到需要加上这个属性来规避bug
    options.addArguments("--hide-scrollbars"); // 隐藏滚动条, 应对一些特殊页面
    options.addArguments("blink-settings=imagesEnabled=false"); // 不加载图片, 提升速度
    options.addArguments("--disable-infobars");
    options.excludeSwitches("enable-automation"); // 解决无法输入中文的问题
    options.addArguments("--no-sandbox");
    options.addArguments("disable-infobars");
    options.addArguments("--disable-images"); // 禁用图像

    var caps = Capabilities.chrome();

    const service = new chrome.ServiceBuilder(path);

    var broswer = new Builder()
      .setChromeOptions(options)
      .withCapabilities(caps)
      .setChromeService(service)
      .forBrowser("chrome")
      .build();
    logger.info("init broswer success");
  } catch (error) {
    logger.error(error.message);
  }
  return broswer;
}

async function exectureTest(step, broswer) {
  current_element = null;
  try {
    switch (
      step["action"]["type"] // 根据action的类型进行不同的操作
    ) {
      case "get":
        await broswer[step["action"]["type"]](step["action"]["value"]);
        logger.info(`${step["action"]["type"]} ${step["action"]["value"]} success`);
        break;
      case "sendKeys":
        await broswer
          .wait(
            until.elementLocated(By[step["by"]](step["value"])),
            20 * 1000,
            `查找${step["by"]}:${step["value"]}元素超时`
          )
          .then(async (element) => {
            if (!(await element.isEnabled())) {
              throw `元素${step[key]["by"]}:steps[key]['value']不可用`;
            } else {
              await element[step["action"]["type"]](step["action"]["value"]);
              logger.info(`${step["action"]["type"]} ${step["action"]["value"]} success`);
            }
          });
        break;
      case "click":
        await broswer
          .wait(
            until.elementLocated(By[step["by"]](step["value"])),
            20 * 1000,
            `查找${step["by"]}:${step["value"]}元素超时`
          )
          .then(async (element) => {
            current_element = element;
            if (!(await element.isEnabled())) {
              throw `元素${step[key]["by"]}:steps[key]['value']不可用`;
            } else {
              await element[step["action"]["type"]]();
              logger.info(`${step["action"]["type"]} success`);
            }
          });
        break;
      case "assert":
        break;
    }
    return "success";
  } catch (error) {
    logger.error(error.message);
    return error.message;
  }
}
