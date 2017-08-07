# coding=utf-8
from django.shortcuts import render
from models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    type_list = TypeInfo.objects.all()
    list = []
    for typeinfo in type_list:
        list.append({
            'type': typeinfo,
            'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
            'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
        })
    print(list)
    # 要得到什么信息？ 商品类duixiang，商品类型里对应点击量最高的商品duixiang，商品类型里对应最新shang品duixiang,这里要传对象过去
    # type_list = TypeInfo.objects.all()
    # list = []
    # for typeinfo in type_list:
    #     list.append({
    #         'type': typeinfo,
    #         'new': typeinfo.objects.order_by('-id')[0:4],
    #         'click': typeinfo.objects.order_by('gclick')[0:3]
    #
    #     })
    context = {'title': '首页', 'cart': '1', 'list': list}
    return render(request, 'tt_goods/index.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk = gid)
    goods_list = goods.gtype.goodsinfo_set.order_by('-gclick')[0:2]

    print goods_list

    context = {'title':'商品详情','goods':goods,'goods_list':goods_list}
    return render(request, 'tt_goods/detail.html',context,)


def list_goods(request, type_id, page_id, order_id):


    # 一个种类的对象
    typeinfo = TypeInfo.objects.get(pk=int(type_id))
    # 得到一个种类对应所有商品对象
    list_goods = typeinfo.goodsinfo_set.all()
    if order_id == '2':
        list_goods =typeinfo.goodsinfo_set.order_by('gprice')
    elif order_id == '3':
        list_goods = typeinfo.goodsinfo_set.order_by('-gclick')
    # 对商品对象进行分页，得到所有页面对象
    pageinator = Paginator(list_goods, 4)
    # 匹配分页
    if int(page_id) <= 0:
        page_id = 1
    if int(page_id) >= pageinator.num_pages:  # num_pages是的到对象总页数
        page_id = pageinator.num_pages
    page = pageinator.page(int(page_id))

    plist = pageinator.page_range
    if pageinator.num_pages > 5:
        if int(page_id) <= 2:
            plist = range(1, 6)
        elif int(page_id) >= pageinator.num_pages - 1:
            plist = range(pageinator.num_pages - 4, pageinator.num_pages + 1)
        else:
            plist = range(int(page_id) - 2, int(page_id) + 3)


    context = {'title': '商品列表', 'cart': '1', 'list_goods': list_goods, 'page': page, 'plist': plist, 'type': typeinfo}
    return render(request, 'tt_goods/list.html', context)
