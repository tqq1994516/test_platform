import express from 'express';
import expressWs from 'express-ws'
import { Builder, By } from 'selenium-webdriver';
import chrome from 'selenium/chrome';


const server = express();
expressWs(server);
server.use((req, res, next) => {
    if (req.path !== '/' && !req.path.includes('.')) {
    res.set({
      // 由于vue启动时会自己占用一个端口，所以我们在服务端进行配置解决跨域问题
        'Access-Control-Allow-Credentials': true,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type,access-token',
        'Access-Control-Allow-Methods': 'PUT,POST,GET,DELETE,OPTIONS',
        'Content-Type': 'application/json; charset=utf-8',
        });
    }
    req.method === 'OPTIONS' ? res.status(204).end() : next();
});

let port = 10099;
var host = 'localhost';
server.listen(port, host, () => {
    console.log(`server running @ http://${host}:${port}`);
});

server.ws('/localTest', (ws, req) => {
    console.log(`request /localTest`);
    
    // jsOpenWeb();
});

function jsOpenWeb () {
    const broswer = new Builder().forBrowser('chrome').build()
    broswer.get('https://www.baidu.com')
    // broswer.wait(until.alertIsPresent()).then(() => {
      // broswer.switchTo().alert().accept().then(() => {
        //broswer.findElement(By.id('fraInterface')).then((value) => {
        // console.log(value)
        // broswer.switchTo().frame(value).then(() => {
          //下面两行代码效果一样的
          //通过元素id找到该元素并写入值
            broswer.findElement(By.id('kw')).sendKeys('搜索内容')
          //通过元素name找到该元素并写入值
            // broswer.findElement(By.name('')).sendKeys('搜索内容')
        // })
       // })
     // })
    // })
}
