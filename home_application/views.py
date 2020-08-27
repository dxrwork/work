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

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
import json
from home_application.models import workRecord
from home_application.models import AreaInfo
from log import logger
from django.http import JsonResponse
# 1.导出excel的库
import xlwt
# 2.实现了在内存中读写bytes
from io import BytesIO
#导入
import xlrd


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    return render(request, 'home_application/index_home.html')

def dev_guide(request):
    return render(request, 'home_application/dev_guide.html')

def contact(request):
    return render(request, 'home_application/contact.html')

def ebase(request):
    return render(request, 'home_application/ebase.html')

def render_json(res_dict):
    return HttpResponse(json.dumps(res_dict), content_type='application/json')

# 输入
def save_record(request):
    """
    保存数据
    """
    no11 = request.POST.get('no1', '')
    no21 = request.POST.get('no2', '')
    no31 = request.POST.get('no3', '')
    no41 = request.POST.get('no4', '')
    appearance = request.POST.get('appearance', '')
    measure = request.POST.get('measure', '')

    if no11 == '':
        no1 = no11
    else:
        no1 = AreaInfo.objects.get(id = no11).atitle
    if no21 == '':
        no2 = no21
    else:
        no2 = AreaInfo.objects.get(id = no21).atitle
    if no31 == '':
        no3 = no31
    else:
        no3 = AreaInfo.objects.get(id = no31).atitle
    if no41 == '':
        no4 = no41
    else:
        no4 = AreaInfo.objects.get(id = no41).atitle

    data = {
        'no1': no1,
        'no2': no2,
        'no3': no3,
        'no4': no4,
        'appearance': appearance,
        'measure': measure,
        'username': request.user.username,
    }
    result = workRecord.objects.save_record(data)
    return render_json(result)

# 显示
def records(request):
    """
    查询记录
    """
    record_list = workRecord.objects.all().order_by('id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'id': index+1,
            'no1': record.no1,
            'no2': record.no2,
            'no3': record.no3,
            'no4': record.no4,
            'appearance': record.appearance,
            'measure': record.measure,
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})

