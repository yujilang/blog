from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def tree_search(d_dic,comment_obj):#这里不用传附近和儿子了因为他是一个对象,可以直接找到父亲和儿子
    for k,v_dic in d_dic.items():
        if k == comment_obj.parent_comment:#如果找到了
            d_dic[k][comment_obj] = {} #如果找到父亲了,你的把自己存放在父亲下面,并把自己当做key,value为一个空字典
            return
        else:#如果找不到递归查找
            tree_search(d_dic[k],comment_obj)



def generate_comment_html(sub_comment_dic,margin_left_val):
    #先创建一个html默认为空
    html = ""
    for k,v_dic in sub_comment_dic.items():#循环穿过来的字典
        html += ('<li style="margin-left:%spx" class="comment-item">' % margin_left_val + "\n\r"
                '<img class="img-circle" width="40" height="40" src="%s" alt="个人头像" />' + "\n\r"
                '<span class="nickname"><a href="/accounts/show/%d">%s</a></span>' + "\n\r"
                '<time class="submit-date">%s</time>' + "\n\r"
                '<div class="text">' + "\n\r"
                + str(k.text) + "\n\r"
                '</div>' + "\n\r"
                '</li>')%(k.name.profile.avatar.url,
                          k.name.id,
                          k.name,
                          k.created_time.strftime("%Y-%m-%d %T"))
        #上面的只是把第一层加了他可能还有儿子,所以通过递归继续加
        if v_dic:
            html += generate_comment_html(v_dic,margin_left_val+30)
    return html



@register.simple_tag
def build_comment_tree(comment_list):
    comment_dic = {}
    for comment_obj in comment_list: #每一个元素都是一个对象
        if comment_obj.parent_comment is None: #如果没有父亲
            comment_dic[comment_obj] = {}
        else:
            #通过递归找
            tree_search(comment_dic,comment_obj)

    # 上面完成之后开始递归拼接字符串

    html = ''
    margin_left = 0
    for k,v in comment_dic.items():
        #第一层的html
        html += ('<li class="comment-item">' + "\n\r"
                '<img class="img-circle" width="40" height="40" src="%s" alt="个人头像" />' + "\n\r"
                '<span class="nickname"><a href="/accounts/show/%d">%s</a></span>' + "\n\r"
                '<time class="submit-date">%s</time>' + "\n\r"
                '<div class="text">' + "\n\r"
                + str(k.text) + "\n\r"
                '</div>' + "\n\r"
                '</li>')%(k.name.profile.avatar.url,
                          k.name.id,
                          k.name,
                          k.created_time.strftime("%Y-%m-%d %T"))

        #通过递归把他儿子加上
        html += generate_comment_html(v,margin_left+30)
    return mark_safe(html)