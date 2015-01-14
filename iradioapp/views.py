from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from iradioapp.commands import command_list

# Create your views here.

def home(request):
	return render(request, "iradioapp/index.html")


def command(request):
	if request.method == 'POST':
		print(request.POST.get('command'))
		cmd = command_list[request.POST.get('command', None)]
		if cmd:
			res = cmd()
			if isinstance(res, dict):
				return JsonResponse(res)
			else:
				return HttpResponse(content=res if isinstance(res, str) else "", status=200)
		return HttpResponse(status=400)
	return HttpResponse(status=405)

