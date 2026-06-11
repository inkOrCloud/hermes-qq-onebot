# NapCat CQ码使用指南

## 核心规则

**所有内容（包括文字）都放在一个CQ码块里，不要拆分！**

❌ 错误示例（拆分文字和CQ码）：
```
我将发送一张图片
```CQ
[CQ:image,file=/tmp/test.jpg]
```
```

✅ 正确示例（一个CQ码块包含所有内容）：
```CQ
我将发送一张图片 [CQ:image,file=/tmp/test.jpg]
```

## CQ码格式

所有CQ码都用 ` ```CQ ` 和 ` ``` ` 包裹：

```CQ
文字内容 [CQ:type,key=value] 更多文字
```

## 常用CQ码类型

### 1. 发送图片（带文字说明）

```CQ
看看这张图 [CQ:image,file=/path/to/image.jpg]
```

### 2. 发送语音（带文字说明）

```CQ
听听这个 [CQ:record,file=/path/to/audio.ogg]
```

### 3. 发送视频（带文字说明）

```CQ
视频来了 [CQ:video,file=/path/to/video.mp4]
```

### 4. 发送文件（带文字说明）

```CQ
这是你要的文件 [CQ:file,file=/path/to/document.pdf,name=文档.pdf]
```

### 5. @某人 + 发送媒体

```CQ
[CQ:at,qq=123456] 看看这个 [CQ:image,file=/tmp/test.jpg]
```

### 6. @全体成员 + 发送媒体

```CQ
[CQ:at,qq=all] 重要通知 [CQ:file,file=/tmp/notice.pdf,name=通知.pdf]
```

### 7. 发送表情

```CQ
[CQ:face,id=123]
```

## 组合示例

### 示例1：@某人 + 文字 + 图片

```CQ
[CQ:at,qq=204676209] 我画了一张图 [CQ:image,file=/tmp/drawing.png]
```

### 示例2：文字 + 多个媒体

```CQ
这是今天的报告 [CQ:file,file=/tmp/report.pdf,name=报告.pdf] 还有截图 [CQ:image,file=/tmp/screenshot.png]
```

### 示例3：纯文字（也可以用CQ码）

```CQ
这是一条普通消息
```

## 常见错误

### 错误1：拆分文字和CQ码块

❌ 错误：
```
我将发送图片
```CQ
[CQ:image,file=/tmp/test.jpg]
```
```

✅ 正确：
```CQ
我将发送图片 [CQ:image,file=/tmp/test.jpg]
```

### 错误2：多个CQ码块

❌ 错误：
```
```CQ
[CQ:at,qq=123]
```
我将发送图片
```CQ
[CQ:image,file=/tmp/test.jpg]
```
```

✅ 正确：
```CQ
[CQ:at,qq=123] 我将发送图片 [CQ:image,file=/tmp/test.jpg]
```

### 错误3：CQ码格式错误

❌ 错误：缺少方括号
```
```CQ
CQ:image,file=/tmp/test.jpg
```
```

✅ 正确：
```CQ
[CQ:image,file=/tmp/test.jpg]
```

### 错误4：在CQ码块外加文字

❌ 错误：
```
```CQ
[CQ:image,file=/tmp/test.jpg]
```
这是图片说明
```

✅ 正确：
```CQ
[CQ:image,file=/tmp/test.jpg] 这是图片说明
```

## URL格式

也可以使用URL：

```CQ
[CQ:image,file=https://example.com/image.jpg]
```

```CQ
[CQ:file,file=https://example.com/doc.pdf,name=文档.pdf]
```

## 调试提示

如果CQ码发送失败，检查：

1. 是否整条消息都是CQ码块（前后不能有文字）
2. CQ码格式是否正确（方括号、逗号、等号）
3. 文件路径是否存在
4. 文件格式是否支持

## 参考

完整CQ码列表请参考 [OneBot v11 文档](https://github.com/botuniverse/onebot-11/blob/master/message/segment.md)。