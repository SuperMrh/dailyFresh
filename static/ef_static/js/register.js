$(function(){
	// 初始化定义
	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;
	var error_tel = false;

	//失焦验证用户名
	$('#user_name').blur(function() {
		check_user_name();
	});

	//失焦验证用户密码
	$('#pwd').blur(function() {
		check_pwd();
	});

	//失焦验证用户名确认
	$('#cpwd').blur(function() {
		check_cpwd();
	});

	//失焦验证邮箱
	$('#email').blur(function() {
		check_email();
	});

	$('#tel').blur(function() {
		check_tel();
	});

	//验证是否勾选同意
	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
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
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').val('');
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}

    //验证确认密码
	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#pwd').val('');
			$('#cpwd').val('');
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	//验证电话号码
    function check_tel() {
        var re = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/;
        if (re.test($('#tel').val())) {
            $('#tel').next().hide();
			error_tel = false;
        } else {
        	$('#tel').val('');
            $('#tel').next().html('你输入的手机号格式不正确')
			$('#tel').next().show();
			error_tel = true;
        }
    }

	//验证邮箱
	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').val('');
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	}

	$(document).ready(function () {

       //表单提交时进行验证
        $('#reg_form').submit(function(e) {
            e.preventDefault();
            check_user_name();
            check_pwd();
            check_cpwd();
            check_email();

            if(error_name == false && error_password == false && error_check_password == false &&
                error_tel == false && error_email == false && error_check == false)
            {
                // return true;
                var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                // console.log(csrf)
                var user_name = $('#user_name').val();
                var pwd = $('#pwd').val();
                var cpwd = $('#cpwd').val();
                var email = $('#email').val();
                var tel = $('#tel').val();
                var address = $('#address').val();
                // alert(user_name)
                $.ajax({
                    url: '/user/register/',
                    data: {'user_name': user_name, 'pwd': pwd, 'cpwd': cpwd,
                    'email': email, 'tel': tel, 'address': address},
                    dataType: 'json',
                    type: 'post',
                    headers: {'X-CSRFToken': csrf},
                    success: function(data){
                        console.log(data)
                        if (data.code == 200) {
                        	location.href = '/user/login/'
						} else if (data.code == 1000) {
                        	$('#user_name').val('');
							$('#pwd').val('');
							$('#cpwd').val('');
							$('#email').val('');
							$('#tel').val('');
							$('#address').val('');
							$('#user_name').focus();
							$('#user_name').next().html(data.msg);
							$('#user_name').next().show();
						}
                    },
                    error:function(data){
                        alert('请求失败')
                    }
                });
            }
            else
            {
                return false;
            }

        });
	})
})