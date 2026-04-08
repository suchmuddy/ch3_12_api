from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def search_list(request):
    if 'cname' in request.GET:
        cname=request.GET['cname']
        print(cname)#http://192.168.58.10:8080/search_list/?cname=黃靖輪
        resultList=students.objects.filter(cname__contains=cname)#模板查詢,包含cname都會查尋出來
    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))
    #return HttpResponse("Hello, this is the search list page.")//HttpResponse用途：直接回傳文字、HTML、JSON 等內容,第一個參數必須是「字串或 bytes」，不能放 request 或模板名稱

    errormessage=""
    #resultList=[]#模擬查詢結果為空,無資料

    if not resultList:
        errormessage="No data found."
    #return render(request,'search_list.html',locals())
    return render(request,'search_list.html',{'resultList':resultList,'errormessage':errormessage})
#render用途：將模板（HTML 文件）渲染成 HTTP 回應，並可以帶資料給模板,顯示複雜 HTML / 帶資料 / 有迴圈或條件

def search_name(request):
    return render(request,'search_name.html')

from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip()#去除前後空白
        keywords=site_search.split()#以空白分割字串成多個關鍵字
        # print(f"site_search={site_search}")
        print(keywords)
        #一個關鍵字+搜尋一個欄位
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid')#查詢如果有顯示
        #一個關鍵字+搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cid__contains=site_search) |
        #     Q(cname__contains=site_search) |
        #     Q(cbirthday__contains=site_search) |
        #     Q(cemail__contains=site_search) |
        #     Q(cphone__contains=site_search) |
        #     Q(caddr__contains=site_search) 
        # )
        #多個關鍵字+多個欄位
        # resultList=[]
        query=Q()
        for keyword in keywords:
            keyword_Q = (
                Q(cid__icontains=keyword) |
                Q(cname__icontains=keyword) |
                Q(cbirthday__contains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__contains=keyword) |
                Q(caddr__icontains=keyword)
            )
            # 🔥 處理布林欄位
            kw = keyword.lower()
            if kw in ["男", "male","m", "1", "true"]:
                keyword_Q |= Q(csex="M")
            elif kw in ["女", "female","m","0", "false"]:
                keyword_Q |= Q(csex="F")
            query &= keyword_Q   # 🔥 AND 關鍵字

        resultList=students.objects.filter(query)
        # for item in students.objects.all():#確認型態 <class 'str'>要修正方法,所
        # 以搜尋性別要改成比對 M / F，不是 True / False。
        #     print(item.cname, item.csex, type(item.csex))
    else:
        resultList = students.objects.all().order_by('cid')   

    for item in resultList:#檢查碼
        print(model_to_dict(item))
    data_count=len(resultList)
    print(f"Total data count: {data_count}")

    status= True
    errormessage=""
    if not resultList:
        status = False
        errormessage="No data found."#當 resultList 是空的（沒有任何資料）時，就會出現 "No data found."

    #return HttpResponse("Hello, this is the index page.")

    #分頁設定,每頁顯示2筆資料
    paginator = Paginator(resultList, 5)
    page_nmber = request.GET.get('page') #獲取當前頁碼
    page_obj = paginator.get_page(page_nmber) #獲取當前頁的資料
    print(f"page_nmber={page_nmber}")
    for item in page_obj:
        print(model_to_dict(item))

    return render(request, 'index.html',
                  {'resultList':resultList,
                   'status':status,
                   'errormessage':errormessage,
                   'data_count':data_count,
                   'page_obj':page_obj,
                   }
                )

