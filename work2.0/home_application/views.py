# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.shortcuts import render
from django.http import HttpResponse
import json
from home_application.models import workRecord
from log import logger
from django.db import transaction

# 1.导出excel的库
import xlwt
# 2.实现了在内存中读写bytes
from io import BytesIO
#导入
import xlrd
from xlrd import xldate_as_tuple

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    return render(request, 'home_application/index_home.html')

def dev_guide(request):
    return render(request, 'home_application/dev_guide.html')

def contact(request):
    return render(request, 'home_application/contact.html')

def helloworld(request):
    return render(request, 'home_application/helloworld.html')

def meeting(request):
    return render(request, 'home_application/meeting.html')

def chaxun(request):
    return render(request, 'home_application/chaxun.html')

def render_json(res_dict):
    return HttpResponse(json.dumps(res_dict), content_type='application/json')


# 输入值提交请求
def say_hello(request):
    data = request.POST.get('input', None)
    data = 'Congratulations!'if data == 'Hello' else 'Try input Hello'
    res = {'data': data}
    return render_json(res)

def save_record(request):
    """
    保存数据
    """
    sort = request.POST.get('sort', '')
    theme = request.POST.get('theme', '')
    content = request.POST.get('content', '')

    data = {
        'sort': sort,
        'theme': theme,
        'content': content,
        'username': request.user.username,
    }
    result = workRecord.objects.save_record(data)

    return render_json(result)


def records(request):
    """
    查询记录
    """
    record_list = workRecord.objects.all().order_by('id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'id': index,
            'sort': record.sort,
            'theme': record.theme,
            'content': record.content,
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})

# 查询
def search(request):
    """
    查询数据
    """
    sort = request.POST.get('sort')
    theme = request.POST.get('theme')
    #content = request.POST.get('content')

    mydata = []
    if sort and theme:
        result = workRecord.objects.filter(sort = sort,theme = theme).values('id','sort','theme','content')
        mydata = json.dumps(list(result))
    if sort:
        result = workRecord.objects.filter(sort = sort).values('id','sort','theme','content')
        mydata = json.dumps(list(result))
    if theme:
        result = workRecord.objects.filter(theme = theme).values('id','sort','theme','content')
        mydata = json.dumps(list(result))

    return HttpResponse(mydata)
    return render(request,'chaxun.html')


# 导出excel数据
def export_excel(request):
    sort = request.GET.get('Key')
    theme = request.GET.get('name')
    print(sort,theme)
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=meeting.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

	# 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入文件标题
    sheet.write(0,0,'序号',style_heading)
    sheet.write(0,1,'类别',style_heading)
    sheet.write(0,2,'会议主题',style_heading)
    sheet.write(0,3,'会议内容',style_heading)

    if sort and theme:
                # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(sort = sort,theme = theme):
            # 格式化datetime
            sheet.write(data_row,0,i.id)
            sheet.write(data_row,1,i.sort)
            sheet.write(data_row,2,i.theme)
            sheet.write(data_row,3,i.content)
            data_row = data_row + 1
    elif sort:
                # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(sort = sort):
            # 格式化datetime
            sheet.write(data_row,0,i.id)
            sheet.write(data_row,1,i.sort)
            sheet.write(data_row,2,i.theme)
            sheet.write(data_row,3,i.content)
            data_row = data_row + 1
    elif theme:
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(theme = theme):
            # 格式化datetime
            sheet.write(data_row,0,i.id)
            sheet.write(data_row,1,i.sort)
            sheet.write(data_row,2,i.theme)
            sheet.write(data_row,3,i.content)
            data_row = data_row + 1
    else:
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.all():
            # 格式化datetime
            sheet.write(data_row,0,i.id)
            sheet.write(data_row,1,i.sort)
            sheet.write(data_row,2,i.theme)
            sheet.write(data_row,3,i.content)
            data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 导入数据
def excel_upload(request):
    if request.method == "POST":

        f = request.FILES.get('mfile')
        type_excel = f.name.split('.')[1]
        if type_excel in ['xlsx','xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read(), formatting_info=True)  # 关键点在于这里
            table = wb.sheets()[0]
             # 获取表的行数
            row_count = table.nrows
                # 获取列数
            col_count = table.ncols
            try:
                # --------业务相关start---------
                # 转换成字典
                if row_count > 1:
                    # 行下标是从0开始；本人的excel表格第一行为列名，所以数据从第2行开始
                    list_data = []
                    for i in range(1, row_count):
                        dict_row = {}
                        dict_row['sort']=table.cell_value(i, 0)
                        dict_row['theme']=table.cell_value(i, 1)
                        dict_row['content']=table.cell_value(i, 2)
                        list_data.append(dict_row)
                    # 执行更新操作
                    for temp in list_data:
                       workRecord.objects.create(operator=request.user.username,**temp)
                    return render(request,'home_application/chaxun.html')
                else:
                    return render(request,'home_application/chaxun.html',{'message':"无可以导入的数据！"})
                # ---------业务相关end----------

                # 3.用完记得删除
                wb.release_resources()
                del wb
            except:
               logger.error('解析excel文件或者数据插入错误')
               print('22222')
        else:
            logger.error('上传文件类型错误！')
            print('33333')
            return render(request,'home_application/chaxun.html',{'message':'导入失败'})





