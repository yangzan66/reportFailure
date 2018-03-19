#功能：分页显示的模块
from django.utils.safestring import mark_safe
#定义Page类
#使用这个类时，必需要指定base_url，
# 可以通过per_page_count指定每页显示几行数据
#可以通过pager_num指定显示几个页的索引，必须是奇数
#前端user_list.html里的js代码不需要修改，直接用就行
class Page:
    '''
    current_page:当前是第几页
    data_count:数据的总个数
    per_page_count:每页显示行数，
    pager_num:显示几个页码索引,必须是奇数
    '''
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
    # self.current_page = current_page
      self.data_count = data_count
      self.per_page_count = per_page_count
      self.pager_num = pager_num
      if current_page > self.all_count():  # 如果当前要显示的页数大于总的页数,在由没有显示10行改到每页显示80行的时候，可能会出现这种问题。显示10行时有地20页，但改为每页显示80行，可能就没第20页了
        self.current_page = 1  # 自动跳转到第一页
      else:
        self.current_page = current_page

    #计算出每页的起始行索引
    def start(self):
        return (self.current_page - 1) * self.per_page_count  # 一页显示count_per_page个数据
    #计算出每页的结束行索引
    def end(self):
        return self.current_page * self.per_page_count

    #计算一共有多少页
    def all_count(self):
        count, yushu = divmod(self.data_count, self.per_page_count)  # 求商和余数,
        if yushu:  # 如果余数不为0
            count += 1  # 总的页数是商+1。count表示总的页数
        return count

    #得到要添加到html里的代码,显示页码索引
    def page_str(self,base_url):
        page_list = []
        # 显示当前页和前5页和后5页共11页的索引
        if self.all_count() < self.pager_num:  # 如果总页数小于page_index_count 11
            start_index = 1
            end_index = self.all_count() + 1
        else:  # 如果总页数大于page_index_count 11
            if self.current_page <= (self.pager_num + 1) / 2:  # 如果当前选的页面<=6
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.all_count():  # 如果当前页+5大于总页数
                    start_index = self.all_count() - self.pager_num + 1
                    end_index = self.all_count() + 1  # 让总页数作为最后一页
        page_str_prefix = '<nav aria-label="Page navigation"> <ul class="pagination">' #bootstrap样式
        page_list.append(page_str_prefix)
        first_page_str = '''  
                            <li>
                                <a href="%s?p=%s">
                                  <span aria-hidden="true">首页</span>
                                </a>
                            </li>
                        ''' % (base_url, 1)  # 跳转到第一页
        page_list.append(first_page_str)
        if self.current_page <= 1:  # 如果当前页是第一页，没有上一页了
            Pre_page_str = '''
                        <li>
                            <a href="#" aria-label="Previous">
                            <span aria-hidden="true">上一页</span>
                            </a>
                        </li>
            '''  # 什么都不干，href=#也表示什么都不干
        else:
            Pre_page_str = '''
                        <li>
                            <a href="%s?p=%s" aria-label="Previous">
                            <span aria-hidden="true">上一页</span>
                            </a>
                        </li>
                        '''% (base_url,self.current_page - 1,)
        page_list.append(Pre_page_str)  # 把上一页的标签先添加进去
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:  # 如果当前标签是选中查看的标签，给它多赋一个active样式，让它高亮显示
                tmp = '<li class="active"><a href="%s?p=%s">%s</a></li>' % (base_url,i, i)  # 字符串拼接
            else:
                tmp = '<li><a href="%s?p=%s">%s</a></li>' % (base_url, i, i)  # 字符串拼接
            page_list.append(tmp)
        if self.current_page >= self.all_count():  # 如果当前页是最后一页
            Next_page_str = '''
                        <li>
                            <a href="#" aria-label="Next">
                              <span aria-hidden="true">下一页</span>
                            </a>
                        </li>
                    '''
        else:
            Next_page_str = '''
                        <li>
                            <a href="%s?p=%s" aria-label="Next">
                              <span aria-hidden="true">下一页</span>
                            </a>
                        </li>
                    ''' % (base_url,self.current_page + 1,)
        page_list.append(Next_page_str)  # 把下一页的标签先添加到最后
        last_page_str = '''  
                            <li>
                                <a href="%s?p=%s">
                                  <span aria-hidden="true">末页</span>
                                </a>
                            </li>
                        ''' % (base_url, self.all_count())  # 跳转到最后一页
        page_list.append(last_page_str)
        page_str_suffix = '</ul></nav>' #bootstrap样式的结尾
        page_list.append(page_str_suffix)
        page_str = ''.join(page_list)  # 转成字符串
        page_str = mark_safe(page_str)  # 把这个字符串标记为安全，效果和html里|safe一样，让编译器把这段字符串解释成html语言，否则，它只是个字符串
        return page_str