$(function () {
    // 初始化定义
	var error_name = false;
	var error_password = false;

	//失焦验证用户名
	$('#user_name').blur(function() {
		check_user_name();
	});

	//失焦验证用户密码
	$('#password').blur(function() {
		check_pwd();
	});

     //验证用户名
	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').val('');
			$('#user_name').next().html('请输入5-20个字符的用户名')
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
			$('#user_name').next().hide();
			error_name = false;
		}
	}

	//验证密码
	function check_pwd(){
		var len = $('#password').val().length;
		if(len<8||len>20)
		{
			$('#password').val('');
			$('#password').next().html('密码最少8位，最长20位')
			$('#password').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}
	}

    $(document).ready(function () {
        // alert(1)
        $('#login_form').submit(function (e) {
            e.preventDefault();

            check_user_name();
            check_pwd();
            if (error_name == false && error_password == false) {
               var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                username = $('#user_name').val();
                password = $('#password').val();
                // alert(1)
                $.ajax({
                    url: '/user/login/',
                    type: 'post',
                    headers: {'X-CSRFToken': csrf},
                    dataType: 'json',
                    data: {'username': username, 'password': password},
                    success: function (data) {
                        console.log(data.code);
                        if (data.code == 200) {
                            location.href = '/demo/index/';
                        } else if (data.code == 1101) {
                            $('#user_name').val('');
                            $('#user_name').next().text(data.msg);
                            $('#user_name').next().show();
                        } else if (data.code == 1102) {
                            $('#password').val('');
                            $('#password').next().text(data.msg);
                            $('#password').next().show();
                        } else if (data.code == 1100) {
                            $('#password').val('');
                            $('#password').next().text(data.msg);
                            $('#password').next().show();
                        }
                    },
                    error: function (data) {
                        console.log(data)
                        alert('请求失败');
                    }
                })
            }
        })
    })
})