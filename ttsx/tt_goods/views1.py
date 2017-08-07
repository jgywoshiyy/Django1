# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator
from models import TypeInfo, GoodsInfo


# Create your views here.
def index(request):
    '''
    book.heroinfo_set.all()
    模板中需要的数据包括：分类信息，当前分类的最新的4个商品，当前分类的人气最高的3个商品
    共6个分类，所以会有6组以上的信息
    list=[{type:,list_new:,list_click:},{type:,list_new:,list_click:},....]
    '''
    type_list = TypeInfo.objects.all()
    list = []
    for typeinfo in type_list:
        list.append({
            'type': typeinfo,
            'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
            'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
        })
    context = {'title': '首页', 'cart': '1', 'list': list}
    return render(request, 'tt_goods/index.html', context)


def list_goods(request, type_id, page_index):
    typeinfo = TypeInfo.objects.get(pk=type_id)

    list = typeinfo.goodsinfo_set.order_by('-id')

    paginator = Paginator(list, 10)

    page_index = int(page_index)
    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(int(page_index))

    plist = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= paginator.num_pages - 1:
            plist = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            plist = range(page_index - 2, page_index + 3)

    context = {'title': '列表页', 'cart': 1, 'type': typeinfo, 'page': page, 'pindex_list': plist}
    return render(request, 'tt_goods/list.html', context)


'''
共n页
第1页：1 2 3 4 5
第2页：1 2 3 4 5
第3页：1 2 3 4 5
    range[pindex-2,pindex+3]
第4页：2 3 4 5 6
...
第p页(p=n-2)：满足公式
第p页(p=n-1)：n-4 n-3 n-2 n-1 n
第p页(p=n)：n-4 n-3 n-2 n-1 n
'''
