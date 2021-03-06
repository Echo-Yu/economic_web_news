# 注册和登录
from . import passport_blue
from flask import request,abort,current_app,make_response,jsonify
from info.utils.captcha.captcha import captcha
from info import redis_store,constants,response_code
import re,random,json
from info.libs.yuntongxun.sms import CCP


@passport_blue.route('/image_code',methods=['GET'])
def image_code():
    """图片验证码"""
    # print(request.url)
    """
    1.接受参数（uuid）
    2.校验参数（判断uuid是否为空）
    3.生成图片验证码
    4.保存图片验证码到redis
    5.修改image的ContentType = 'image/jpg'
    6.响应图片验证码
    """
    #1.接受参数（uuid）
    imageCodeId = request.args.get('imageCodeId')
    #2.校验参数（判断uuid是否为空）
    if not imageCodeId:
        abort(403)
    # 3.生成图片验证码
    name,text,image = captcha.generate_captcha()
    current_app.logger.debug(text)
    #4.保存图片验证码到redis
    try:
        redis_store.set('imageCodeId:'+imageCodeId,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
    #5.修改image的ContentType = 'image/jpg'
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    #6.响应图片验证码
    return response

@passport_blue.route('/sms_code',methods=['POST'])
def sms_code():
    """发送短信"""
    """
    1.接受参数（手机号，图片验证码，uuid）
    2.校验参数是否齐全，手机号是否合法
    3.查询服务器存储的图片验证码
    4.跟客户端传入的图片验证码对比
    5.如果对比成功，生成短信验证码，并发送短信
    6.存储短信验证码到redis,方便注册时比较
    7.响应短信验证码发送的结果
    """
    #1.接受参数（手机号，图片验证码，uuid）
    json_str = request.data.decode()
    json_dict = json.loads(json_str)
    mobile = json_dict.get('mobile')
    image_code_client = json_dict.get('image_code')
    image_code_id = json_dict.get('image_code_id')
    #2.校验参数是否齐全，手机号是否合法
    if not all([mobile,image_code_client]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1[345678][0-9]{9}$',mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')
    #3.查询服务器存储的图片验证码
    try:
        image_code_server = redis_store.get('imageCodeId:'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询图片验证码失败')
    if not image_code_server:
        return jsonify(errno=response_code.RET.NODATA, errmsg='图片验证码不存在')
    #4.跟客户端传入的图片验证码对比
    if image_code_server.lower() != image_code_client.lower():
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='输入验证码有误')
    #5.如果对比成功，生成短信验证码，并发送短信
    # '%06d' : 如果不够6位，补0.比如:28-->000028
    sms_code = '%06d' % random.randint(0,999999)
    current_app.logger.debug(sms_code)
    result = CCP().send_template_sms(mobile,[sms_code,5],1)
    if result != 0:
        return jsonify(errno=response_code.RET.THIRDERR, errmsg='发送短信验证码失败')
    #6.存储短信验证码到redis,方便注册时比较
    try:
        redis_store.set('SMS:'+mobile,sms_code,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='保存短信验证码失败')
    #7.响应短信验证码发送的结果
    return jsonify(errno=response_code.RET.OK, errmsg='发送短信验证码成功')

