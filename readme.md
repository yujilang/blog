# 一级标题
## 二级标题
###### 六级标题

### 无序列表
* 1111
- 2222
- 3333
* 4444

### 有序列表
1. 1111
2. 2222
3. 3333

### 引用
> 阿萨大大实打实的

### 图片和链接
[百度](www.baidu.com)
![图片](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1507716993438&di=558f9b63bb87988efd1cbff1bc4cc302&imgtype=0&src=http%3A%2F%2Fwww.005.tv%2Fuploads%2Fallimg%2F160609%2F21-160609125052P7.jpg)

### 粗体和斜体，只支持英文
**baidu**
*baidu*


### python代码

```python

def detail(request,pk):
    #  根据pk主键在Post中查找数据，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
    #  get_object_or_404() 包含try：  except:
    post = get_object_or_404(Post,pk=pk)
    #  对 post.body 多了一个中间步骤，先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
    post.body = markdown(post.body,extensions=[
                         'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                        ])
    context = {'post':post}
    return  render(request,'blog/detail.html',context)

```
