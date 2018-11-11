var apiSpided = function(callback) {
    var path = '/api/spided'
    ajax('GET', path, '', callback)
}

var loadData = function() {
    apiSpided(function(r) {
        var datas = JSON.parse(r)
        var t_body = document.getElementsByTagName('tbody')
        var table = e('.spided')
        table.removeChild(t_body[0])
        var n_tbody = table.createTBody()
        for (var i = 0; i < datas.length; i++) {
            var tr = document.createElement('tr')
            var form = document.createElement('form')
            form.setAttribute('action', '/task')
            form.setAttribute('method', 'post')
            var data = datas[i]
            var trHtml = `<input type="hidden" name="url" value="${data.url}">
                            <input type="text" name="university" value="${data.university}">
                            <input type="text" name="department" value="${data.department}">
                            <input type="hidden" name="slowdown" value="2">
                            <input type="submit" name="submit" value="重爬" class= "btn btn-defaul">
                            `
            form.innerHTML = trHtml
            n_tbody.appendChild(form)
        }
    })
}


var bindEvenClickRespided = function(){
    var a = 'a'
    pass
}

window.onload = loadData