from django.shortcuts import redirect
def post(request):
    if request.method == 'POST':
        cname=request.POST.get('cname')
        csex=request.POST.get('csex')
        cbirthday=request.POST.get('cbirthday')
        cemail=request.POST.get('cemail')
        cphone=request.POST.get('cphone')
        caddr=request.POST.get('caddr')
        print(f"Received POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
        add=students(cname=cname,csex=csex,cbirthday=cbirthday,cemail=cemail,cphone=cphone,caddr=caddr)
        add.save()
        return redirect('index')
    else:
        return render(request,'post.html')
    
    #return HttpResponse("Hello,this is the post page.")

def edit(request, id):
    print(id)
    if request.method == 'POST':
        cname=request.POST.get('cname')
        csex=request.POST.get('csex')
        cbirthday=request.POST.get('cbirthday')
        cemail=request.POST.get('cemail')
        cphone=request.POST.get('cphone')
        caddr=request.POST.get('caddr')
        print(f"Received POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
        #orm
        updata = students.objects.get(cid=id)
        updata.cname=cname
        updata.csex=csex
        updata.cbirthday=cbirthday
        updata.cemail=cemail
        updata.cphone=cphone
        updata.caddr=caddr
        updata.save()
        return redirect('index')#重定向到 index頁面,顯示更新後的數據列表
        #return HttpResponse("已送出POST請求。")
    else:
        obj_data=students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        #return HttpResponse("Hello") 
        return render(request,'edit.html',{'obj_data':obj_data})

def delete(request, id): 
    print(id)
    if request.method == 'POST':
        delete_data = students.objects.get(cid=id)
        delete_data.delete()
        return redirect('index')#重定向到 index 頁面.顯示更新後的數據列表
        #return HttpResponse("已送出 POST 請求。")
    else:
        obj_data=students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request,'delete.html',{'obj_data':obj_data})
    
from django.http import JsonResponse 
def getAllItems(request):
    resultObject=students.objects.all().order_by('cid')
    # print(type(resultObject))
    # for item in resultObject:
    #     print(model_to_dict(item))
    #     print(type(item))
    resultList=list(resultObject.values())#將querySet元素為object,轉成list元素為dict的型態)
    #Django QuerySet（QuerySet of object）→ .values() = object → dict(把「每個 object」拆成 dict,<object → dict>),list() = QuerySet → list<QuerySet → list>
    #把「資料庫查出來的一堆物件」,轉成「一個 list，裡面每個都是 dict」->一堆盒子（object）,.values()：把每個盒子打開 → 變成內容（dict）,list()：把所有內容裝進清單（list）
    #API 回傳要用 JSON,JSON = dict / list 才能用,object 不能直接轉 JSON
    #JSON 最外層只能是：dict（物件）/list（陣列）,因為你現在的資料是多筆資料(list)，不是一筆(dict)
    # print(type(resultList))
    # for item in resultList:
    #     print(model_to_dict(item))
    #     print(type(item))
    #return HttpResponse("Hello")
    return JsonResponse(resultList,safe=False)
    #  safe=True,只允許傳入dict
    #  safe=False,只允許傳非dict

def getItem(request,id):
    try:
        obj = students.objects.get(cid=id)
        # print(model_to_dict(obj))#用 model_to_dict將object轉成dict
        resultDict=model_to_dict(obj)
        # return HttpResponse("Hello")
        return JsonResponse(resultDict,safe=False)
    except:
        return HttpResponse({"error": "Item not found"},status=404)

from django.views.decorators.csrf import csrf_exempt#停止CSRF驗證,讓外部程式也能呼叫這個API,任何 POST 都能送進來
#CSRF = 跨站請求偽造（Cross-Site Request Forgery）,表單 POST 必須有 csrf_token
#不要用在：登入系統/會員資料/金流 / 敏感操作,因為會有安全風險
@csrf_exempt#@csrf_exempt = 我不檢查安全，直接放行  
def createItem(request):
    try:
        if request.method == "GET":#https://example.com/user?id=1,問號拿資料
            cname = request.GET.get("cname")
            csex =request.GET.get("csex")
            cbirthday =request.GET.get("cbirthday")
            cemail =request.GET.get("cemail")
            cphone =request.GET.get("cphone")
            caddr =request.GET.get("caddr")
            print(f"Received GET data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            # return HttpResponse("get.......")#測試用
        elif request.method == "POST":#送資料（修改/新增）
            cname = request.POST.get("cname")
            csex =request.POST.get("csex")
            cbirthday =request.POST.get("cbirthday")
            cemail =request.POST.get("cemail")
            cphone =request.POST.get("cphone")
            caddr =request.POST.get("caddr")
            print(f"Received POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            # return HttpResponse("post.......")
        try:
            add=students(cname=cname,csex=csex,cbirthday=cbirthday,cemail=cemail,cphone=cphone,caddr=caddr)
            add.save()
            return JsonResponse({"message": "Item created successfully"},status=201)  
        except Exception as e:
            return JsonResponse({"error": "Failed to create item"},status=500)  
    except Exception as e:
        return JsonResponse({"error": "Item not found"},status=400)
    
@csrf_exempt
def updateItem(request,id):
    print(f"id={id}")
    try:
        if request.method == "GET":
            cname = request.GET.get("cname")
            csex =request.GET.get("csex")
            cbirthday =request.GET.get("cbirthday")
            cemail =request.GET.get("cemail")
            cphone =request.GET.get("cphone")
            caddr =request.GET.get("caddr")
            print(f"GET data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            return HttpResponse("get.......")#測試用
        elif request.method == "POST":
            cname = request.POST.get("cname")
            csex =request.POST.get("csex")
            cbirthday =request.POST.get("cbirthday")
            cemail =request.POST.get("cemail")
            cphone =request.POST.get("cphone")
            caddr =request.POST.get("caddr")
            print(f"POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            # return HttpResponse("post.......")
        try:
            #orm
            updata = students.objects.get(cid=id)
            updata.cname=cname
            updata.csex=csex
            updata.cbirthday=cbirthday
            updata.cemail=cemail
            updata.cphone=cphone
            updata.caddr=caddr
            updata.save()
            return JsonResponse({"message": "Item updated successfully"},status=200)
        except Exception as e:
            return JsonResponse({"error": "Failed to update item"},status=500)
    except Exception as e:
        return JsonResponse({"error": "Invalid data"},status=400)

