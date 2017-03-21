# Wbot

基于 ItChat 开发的机器人，ItChat 代码 clone 于 d9a7cec(Nov 3, 2016)，后根据需求
修改。

机器人主要服务于 PY Learning 微信群。


## Usage

首先安装各种依赖。目前机器人只在 Python3 环境下测试通过。

```bash
pip install -r requirements.txt
```

然后执行启动脚本:

```bash
python run.py
```

## Configuration

配置文件的加载顺序为：

1. 加载模版配置文件`wbot/config.dist.py`，载入默认配置
1. 加载执行目录文件`config.py`, 载入用户配置
1. 加载环境变量中的`WXBOT_CONFIG`变量所指向的文件，载入生产环境配置

后载入的配置会覆盖先载入的配置。

配置项目的相关说明参照配置模版文件。

如果您要修改配置文件，请复制文件`wbot/config.dist.py`到项目根目录，并命名为`config.py`，或执行以下指令：
```bash
cp wbot/config.dist.py ./config.py
```

### 配置变量命名

要求全部大写。

顶层配置项目按照模版方式命名。

模块相关配置按照模块前缀的方式命名，例如Recall模块定义的前缀为`"RECALL"`，
则其相关配置项目的命名遵守`"RECALL_XXXXX"`的形式进行命名。

模块内部读取配置时，只能看到自己相关的配置变量，并会自动消除前缀。

## Contribute

### 基本概念

1. 微信的诸多基本使用
2. [itchat](http://itchat.readthedocs.io/zh/latest/) 接口使用

### 模型说明

#### Bot

基础的机器人类型，由多个模块构成，一个微信账号对应一个Bot，处理该微信号下的全部消息分发

#### Module

机器人的逻辑模块，专注于某一项的功能

#### 消息分发机制

收到一条消息时，Bot从模块注册表中轮询各个模块对于该消息的匹配值,

+ 0表示模块不愿意处理该消息
+ 100表示模块一定要处理该消息
+ -1表示该模块希望收到该消息但不做回复处理

每次分发的过程最多有一个主处理模块，和不限个数后台模块被通知。

#### 预设模块

1. TulingModule。自动问答模块
2. RecallModule。自动防撤回模块
3. InterpreterModule。一个微信在线的Python解释器模块
