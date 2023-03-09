//This file can help you generate uuid via the same way as official

function uuid() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(n) {
        var t = Math.random() * 16 | 0
          , i = n == "x" ? t : t & 3 | 8;
        return i.toString(16)
    })
  }

var num = uuid()
console.log(num)