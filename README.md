# QA over Paper

一个基于命令行的学术论文QA工具，大模型技术支持来自moonshot。

## 支持平台 

本工具支持Windows、Linux和MacOS，最新的命令行工具可到[发布页面](https://github.com/mcgrady20150318/qa/releases/tag/v0.1.7)下载。

## 使用

### id模式

该模式可直接通过输入arxiv id来执行后续操作，如下：

`./qa --id 2310.11511`

### 本地模式

该模式可直接通过输入本地pdf地址来执行后续操作，如下：

`./qa --pdf ./2310.11511.pdf`

## 工具截图

![demo](./assets/demo.png)

## Todo

- [x] 支持arxiv QA
- [x] 支持本地pdf QA
- [ ] 论文解析工具升级，目前用PyPDF2

## 加群交流

感兴趣的同学欢迎加微信：pwbot02交流，请备注：QA。