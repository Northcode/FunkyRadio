from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from iradioapp.commands import command_list

# Create your views here.

def home(request):
	return render(request, "iradioapp/index.html")


def command(request):
	if request.method == 'POST':
		cmd_str = request.POST.get('command', None)
		if not cmd_str:
			return HttpResponse("No command given", status=400)
		cmd = command_list[cmd_str]
		if cmd:
			res = cmd(request)
			if isinstance(res, dict) or isinstance(res, list):
				return JsonResponse(res)
			else:
				return HttpResponse(content=res if isinstance(res, str) else "", status=200)
		return HttpResponse(status=400)
	return HttpResponse(status=405)