# 查询
def search(request):
    """
    查询数据
    """
    no11 = request.POST.get('no1')
    no21 = request.POST.get('no2')
    no31 = request.POST.get('no3')
    no41 = request.POST.get('no4')
    keyword = request.POST.get('keyword')
    if no11 == '':
        no1 = no11
    else:
        no1 = AreaInfo.objects.get(id = no11).atitle
    if no21 == '':
        no2 = no21
    else:
        no2 = AreaInfo.objects.get(id = no21).atitle
    if no31 == '':
        no3 = no31
    else:
        no3 = AreaInfo.objects.get(id = no31).atitle
    if no41 == '':
        no4 = no41
    else:
        no4 = AreaInfo.objects.get(id = no41).atitle

    mydata = []
    if no1 and no2 and no3 and no4:
        result = workRecord.objects.filter(no4 = no4).values('id','no1','no2','no3','no4','appearance','measure')
        mydata = json.dumps(list(result))
    elif no1 and no2 and no3:
        result = workRecord.objects.filter(no3 = no3).values('id','no1','no2','no3','no4','appearance','measure')
        mydata = json.dumps(list(result))
    elif no1 and no2:
        result = workRecord.objects.filter(no2 = no2).values('id','no1','no2','no3','no4','appearance','measure')
        mydata = json.dumps(list(result))
    elif keyword:
        mdata=[]
        result1 = list(workRecord.objects.filter(no1__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result2 = list(workRecord.objects.filter(no2__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result3 = list(workRecord.objects.filter(no3__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result4 = list(workRecord.objects.filter(no4__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result5 = list(workRecord.objects.filter(appearance__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result6 = list(workRecord.objects.filter(measure__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result = result1+result2+result3+result4+result5+result6
        for i in result:
            if i not in mdata:
                mdata.append(i)
        mydata = json.dumps(mdata)
    elif no1 :
        result = workRecord.objects.filter(no1 = no1).values('id','no1','no2','no3','no4','appearance','measure')
        mydata = json.dumps(list(result))

    return HttpResponse(mydata)
    return render(request,'meeting.html')

# 导出excel数据
def export_excel(request):
    no11 = request.GET.get('Key')
    no21 = request.GET.get('name')
    no31 = request.GET.get('Key1')
    no41 = request.GET.get('name1')
    keyword = request.GET.get('keyword')
    if no11 == '':
        no1 = no11
    else:
        no1 = AreaInfo.objects.get(id = no11).atitle
    if no21 == '':
        no2 = no21
    else:
        no2 = AreaInfo.objects.get(id = no21).atitle
    if no31 == '':
        no3 = no31
    else:
        no3 = AreaInfo.objects.get(id = no31).atitle
    if no41 == '':
        no4 = no41
    else:
        no4 = AreaInfo.objects.get(id = no41).atitle

    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=ebase.xls'
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
    sheet.write(0,0,'专业',style_heading)
    sheet.write(0,1,'故障类型',style_heading)
    sheet.write(0,2,'故障大类',style_heading)
    sheet.write(0,3,'故障小类',style_heading)
    sheet.write(0,4,'故障现象',style_heading)
    sheet.write(0,5,'处理措施',style_heading)

    if no1 and no2 and no3 and no4:
                # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(no1=no1,no2=no2,no3=no3,no4 = no4):
            # 格式化datetime
            sheet.write(data_row,0,i.no1)
            sheet.write(data_row,1,i.no2)
            sheet.write(data_row,2,i.no3)
            sheet.write(data_row,3,i.no4)
            sheet.write(data_row,4,i.appearance)
            sheet.write(data_row,5,i.measure)
            data_row = data_row + 1
    elif no1 and no2 and no3:
                # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(no1=no1,no2=no2,no3=no3):
            # 格式化datetime
            sheet.write(data_row,0,i.no1)
            sheet.write(data_row,1,i.no2)
            sheet.write(data_row,2,i.no3)
            sheet.write(data_row,3,i.no4)
            sheet.write(data_row,4,i.appearance)
            sheet.write(data_row,5,i.measure)
            data_row = data_row + 1
    elif no1 and no2:
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(no1=no1,no2=no2):
            # 格式化datetime
            sheet.write(data_row,0,i.no1)
            sheet.write(data_row,1,i.no2)
            sheet.write(data_row,2,i.no3)
            sheet.write(data_row,3,i.no4)
            sheet.write(data_row,4,i.appearance)
            sheet.write(data_row,5,i.measure)
            data_row = data_row + 1

    elif no1:
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.filter(no1=no1):
            # 格式化datetime
            sheet.write(data_row,0,i.no1)
            sheet.write(data_row,1,i.no2)
            sheet.write(data_row,2,i.no3)
            sheet.write(data_row,3,i.no4)
            sheet.write(data_row,4,i.appearance)
            sheet.write(data_row,5,i.measure)
            data_row = data_row + 1
    elif keyword:
        # 写入数据
        data_row = 1

        mdata=[]
        result1 = list(workRecord.objects.filter(no1__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result2 = list(workRecord.objects.filter(no2__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result3 = list(workRecord.objects.filter(no3__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result4 = list(workRecord.objects.filter(no4__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result5 = list(workRecord.objects.filter(appearance__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result6 = list(workRecord.objects.filter(measure__contains=keyword).values('id','no1','no2','no3','no4','appearance','measure'))
        result = result1+result2+result3+result4+result5+result6
        for i in result:
            if i not in mdata:
                mdata.append(i)
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in mdata:
            # 格式化datetime
            sheet.write(data_row,0,i['no1'])
            sheet.write(data_row,1,i['no2'])
            sheet.write(data_row,2,i['no3'])
            sheet.write(data_row,3,i['no4'])
            sheet.write(data_row,4,i['appearance'])
            sheet.write(data_row,5,i['measure'])
            data_row = data_row + 1
    else:
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in workRecord.objects.all():
            # 格式化datetime
            sheet.write(data_row,0,i.no1)
            sheet.write(data_row,1,i.no2)
            sheet.write(data_row,2,i.no3)
            sheet.write(data_row,3,i.no4)
            sheet.write(data_row,4,i.appearance)
            sheet.write(data_row,5,i.measure)
            data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response

# 导出模板
def export(request):

    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=example.xls'
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
    sheet.write(0,0,'专业',style_heading)
    sheet.write(0,1,'故障类型',style_heading)
    sheet.write(0,2,'故障大类',style_heading)
    sheet.write(0,3,'故障小类',style_heading)
    sheet.write(0,4,'故障现象',style_heading)
    sheet.write(0,5,'处理措施',style_heading)

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response

# 导入excel数据
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
                        dict_row = {'no1': table.cell_value(i, 0), 'no2': table.cell_value(i, 1),
                                    'no3': table.cell_value(i, 2),'no4': table.cell_value(i, 3),
                                    'appearance': table.cell_value(i, 4), 'measure': table.cell_value(i, 5)}
                        list_data.append(dict_row)
                    # 执行更新操作
                    for temp in list_data:
                       workRecord.objects.create(operator=request.user.username,**temp)
                    return render(request,'home_application/ebase.html')
                else:
                    return render(request,'home_application/ebase.html',{'message':"无可以导入的数据！"})
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
            return render(request,'home_application/ebase.html',{'message':'导入失败'})

#下拉框联动
def getNo1(request):
     no1 = AreaInfo.objects.filter(aParent__isnull = True)
     res = []
     for i in no1:
         res.append( [i.id , i.atitle] )
     return JsonResponse({'no1':res})

def getNo2(request):
    no2_id = request.GET.get('no2_id')
    no2 = AreaInfo.objects.filter(aParent_id=no2_id)
    res = []
    for i in no2:
        res.append([i.id, i.atitle])
    return JsonResponse({'no2':res})

def getNo3(request):
    no3_id = request.GET.get('no3_id')
    no3 = AreaInfo.objects.filter(aParent_id=no3_id)
    res = []
    for i in no3:
        res.append([i.id, i.atitle])
    return JsonResponse({'no3': res})

 #获得4

def getNo4(request):
    no4_id = request.GET.get('no4_id')
    no4 = AreaInfo.objects.filter(aParent_id=no4_id)
    res = []
    for i in no4:
        res.append([i.id, i.atitle])
    return JsonResponse({'no4': res})

# 左侧菜单更新查找
def research(request):

    tag3 = request.POST.get('Key')
    #print(tag3)
    mydata = []
    if tag3:
        result = workRecord.objects.filter(no3=tag3).values('id','no1','no2','no3','no4','appearance','measure')
        mydata = json.dumps(list(result))

    return HttpResponse(mydata)
    return render(result,'home_application/ebase.html')