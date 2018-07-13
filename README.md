# MXJDSpider
## 数据库
```
# Mac OS 安装MongoDB
brew install mongodb
```
## 要求
* *Python 3.5+*
* *selenium >= 3.11.0*
* *Beautiful Soup >= 4.6.0*
* *pymongo >= 3.4.0*
* *scrapy >= 1.5.0*

## 工作
* 使用selenium驱动无界面浏览器获取网页信息
* 模拟翻页操作，进行翻页爬取
* 将产品信息存储到MongoDB

## 使用
```
git clone git@github.com:iamhmx/MXJDSpider.git
```
* 普通方式

```
cd MXJDSpider/jd_products
python jd_spider.py
```

* scrapy

```
cd MXJDSpider/jd_products/scrapy/jd
scrapy crawl jd
```

## 效果
![运行](https://github.com/iamhmx/MXJDSpider/blob/master/screenshots/result.png?raw=true)

![手机](https://github.com/iamhmx/MXJDSpider/blob/master/screenshots/db1.png?raw=true)

![空气净化器](https://github.com/iamhmx/MXJDSpider/blob/master/screenshots/db2.png?raw=true)