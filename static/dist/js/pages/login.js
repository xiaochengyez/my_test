function check() {
    //alert("aa");
    /**校验用户名*/
        //1.获取用户输入的数据
    var uValue =  document.getElementById("user").value;
    //alert(uValue);
    if (uValue == "") {
        //2.给出错误提示信息
        showMsg("邮箱不能为空!");
        return false;
    }
    if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/.test(uValue)) {
        showMsg("邮箱格式不正确!");
        return false;
    }

        var pValue = document.getElementById("passwd").value;
        if(pValue==""){
            showMsg("密码不能为空!");

            return false;
        }
        if (uValue && pValue){
            showMsg("正在登录中!");
        }
}


 function showMsg(msg){
    $("#CheckMsg").text(msg);
    }