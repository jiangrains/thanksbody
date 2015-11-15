from django.http import HttpResponse
from django.template.loader import get_template
from django.template import  Context
import datetime, hashlib

def helloworld(request):
	return HttpResponse("Hello world.")

def weixin_checkSignature(request):
    token = 'IMAXGINE'
    flag = True
    if 'signature' in request.GET:
        signature = request.GET['signature']
    else:
        flag = False
    
    if 'timestamp' in request.GET:
        timestamp = request.GET['timestamp']
    else:
        flag = False

    if 'nonce' in request.GET:
        nonce = request.GET['nonce']
    else:
        flag = False
    
    if 'echostr' in request.GET:
        echostr = request.GET['echostr']
    else:
        flag = False
        
    if flag:
        checkstr = [timestamp, nonce, token]
        checkstr.sort()
        checkstr = ''.join(checkstr)
        
        if hashlib.sha1(checkstr).hexdigest() == signature:
            return HttpResponse(echostr)

    return HttpResponse('signature %s timestamp %s nonce %s echostr %s' % (signature, timestamp, nonce, echostr))
    
def weixin_checkSignature2(request):
    token = "IMAXGINE"
    params = request.GET
    args = [token, params['timestamp'], params['nonce']]
    args.sort()
    if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
        if params.has_key('echostr'):
            return HttpResponse(params['echostr'])
    return HttpResponse('Invalid Request')

def test(request):
    if 'name' in request.GET:
        name = request.GET['name']
    else:
        name = 'You have not input a name.'
    return HttpResponse(name)

