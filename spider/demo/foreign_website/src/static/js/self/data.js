// 全局变量 o
var getKeys = function(){
    var k = {}
    k.university = function(){
        var u = e('.universitys')
        var uIndex = u.options.selectedIndex
        var university = u.options[uIndex].value
        return university
    }

    k.department = function(){
        var d = e('.departments')
        var dIndex = d.options.selectedIndex
        var department = d.options[dIndex].value
        return department
    }

    k.loadAllpage = function(){
        form = {
            university: k.university(),
            department: k.department(),
        }
        apiAllPage(form, function(r){
            var data = JSON.parse(r)
            var page = Math.ceil(data.countData/20)
            loadAllPage(page)
            getData()
        })
    }

    k.nowPage = function(){
        var p = document.getElementsByClassName('active')
        if(p[0]){
            var page = p[0].innerText
        }
        else{
            var page = 1
        }
        return page
    }
    return k
}

// ajax api
var apiAllPage = function(form, callback){
    var path = '/data/api/page'
    ajax('POST', path, form, callback)
}


var apiUniversity = function(callback){
    var path = '/data/api/universitys'
    ajax('GET', path, '', callback)
}


var apiDeparments = function(form, callback){
    var path = '/data/api/deparments'
    ajax('POST', path, form, callback)
}


var apiData = function(form, callback){
    var path = '/data/api/data'
    ajax('POST', path, form, callback)
}

var apiDelete = function(id, callback){
    var path = `/data/api/delete?id=${id}`
    ajax('GET', path, '', callback)
}


//事件函数
var loadAllPage = function(page){
    var allpage = page
    var pageList = e('.pagination')
    var preButton = `<li><a href="#" aria-label="Previous">上一页</a></li>`
    var nextButton = `<li><a href="#" aria-label="Next">下一页</a></li>`
    var html = preButton
    for (var i = 0; i < allpage; i++) {
        if( i + 1 === 1){
            var tr = `<li class="active"><a href='#'>${i+1}</li>`
        }
        else{
            var tr = `<li><a href='#'>${i+1}</li>`
        }
        html += tr
    }
    html += nextButton
    pageList.innerHTML = html
}


var loadUniversity = function(){
    apiUniversity(function(r){
        var datas = JSON.parse(r)
        var sel = e('.universitys')
        for (var i = 0; i < datas.length; i++) {
            sel.options.add(new Option(datas[i], datas[i]))
        }
        getDepartments()
    })
}


var loadData = function(datas){
    var table = e('.data')
    var t_body = document.getElementsByTagName('tbody')
    table.removeChild(t_body[0])
    var n_tbody = table.createTBody()
    for (var i = 0; i < datas.length; i++) {
        var tr = document.createElement('tr')
        var data = datas[i]
        var trHTMl = `<td>${data.university}</td>
                        <td>${data.department}</td>
                        <td><a href="../data/content/${data.id}" target='_blank'>${data.teacher}</a></td>
                        <td class="data-delete"><button class= "btn btn-defaul" type="button" name="delete" id="${data.id}">删除</button></td>`
        tr.innerHTML = trHTMl
        n_tbody.appendChild(tr)
    }
}


var defaultListClass = function(lNode){
    for (var i = 0; i < lNode.length; i++) {
        lNode[i].removeAttribute('class')
    }
}


var defaultPage = function(){
    var nar = document.getElementsByClassName('pagination')[0]
    var list = nar.getElementsByTagName('li')
    defaultListClass(list)
    list[1].setAttribute('class', 'active')
}


var getDepartments = function(){
    var form = {
        'university': o.university(),
    }
    apiDeparments(form, function(r){
        var datas = JSON.parse(r)
        var sel = e('.departments')
        sel.options.length = 0
        for (var i = 0; i < datas.length; i++) {
            sel.options.add(new Option(datas[i], datas[i]))
        }
        o.loadAllpage()
        getData()
    })
}


var getData = function(){
    var form = {
        'university': o.university(),
        'department': o.department(),
        'page': o.nowPage(),
        }
        apiData(form, function(r){
            var datas = JSON.parse(r)
            loadData(datas)
    })
}

// 事件绑定
var bindEvenClickPage = function(){
    var p = e('.pagination')
    p.addEventListener('click', function(event){
        var nowPageNode = document.getElementsByClassName('active')[0]
        var a = event.target
        var nextOrPrevious = a.getAttribute('aria-label')
        if (a.getAttribute('href')){
            var liList = document.getElementsByTagName('li')
            defaultListClass(liList)
            if (nextOrPrevious) {
                if (nextOrPrevious === 'Next') {
                    if (!nowPageNode.nextElementSibling.children[0].getAttribute('aria-label')) {
                        nowPageNode.nextElementSibling.setAttribute('class', 'active')
                    }
                    else {
                        nowPageNode.setAttribute('class', 'active')
                    }
                }
                else {
                    if (!nowPageNode.previousElementSibling.children[0].getAttribute('aria-label')) {
                        nowPageNode.previousElementSibling.setAttribute('class', 'active')
                    }
                    else {
                        nowPageNode.setAttribute('class', 'active')
                    }
                }

            }
            else {
                var l = a.parentNode
                l.setAttribute('class', 'active')
            }
            getData()
        }
    })
}


var bindEvenGetDeparment = function(){
    var s = e('.universitys')
    s.addEventListener('change', getDepartments)
}


var bindEvenGetData = function(){
    var d = e('.departments')
    d.addEventListener('change', o.loadAllpage)
}


var bindEvenLoadUniversity = function(){
    window.onload = loadUniversity
}


var bindEvenDeleteMsg = function(){
    var p = e('.data')
    p.addEventListener('click', function(event){
        var t = event.target
        if(t.name == 'delete'){
            apiDelete(t.id, function(r){
                getData()
            })
        }
    })
}


var bindEven = function(){
    bindEvenGetDeparment()
    bindEvenGetData()
    bindEvenClickPage()
    bindEvenLoadUniversity()
    bindEvenDeleteMsg()
}

// 主函数
var main = function () {
    window.o = getKeys()
    bindEven()
}


main()
